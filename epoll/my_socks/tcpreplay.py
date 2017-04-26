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


import socket, struct, errno
from common import *
from select import EPOLLIN, EPOLLERR, EPOLLOUT


class TcpReplay(object):
    def __init__(self, sock, loop, inst_dict, stage = STAGE_INIT, remoteinst = None):
        self.sockfd = sock.fileno()
        self.sock = sock
        self.stage = stage
        self.remoteinst = remoteinst
        self.loop = loop
        self.inst_dict = inst_dict
        self.loop.register(self.sockfd, EPOLLERR|EPOLLIN)
        self.inst_dict[self.sockfd] = self
        self.left_datas = b''
        self._all_recv_datas = b''
        self._read_closed = False
        self._write_closed = False


    def handler_datas(self, flag = 'r'):
        if flag == 's':
            self.send_datas()
            if self._read_closed:
                return
            self.loop.modify(self.sockfd, EPOLLERR|EPOLLIN)
            return

        send_datas = b'\x05'
        if self.stage == STAGE_INIT:
            datas = self.recv_datas(2)
            if not datas:
                return
            ver, nmethods = struct.unpack('BB', datas)
            #print('ver:%s, nmethods:%s' % (ver, nmethods))
            if ver != 0x05:
                send_datas += b'\xff'
                self.send_datas(send_datas)
                self._mark_Destory()
                return

            if nmethods > 0:
                datas = self.recv_datas(nmethods)
                if not datas:
                    return
                send_datas += datas

            else:
                send_datas += b'\x00'

            #print('send_datas:', send_datas)
            self.send_datas(send_datas)
            self.stage = STAGE_CONN
            return

        elif self.stage == STAGE_CONN:
            datas = self.recv_datas(4)
            if not datas:
                return

            ver, cmd, rsv, atype = struct.unpack('BBBB', datas)
            if ver != 0x05:
                send_datas += b'\x05'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self._mark_Destory()
                return

            if cmd != 0x01:     #BINd:0x02, UDP ASSOCIATE:0x03 not supported yet
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self._mark_Destory()
                return

            if atype == 0x01: #ipv4
                datas = self.recv_datas(6)
                host, port = struct.unpack('!IH', datas)
                host_byte = struct.pack('!I', host)
                hostip = socket.inet_ntoa(host_byte)

            elif atype == 0x03: #domain name
                datas = self.recv_datas(1)
                length = struct.unpack('B', datas)[0]
                length = int(length)
                datas = self.recv_datas(length+2)
                hostname, port = struct.unpack('!%dsH' % length, datas)
                try:
                    hostip = socket.gethostbyname(hostname)
                except TimeoutError as msg:
                    send_datas += b'\x07'
                    send_datas += b'\x00'
                    send_datas += b'\x01'
                    send_datas += b'\x00'
                    send_datas += b'\x00'
                    self.send_datas(send_datas)
                    self._mark_Destory()
                    return
                host = struct.unpack("!I", socket.inet_aton(hostip))[0]

            elif atype == 0x04: #ipv6, not support yet
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self._mark_Destory()
                return

            else:
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self._mark_Destory()
                return

            send_datas += b'\x00'
            send_datas += b'\x00'
            send_datas += b'\x01'
            send_datas += struct.pack('!I', host)
            send_datas += struct.pack('!H', port)
            remotesock = Create_TCP_Socket(hostip, port)
            remoteinst = TcpReplay(remotesock, self.loop, self.inst_dict, stage = STAGE_DONE, remoteinst = self)
            self.remoteinst = remoteinst
            self.send_datas(send_datas)
            self.stage = STAGE_DONE
            return

        elif self.stage == STAGE_DONE:
            datas = self.recv_datas()
            #print('datas:', datas)
            if not datas:
                return
            self._all_recv_datas += datas
            self.remoteinst.send_datas(datas)


    def recv_datas(self, length=BUF_SIZE):
        try:
            datas = self.sock.recv(length)
        except ConnectionResetError as msg:
            self._read_closed = True
            return

        if datas == b'':
            self._read_closed = True
            self.loop.modify(self.sockfd, EPOLLERR|EPOLLOUT)
            self._read_closed = True

        return datas


    def send_datas(self, datas=b''):
        self.left_datas += datas
        if self.left_datas == b'':
            self._write_closed = True
            return
        if self._write_closed:
            return
        try:
            length = self.sock.send(self.left_datas)
        except BlockingIOError as msg:
            if msg.errno == errno.EAGAIN or msg.errno == errno.EINPROGRESS or msg.errno == errno.EWOULDBLOCK:
                self.loop.modify(self.sockfd, EPOLLERR|EPOLLOUT)
                return
            self._write_closed = True
            return
        except OSError as msg:
            self._write_closed = True
            return

        self.left_datas = b''


    def destroy(self):
        if not self._write_closed or not self._read_closed:
            return False

        self.loop.unregister(self.sockfd)
        del self.inst_dict[self.sockfd]
        self.sock.close()
        #self._datas_Parser()
        #print('removed done %d      %s' % (self.sockfd, self.sock))
        return True


    def _mark_Destory(self):
        self._write_closed = True
        self._read_closed = True


    def _datas_Parser(self):
        datas_parser(self._all_recv_datas, 1)
