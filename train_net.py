import tensorflow as tf
import sys
import json
from model import createModel

import keras
from keras.layers import Conv1D, Dense, Flatten, MaxPooling1D, Dropout
from keras.optimizers import adam_v2

import os
import input_data
import numpy as np

config = json.load(open("configure.json", "r"))["model_param"]

DATA_DIR = config["data_dir"]
CLASS_NUM = config["class_num"]

dict_2class = {0:'Novpn',1:'Vpn'}
dict_6class_novpn = {0:'Chat',1:'Email',2:'File',3:'P2p',4:'Streaming',5:'Voip'}
dict_6class_vpn = {0:'Vpn_Chat',1:'Vpn_Email',2:'Vpn_File',3:'Vpn_P2p',4:'Vpn_Streaming',5:'Vpn_Voip'}
dict_12class = {0:'Chat',1:'Email',2:'File',3:'P2p',4:'Streaming',5:'Voip',6:'Vpn_Chat',7:'Vpn_Email',8:'Vpn_File',9:'Vpn_P2p',10:'Vpn_Streaming',11:'Vpn_Voip'}
dict = {}

folder = os.path.split(DATA_DIR)[1]

(train_data, train_labels), (test_data, test_labels) = input_data.read_data_sets_keras(DATA_DIR, one_hot=True, class_num=CLASS_NUM)

#print(np.sum(train_labels, axis=0))

train_data = tf.reshape(train_data,[-1,784,1])
test_data = tf.reshape(test_data,[-1,784,1])

model = createModel(True, class_num=CLASS_NUM)

model.summary()

model.fit(train_data, train_labels, config["train_param"]["batch_size"], config["train_param"]["epoch"])

model.save_weights(config["ckpt_path"])
print("\r\rstart eva\r")
model.evaluate(test_data, test_labels)



