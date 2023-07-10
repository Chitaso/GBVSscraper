import os

mappings = {
    "pariahCarevCANI": "pariahCarey",
    "Son-o": "son-o",
    "player5mok9l1fhh": "日本翼",
    "playernzjzr6vp35": "日本翼",
    "player0a50vfq2uz": "日本翼",
    "playeriqq3jek2wj": "日本翼",
    "playerm1t7jbp5hl": "日本翼",
    "playerrkwzhvi4mi": "日本翼",
    "playerr4z81691jf": "日本翼",
    "player3tpouj53ei": "日本翼",
    "player81gn04ro7y": "日本翼",
    "player2d69o2wfa2": "日本翼",
    "playerb9m4vcra45": "日本翼",
    "player6p4tselwmq": "日本翼",
    "player0acpwxxz5i": "日本翼",
    "player6alaq7sotv": "日本翼",
    "playeruxsji7tsyt": "日本翼",
    "player43kv006r2v": "日本翼",
    "playeryzprc15ssi": "日本翼",
    "playert3ru49utja": "日本翼",
    "player34x25jqsti": "日本翼",
    "playerackx48oene": "日本翼",
    "playerxsvat5361i": "日本翼",
    "nan(篆nan nanl": "nan",
    "nan(ç¯†nan nanl": "nan",
}

path = os.path.abspath(f"{__file__}/../ending_anim")
for i in os.listdir(path):
    m, n = i.rsplit(".", 1)
    a, b, c, d, e = m.split("--")

    for j, k in mappings.items():
        if b == j:
            b = k

        if d == j:
            d = k

    os.rename(f"{path}/{i}", f"{path}/{'--'.join((a, b, c, d, e))}.{n}")
