#!/usr/bin/env python3
# coding=utf-8

#　　　　　 　　┏┓ 　┏┓+ +
#　　　　　　　┏┛┻━━━┛┻┓ + +
#　　　　　　　┃　　　　　　　┃ 　
#　　　　　　　┃　　　━　　　┃ ++ + + +
# 　　 　　　  ████━████ ┃+
#　　　　　　　┃　　　　　　　┃ +
#　　　　　　　┃　　　┻　　　┃
#　　　　　　　┃　　　　　　　┃ + +
#　　　　　　　┗━┓　　　┏━┛
#　　　　　　　　┃　　　┃ + + + +
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　　　Code is far away from bug with the animal protecting
#　　　　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug
#　　　　　　　　┃　　　┃
#　　　　　　　　┃　　　┃　　+
#　　　　　　　　┃　 　　┗━━━┓ + +
#　　　　　　　　┃ 　　　　　　　┣┓
#　　　　　　　　┃ 　　　　　　　┏┛
#　　　　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　　　┃┫┫　┃┫┫
# 　　　　　　　　┗┻┛　┗┻┛+ + + +


import socket


STAGE_INIT = 0
STAGE_CONN = 1
STAGE_DONE = 2
STAGE_DESTROYED = 3

BUF_SIZE = 32*1024

def Create_TCP_Socket(hostip, port):
    remoteaddrs = socket.getaddrinfo(hostip, port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
    af, socktype, proto, canonname, sa = remoteaddrs[0]
    remotesock = socket.socket(af, socktype, proto)
    remotesock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    remotesock.setblocking(False)

    try:
        remotesock.connect(sa)
    except BlockingIOError as msg:
        #print('catch BlockingIOError on Create_TCP_Socket', msg)
        return remotesock

    return remotesock
