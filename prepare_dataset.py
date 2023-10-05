import os
import json
from net_basic import file2vec
import numpy as np

root_dir=".\\data\\"
config = json.load(open("configure.json", "r"))["model_param"]

cnt = 0
vecs = []
for cdir in os.listdir(root_dir):
    son = os.path.join(root_dir, cdir, "split")
    if os.path.isdir(son):
        for file in os.listdir(son):
            file = os.path.join(son, file)
            vec = file2vec(file).tolist()
            label = [0 for _ in range(config["class_num"])]
            label[cnt] = 1
            unit = (vec, label)
            vecs.append(unit)
        cnt += 1
        if cnt >= config["class_num"]:
            break

np.random.shuffle(vecs)

json.dump(vecs[:int(config["test_ratio"]*len(vecs))], open(root_dir+"testvecs.json", "w"))
json.dump(vecs[int(config["test_ratio"]*len(vecs)):], open(root_dir+"trainvecs.json", "w"))