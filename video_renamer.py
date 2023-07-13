import os

mappings = {
    "速抱抱凱示希号": "请抱抱凯尔希吧",
    "波藍鬼オ_老男人ver.": "波蓝鬼オu0020]老男人ver",
    "夙同財云": "风间时云",
    "囚囚囚囚に": "Percival",
    "Son-o": "son-o",
    "mizo_re": "mizo_re"
}

path = os.path.abspath(f"{__file__}/../videos")
for i in os.listdir(path):
    m, n = i.rsplit(".", 1)
    a, b, c, d, e = m.split("--")

    for j, k in mappings.items():
        if b == j:
            b = k

        if d == j:
            d = k

    os.rename(f"{path}/{i}", f"{path}/{'--'.join((a, b, c, d, e)).replace(' ', '_')}.{n}")

if os.path.exists(f"{__file__}/../thumbnails_temp"):
    temp = {i.split("--")[0]: i[:-4] for i in os.listdir(path)}
    path1 = os.path.abspath(f"{__file__}/../thumbnails_temp")
    for i in os.listdir(path1):
        os.rename(f"{path1}/{i}", f"{path1}/{temp[i.split('--')[0]]}.png")

    path1 = os.path.abspath(f"{__file__}/../ending_anim")
    for i in os.listdir(path1):
        os.rename(f"{path1}/{i}", f"{path1}/{temp[i.split('--')[0]]}.mp4")

    path1 = os.path.abspath(f"{__file__}/../trimmed_videos")
    for i in os.listdir(path1):
        os.rename(f"{path1}/{i}", f"{path1}/{temp[i.split('--')[0]]}.mp4")
