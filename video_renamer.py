import os

mappings = {
    "_Prof Nekotech": "Prof Nekotech",
    "SEG overraled": "SF6 Overrated",
    "_ SF⑥ overraled": "SF6 Overrated",
    "_ SFG overraled": "SF6 Overrated",
    "Promelhens": "Prometheus",
    "~kKethero": "Kether",
    "火を放て ! ": "火を放て",
    "ichan ( 手柄変難 )": "yuu'chan",
    "況忠・互克息 ( 渇望弥": "況忠・互克息",
    "FU": "ナツキ"
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

    os.rename(f"{path}/{i}", f"{path}/{'--'.join((a, b, c, d, e))}.{n}")
