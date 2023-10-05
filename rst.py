import socket
import struct
import sys
import _thread

class rst():
    # 五元组的源IP地址
    src = sys.argv[1]
    # 五元组的目标IP
    dst = sys.argv[2]
    # 和源IP对应的源端口
    sport = sys.argv[3]
    # 和目标IP对应的目标端口
    dport = sys.argv[4]

    def new_test(self,threadName, threadLoop):
        for i in range(0, int(threadLoop), 1):
            # 第一个参数意思是这是ipv4的地址，第二个参数意思是用的是TCP协议
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.src,int(self.sport)))
            s.connect((self.dst, int(self.dport)))
            # set reset attr
            # l_onoff非0，l_linger设置0，函数close()立即返回，并发送RST终止连接，发送缓冲区的数据丢弃。
            s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
            # http get and recv 200 ok
            s.sendall("Get.".encode())
            data = s.recv(1024)
            # will send tcp reset
            s.close()


    # noinspection PyBroadException
    def send(self):
        try:
            # _thread.start_new_thread(new_test, ("Thread-1", LOOP,))
            self.new_test("Thread-1",1)
        except:
            print("Error: unable to start thread")
        else:
            exit(0)

    while 1:
        pass

    # python rst.py 192.168.71.1 192.168.71.134 11560 23
