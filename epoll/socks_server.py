#!/usr/bin/env python3
# coding=utf-8

import socket, logging
import select, re, struct, gzip
from subprocess import getstatusoutput
#import chardet

CONTEN_LENGTH = re.compile(b'Content\-Length: (\d+)\\r\\n')
CONTEN_TYPE = re.compile(b'Content\-Type: (.*)\\r\\n')
CONTEN_ENCODING = re.compile(b'Content\-Encoding: (\w+)\\r\\n')
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
        listen_fd.listen(100)
    except socket.error as msg:
        logger.error(msg)

    try:
        # 创建 epoll 句柄
        epoll_fd = select.epoll()
        # 向 epoll 句柄中注册 监听 socket 的 可读 事件
        epoll_fd.register(listen_fd.fileno(), select.EPOLLIN)
    except select.error as msg:
        logger.error(msg)

    first_step = {}
    second_step = {}
    connections = {}
    collect_datas = {}

    while True:
        epoll_list = epoll_fd.poll()

        for fd, events in epoll_list:
            if fd == listen_fd.fileno():
                conn, addr = listen_fd.accept()
                logger.info("accept connection from %s, %d, fd = %d" % (addr[0], addr[1], conn.fileno()))

                conn.setblocking(0)
                if conn.fileno() in first_step:
                    logger.warning("fileno is already in first_step, please check:%d" % conn.fileno())
                #epoll_fd.register(conn.fileno(), select.EPOLLIN | select.EPOLLET)
                epoll_fd.register(conn.fileno(), select.EPOLLIN)
                first_step[conn.fileno()] = conn 

            elif select.EPOLLIN & events:
                if fd in first_step:
                    #print('goto first_step')
                    send_data = b''
                    data = first_step[fd].recv(2)
                    #print("first_step fileno:", fd)
                    #print('first_step:', data)
                    #print('first_step length:', len(data))
                    ver, nmethods = struct.unpack('BB', data)
                    send_data += b'\x05'
                    if ver != 0x05:
                        send_data += b'\xff'
                        first_step[fd].send(send_data)
                        epoll_fd.unregister(fd)
                        first_step[fd].close()
                        del first_step[fd]
                        break

                    if nmethods > 0:
                        data = first_step[fd].recv(nmethods)
                        #print('in nmethods recv data:', data)
                        send_data += data
                        first_step[fd].send(send_data)
                        #print("in nmethods send_data:", send_data)
                        second_step[fd] = first_step[fd]
                        del first_step[fd]
                        #print("done of first_step in nmethods")
                        break
                    send_data += b'\x00'
                    first_step[fd].send(send_data)
                    second_step[fd] = first_step[fd]
                    del first_step[fd]
                    #print("done of first_step")
                    break

                elif fd in second_step:
                    #print('goto second_step:', fd)
                    send_data = b''
                    try:
                        datas = second_step[fd].recv(4)
                    except ConnectionResetError as msg:
                        logger.error("recv error:$s" % msg)
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break
                    #print('second_step recv data1:', datas)
                    if datas == b'':
                        logger.debug('not recv anydata, close')
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break
                    ver, cmd, rsv, atype = struct.unpack('BBBB', datas)
                    if ver != 0x05:
                        send_data += b'\x05'
                        send_data += b'\x05'
                        send_data += b'\x00'
                        send_data += b'\x01'
                        send_data += b'\x00'
                        send_data += b'\x00'
                        second_step[fd].send(send_data)
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break

                    if cmd != 0x01:     #BINd:0x02, UDP ASSOCIATE:0x03 not supported yet
                        send_data += b'\x05'
                        send_data += b'\x07'
                        send_data += b'\x00'
                        send_data += b'\x01'
                        send_data += b'\x00'
                        send_data += b'\x00'
                        second_step[fd].send(send_data)
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break

                    if atype == 0x01: #ipv4
                        #logger.info('IPV4')
                        datas = second_step[fd].recv(6)
                        host, port = struct.unpack('!IH', datas)
                        #logger.info("host:$s" % host)
                        #logger.info("port:%d" % port)
                        host_byte = struct.pack('!I', host)
                        #logger.info("host:%d" % host_byte)
                        hostip = socket.inet_ntoa(host_byte)
                        #logger.info("hostip:%s" % hostip)
                    elif atype == 0x03: #domain name
                        #logger.info('domain')
                        datas = second_step[fd].recv(1)
                        length = struct.unpack('B', datas)[0]
                        length = int(length)
                        datas = second_step[fd].recv(length+2)
                        hostname, port = struct.unpack('!%dsH' % length, datas)
                        hostip = socket.gethostbyname(hostname)
                        host = struct.unpack("!I", socket.inet_aton(hostip))[0]
                    elif atype == 0x04: #ipv6, not support yet
                        #logger.info('IPV6')
                        send_data += b'\x05'
                        send_data += b'\x07'
                        send_data += b'\x00'
                        send_data += b'\x01'
                        send_data += b'\x00'
                        send_data += b'\x00'
                        second_step[fd].send(send_data)
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break
                    else:
                        send_data += b'\x05'
                        send_data += b'\x07'
                        send_data += b'\x00'
                        send_data += b'\x01'
                        send_data += b'\x00'
                        send_data += b'\x00'
                        second_step[fd].send(send_data)
                        epoll_fd.unregister(fd)
                        second_step[fd].close()
                        del second_step[fd]
                        break

                    send_data += b'\x05'
                    send_data += b'\x00'
                    send_data += b'\x00'
                    send_data += b'\x01'
                    send_data += struct.pack('!I', host)
                    #send_data += host
                    send_data += struct.pack('!H', port)

                    destaddrs = socket.getaddrinfo(hostip, port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
                    af, socktype, proto, canonname, sa = destaddrs[0]
                    destsock = socket.socket(af, socktype, proto)
                    destsock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

                    try:
                        destsock.connect((hostip, port))
                        destsock.setblocking(False)
                    except ConnectionRefusedError as msg:
                        logger.error('connection error msg:$s' % msg)
                        logger.error('connection to $s:%d error' % hostip, port)
                        break
                    except IOError as e:
                        #print('catch IOError')
                        pass
                    #epoll_fd.register(destFd.fileno(), select.EPOLLIN | select.EPOLLET)
                    epoll_fd.register(destsock.fileno(), select.EPOLLIN)
                    connections[destsock.fileno()] = (destsock, second_step[fd])
                    connections[fd] = (second_step[fd], destsock)
                    collect_datas[fd] = b''
                    collect_datas[destsock.fileno()] = b''
                    second_step[fd].send(send_data)
                    del second_step[fd]
                    #print('connected!!')
                    break


                elif fd in connections:
                    data = b''
                    try:
                        data = connections[fd][0].recv(4096)
                        #remote side has close socket, closed this side
                        if not data:
                            logger.debug('recvive datas from done  :%s' % connections[fd][0])
                            logger.debug('send those datas below to:%s' % connections[fd][1])
                            match = CONTEN_LENGTH.search(collect_datas[fd])
                            if match:
                                datas = collect_datas[fd]
                                content_length = match.groups(0)[0]
                                content_length = content_length.decode('utf8')
                                content_length = int(content_length)
                                headers = datas[:-content_length]
                                #headers = headers.decode('utf8')
                                content = datas[-content_length:]
                                match = CONTEN_TYPE.search(headers)
                                if match and match.groups(0)[0] == b'text/html':
                                    content = gzip.decompress(content)
                                    content = content.decode('utf8')
                                    logger.debug('all recv headers:%s' % headers)
                                    logger.debug('all recv content:%s' % content)
                            #print('data type:', chardet.detect(collect_datas[fd]))
                            second_file = connections[fd][1].fileno()
                            epoll_fd.unregister(fd)
                            epoll_fd.unregister(second_file)
                            connections[fd][0].close()
                            connections[fd][1].close()
                            del connections[fd]
                            del connections[second_file]
                            del collect_datas[fd]
                            break
                        #logger.info("#####################################")
                        #logger.info("recv fd:%s" % connections[fd][0])
                        #logger.info("data_length:%d" % len(data))
                        #logger.info("recv datas: %s" % data)
                        collect_datas[fd] += data
                        connections[fd][1].send(data)
                    except ConnectionResetError as msg:
                        logger.error('recv error on connections %s' % connections[fd][0])
                        logger.error('send those datas below to %s' % connections[fd][1])
                        logger.error('all recv datas:%s' % collect_datas[fd])
                        second_file = connections[fd][1].fileno()
                        epoll_fd.unregister(fd)
                        epoll_fd.unregister(second_file)
                        connections[fd][0].close()
                        connections[fd][1].close()
                        del connections[fd]
                        del connections[second_file]
                        del collect_datas[fd]
                        break
                    except BlockingIOError as msg:
                        #logger.info('recv done:%s' % msg)
                        break
