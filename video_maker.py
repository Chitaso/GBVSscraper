import shutil
import subprocess
import cv2
import ffmpeg
import json
from PIL import ImageFont, ImageDraw
from util import *

os.makedirs(os.path.abspath(f"{__file__}/../final"), exist_ok=True)
MATCH_TYPE = "Ranked"


def get_video_duration(file_path):
    probe = ffmpeg.probe(file_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    duration = float(video_info['duration'])
    return duration


def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return text_width, text_height


def convert(seconds):
    minutes = int(seconds // 60)
    seconds = seconds % 60

    return f"{minutes}:{int(seconds):02d}"


video_count = 0


def create_video(file_path):
    with open(file_path) as f:
        data = json.load(f)

    if data["runtime"] < 270:
        print(f"Video Length Insufficient for video {file_path}")
        return

    global video_count
    video_count += 1

    uuid = gen_uuid()
    temp_path = os.path.abspath(f"{__file__}/../final/temp/{uuid}")
    os.makedirs(os.path.abspath(temp_path), exist_ok=True)
    os.makedirs(f"{temp_path}/videos", exist_ok=True)
    os.makedirs(f"{temp_path}/overlays", exist_ok=True)

    for i, [p1, p2] in enumerate(data["wins"][:-1]):
        overlay = cv2.imread(f"{__file__}/../images/overlay.png", cv2.IMREAD_UNCHANGED)

        text1 = f"{data['player1']['name']} {p1}"
        text2 = f"{p2} {data['player2']['name']}"

        font_path = f"{__file__}/../images/font.otf"
        font = ImageFont.truetype(font_path, 32)

        text_width1, text_height1 = get_text_dimensions(text1, font)
        __, text_height2 = get_text_dimensions(text2, font)

        padding_lr = 30
        img_pil = Image.fromarray(overlay)
        draw = ImageDraw.Draw(img_pil)
        draw.text((809 - padding_lr - text_width1, 25 - text_height1 // 2), text1, font=font, fill=(255, 255, 255, 255))
        draw.text((1110 + padding_lr, 25 - text_height2 // 2), text2, font=font, fill=(255, 255, 255, 255))

        cv2.imwrite(f"{temp_path}/overlays/overlay{i}.png", np.array(img_pil))

    clips = []
    for i, j in enumerate(data["files"]):
        print(f"Creating clip: {i}")
        clip_path = f"{temp_path}/videos/clip{i}.mp4"
        clips.append(clip_path)

        overlay = f"{temp_path}/overlays/overlay{i}.png"

        if i == 0:
            subprocess.call(
                f'ffmpeg -hwaccel cuda -i "{j[0]}" -loop 1 -t {get_video_duration(j[0])} -i "{overlay}" -c:v h264_nvenc -filter_complex "[1:v]fade=in:st=0.5:d=0.33:alpha=1[i];[0:v][i]overlay=0:0" -c:a copy \"{clip_path}\"')
        else:
            subprocess.call(
                f'ffmpeg -hwaccel cuda -i "{j[0]}" -loop 1 -t {get_video_duration(j[0])} -i "{overlay}" -c:v h264_nvenc -filter_complex "[0:v][1:v]overlay=0:0" -c:a copy \"{clip_path}\"')

    concat_path = f"{temp_path}/concat.txt"

    with open(concat_path, "w", encoding="utf-8") as f:
        f.write("\n".join(map(lambda x: f"file {temp_path}/videos/{x}".replace("\\", "/"), os.listdir(f"{temp_path}/videos"))))

        ending_path = data['files'][-1][0].replace('trimmed_videos', 'ending_anim').replace("\\", "/").replace(" ", "_")
        f.write(f"\nfile {ending_path}")

    final_path = os.path.abspath(
        f"{__file__}/../final/[GBVS] Granblue Fantasy Versus {MATCH_TYPE} Match {data['player1']['name']} ({data['player1']['character']}) vs {data['player2']['name']} ({data['player2']['character']})-{video_count}.mp4")

    subprocess.call(f'ffmpeg -f concat -safe 0 -i \"{concat_path}\" -c copy -y \"{final_path}\"')

    with open(f"{__file__}/../final/temp/output.log", "a", encoding="utf-8") as f:
        f.write(f"[{convert(data['runtime'])}] {final_path}\n")

    shutil.rmtree(temp_path)


def create_thumbnail(file_path):
    with open(file_path) as f:
        data = json.load(f)

    if data["runtime"] < 270:
        return

    thumbnail_path = data["files"][0][0]
    thumbnail_path = thumbnail_path[:-4].replace("trimmed_videos", "thumbnails_temp") + ".png"

    with open(thumbnail_path, "rb") as f:
        arr = np.asarray(bytearray(f.read()), dtype=np.uint8)
    thumbnail = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    thumbnail = cv2.resize(thumbnail, (1280, 720), interpolation=cv2.INTER_AREA)

    overlay = cv2.imread(f"{__file__}/../images/thumbnail_overlay.png", cv2.IMREAD_UNCHANGED)

    text1 = data["player1"]["name"]
    text2 = data["player2"]["name"]

    font_path = f"{__file__}/../images/font_overlay2.ttf"
    font = ImageFont.truetype(font_path, 55)

    text_width1, text_height1 = get_text_dimensions(text1, font)
    text_width2, text_height2 = get_text_dimensions(text2, font)

    img_pil = Image.fromarray(thumbnail)
    overlay_pil = Image.fromarray(overlay)

    img_pil.paste(overlay_pil, (0, 0), mask=overlay_pil)

    draw = ImageDraw.Draw(img_pil)
    draw.text((304 - text_width1 // 2, 610 - text_height1 // 2), text1, font=font, fill=(255, 255, 255, 255))
    draw.text((974 - text_width2 // 2, 610 - text_height2 // 2), text2, font=font, fill=(255, 255, 255, 255))

    final_path = os.path.abspath(
        f"{__file__}/../final/[GBVS] Granblue Fantasy Versus {MATCH_TYPE} Match {data['player1']['name']} ({data['player1']['character']}) vs {data['player2']['name']} ({data['player2']['character']})-{video_count}.png")
    cv2.imwrite(final_path, np.array(img_pil))


def create_description(file_path):
    with open(file_path) as f:
        data = json.load(f)

    if data["runtime"] < 270:
        return

    with open(f"{__file__}/../images/playlists.json") as f:
        playlists = json.load(f)

    with open(f"{__file__}/../images/template_description.txt") as f:
        desc = f.read()

    title = f"[GBVS] Granblue Fantasy Versus {MATCH_TYPE} Match {data['player1']['name']} ({data['player1']['character']}) vs {data['player2']['name']} ({data['player2']['character']})"

    final_path = os.path.abspath(
        f"{__file__}/../final/{title}-{video_count}.txt")

    with open(final_path, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + desc.format(p1_char=data['player1']['character'], p1_playlist=playlists[data['player1']['character']], p2_char=data['player2']['character'],
                                             p2_playlist=playlists[data['player2']['character']], match_type=MATCH_TYPE, match_playlist=playlists[MATCH_TYPE]))


def run(file_path):
    create_video(file_path)
    create_thumbnail(file_path)
    create_description(file_path)


path = os.path.abspath(f"{__file__}/../compilation")
for i in os.listdir(path):
    print(f"Compiling video {i}")
    run(f"{path}/{i}")

# create_description(f"{__file__}/../compilation/roku--Belial--STREETu0020FIGHTERu00206--Ladiva-1.json")
