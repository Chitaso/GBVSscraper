import time
import obsws_python as obs
from util import *
import os

os.makedirs(os.path.abspath(f"{__file__}/../videos"), exist_ok=True)

req_cl = obs.ReqClient()
ev_cl = obs.EventClient()

replay_data = {}


def get_new_path(ext="mp4"):
    global replay_data
    if not replay_data:
        raise RuntimeError("Replay data is empty")

    path = os.path.abspath(
        f"{__file__}/../videos/{replay_data['replay_number']}--{re.sub(r'--+', r'-', replay_data['player1']['name'])}--{replay_data['player1']['character']}--{re.sub(r'--+', r'-', replay_data['player2']['name'])}--{replay_data['player2']['character']}.{ext}")
    replay_data = {}

    return path


def on_record_state_changed(data):
    if data.output_state != "OBS_WEBSOCKET_OUTPUT_STOPPED":
        return

    os.rename(data.output_path, get_new_path(data.output_path.split(".")[-1]))


ev_cl.callback.register(on_record_state_changed)

hwnd = find_window("GRANBLUE FANTASY Versus")
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ~win32con.WS_EX_TOPMOST)
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TOPMOST)

images = {
    "replay_menu": np.array(Image.open(os.path.abspath(f"{__name__}/../images/replay_menu_play.png"))),
    "hide_guide": np.array(Image.open(os.path.abspath(f"{__name__}/../images/hide_guide.png")))
}


def replay_menu_screen():
    return np.array_equal(background_screenshot(hwnd)[270:340, 865:1080], images["replay_menu"])


def hide_guide_overlay(p):
    return np.array_equal(p[984:1012, 1260:1286], images["hide_guide"])


replays_to_record = 3

for last_replay_num in range(1, replays_to_record + 1):
    print(f"Saving Replay {last_replay_num}")

    # Putting the replay on the top
    last_direction = "w"
    while True:
        temp1 = background_screenshot(hwnd)
        temp = get_replay_number(temp1)

        if temp is None:
            send_key(hwnd, last_direction)
        elif last_replay_num == 1 and get_fighter_characters(temp1)[0] is None:
            send_key(hwnd, "s")
            last_direction = "s"
        elif temp < last_replay_num:
            send_key(hwnd, "s")
            last_direction = "s"
        elif temp > last_replay_num:
            send_key(hwnd, "w")
            last_direction = "w"
        else:
            break

    # Grabbing the data
    replay_data = get_replay_data(background_screenshot(hwnd))

    # Selection the data
    last_direction = "w"
    while True:
        temp1 = background_screenshot(hwnd)
        temp = get_replay_number(temp1)

        if temp is None:
            send_key(hwnd, last_direction)
        elif last_replay_num == 1 and get_fighter_characters(temp1)[0] is None:
            break
        elif temp < last_replay_num - 1:
            send_key(hwnd, "s")
            last_direction = "s"
        elif temp > last_replay_num - 1:
            send_key(hwnd, "w")
            last_direction = "w"
        else:
            break

    req_cl.start_record()

    flag = False
    calls_before_last = 0
    calls_before_last1 = 0

    while True:
        if not replay_menu_screen():
            if not flag:
                if calls_before_last1 > 0:
                    calls_before_last1 -= 1
                else:
                    send_key(hwnd, win32con.VK_RETURN)
                    calls_before_last1 = 3
            else:
                break

        else:
            if calls_before_last > 0:
                calls_before_last -= 1
            else:
                send_key(hwnd, win32con.VK_RETURN)
                calls_before_last = 3

            flag = True

        time.sleep(0.5)

    while True:
        temp1 = background_screenshot(hwnd)
        temp = get_fighter_ranks(temp1)
        if temp[0]:
            break

        if hide_guide_overlay(temp1):
            send_key(hwnd, "u")

        time.sleep(0.5)

    req_cl.stop_record()

# Allowing for any final events to go through
time.sleep(5)