#!/usr/bin/env python3
# coding=utf-8

import socket
import time
import logging
import select
import errno
import _thread

logger= logging.getLogger("network-client")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("network-client.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def start_epoll(epoll_fd):
    while True:
        epoll_list = epoll_fd.poll()

        for fd, events in epoll_list:
            if select.EPOLLIN & events:
                while True:
                    #datas = b''
                    try:
                        data = connections[fd].recv(4096)
                        if not data:
                            epoll_fd.unregister(fd)
                            connections[fd].close()
                            break

                        logger.debug(data)
                        print(data)
                        break

                    except socket.error as msg:
                        print("error break")
                        epoll_fd.unregister(fd)
                        connections[fd].close()
                        break
            else:
                continue


if __name__=="__main__":
    global connections
    connections = {}

    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as msg:
        logger.error(msg)

    try:
        connFd.connect(("127.0.0.1", 2099))
        logger.debug("Connect to network server success")
    except socket.error as msg:
        logger.error(msg)

    connections[connFd.fileno()] = connFd

    epoll_fd = select.epoll()
    epoll_fd.register(connFd.fileno(), select.EPOLLIN)

    _thread.start_new_thread(start_epoll, (epoll_fd,))

    while True:
        data = input("# ")
        if data == '':
            break

        data = data.encode('utf-8')
        if connFd.send(data) != len(data):
            logger.error("Send data to network server failed")
            break

    connFd.close()
