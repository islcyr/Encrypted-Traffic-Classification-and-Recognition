import numpy as np
from scapy.all import rdpcap, PcapReader
import socket

def get_self_port(self_ip, sess):
    if sess.src_ip == self_ip[0] or sess.src_ip == self_ip[1].replace(':','.'):
        return sess.src_port
    if sess.dst_ip == self_ip[0] or sess.dst_ip == self_ip[1].replace(':','.'):
        return sess.dst_port
    return None

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ipv4 = s.getsockname()[0]

    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    s.connect(("2001:4860:4860::8888", 80))
    ipv6 = s.getsockname()[0]
    return ipv4, ipv6

def file2vec(filename, N=784, mode='All'):
    packets = rdpcap(filename)

    if len(packets) < 10:
        return None
    vec = []
    for data in packets:
        if mode == 'All':
            t = list(data.original)
        else:
            if data.haslayer('TCP'):
                t = list(data['TCP'].payload.original)
            elif data.haslayer('UDP'):
                t = list(data['UDP'].payload.original)
            else:
                continue
        vec.extend(t)

    if len(vec) >= N:
        ninput = np.array(vec[0:N], dtype='float32')
        return ninput
    else:
        ninput = np.zeros(N, dtype='float32')
        ninput[0:len(vec)] = vec[:]
        return ninput

class Session:
    def __init__(self, proto=None, src_ip=None, src_port=None, dst_ip=None, dst_port=None, session_str=None, src_file=None):
        if proto is not None:
            self.__proto=proto
            self.__src_ip=src_ip
            self.__src_port=src_port
            self.__dst_ip=dst_ip
            self.__dst_port=dst_port
        elif session_str is not None:
            if isinstance(session_str, str):
                params = session_str.split('_')
                self.__proto = params[0]
                self.__src_ip = params[1].replace('-','.')
                self.__src_port = params[2]
                self.__dst_ip = params[3].replace('-','.')
                self.__dst_port = params[4]
        elif src_file is not None:
            rd = PcapReader(src_file)
            data = rd.read_packet()
            if data.haslayer('IP'):
                self.__src_ip = str(data["IP"].src)
                self.__dst_ip = str(data["IP"].dst)
            elif data.haslayer('IPv6'):
                self.__src_ip = str(data["IPv6"].src)
                self.__dst_ip = str(data["IPv6"].dst)
            if data.haslayer('TCP'):
                self.__proto = "TCP"
                self.__src_port = str(data["TCP"].sport)
                self.__dst_port = str(data["TCP"].dport)
            elif data.haslayer('UDP'):
                self.__proto = "UDP"
                self.__src_port = str(data["UDP"].sport)
                self.__dst_port = str(data["UDP"].dport)

    @property
    def src_ip(self):
        return self.__src_ip

    @property
    def src_port(self):
        return self.__src_port

    @property
    def dst_ip(self):
        return self.__dst_ip

    @property
    def dst_port(self):
        return self.__dst_port

    @property
    def proto(self):
        return self.__proto

    def __eq__(self, other):
        if (not hasattr(self, 'proto')) or (not hasattr(other, 'proto')):
            return False
        b1 = (self.__proto == other.proto)
        b2 = (self.__src_ip == other.src_ip)
        b3 = (self.__src_port == other.src_port)
        b4 = (self.__dst_ip == other.dst_ip)
        b5 = (self.__dst_port == other.dst_port)
        b6 = (self.__src_ip == other.dst_ip)
        b7 = (self.__src_port == other.dst_port)
        b8 = (self.__dst_ip == other.src_ip)
        b9 = (self.__dst_port == other.src_port)

        return b1 and ((b2 and b3 and b4 and b5) or (b6 and b7 and b8 and b9))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.__proto is None:
            return 'None'
        return self.__proto+"_"+self.__src_ip+":"+self.__src_port+"--"+self.__dst_ip+":"+self.__dst_port
