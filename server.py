from socket import *
import sys
import threading
from time import ctime
from time import localtime
import traceback
import time
import subprocess

HOST = '127.0.0.1'
PORT = 8555  # 设置侦听端口
BUFSIZ = 1024


class TcpServer():
    def __init__(self):
        self.ADDR = (HOST, PORT)
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            print
            '%d is open' % PORT

            self.sock.bind(self.ADDR)
            self.sock.listen(5)
            # 设置退出条件
            self.STOP_CHAT = False

            # 所有监听的客户端
            self.clients = {}
            self.thrs = {}
            self.stops = []

        except Exception as e:
            print
            "%d is down" % PORT
            return False

    def IsOpen(ip, port):

        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            # s.shutdown(2)
            # 利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
            # 该参数表示s了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
            print
            '%d is open' % port
            return True
        except:
            print
            '%d is down' % port
            return False

    def listen_client(self):
        while not self.STOP_CHAT:
            print(u'等待接入，侦听端口:%d' % (PORT))
            self.tcpClientSock, self.addr = self.sock.accept()
            print(u'接受连接，客户端地址：', self.addr)
            address = self.addr
            # 将建立的client socket链接放到列表self.clients中
            self.clients[address] = self.tcpClientSock
            # 分别将每个建立的链接放入进程中，接收且分发消息
            self.thrs[address] = threading.Thread(target=self.readmsg, args=[address])
            self.thrs[address].start()
            time.sleep(0.5)

    def readmsg(self, address):
        # 如果地址不存在，则返回False
        if address not in self.clients:
            return False
        # 得到发送消息的client socket
        client = self.clients[address]
        while True:
            try:
                # 获取到消息内容data
                data = client.recv(BUFSIZ)
            except:
                print
                error
                self.close_client(address)
                break
            if not data:
                break
            # python3使用bytes，所以要进行编码
            # s='%s发送给我的信息是:[%s] %s' %(addr[0],ctime(), data.decode('utf8'))
            # 对日期进行一下格式化
            ISOTIMEFORMAT = '%Y-%m-%d %X'
            stime = time.strftime(ISOTIMEFORMAT, localtime())
            s = u'%s发送给我的信息是:%s' % (str(address), data.decode('utf8'))
            # 将获得的消息分发给链接中的client socket
            for k in self.clients:
                self.clients[k].send(s.encode('utf8'))
                self.clients[k].sendall(s.encode('utf-8'))

                print
                str(k)
            print(stime), ':', data.decode('utf8')
            # 如果输入quit(忽略大小写),则程序退出
            STOP_CHAT = (data.decode('utf8').upper() == "QUIT")
            if STOP_CHAT:
                print
                "quit"
                self.close_client(address)
                print
                "already quit"
                break

    def close_client(self, address):
        try:
            client = self.clients.pop(address)
            self.stops.append(address)
            client.close()
            for k in self.clients:
                self.clients[k].send(str(address) + u"已经离开了")
        except:
            pass
        print
        str(address) + u'已经退出'


if __name__ == '__main__':
    tserver = TcpServer()
    tserver.listen_client()
