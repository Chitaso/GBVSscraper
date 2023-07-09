import os
import cv2


def get_wins(img):
    wins = [0, 0]

    for a, [j, k] in enumerate([[229, 31], [254, 31]], 1):
        if (img[k][j] > 30).all():
            wins[0] = a

    for a, [j, k] in enumerate([[1693, 31], [1666, 31]], 1):
        if (img[k][j] > 30).all():
            wins[1] = a

    return wins  # Player 1 Wins, Player 2 Wins


def analyze_video(file_path, file_name):
    cap = cv2.VideoCapture(file_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)  # Getting Last Frame
    _, img = cap.read()

    if get_wins(img) not in [[0, 2], [1, 2], [2, 0], [2, 1]]:
        print(f"{file_name} has a problem")


path = os.path.abspath(f"{__file__}/../trimmed_videos")
for i in os.listdir(path):
    analyze_video(f"{path}/{i}", i)
