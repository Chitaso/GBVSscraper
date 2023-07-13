import time
from collections import defaultdict
from util import *

hwnd = find_window("GRANBLUE FANTASY Versus")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_TOPMOST)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST)

images = {
    "replay_menu": np.array(Image.open(os.path.abspath(f"{__name__}/../images/replay_menu.png"))),
    "replay_saved_screen": np.array(Image.open(os.path.abspath(f"{__name__}/../images/replay_saved_screen.png")))
}

game_count = defaultdict(lambda: 0)


def hash_game(game_data):
    p1 = game_data["player1"]
    p2 = game_data["player2"]

    temp = f"{p1['rank']}-{p1['character']}"
    temp1 = f"{p2['rank']}-{p2['character']}"

    if not re.fullmatch(r"player[a-z0-9]{10}", p1['name']):
        temp = f"{p1['name']}-{temp}"

    if not re.fullmatch(r"player[a-z0-9]{10}", p2['name']):
        temp1 = f"{p1['name']}-{temp}"

    return f"{temp}-{temp1}"


last_replay_num = 0


def should_save_replay():
    global last_replay_num

    pixels = background_screenshot(hwnd)
    temp = get_replay_data(pixels)
    temp1 = last_replay_num

    game_hash = hash_game(temp)
    c = game_count[game_hash]
    print(temp)
    print(f"{game_hash}: {c}")

    if c < 7:
        c += 1
        return validate_replay_data(temp) and ((last_replay_num := max(last_replay_num, temp["replay_number"])) > temp1)


def replay_menu_selection():
    ss = background_screenshot(hwnd)
    if not np.array_equal(ss[286:310, 890:1030], images["replay_menu"]):
        return 0

    for i, [j, k] in enumerate([[719, 377], [719, 429], [719, 464]], 1):
        if ss[k][j][0] != 30:
            return i
    raise RuntimeError("Could not determine what section of replay menu we are on")


def replay_saved_screen():
    return np.array_equal(background_screenshot(hwnd)[350:530, 850:1090], images["replay_saved_screen"])


def save_replay():
    for _ in range(3):
        send_key(hwnd, "w")
        time.sleep(0.25)

    switches_left = 3

    last_direction = "w"
    while switches_left > 0:
        temp1 = background_screenshot(hwnd)
        temp = get_replay_number(temp1)

        print(temp)

        if temp is None:
            send_key(hwnd, last_direction)
        elif last_replay_num == 1 and get_fighter_characters(temp1)[0] is None:
            break
        elif temp < last_replay_num - 1:
            switches_left -= last_direction != "s"

            send_key(hwnd, "s")
            last_direction = "s"
        elif temp > last_replay_num - 1:
            switches_left -= last_direction != "w"

            send_key(hwnd, "w")
            last_direction = "w"
        else:
            break

        time.sleep(0.5)

    if switches_left == 0:
        return False

    flag = False
    while True:
        curr_selection = replay_menu_selection()
        if curr_selection == 0:
            if not flag:
                send_key(hwnd, win32con.VK_RETURN)
            else:
                break
        elif curr_selection == 1:
            send_key(hwnd, "s")
        elif curr_selection == 2:
            send_key(hwnd, win32con.VK_RETURN)
            flag = True
        elif curr_selection == 3:
            send_key(hwnd, "w")

        time.sleep(0.5)

    calls_before_last = 0
    flag = False
    while True:
        if not replay_saved_screen():
            if flag:
                break
        else:
            if calls_before_last > 0:
                calls_before_last -= 1
            else:
                send_key(hwnd, win32con.VK_RETURN)
                calls_before_last = 3

            flag = True

        time.sleep(0.5)

    for _ in range(4):
        send_key(hwnd, "s")
        time.sleep(0.25)

    last_direction = "s"
    while True:
        temp = get_replay_number(background_screenshot(hwnd))

        if temp is None:
            send_key(hwnd, last_direction)
        elif temp < last_replay_num + 1:
            send_key(hwnd, "s")
            last_direction = "s"
        elif temp > last_replay_num + 1:
            send_key(hwnd, "w")
            last_direction = "w"
        else:
            break

    return True


def next_replay():
    send_key(hwnd, "s")


num_to_save = 49
while num_to_save > 0:
    print(f"Replays left: {num_to_save}")
    if should_save_replay():
        num_to_save -= save_replay()
    else:
        next_replay()
    time.sleep(0.5)
