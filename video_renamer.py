import os

mappings = {
    "_Prof Nekotech": "Prof Nekotech"
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
