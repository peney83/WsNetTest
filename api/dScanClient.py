#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 15:39'
# @Author  : ZhangXianghui
# @File    : dScanClient.py
# @Software: PyCharm


import json
from datetime import datetime
import time, os
from logger import logger
from websocket import WebSocket
from api.wsClient import wsClient

import websocket
import threading



class dScanClient(wsClient):
    def __init__(self, url):
        super(dScanClient, self).__init__(url)
        self.count = 0
        self.msglist = []
        # wsClient.__init__(self, url)


    def start(self):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        t = threading.Thread(target=self.ws.run_forever, )
        t.start()
        time.sleep(0.1)

    def on_message(self, message):
        self.count = self.count + 1
        print("#######dScanClient on_message:{} #######".format(self.count))
        print(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        print(message)
        message = json.loads(message)
        if message["topic"] == "equipment/deviceInfoResult" \
                or message["topic"] == "equipment/net/result" \
                or message["topic"] == "wifiStatusResult" \
                or message["topic"] == "wifiListResult":
            return

        # 设置用例数据的json文件路径
        jcasef = os.path.join(self.prj_dir, "mockdata", self.caseName.split(":")[0], (self.caseName.split(":")[1] + ".json"))
        # print(jcasef)
        with open(jcasef, encoding="UTF-8") as f:
            cases = json.load(f)

        req = [case for case in cases if self.caseName.split(":")[-1] in case["case"]]
        if len(req) > 0:
            req = req[0]["data"]
            self.send_message(json.dumps(req))
        # data = json.dumps(message, default=lambda obj: obj.__dict__, sort_keys=True, indent=4,
        #                   separators=(",", ":"),
        #                   ensure_ascii=False)
        self.msglist.append(message)
        self.recv_flag = True
        # print(data)