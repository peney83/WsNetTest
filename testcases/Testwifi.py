#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 14:07'
# @Author  : ZhangXianghui
# @File    : test_aliscan.py
# @Software: PyCharm

import pytest
import allure
import json, os, time
# from testcases.conftest import aliscan_client
# from testcases.conftest import dscan_client
from api.util import wait_unitl_aliclient_receive_message
from api.util import wait_unitl_dScanclient_receive_message
from api.util import wait_unitl_client_receive_message



# Allure中对严重级别的定义：
# 1、 Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
# 2、 Critical级别：临界缺陷（ 功能点缺失）
# 3、 Normal级别：普通缺陷（数值计算错误）
# 4、 Minor级别：次要缺陷（界面错误与UI需求不符）
# 5、 Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）

padid = "123456"
@pytest.mark.usefixtures("start_sdk")
class Testwifi(object):


    def test_run(self,):
        print("test_run")



    @allure.feature("设备检查")
    @allure.severity("Blocker")
    @allure.issue("http://10.10.2.29:7777")
    @allure.testcase("http://10.10.2.28:8000")
    @pytest.mark.equipment
    def test_deviceInfo(self, aliscan_client, serverVariabes):

        """
        用例描述： 查询设备信息
        """

        softVer = []
        req = {
            "topic": "equipment/deviceInfo",
            "padId": padid,
            "data": {}
        }
        # allure.step("发送deviceInfo到foot-ali，并且等待返回")
        aliscan_client.send_message(json.dumps(req))
        wait_unitl_client_receive_message(aliscan_client, "equipment/deviceInfoResult", 0.5, 10)
        for e in serverVariabes["global"]["softs"]:
            if e["modelCode"] == "foot3dscan":
                softVer = e

        is_deviceInfoResult = False
        for msg in aliscan_client.msglist:
            if msg["topic"] == "equipment/deviceInfoResult" and msg["padId"] == padid:
                is_deviceInfoResult = True
                assert(msg["data"]["algorighmVer"] == softVer["other"]["algorighmVer"])
                assert (msg["data"]["communityVer"] == softVer["other"]["communityVer"])
                assert (msg["data"]["error"]["code"] == 0)
                assert (msg["data"]["firmwareVer"] == softVer["other"]["firmwareVer"])
                assert (msg["data"]["frontVer"] == softVer["other"]["frontVer"])
                assert (msg["data"]["sdkVer"] == softVer["other"]["sdkVer"])
                assert (msg["data"]["status"] == "success")
                assert (msg["data"]["version"] == softVer["version"])
        assert(is_deviceInfoResult)

    @allure.feature("wifi接口功能测试")
    @allure.severity("Blocker")
    @allure.story("wifi列表查询成功")
    @pytest.mark.equipment
    def test_query_wifi_list_success(self, aliscan_client, dscan_client):
        """
        用例描述： 查询wifi列表成功
        """
        softVer = []
        req = {
            "topic": "equipment/wifi/list",
            "padId": padid,
            "data": {}
        }
        # allure.step("发送deviceInfo到foot-ali，并且等待返回")
        aliscan_client.send_message(json.dumps(req))
        # 判断模拟设备端dScan 收到equipment/wifi/list 消息
        # 判断模拟前端aliScan 收到wifiListResult消息
        wait_unitl_client_receive_message(aliscan_client, "equipment/wifi/result", 0.5, 10)
        wait_unitl_client_receive_message(dscan_client, "wifiList", 0.5, 10)

        # e = [e for e in dscan_client.msglist if e["topic"] == "wifiList" and e["padId"] == padid]
        # if not e:
        #     pytest.fail("模拟设备端dScan没有收到wifiList 消息")
        e = [e for e in aliscan_client.msglist if e["topic"] == "equipment/wifi/result" and e["padId"] == padid]
        # if not e:
        #     pytest.fail("模拟前端aliScan没有收到equipment/wifi/result 消息")

        assert (e[0]["data"]["count"] == 2)

    @allure.feature("wifi接口功能测试")
    @allure.severity("Blocker")
    @allure.story("wifi列表查询失败")
    @pytest.mark.equipment
    def test_query_wifi_list_failed(self, aliscan_client, dscan_client):
        """
        用例描述： 查询wifi列表失败
        """
        softVer = []
        req = {
            "topic": "equipment/wifi/list",
            "padId": padid,
            "data": {}
        }
        allure.step("aliscan发送deviceInfo到foot-ali，并且等待返回")
        aliscan_client.send_message(json.dumps(req))
        # 判断模拟设备端dScan 收到wifiList消息
        wait_unitl_client_receive_message(dscan_client, "wifiList", 0.5, 10)

        # # 判断模拟设备端dScan 收到wifiList消息
        # allure.step("判断模拟设备端dScan 收到wifiList消息")
        # e = [e for e in dscan_client.msglist if e["topic"] == "wifiList" and e["padId"] == padid]
        # if not e:
        #     pytest.fail("模拟设备端dScan没有收到wifiList 消息")

        # 判断模拟前端aliScan 无法收到wifiListResult消息，导致超时
        allure.step("判断模拟前端aliScan 在5秒内无法收到wifiListResult消息")
        for i in range(10):
            e = [e for e in aliscan_client.msglist if e["topic"] == "equipment/wifi/result" and e["padId"] == padid]
            if e:
                pytest.fail("模拟前端aliScan收到了不应该的equipment/wifi/result 消息")
            time.sleep(0.5)

    @allure.feature("wifi接口功能测试")
    @allure.severity("Blocker")
    @allure.story("成功查询wifi状态，并返回正确的状态")
    @pytest.mark.parametrize("netstatus", ["connected", "unconnected", "noInternet"])
    def test_query_wifi_status_return(self, aliscan_client, dscan_client, netstatus):
        """
        用例描述： 成功查询wifi状态
        """
        req = {
            "topic": "equipment/wifi/qst",
            "padId": padid,
            "data": {}
        }
        with allure.step("模拟前端发送equipment/wifi/qst到foot-ali，并且等待返回结果"):
            aliscan_client.send_message(json.dumps(req))

        with allure.step("等待模拟前端aliScan收到equipment/wifi/status消息"):
            wait_unitl_client_receive_message(aliscan_client, "equipment/wifi/status", 0.5, 10)
        with allure.step("等待模拟设备端dScan收到wifiStatus消息"):
            wait_unitl_client_receive_message(dscan_client, "wifiStatus", 0.5, 10)

        e = [e for e in aliscan_client.msglist if e["topic"] == "equipment/wifi/status" and e["padId"] == padid]
        assert (e[0]["data"]["status"] == netstatus)

    @allure.feature("wifi接口功能测试")
    @allure.severity("Blocker")
    @allure.story("设置连接指定wifi，并返回正确的状态")
    def test_connect_wifi_and_return(self, aliscan_client, dscan_client):
        pass



if __name__ == "__main__":
    import subprocess
    cur_path = os.path.dirname(__file__)
    sdk_exe = cur_path + "../sdk/dist/footer-ali.exe"
    cmd = sdk_exe + " run"
    subprocess.Popen(cmd, shell=True)