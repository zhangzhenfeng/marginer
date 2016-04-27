#!/usr/bin/env python2 
# coding:utf-8
import os
def get_setting_config(file):
    config_file = os.getcwdu() + os.sep + file
    # 获取配置文件内的配置信息
    config = ""
    if os.path.isfile(config_file):
        config = open(config_file).readlines()
    else:
        print("配置文件[%s]不存在" % config_file)
    # 存放配置信息的字典
    config_dic = {}
    for cfg in config:
        key,value = cfg.split(":")
        config_dic[key.replace("\n","")] = value.replace("\n","")
    return config_dic