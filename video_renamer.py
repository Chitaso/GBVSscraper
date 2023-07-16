import os

mappings = {
    "iu0020BYu0020Fyu0020BRu0020LEu0020BRK": "我要成为英雄联盟高手",
    "担美得到迦": "扣类得到达",
    "提硯②③③": "提碳223",
    "player1evl5uzwvw": "...",
    "playerg2x7i9sg3w": "...",
    "playerv4biq3yz8g": "...",
    "供原禽肉配送": "优质离肉配送",
    "IAYLEN": "JAYLEN",
    "ICloudice": "JCloudice",
    "playerlp8vuo6hmk": "我要成为英雄联盟高手",
    "player9f313j2e7e": "我要成为英雄联盟高手",
    "playervt76uwi1uh": "我要成为英雄联盟高手",
    "LiGaMa": "LiSaMa",
    "Promelhens": "Prometheus",
    "川口": "llllIIII",
    "AYIYAPC": "カンニングPC",
    "Ibn": "Dom",
    "砂巻刃死不放必細": "刀砍卷刃死不放必杀"
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
