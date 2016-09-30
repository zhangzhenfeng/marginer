#!/usr/bin/env python2 
# coding:utf-8
import os
import ConfigParser
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

def get_config(file="setting.cfg",keys=[]):
    file = os.getcwdu() + os.sep + file
    # 获取配置文件内的配置信息
    if not os.path.isfile(file):
        print("配置文件[%s]不存在" % file)
    config=ConfigParser.ConfigParser()
    config_dic = {}
    with open(file,"rb") as cfgfile:
        config.readfp(cfgfile)
        for key in keys:
            config_dic[key] = config.get("info",key)
        cfgfile.close()    
    return config_dic

def set_config(file="setting.cfg",values={}):
    file = os.getcwdu() + os.sep + file
    #print values
    # 获取配置文件内的配置信息
    if not os.path.isfile(file):
        print("配置文件[%s]不存在" % file)

    cf = ConfigParser.RawConfigParser()
    cf.read(file)
    for k,v in values.items():
        cf.set("info", k, v)
    cf.write(open(file, 'w'))
    return True