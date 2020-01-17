#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 9:01'
# @Author  : ZhangXianghui
# @File    : conftest.py
# @Software: PyCharm


import pytest
import os
import time
import yaml
import pkg_resources
import sys
import json
from os.path import abspath, join, dirname
from api.util import wait_unitl_client_receive_message
from api.util import wait_unitl_device_status_to_expect


if os.path.abspath(".") not in sys.path:
    sys.path.append(os.path.abspath("."))
print(sys.path)


from api.wsClient import wsClient
from api.dScanClient import dScanClient
from api.ReadServerJson import readServerJson
import collections
import parameterize
import subprocess


g = collections.defaultdict(parameterize.Parameter)


server_jsonf = os.path.dirname(__file__) + "/../sdk/dist/.server.json"

cur_path = os.path.dirname(__file__)


@pytest.fixture(scope="session")
def start_sdk():
    sdk_path = os.path.join(cur_path, "../sdk/dist")
    sdk_exe = os.path.join(sdk_path, "footer-ali.exe")
    cmd = sdk_exe + " run --config " + os.path.join(os.path.dirname(sdk_exe), ".server.json")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(p.stdout.readline, ""):
        print(line)
        if "starting socket server" in str(line):
            print("====start")
            break
    yield
    print("terminate footer-ali.exe")
    os.system("chcp 65001 && taskkill /f /im footer-ali.exe")



@pytest.fixture(scope="session")
def variables(variables):
    config_file = pkg_resources.resource_filename(__name__, "default.yaml")
    with open(config_file, "r") as f:
        variables.update(yaml.load(f.read()))

    with g["variables"].parameterize(variables):
        yield variables


@pytest.fixture(scope="function")
def aliscan_client():
    url = "ws://127.0.0.1:8080/aliscan"
    ali_c = wsClient(url)
    ali_c.start()
    yield ali_c
    ali_c.msglist.clear()
    ali_c.recv_flag = False
    ali_c.close()


@pytest.fixture(scope="function")
def dscan_client():
    url = "ws://127.0.0.1:8080/dscan"
    d_c = dScanClient(url)

    c_l = os.environ.get("PYTEST_CURRENT_TEST").split("::")
    case = c_l[-1].split()[0]
    d_c.caseName = "dscan:" + ":".join([c_l[1], case])
    print(d_c.caseName)

    d_c.start()
    yield d_c
    d_c.msglist.clear()
    d_c.recv_flag = False
    d_c.close()



@pytest.fixture
def serverVariabes():
    server_config = readServerJson(server_jsonf)
    return server_config



@pytest.fixture(scope="function")
def device_connect_wifi_and_setup_Ap(aliscan_client, dscan_client, wissid="shining3d"):
    padid = "123456"
    req = {
            "topic": "wifiListResult",
            "status": "success",
            "errorCode": 0,
            "padId": padid,
            "params": [
                {
                    "ssid": wissid,
                    "rssi": "-50",
                    "isCurrent": True,
                    "isOurAp": False
                },
                {
                    "ssid": "zbb-hahaha-rc1",
                    "rssi": "-50",
                    "isCurrent": False,
                    "isOurAp": True
                }
            ]
        }
    dscan_client.send_message(json.dumps(req))
    wait_unitl_client_receive_message(aliscan_client, "equipment/wifi/result", 0.5, 10)
    e = [e for e in aliscan_client.msglist if e["topic"] == "equipment/scan/status" and e["padId"] == padid]
    assert (e[0]["data"]["status"] == "success")
    wait_unitl_client_receive_message(aliscan_client, "equipment/wifi/status", 0.5, 10)
    wait_unitl_device_status_to_expect(aliscan_client, "waitLicense", 0.5, 10)
    return aliscan_client, dscan_client


@pytest.fixture(scope="function")
# def device


def CaseDataPath(dscan_client):
    json_dir = dscan_client.caseName.split("::")[0]
    json_file = dscan_client.caseName.split("::")[1] + ".json"
    # 设置用例数据的json文件路径
    casepath = os.path.join(dscan_client.prj_dir, "mockdata", json_dir, json_file)
    return casepath


if __name__ == "__main__":
    start_sdk()