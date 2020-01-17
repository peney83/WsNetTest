#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/12 18:46'
# @Author  : ZhangXianghui
# @File    : Testscan.py
# @Software: PyCharm

import pytest
import allure
import json, os, time

from api.util import wait_unitl_client_receive_message


# Allure中对严重级别的定义：
# 1、 Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
# 2、 Critical级别：临界缺陷（ 功能点缺失）
# 3、 Normal级别：普通缺陷（数值计算错误）
# 4、 Minor级别：次要缺陷（界面错误与UI需求不符）
# 5、 Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）

padid = "123456"
DEVICE_DISK_ID = "S2G0NX0H515606"
DEVICE_ID = "G6BE92800GEC"
STORE_ID = "XLMLSTEST001"



class Testscan():
    # def CaseDataPath(dscan_client):
    #     json_dir = dscan_client.caseName.split("::")[0]
    #     json_file = dscan_client.caseName.split("::")[1] + ".json"
    #     # 设置用例数据的json文件路径
    #     casepath = os.path.join(dscan_client.prj_dir, "mockdata", json_dir, json_file)
    #     return casepath


    @allure.feature("扫描接口功能测试")
    @allure.severity("Blocker")
    @allure.issue("http://10.10.2.29:7777")
    @allure.testcase("http://10.10.2.28:8000")
    @pytest.mark.equipment
    # @pytest.mark.parametrize("status", ["unready", "waitBinding", "duringDownLicense", "licenseChecking",
    #                                     "waitWifiSetting", "init", "free", "debug", "booking", "calibrating",
    #                                     "scanning", "computing", "abnormal"])
    @pytest.mark.parametrize("status", "unready")
    def test_scan_send_status_to_front(self, aliscan_client, dscan_client, status):
        """
        用例描述： 设备端主动推送相应的状态到前端
        """
        # json_dir = dscan_client.caseName.split(":")[0]
        # json_file = dscan_client.caseName.split(":")[1] + ".json"
        # # 设置用例数据的json文件路径
        # casepath = os.path.join(dscan_client.prj_dir, "mockdata", json_dir, json_file)
        # print(casepath)
        # with open(casepath, encoding="UTF-8") as f:
        #     cases = json.load(f)
        # t = dscan_client.caseName.split(":")[-1].split("[")[0]
        # print(t)
        # req = [e for e in cases if dscan_client.caseName.split(":")[-1].split("[")[0] in e["case"]]
        # if len(req) > 0:
        #     req = req[0]["data"]
        #     req["status"] = status
        #     dscan_client.send_message(json.dumps(req))
        req = {
            "topic": "wifiListResult",
            "status": "success",
            "errorCode": 0,
            "padId": "123456",
            "params": [
                {
                    "ssid": "ABC",
                    "rssi": "-50",
                    "isCurrent": False,
                    "isOurAp": False
                },
                {
                    "ssid": "中文@#￥%AAA",
                    "rssi": "-50",
                    "isCurrent": False,
                    "isOurAp": True
                }
            ]
        }
        dscan_client.send_message(json.dumps(req))
        # 判断模拟设备端dScan 收到wifiList消息
        wait_unitl_client_receive_message(aliscan_client, "equipment/scan/status", 0.5, 10)
        e = [e for e in aliscan_client.msglist if e["topic"] == "equipment/scan/status" and e["padId"] == padid]
        print("===={}".format(e))
        assert (e[0]["data"]["status"] == status)

   # def test_test(self, aliscan_client, dscan_client):