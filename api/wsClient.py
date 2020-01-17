#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/6 10:25'
# @Author  : ZhangXianghui
# @File    : wsClient.py
# @Software: PyCharm


import asyncio
import json
import websockets
from websockets.exceptions import (
    ConnectionClosedError,
    ConnectionClosedOK,
    ConnectionClosed
)
from datetime import datetime
import time, os
from logger import logger
from websocket import WebSocket


import websocket
import threading


class wsClient(object):
    def __init__(self, url):
        # super(wsClient, self).__init__()
        self.recv_num = 0
        self.recv_flag = False
        self.send_num = 0
        self.msglist = []
        self.url = url
        self.ws = None
        self.caseName = ""
        # 获取项目根路径
        self.prj_dir = os.path.dirname(os.path.dirname(__file__))

    def on_message(self, message):
        print("#######aliClient on_message #######")
        print(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        message = json.loads(message)
        if message["topic"] == "equipment/scan/status" and message["padId"] == "":
            return

        data = json.dumps(message, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
                          separators=(",", ":"),
                          ensure_ascii=False)
        self.msglist.append(message)
        self.recv_flag = True
        print(data)

    def on_error(self, error):
        print("####### on_error #######")
        # print(self)
        print(error)

    def on_close(self):
        print("####### on_close #######")
        # print(self)

    def on_open(self):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                req = {
                    "topic": "equipment/deviceInfo",
                    "padId": "1111",
                    "mockdata": {}
                }
                req = json.dumps(req)
                self.ws.send(req)

        t = threading.Thread(target=run, )
        t.setDaemon(True)
        t.start()

    def start(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        # def run(*args):
        #     self.ws.run_forever()
        t = threading.Thread(target=self.ws.run_forever, )
        t.start()
        time.sleep(0.1)

    def on_recv(self, ws):
        def recv_msg(*args):
            while True:
                data = ws.recv()
                if data is not None:
                    data = json.loads(data)
                    self.recv_num += 1
                    self.recv_flag = True
                    self.msglist.append(data)
                    data = json.dumps(data, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
                                      separators=(",", ":"),
                                      ensure_ascii=False)
                    print(data)
        t = threading.Thread(target=recv_msg, )
        t.setDaemon(True)
        t.start()

    def send_message(self, req):
        self.ws.send(req)

    def close(self):
        self.ws.close()



# class wsClient(object):
#     def __init__(self, url):
#         self.recv_num = 0
#         self.recv_flag = False
#         self.send_num = 0
#         self.msglist = []
#         self.url = url
#         self.ws = websocket.create_connection(self.url)
#         # self.ws.on_open = on_open
#         WebSocket.recv_frame()
#         # self.ws.run_forever()
#
#     def on_recv(self):
#         def recv_msg(*args):
#             while True:
#                 mockdata = self.ws.recv()
#                 if mockdata is not None:
#                     mockdata = json.loads(mockdata)
#                     self.recv_num += 1
#                     self.recv_flag = True
#                     self.msglist.append(mockdata)
#                     # mockdata = json.dumps(mockdata, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
#                     #                   separators=(",", ":"),
#                     #                   ensure_ascii=False)
#                     print(mockdata)
#         t = threading.Thread(target=recv_msg, )
#         t.setDaemon(True)
#         t.start()
#
#     def send(self):
#         req = {
#             "topic": "equipment/deviceInfo",
#             "padId": "1111",
#             "mockdata": {}
#         }
#         req = json.dumps(req)
#         self.ws.send(req)












# class wsClient2(object):
#     def __init__(self, url):
#         self.recv_num = 0
#         self.recv_flag = False
#         self.send_num = 0
#         self.msglist = []
#         self.url = url
#         with websockets.connect("ws://127.0.0.1:8080/aliscan") as websocket:
#             self.ws = websocket
#
#
#     def send_msg(self, req):
#         # while True:
#         self.ws.send(req)
#
#     def recv(self):
#         t = threading.Thread(target=self.recv_msg, )
#         t.setDaemon(True)
#         t.start()
#
#
#     def recv_msg(self):
#         while True:
#             mockdata =  self.ws.recv()
#             if mockdata is not None:
#                 mockdata = json.loads(mockdata)
#                 self.recv_num += 1
#                 self.recv_flag = True
#                 self.msglist.append(mockdata)
#                 mockdata = json.dumps(mockdata, default=lambda obj: obj.__dict__, sort_keys=True, indent=4, separators=(",", ":"),
#                                   ensure_ascii=False)
#                 print(mockdata)

# class wsClient(object):
#     def __init__(self, url):
#         self.recv_num = 0
#         self.recv_flag = False
#         self.send_num = 0
#         self.msglist = []
#         self.url = url
#
#
#     def open_ws(self):
#         self.ws = websockets.connect(self.url)
#         asyncio.get_event_loop().run_until_complete(self.recv_msg())
#
#     async def send_msg(self, req_json):
#         # while True:
#         await self.ws.send(req_json)
#
#     async def recv_msg(self):
#         while True:
#             mockdata = await self.ws.recv()
#             if mockdata is not None:
#                 mockdata = json.loads(mockdata)
#                 self.recv_num += 1
#                 self.recv_flag = True
#                 self.msglist.append(mockdata)
#                 mockdata = json.dumps(mockdata, default=lambda obj: obj.__dict__, sort_keys=True, indent=4, separators=(",", ":"),
#                                   ensure_ascii=False)
#                 print(mockdata)

























# import socket
# from websocket import create_connection, WebSocket
#
# class MyWebSocket(WebSocket):
#     def recv_frame(self):
#         frame = super().recv_frame()
#         print(frame)
#         return frame






if __name__ == "__main__":
    url = "ws://127.0.0.1:8080/aliscan"
    # aliscanclient = wsClient("ws://127.0.0.1:8080/aliscan")
    req = {
        "topic": "equipment/deviceInfo",
        "padId": "1111",
        "mockdata": {}
    }
    req = json.dumps(req)

    wsc = wsClient(url)
    wsc.start()

    wsc.send_message(req)
    time.sleep(1)
    # wsc.close()



