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
        self._uncomplete = False
        self._all_recv_datas = b''


    def handler_datas(self, flag = 'r'):
        if flag == 's':
            #print('can sendddddddd')
            self.loop.unregister(self.sockfd)
            self.loop.register(self.sockfd, EPOLLERR|EPOLLIN)
            self.send_datas(self.left_datas)
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
                #need remove socket and instance 
                self.stage = STAGE_DESTROYED
                #self.destroy()
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
                self.stage = STAGE_DESTROYED
                #self.destroy()
                return

            if cmd != 0x01:     #BINd:0x02, UDP ASSOCIATE:0x03 not supported yet
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self.stage = STAGE_DESTROYED
                #self.destroy()
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
                hostip = socket.gethostbyname(hostname)
                host = struct.unpack("!I", socket.inet_aton(hostip))[0]

            elif atype == 0x04: #ipv6, not support yet
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self.stage = STAGE_DESTROYED
                #self.destroy()
                return

            else:
                send_datas += b'\x07'
                send_datas += b'\x00'
                send_datas += b'\x01'
                send_datas += b'\x00'
                send_datas += b'\x00'
                self.send_datas(send_datas)
                self.stage = STAGE_DESTROYED
                #self.destroy()
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
            #self.left_datas += datas
            #self.remoteinst.send_datas(self.left_datas)


    def recv_datas(self, length=BUF_SIZE):
        try:
            datas = self.sock.recv(length)
        except ConnectionResetError as msg:
            #print('catch error message on recv_datas:', msg)
            self.stage = STAGE_DESTROYED
            #self.destroy()
            return

        if datas == b'':
            #print('not recv any datas, mark destroy')
            self.stage = STAGE_DESTROYED
            #self.destroy()

        return datas


    def send_datas(self, datas):
        try:
            length = self.sock.send(datas)
        except BlockingIOError as msg:
            if msg.errno == errno.EAGAIN or msg.errno == errno.EINPROGRESS or msg.errno == errno.EWOULDBLOCK:
                #print('modify epoll')
                self.loop.unregister(self.sockfd)
                self.loop.register(self.sockfd, EPOLLERR|EPOLLOUT)
                self.left_datas += datas
                self._uncomplete = True
                return
            print('IOError catach exception on send_datas:%s     %d     %s' % (msg, self.sockfd, self.sock))
            self.stage = STAGE_DESTROYED
            #self.destroy()
            return
        except OSError as msg:
            print('OSError catach exception on send_datas:%s     %d     %s' % (msg, self.sockfd, self.sock))
            print('send those datas error:', datas)
            self.stage = STAGE_DESTROYED
            #self.destroy()
            return

        self.left_datas = b''
        self._uncomplete = False
        #print('send length:', length)

        #self.left_datas = datas[length:]

    def destroy(self):
        self.loop.unregister(self.sockfd)
        del self.inst_dict[self.sockfd]
        #print('inst_dict length:%d' % len(self.inst_dict))
        #self.sock.close()
        print('removed done %d      %s' % (self.sockfd, self.sock))


#    def destroy(self):
#        if self.stage == STAGE_DESTROYED:
#            print('already destroy')
#            return
#        self.loop.unregister(self.sockfd)
#        del self.inst_dict[self.sockfd]
#        self.sock.close()
#        print('removed done')
#        self.stage = STAGE_DESTROYED