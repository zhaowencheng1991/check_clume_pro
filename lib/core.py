#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng
# desc    :check_flume
import json
from tool import *
from ThreadPool import *

allert_users = 'wencheng'
cmd_get_ip = '''/sbin/ifconfig |sed 's/addr://g' |awk -F " " '{if($1=="inet") print $2}' | head -1'''
ip = ex_cmd(cmd_get_ip)[0]
position_dir = '/data0/flume/positionFile/'
model_list = ['sima_mrt','clickmap','clickstream']

def check_pro(ps_cmd):
    ex_result = ex_cmd(ps_cmd)
    status = ex_result[2]
    return status

def get_last_file(model):
    position_file = position_dir + model + '_position.json'
    with open(position_file,'r') as f:
        data = json.load(f,encoding='utf-8')
        return [data[-1]["inode"],data[5]["pos"],data[5]["file"]]  #{u'inode': 922009, u'pos': 55574166, u'file': u'/data0/logs/clickstream/staytime.20171221160000'}

def check_size(model):
    size_ngixn_cmd = "du -sb " + get_last_file(model)[2] + "|awk '{print $1}'"
    size_flume_pos,size_nginx_log = int(get_last_file(model)[1]),int(ex_cmd(size_ngixn_cmd)[0])
    if  size_flume_pos and size_nginx_log:
        diff_num = size_nginx_log - size_flume_pos
        get_flag = "YES"
    else:
        get_flag = "NO"
        diff_num = 1000000
    return {"size_nginx_log": size_nginx_log, "size_flume_pos": size_flume_pos, "diff_num": diff_num, "get_flag": get_flag}

def diff_model_allert(model,p):
    for i in range(3):
        size_list = check_size(model)
        if size_list["get_flag"] == "NO":
            print model,"未获取到对比数据,将会重试2次,间隔20秒"
            time.sleep(20)
            continue

    print model + ": size_flume_pos :", size_list["size_flume_pos"], "  size_nginx_log:", size_list["size_nginx_log"], "diff_num:",size_list["diff_num"]

    p.add_thread()
def main(ps_cmd,):
    status = check_pro(ps_cmd)
    print status
    if status != 0:
        allert_mail('SUDA前端服务器:'+ip+'flume进程不存在 请检查',allert_users)
        print "flume err"
        exit(127)
    else:
        pool =  ThreadPool(3)
        for i in model_list:
            t = pool.get_thread()
            obj = t(target=diff_model_allert, args=(i, pool))
            obj.start()

main("ps aux | grep flume|grep -v grep")








