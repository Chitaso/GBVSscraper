import os
import cv2
import ffmpeg
import numpy as np

os.makedirs(os.path.abspath(f"{__file__}/../trimmed_videos"), exist_ok=True)
os.makedirs(os.path.abspath(f"{__file__}/../ending_anim"), exist_ok=True)
os.makedirs(os.path.abspath(f"{__file__}/../thumbnails_temp"), exist_ok=True)


def is_frame_black(arr):
    return not (arr > 10).any()


# TODO:
#   - 12, 13 Ending Anim ->
#   - 20 Ending Anim

def get_video_bounds(file_path):
    cap = cv2.VideoCapture(file_path)

    success, img = cap.read()
    fno = 0

    start_frame = -1
    last_black_frame = -1

    # Coordinate : Color
    validate_start = [
        [[945, 566], [171, 171, 169]],
        [[284, 525], [168, 171, 171]],
        [[400, 566], [167, 167, 158]],
        [[902, 469], [184, 177, 162]],
        [[1284, 581], [42, 39, 38]],
        [[1586, 512], [247, 244, 238]],
        [[1645, 555], [49, 47, 43]],
        [[1150, 585], [119, 108, 99]]
    ]

    end_frame = -1
    end_frame_flag = False

    black_frame_end_flag = False
    black_frame_end = -1

    validate_end = [
        # Lose - Win
        [[[204, 151], [135, 126, 123]], [[226, 229], [255, 250, 254]], [[280, 221], [40, 30, 37]], [[405, 194], [255, 251, 253]], [[450, 175], [205, 184, 196]],
         [[1424, 169], [92, 192, 248]], [[1488, 218], [98, 181, 235]], [[1560, 205], [75, 165, 226]], [[1672, 188], [173, 255, 253]]],
        # Win - Lose
        [[[234, 151], [84, 183, 247]], [[302, 218], [101, 191, 241]], [[379, 192], [146, 208, 255]], [[414, 175], [71, 175, 230]], [[1384, 166], [77, 64, 72]],
         [[1409, 223], [85, 73, 80]], [[1470, 224], [36, 26, 33]], [[1588, 191], [240, 222, 230]], [[1653, 191], [64, 55, 60]]]
    ]
    for a in validate_end:
        for b, c in enumerate(a):
            a[b][1] = np.array(c[1])

    final_anim_frame = -1

    while success:
        if start_frame == -1:
            if is_frame_black(img):
                last_black_frame = fno

            if last_black_frame != -1:
                flag = False
                for i, j in validate_start:
                    p = img[i[1]][i[0]]

                    for k in range(3):
                        if abs(p[k] - j[k]) > 25:
                            flag = True
                            break

                    if flag:
                        break
                else:
                    start_frame = last_black_frame + 11
                    print(start_frame)

        if start_frame != -1 and not end_frame_flag:
            if is_frame_black(img):
                if not black_frame_end_flag:
                    black_frame_end_flag = True
                    black_frame_end = fno
            else:
                black_frame_end_flag = False

        if black_frame_end != -1 and not end_frame_flag:
            for a in validate_end:
                for [pix, color] in a:
                    p = img[pix[1]][pix[0]]
                    if not (np.abs(color - p) < 15).all():
                        break
                else:
                    print(fno)
                    end_frame_flag = True
                    end_frame = black_frame_end - 1

        if end_frame_flag:
            if is_frame_black(img):
                final_anim_frame = fno - 268
                break

        success, img = cap.read()
        fno += 1

    print(start_frame, end_frame, final_anim_frame)

    if start_frame >= 0 and end_frame >= 0:
        return start_frame, end_frame, final_anim_frame


def trim_video(file_path, bounds):
    frame_rate = 60

    for j, k in enumerate(["trimmed_videos", "ending_anim"]):
        output_path = file_path.replace("videos", k, 1)

        start_time = round(bounds[j] / frame_rate, 5)
        end_time = round(bounds[j + 1] / frame_rate, 5)

        kwargs = {}
        if j == 1:
            kwargs["filter_complex"] = "[0:a]volume=enable='lt(t,0.25)':volume=0"

        ffmpeg.input(file_path, ss=start_time, to=end_time, **kwargs).output(output_path).run(overwrite_output=True)


def extract_thumbnail(file_path, start_frame):
    cap = cv2.VideoCapture(file_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 460)
    _, img = cap.read()

    file_path = file_path.replace("videos", "thumbnails_temp")
    file_path = file_path[:-4] + ".png"

    cv2.imwrite(file_path, img)


def run(file_path):
    bounds = get_video_bounds(file_path)
    trim_video(file_path, bounds)
    extract_thumbnail(file_path, bounds[0])


path = os.path.abspath(f"{__file__}/../videos")
blacklist = os.listdir(f"{__file__}/../trimmed_videos")

for i in os.listdir(path):
    if i not in blacklist or True:
        print(f"Trimming video: {i}")
        run(f"{path}/{i}")
