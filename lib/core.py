#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng
# desc    :check_flume
import os
import time
import json
from tool import *

cmd_get_ip = '''/sbin/ifconfig |sed 's/addr://g' |awk -F " " '{if($1=="inet") print $2}' | head -1'''
ip = ex_cmd(cmd_get_ip)[0]
position_dir = '/data0/flume/positionFile/'

def check_pro(ps_cmd):
    ex_result = ex_cmd(ps_cmd)
    status = ex_result[2]
    if status != 0:
        allert_mail('SUDA前端服务器:'+ip+'flume进程不存在 请检查')
    else:
        pass

def diff_file(model):
    position_file = position_dir + model + '_position.json'
    with open(position_file,'r') as f:
        data = json.load(f,encoding='utf-8')
        print data[5]["file"]    #{u'inode': 922009, u'pos': 55574166, u'file': u'/data0/logs/clickstream/staytime.20171221160000'}


diff_file('staytime')


