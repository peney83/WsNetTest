#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : '2020/1/10 10:29'
# @Author  : ZhangXianghui
# @File    : sdk_t.py
# @Software: PyCharm

import os


if __name__ == "__main__":
    import subprocess
    import logging
    cur_path = os.path.dirname(__file__)
    sdk_path = os.path.join(cur_path, "../sdk/dist")
    sdk_exe = os.path.join(sdk_path, "footer-ali.exe")
    sdk_exe = os.path.abspath(sdk_exe)

    cmd = sdk_exe + " run --config " + os.path.join(os.path.dirname(sdk_exe), ".server.json")
    # cmd = "ping 127.0.0.1 -t "
    print(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # p = subprocess.Popen(["ping", "127.0.0.1", "-t"], stdin=subprocess.PIPE,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for line in iter(p.stdout.readline, ""):
        print(line)
        if "starting socket server" in str(line):
            print("====start")
            break
    # p.terminate()
    # p.kill()
    # os.killpg()
    # os.killpg(os.getpgid(p.pid), 9)
    os.system("taskkill /f /im footer-ali.exe")
    print("end")

    # for info in p.communicate():
    #     print(info)
    #     logging.info(info)
    #     if "starting socket server" in info:
    #         break



    # p.communicate()
    # output = p.stdout.read()
    # print(output)

