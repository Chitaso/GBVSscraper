import shutil
import os

base_path = os.path.abspath(f"{__file__}/../")

paths = [
    f"{base_path}/compilation",
    f"{base_path}/videos",
    f"{base_path}/analysis",
    f"{base_path}/trimmed_videos",
    f"{base_path}/ending_anim",
]

for i in paths:
    if os.path.exists(i):
        shutil.rmtree(i)

os.makedirs(f"{base_path}/videos")
