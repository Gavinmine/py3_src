#!/usr/bin/env python3
# coding=utf-8

import socket
import time
import logging

logger= logging.getLogger("cmd-client")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("cmd-client.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

if __name__=="__main__":
    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error as msg:
        logger.error(msg)

    try:
        connFd.connect(("127.0.0.1", 2199))
        logger.debug("Connect to cmd server success")
    except socket.error as msg:
        logger.error(msg)

    while True:
        data = input("# ")
        if data == '':
            break
        data = data.encode('utf-8')
        if connFd.send(data) != len(data):
            logger.error("Send data to network server failed")
            break
        readData = connFd.recv(1024)
        print(readData)

    connFd.close()
