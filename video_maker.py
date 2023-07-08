import shutil
import subprocess
import numpy as np
import cv2
import ffmpeg
import os
import json
import random

os.makedirs(os.path.abspath(f"{__file__}/../final"), exist_ok=True)


def gen_uuid():
    # return "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(20))
    return "a"


def get_video_duration(file_path):
    probe = ffmpeg.probe(file_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    duration = float(video_info['duration'])
    return duration


def create_video(file_path):
    with open(file_path) as f:
        data = json.load(f)

    # if data["runtime"] < 300:
    #     print(f"Video Length Insufficient for video {file_path}")

    uuid = gen_uuid()
    temp_path = os.path.abspath(f"{__file__}/../final/temp/{uuid}")
    os.makedirs(os.path.abspath(temp_path), exist_ok=True)
    os.makedirs(f"{temp_path}/videos", exist_ok=True)
    os.makedirs(f"{temp_path}/overlays", exist_ok=True)

    for i, [p1, p2] in enumerate(data["wins"][:-1]):
        overlay = cv2.imread(f"{__file__}/../images/overlay.png", cv2.IMREAD_UNCHANGED)

        text1 = f"{data['player1']['name']} {p1}"
        text2 = f"{p2} {data['player2']['name']}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.3
        font_thickness = 2

        (text_width1, text_height1), _ = cv2.getTextSize(text1, font, font_scale, font_thickness)
        (__, text_height2), _ = cv2.getTextSize(text2, font, font_scale, font_thickness)

        padding_lr = 30

        text_image = np.zeros_like(overlay)
        cv2.putText(text_image, text1, (809 - padding_lr - text_width1, 70 - text_height1), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
        cv2.putText(text_image, text2, (1110 + padding_lr, 70 - text_height2), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

        result = cv2.add(overlay, text_image)
        cv2.imwrite(f"{temp_path}/overlays/overlay{i}.png", result)

    clips = []
    for i, j in enumerate(data["files"]):
        clip_path = f"{temp_path}/videos/clip{i}.mp4"
        clips.append(clip_path)

        overlay = f"{temp_path}/overlays/overlay{i}.png"

        if i == 0:
            subprocess.call(
                f'ffmpeg -i "{j[0]}" -loop 1 -t {get_video_duration(j[0])} -i "{overlay}" -filter_complex "[1:v]fade=in:st=0.5:d=0.33:alpha=1[i];[0:v][i]overlay=0:0" -c:a copy \"{clip_path}\"')
        else:
            subprocess.call(
                f'ffmpeg -i "{j[0]}" -loop 1 -t {get_video_duration(j[0])} -i "{overlay}" -filter_complex "[0:v][1:v]overlay=0:0" -c:a copy \"{clip_path}\"')

    concat_path = f"{temp_path}/concat.txt"

    with open(concat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(map(lambda x: f"file {temp_path}/videos/{x}".replace("\\", "/"), os.listdir(f"{temp_path}/videos"))))
        f.write(f"\nfile {data['files'][-1][0].replace('trimmed_videos', 'ending_anim')}")

    final_path = os.path.abspath(
        f"{__file__}/../final/[GBVS] Granblue Fantasy Versus Match {data['player1']['name']} ({data['player1']['character']}) vs {data['player2']['name']} ({data['player2']['character']}).mp4")

    subprocess.call(f'ffmpeg -f concat -safe 0 -i \"{concat_path}\" -c copy \"{final_path}\"')

    shutil.rmtree(temp_path)


path = os.path.abspath(f"{__file__}/../compilation")
for i in os.listdir(path):
    create_video(f"{path}/{i}")
