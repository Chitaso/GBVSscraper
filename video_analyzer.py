import os
import cv2
import json

os.makedirs(os.path.abspath(f"{__file__}/../analysis"), exist_ok=True)


# def is_frame_black(arr):
#     return not (arr > 5).any()


# def get_game_timestamps(file_path):
#     return [3815, 5993, 9757]
#
#     cap = cv2.VideoCapture(file_path)
#
#     success, img = cap.read()
#     fno = 0
#     frames = []
#
#     flag = False
#     while success:
#         if is_frame_black(img):
#             flag = True
#         elif flag:
#             flag = False
#             frames.append(fno)
#
#         success, img = cap.read()
#         fno += 1
#
#     frames.append(fno - 1)
#
#     return frames

def get_wins(img):
    wins = [0, 0]

    for a, [j, k] in enumerate([[229, 31], [254, 31]], 1):
        if (img[k][j] > 30).all():
            wins[0] = a

    for a, [j, k] in enumerate([[1693, 31], [1666, 31]], 1):
        if (img[k][j] > 30).all():
            wins[1] = a

    return wins  # Player 1 Wins, Player 2 Wins


# def find_win_timeline(file_path):
#     timestamps = get_game_timestamps(path)
#     timestamps = [(b + a) // 2 for a, b in zip(timestamps, timestamps[1:])] + [timestamps[-1]]
#
#     wins = []
#
#     cap = cv2.VideoCapture(file_path)
#     for fno in timestamps:
#         cap.set(cv2.CAP_PROP_POS_FRAMES, fno)
#         _, img = cap.read()
#         wins.append(get_wins(img))
#
#     return wins


def analyze_video(file_path, file_name):
    cap = cv2.VideoCapture(file_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)  # Getting Last Frame
    _, img = cap.read()

    winner = 2 - (get_wins(img)[0] == 2)

    new_path = file_path.replace("trimmed_videos", "analysis").rsplit(".", 1)[0] + ".json"
    _, a, b, c, d = file_name.rsplit(".")[0].split("--")

    with open(new_path, "w") as f:
        json.dump({
            "file_path": file_path,
            "winner": winner,
            "frame_count": frame_count,
            "player1": {
                "name": a,
                "character": b
            },
            "player2": {
                "name": c,
                "character": d
            }
        }, f)


path = os.path.abspath(f"{__file__}/../trimmed_videos")
for i in os.listdir(path):
    analyze_video(f"{path}/{i}", i)
