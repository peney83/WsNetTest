#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 14:04'
# @Author  : ZhangXianghui
# @File    : test_test.py
# @Software: PyCharm

#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 9:12'
# @Author  : ZhangXianghui
# @File    : test_ali.py
# @Software: PyCharm

import pytest
import allure
import json
from testcases.conftest import aliscan_client
from api.util import wait_unitl_aliclient_receive_message


# Allure中对严重级别的定义：
# 1、 Blocker级别：中断缺陷（客户端程序无响应，无法执行下一步操作）
# 2、 Critical级别：临界缺陷（ 功能点缺失）
# 3、 Normal级别：普通缺陷（数值计算错误）
# 4、 Minor级别：次要缺陷（界面错误与UI需求不符）
# 5、 Trivial级别：轻微缺陷（必输项无提示，或者提示不规范）
@pytest.mark.usefixtures("start_sdk")
class TestAli(object):

    @allure.feature("设备检查")
    @allure.severity("Blocker")
    @allure.issue("http://10.10.2.29:7777")
    @allure.testcase("http://10.10.2.28:8000")
    @pytest.mark.equipment
    def test_deviceInfo(self, aliscan_client, server_J):
        """
        用例描述： 查询设备信息
        """
        softVer = []
        padid = "123456"
        req = {
            "topic": "equipment/deviceInfo",
            "padId": padid,
            "mockdata": {}
        }
        # allure.step("发送deviceInfo到foot-ali，并且等待返回")
        aliscan_client.send_message(json.dumps(req))
        wait_unitl_aliclient_receive_message(aliscan_client, 0.5, 10)
        for e in server_J["global"]["softs"]:
            if e["modelCode"] == "foot3dscan":
                softVer = e

        is_deviceInfoResult = False
        for msg in aliscan_client.msglist:
            if msg["topic"] == "equipment/deviceInfoResult" and msg["padId"] == padid:
                is_deviceInfoResult = True
                assert(msg["mockdata"]["algorighmVer"] == softVer["other"]["algorighmVer"])
                assert (msg["mockdata"]["communityVer"] == softVer["other"]["communityVer"])
                assert (msg["mockdata"]["error"]["code"] == 0)
                assert (msg["mockdata"]["firmwareVer"] == softVer["other"]["firmwareVer"])
                assert (msg["mockdata"]["frontVer"] == softVer["other"]["frontVer"])
                assert (msg["mockdata"]["sdkVer"] == softVer["other"]["sdkVer"])
                assert (msg["mockdata"]["status"] == "success")
                assert (msg["mockdata"]["version"] == softVer["version"])
        assert(is_deviceInfoResult)
        aliscan_client.msglist.clear()
        aliscan_client.recv_flag = False
        aliscan_client.close()

    @allure.feature("设备检查")
    @allure.severity("Blocker")
    @allure.issue("http://10.10.2.29:7777")
    @allure.testcase("http://10.10.2.28:8000")
    @allure.story("wifi列表查询")
    @pytest.mark.equipment
    def test_wifi_list(self, aliscan_client, server_J):
        """
        用例描述： 查询wifi列表
        """
        softVer = []
        padid = "123456"
        req = {
            "topic": "equipment/wifi/list",
            "padId": padid,
            "mockdata": {}
        }
        # allure.step("发送deviceInfo到foot-ali，并且等待返回")
        aliscan_client.send_message(json.dumps(req))
        wait_unitl_aliclient_receive_message(aliscan_client, 0.5, 10)
        # print(aliscan_client.msglist)
        aliscan_client.close()

    # def test_wifi_qst(self, aliscan_client, server_J):
    #     """
    #             用例描述： 查询wifi列表
    #             """
    #     softVer = []
    #     padid = "123456"
    #     req = {
    #         "topic": "equipment/wifi/qst",
    #         "padId": padid,
    #         "mockdata": {}
    #     }
    #     allure.step("发送deviceInfo到foot-ali，并且等待返回")
    #     aliscan_client.send_message(json.dumps(req))
    #     wait_unitl_aliclient_receive_message(aliscan_client, 0.5, 10)