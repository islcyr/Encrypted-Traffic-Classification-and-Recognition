import signal
import subprocess
import json
from time import sleep
import os
import datetime

import numpy as np

from find_proc import get_proc_by_port
from interface import config, dict_6class, model
from net_basic import Session, get_self_port, get_ip, file2vec


def catch():
    # p = subprocess.Popen('.\SplitCap\WinDump1.exe -n -s 0 -U -i 5 -c 1000 -w .\SplitCap\\tempcap.pcap', shell=True)
    os.system('.\SplitCap\WinDump1.exe -n -s 0 -U -i 5 -c 10000 -w .\SplitCap\\tempcap.pcap')
    sleep(3)
    os.system('.\\pcapplusplus-22.05-windows-vs2019\\x64\\examples\\PcapSplitter -f .\\SplitCap\\tempcap.pcap -o .\\package\\pack -m connection')


def split(filename):
    #.\WinDump.exe -n -s0 -U -i 7 -w package
    # os.system('.\SplitCap\SplitCap.exe -r .\SplitCap\\all -o .\package\pack_local')
    os.system('.\\pcapplusplus-22.05-windows-vs2019\\x64\\examples\\PcapSplitter -f '+filename.replace('/','\\')+' -o .\\package\\pack_local -m connection')


def classfication(src_dir):
    pass
    output_path = config["detlog"]
    #TODO:Read pcap
    resnum = [0 for _ in range(6)]
    ressize = [0 for _ in range(6)]
    procl = []
    sess_dir = config[src_dir]
    self_ip = get_ip()
    f = open(output_path, "a")
    for file in os.listdir(sess_dir):
        if file.endswith(".pcap") and os.path.getsize(os.path.join(sess_dir, file)) > 0:
            ses = Session(src_file=os.path.join(sess_dir, file))
            if not hasattr(ses, "src_ip") or not hasattr(ses, "src_port"):
                continue
            sport = get_self_port(self_ip, ses)
            proc = None
            pid = None
            if sport is not None:
                pid, proc = get_proc_by_port(sport)
                if proc in config["unconsider_procs"]:
                    continue
            file = os.path.join(sess_dir, file)
            vec = file2vec(file, mode=config["mode"])
            if vec is not None:
                #TODO:Predict->result
                vec = np.reshape(vec, (1, 784, 1))
                result = model.predict(vec)
                prob = np.max(result)
                result = np.argmax(result)
                if result == 3:
                    continue
                if result == 5:
                    result = 4
                resnum[result]+=1
                ressize[result]+=int(os.path.getsize(file)*prob)
                f.write(str(datetime.datetime.now())+"\t"+str(ses)+"\t"+dict_6class[result]+"\t"+str(prob)+"\t"+str(int(os.path.getsize(file)*prob))+"\n")
                if sport is not None and proc is not None and pid is not None:
                    procl.append((sport, dict_6class[result], proc, pid))

    for file in os.listdir(sess_dir):
        print(file)
        if file.endswith(".pcap"):
            os.remove(os.path.join(sess_dir,file))

    return ressize, procl

def packet_web():
    catch()
    res, pr = classfication("online_session_dir")
    res = [res[0], res[1], res[2], res[4], res[5]]
    json.dump(res, open("sizetemp.tmp", 'w'))
    json.dump(pr, open("proctemp.tmp", 'w'))

def packet_local(filename):
    split(filename)
    res, pr = classfication("local_session_dir")
    res = [res[0], res[1], res[2], res[4]+res[5]]
    json.dump(res, open("sizetemp.tmp", 'w'))
    json.dump(pr, open("proctemp.tmp", 'w'))

# packet_web()
# packet_local()

# catch()