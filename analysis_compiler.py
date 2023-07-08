import os
import json
from collections import defaultdict

os.makedirs(os.path.abspath(f"{__file__}/../compilation"), exist_ok=True)


class defaultkeydict(dict):
    def __init__(self, cb):
        super().__init__()
        self.cb = cb

    def __missing__(self, key):
        ret = self[key] = self.cb(key)
        return ret


# class Player:
#     players = defaultkeydict(lambda x: Player(x))
#
#     def __init__(self, name):
#         self.name = name
#         self.videos = defaultdict(list)  # Videos in order
#
#     def _add_video(self, file_path, file_name):
#         hash_ = file_name.split("--")[1][:-4]
#         self.videos[hash_].insert(0, file_path)
#
#     @staticmethod
#     def add_video(file_path, file_name):
#         _, a, __, b, ___ = file_name.rsplit(".", 1)[0].split("--")
#         Player.players[a]._add_video()


videos = defaultdict(list)


def add_video(file_path, file_name):
    hash_ = file_name.split("--", 1)[1][:-5]
    videos[hash_].append(file_path)


path = os.path.abspath(f"{__file__}/../analysis")
for i in os.listdir(path):
    add_video(f"{path}/{i}", i)

path1 = os.path.abspath(f"{__file__}/../compilation")
for i, j in videos.items():
    data = {
        "player1": {
            "name": None,
            "character": None
        },
        "player2": {
            "name": None,
            "character": None
        },
        "wins": [
            [0, 0]
        ],
        "files": [

        ],
    }

    for k in j:
        with open(k) as f:
            temp = json.load(f)
            data["player1"] = temp["player1"]
            data["player2"] = temp["player2"]
            data["files"].append([temp["file_path"], temp["frame_count"]])
            data["wins"].append([j + (i == temp["winner"]) for i, j in enumerate(data["wins"][-1], 1)])

    # In seconds
    data["runtime"] = sum(map(lambda x: x[1], data["files"])) / 60

    with open(f"{path1}/{i}.json", "w") as f:
        json.dump(data, f)
