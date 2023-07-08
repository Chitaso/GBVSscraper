import os
import cv2
import ffmpeg

os.makedirs(os.path.abspath(f"{__file__}/../trimmed_videos"), exist_ok=True)
os.makedirs(os.path.abspath(f"{__file__}/../ending_anim"), exist_ok=True)


def is_frame_black(arr):
    return not (arr > 7).any()


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

    # Coordinates where a win is awarded
    validate_end = [[254, 31], [1666, 31]]

    final_anim_frame = -1
    final_anim_flag = False
    final_anim_flag1 = False

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
            flag = False
            for a in validate_end:
                if (img[a[1]][a[0]] > 30).all():
                    flag = True
                    break

            if flag:
                from PIL import Image
                Image.fromarray(img).show()
                input()

                end_frame_flag = True

        if end_frame_flag and not final_anim_flag:
            if is_frame_black(img):
                end_frame = fno - 1
                final_anim_flag = True

        if final_anim_flag and not final_anim_flag1:
            if not is_frame_black(img):
                final_anim_flag1 = True

        if final_anim_flag1:
            if is_frame_black(img):
                final_anim_frame = fno - 265
                break

        success, img = cap.read()
        fno += 1

    print(start_frame, end_frame, final_anim_frame)

    if start_frame >= 0 and end_frame >= 0:
        return start_frame, end_frame, final_anim_frame


def trim_video(file_path):
    bounds = get_video_bounds(file_path)
    frame_rate = 60

    for j, k in enumerate(["trimmed_videos", "ending_anim"]):
        output_path = file_path.replace("videos", k, 1)

        start_time = round(bounds[j] / frame_rate, 5)
        end_time = round(bounds[j + 1] / frame_rate, 5)

        kwargs = {}
        if j == 1:
            kwargs["filter_complex"] = "[0:a]volume=enable='lt(t,0.25)':volume=0"

        ffmpeg.input(file_path, ss=start_time, to=end_time, **kwargs).output(output_path).run(overwrite_output=True)


path = os.path.abspath(f"{__file__}/../videos")
# for i in os.listdir(path):
#     trim_video(f"{path}/{i}")

trim_video(f"{path}/1--SF6 Overrated--Cagliostro--Inno--Percival.mp4")