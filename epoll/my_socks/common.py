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


import socket,re,gzip


STAGE_INIT = 0
STAGE_CONN = 1
STAGE_DONE = 2
STAGE_DESTROYED = 3

BUF_SIZE = 32*1024

CONTEN_LENGTH = re.compile(b'Content\-Length: (\d+)\\r\\n')
CONTEN_TYPE = re.compile(b'Content\-Type: (.*)\\r\\n')
CONTEN_ENCODING = re.compile(b'Content\-Encoding: (\w+)\\r\\n')

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


def datas_parser(datas, count = 1):
    try:
        headers, contents = datas.split(b'\r\n\r\n', 1)
    except ValueError as msg:
        return count
        #headers = datas

    match = CONTEN_LENGTH.search(headers)
    if match:
        content_length = match.groups(0)[0]
        content_length = content_length.decode('utf8')
        content_length = int(content_length)
        if len(contents) == content_length:
            content = contents
        elif len(contents) > content_length:
            content = contents[:content_length]
            left_datas = contents[content_length:]
            count += 1
            datas_parser(left_datas, count)

        else:   #connect error
            return count

        match = CONTEN_TYPE.search(headers)
        if match and match.groups(0)[0] == b'image/jpeg':
            jpg_name = 'test_%d.jpg' % count
            #print('JPG_%d Content Length:%d' % (count, content_length))
            jpg_w = open(jpg_name, 'wb')
            jpg_w.write(content)
            jpg_w.close()
            count += 1
        elif match and match.groups(0)[0] == b'text/html':
            content = gzip.decompress(content)
            content = content.decode('utf8')
        elif match and match.groups(0)[0] == b'audio/mpeg;charset=UTF-8':
            mp3_name = 'mp3_%d.mp3' % count
            #print('MP3_%d Content Length:%d' % (count, content_length))
            mp3_w = open(mp3_name, 'wb')
            mp3_w.write(content)
            mp3_w.close()
            count += 1

        elif match and match.groups(0)[0] == b'video/mp4':
            mp4_name = 'mp4_%d.mp4' % count
            #print('MP3_%d Content Length:%d' % (count, content_length))
            mp4_w = open(mp4_name, 'wb')
            mp4_w.write(content)
            mp4_w.close()
            count += 1

    return count
