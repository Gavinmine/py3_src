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


import socket, select
from tcpreplay import TcpReplay
from common import *

if __name__ == '__main__':
    try:
        listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as msg:
        print("Create socket failed")

    try:
        listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Setsocketopt SO_REUSEADDR failed")

    try:
        # 进行 bind -- 此处未指定 ip 地址，即 bind 了全部网卡 ip 上
        listen_fd.bind(('127.0.0.1', 2499))
    except socket.error as msg:
        print("Bind failed")

    try:
        # 设置 listen 的 backlog 数
        listen_fd.listen(1000)
    except socket.error as msg:
        print(msg)

    try:
        # 创建 epoll 句柄
        epoll_fd = select.epoll()
        # 向 epoll 句柄中注册 监听 socket 的 可读 事件
        epoll_fd.register(listen_fd.fileno(), select.EPOLLIN)
    except select.error as msg:
        print(msg)

    #listen_fd.setblocking(0)

    inst_dict = {}

    while True:
        epoll_list = epoll_fd.poll()

        for fd, events in epoll_list:
            if fd == listen_fd.fileno():
                conn, addr = listen_fd.accept()
                #print("accept connection from %s, %d, fd = %d" % (addr[0], addr[1], conn.fileno()))
                conn.setblocking(0)
                TcpReplay(conn, epoll_fd, inst_dict)

            elif select.EPOLLIN & events:
                inst = inst_dict.get(fd, None)
                if not inst:
                    print('not found this socket inst:%d' % fd)
                    break
                inst.handler_datas()
                if inst.destroy():
                    del inst

            elif select.EPOLLOUT & events:
                inst = inst_dict.get(fd, None)
                if not inst:
                    print('not found this socket inst:%d on EPOLLOUT' % fd)
                    break
                inst.handler_datas('s')
                if inst.destroy():
                    del inst
