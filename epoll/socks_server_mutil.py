#!/usr/bin/env python3
# coding=utf-8

import socket, logging
import struct 
import _thread
from subprocess import getstatusoutput

logger = logging.getLogger("scoks_server")

def InitLog():
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler("socks_server.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


def Runcmd(cmd=None):
    if not cmd:
        return None

    result=getstatusoutput(cmd)
    return result[1].encode('utf-8')


def switch_datas(src, dest):
    try:
        while True:
            data = src.recv(1024)
            if not data:
                break
            dest.sendall(data)
    finally:
        src.close()
        dest.close()


def switch_traffic(conn):
    datas = conn.recv(1024)
    print("1 datas:%s" % datas)
    senddata=b'\x05\x00'
    conn.send(senddata)
    datas = conn.recv(1024)
    print("2 datas:%s" % datas)
    unpack_datas = datas[:4]
    ver, cmd, rsv, atype = struct.unpack('BBBB', unpack_datas)
    print("Ver:%d, cmd:%d, rsv:%d, atype:%d" % (ver, cmd, rsv, atype))
    length_datas = datas[4:5]
    length = struct.unpack('B', length_datas)[0]
    length = int(length)
    print("length:%d" % length)
    addr_datas = datas[5:]
    hostname, port = struct.unpack('!%dsH' % length, addr_datas)
    print("hostname:%s" % hostname)
    print("port:%s" % port)

    hostip = socket.gethostbyname(hostname)
    print("hostip:%s" % hostip)

    #nothing different
    #host = struct.unpack("!I", socket.inet_aton('127.0.0.1'))[0]
    host = struct.unpack("!I", socket.inet_aton(hostip))[0]

    senddata = struct.pack('!BBBBIH', 0x05, 0x00, 0x00, 0x01, host, port)
    conn.send(senddata)

    destFd = socket.create_connection((hostip, port))
    _thread.start_new_thread(switch_datas, (conn, destFd,))
    _thread.start_new_thread(switch_datas, (destFd, conn,))


if __name__=="__main__":
    InitLog()
    
    try:
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as msg:
        logger.error("Create socket failed")

    try:
        listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        logger.error("Setsocketopt SO_REUSEADDR failed")

    try:
        # 进行 bind -- 此处未指定 ip 地址，即 bind 了全部网卡 ip 上
        listen_fd.bind(('127.0.0.1', 2499))
    except socket.error as msg:
        logger.error("Bind failed")

    try:
        # 设置 listen 的 backlog 数
        listen_fd.listen(10)
    except socket.error as msg:
        logger.error(msg)

    while True:
        conn, addr = listen_fd.accept()
        print("accept connection from %s, %d, fd = %d" % (addr[0], addr[1], conn.fileno()))
        _thread.start_new_thread(switch_traffic, (conn,))
