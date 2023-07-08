import win32con, win32ui, win32gui, win32api
import numpy as np
from PIL import Image
import pytesseract
import re
import os

chars = {}


def load_chars():
    for i in os.listdir(os.path.abspath(f"{__name__}/../characters")):
        # chars[i.split(".")[0]] = np.array(cv2.imread(os.path.abspath(f"{__name__}/../characters/{i}")))
        chars[i.split(".")[0]] = np.array(Image.open(os.path.abspath(f"{__name__}/../characters/{i}")))


load_chars()


def find_window(window_name):
    win_list = []

    def cb(hwnd, *_):
        if window_name in win32gui.GetWindowText(hwnd):
            win_list.append(hwnd)

    win32gui.EnumWindows(cb, None)
    if win_list:
        return win_list[0]
    return None


# Grabs the full window
def background_screenshot(hwnd):
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()

    bbox = win32gui.GetWindowRect(hwnd)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((bbox[0], bbox[1]), (width, height), dcObj, (0, 0), win32con.SRCCOPY)

    # dataBitMap.SaveBitmapFile(cDC, 'temp/gbvs.bmp')

    p = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype=np.uint8).reshape((height, width, -1))

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return p


def get_replay_number(p):
    replay_number = p[270:301, 250:301]
    text = pytesseract.image_to_string(replay_number).strip().replace("O", "0")

    if re.match(r"\d{3}", text):
        return int(text)
    return None


def get_date(p):
    date = p[265:296, 1390:1581]

    text = pytesseract.image_to_string(date).strip()

    if re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", text):
        return text
    return None


LANGUAGES = ["jpn", "eng", "chi_sim"]


def read_langs(p):
    for i in LANGUAGES:
        text = pytesseract.image_to_string(p, lang=i, config=r"-c preserve_interword_spaces=1 -c paragraph_text_based=false").strip().strip("ー").strip()
        if text:
            return text
    return None


def get_fighter_names(p):
    name1 = p[305:343, 500:705]
    name2 = p[305:343, 1212:1437]

    text1 = read_langs(name1)
    text2 = read_langs(name2)

    return text1, text2


def get_fighter_ranks(p):
    ranks = {
        "Master": [
            [[16, 250, 255], [[553, 357], [1247, 357]]]
        ],
        #  Meh, it's fine
        "S+/S++": [
            [[49, 50, 55], [[661, 368], [1250, 368]]]
        ],
        "S": [
            [[48, 51, 56], [[663, 354], [1253, 354]]]
        ],
        # "A": [  # Figure out if we want to keep A's
        #     [[26, 43, 67], [[662, 356], [1254, 356]]]
        # ]
    }

    rank1 = None
    rank2 = None

    # Player 1
    for i, j in ranks.items():
        for a, b in j:
            r, c = b[0]

            if abs(p[c][r][0] - a[0]) > 5 or abs(p[c][r][1] - a[1]) > 5 or abs(p[c][r][2] - a[2]) > 5:
                break
        else:
            rank1 = i
            break

    # Player 2
    for i, j in ranks.items():
        for a, b in j:
            r, c = b[1]

            # Not strictly necessary
            if abs(p[c][r][0] - a[0]) > 5 or abs(p[c][r][1] - a[1]) > 5 or abs(p[c][r][2] - a[2]) > 5:
                break
        else:
            rank2 = i
            break

    return rank1, rank2


def get_fighter_characters(p):
    char1 = p[322:365, 724:850]
    char2 = p[322:365, 1013:1139]

    p1, p2 = None, None

    for a, b in chars.items():
        if np.array_equal(b, char1):
            p1 = a
            break
    # else:
    #     Image.fromarray(char1).save(os.path.abspath(f"{__name__}/../characters/unknown{len(chars) + 1}.png"))
    #     chars[f"unknown{len(chars) + 1}.png"] = char1

    for a, b in chars.items():
        if np.array_equal(b, char2):
            p2 = a
            break
    # else:
    #     Image.fromarray(char2).save(os.path.abspath(f"{__name__}/../characters/unknown{len(chars) + 1}.png"))
    #     chars[f"unknown{len(chars) + 1}.png"] = char2

    return p1, p2


def get_replay_data(p):
    data = {
        "replay_number": get_replay_number(p),
        "date": get_date(p),
        "player1": {
            "name": None,
            "rank": None,
            "character": None
        }, "player2": {
            "name": None,
            "rank": None,
            "character": None
        }
    }

    a, b = get_fighter_names(p)
    data["player1"]["name"] = a
    data["player2"]["name"] = b

    a, b = get_fighter_ranks(p)
    data["player1"]["rank"] = a
    data["player2"]["rank"] = b

    a, b = get_fighter_characters(p)
    data["player1"]["character"] = a
    data["player2"]["character"] = b

    return data


def validate_replay_data(data):
    return data["replay_number"] and data["date"] and all(data["player1"].values()) and all(data["player2"].values())


def send_key(hwnd, key):
    if isinstance(key, str):
        key = win32api.VkKeyScan(key)

    # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST)
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, key, 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, key, 0)
    # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_TOPMOST)


# Testing Code
if __name__ == "__main__":
    hwnd = find_window("GRANBLUE FANTASY Versus")
    pixels = background_screenshot(hwnd)


    # get_fighter_characters(pixels)

    # print(get_replay_data(pixels))

    # print(get_fighter_ranks(pixels))

    # a = pixels[984:1012, 1260:1286]
    # Image.fromarray(a).save(os.path.abspath(f"{__name__}/../images/hide_guide.png"))