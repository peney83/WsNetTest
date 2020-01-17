#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 9:54'
# @Author  : ZhangXianghui
# @File    : ReadServerJson.py
# @Software: PyCharm


import json



server_jsonf = "../sdk/dist/.server.json"


def readServerJson(server_jsonf):
    with open(server_jsonf) as load_f:
        load_dict = json.load(load_f)
        return load_dict