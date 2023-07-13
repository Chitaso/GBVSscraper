import os
import subprocess

path = os.path.abspath(f"{__file__}/../ending_anim")
for i in os.listdir(path):
    subprocess.call(f"ffmpeg -err_detect ignore_err -i \"{path}/{i}\" -c copy \"{path}/test.mp4\"")
    os.replace(f"{path}/test.mp4", f"{path}/{i}")
