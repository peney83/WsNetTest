#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2019/11/7 10:23'
# @Author  : ZhangXianghui
# @File    : util.py
# @Software: PyCharm

import time
import pytest
import allure
import json


@allure.step("等待ali客户端接收到sdk传送的消息，参数轮询间隔{1}s, 超时时间{2}s")
def wait_unitl_aliclient_receive_message(aliscan_client, interval, timeout=15):
    """
    :param aliscan_client:  ali 客户端(模拟前端)
    :param interval:    每次查询的时间间隔，单位:s
    :param timeout:     总timeout时间
    :return:
    """
    ori_timeout = timeout
    while timeout >= 0:
        if aliscan_client.recv_flag:
            break
        time.sleep(interval)
        timeout = timeout - interval
        print("timeout:{}".format(timeout))
    if timeout < 0:
        pytest.fail("ali_client do not receive the  message in {}s".format(ori_timeout))


@allure.step("等待dScan客户端接收到sdk传送的消息，参数轮询间隔{1}s, 超时时间{2}s")
def wait_unitl_dScanclient_receive_message(dscan_client, interval, timeout=15):
    """
    :param dscan_client:  dScan 客户端(模拟设备端)
    :param interval:    每次查询的时间间隔，单位:s
    :param timeout:     总timeout时间
    :return:
    """
    ori_timeout = timeout
    while timeout >= 0:
        if dscan_client.recv_flag:
            break
        time.sleep(interval)
        timeout = timeout - interval
        print("timeout:{}".format(timeout))
    if timeout < 0:
        pytest.fail("dscan_client do not receive the {} message in {}s".format( ori_timeout))


@allure.step("等待客户端{0}接收到sdk传送的{1}消息，参数轮询间隔{2}s, 超时时间{3}s")
def wait_unitl_client_receive_message(client, topic, interval, timeout=15):
    """
    :param client:      客户端(模拟)
    :param topic:       轮询检查的消息类型
    :param interval:    每次查询的时间间隔，单位:s
    :param timeout:     总timeout时间
    :return:
    """
    ori_timeout = timeout
    while timeout >= 0:
        e = [e for e in client.msglist if e["topic"] == topic]
        if e:
            break
        time.sleep(interval)
        timeout = timeout - interval
        print("timeout:{}".format(timeout))
    if timeout < 0:
        pytest.fail("Client do not receive the {} message in {}s".format(topic, ori_timeout))


@allure.step("等待模拟前端{0}接收到sdk传送的设备状态信息equipment/scan/status的消息，其中状态为{1}，参数轮询间隔{2}s, 超时时间{3}s")
def wait_unitl_device_status_to_expect(client, status, interval, timeout=15):
    """
    :param client:      客户端(模拟)
    :param status:       轮询检查设备状态消息的状态
    :param interval:    每次查询的时间间隔，单位:s
    :param timeout:     总timeout时间
    :return:
    """
    is_expect = False
    ori_timeout = timeout
    while timeout >= 0:
        msgs = [e for e in client.msglist if e["topic"] == "equipment/scan/status"]
        for e in msgs:
            if e["data"]["status"] == status:
                is_expect = True

        if is_expect:
            break
        time.sleep(interval)
        timeout = timeout - interval
        # print("timeout:{}".format(timeout))
    if timeout < 0:
        pytest.fail("Client do not receive the status: {} of \"equipment/scan/status\" message in {}s".format(status, ori_timeout))