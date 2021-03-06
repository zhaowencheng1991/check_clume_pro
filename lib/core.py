#!/usr/bin/python
# -*- coding: utf-8 -*-
# author  :zhaowencheng
# desc    :check_flume
import json
from tool import *
from ThreadPool import *
from conf import conf



reload(sys)
sys.setdefaultencoding('utf8')

allert_num = conf.allert_num
allert_num_display = allert_num / 1000000
#print allert_num_display
allert_users = conf.allert_users
cmd_get_ip = '''/sbin/ifconfig |sed 's/addr://g' |awk -F " " '{if($1=="inet") print $2}' | head -1'''
ip = ex_cmd(cmd_get_ip)[0]
position_dir = conf.position_dir
model_list = conf.model_list


err_mess_list = []
read_err_model_list = []
def check_pro(ps_cmd):
    ex_result = ex_cmd(ps_cmd)
    status = ex_result[2]
    return status

def get_last_file(model):
    position_file = position_dir + model + '_position.json'
    with open(position_file,'r') as f:
        data = json.load(f,encoding='utf-8')
        return [data[-1]["inode"],data[-1]["pos"],data[-1]["file"]]  #{u'inode': 922009, u'pos': 55574166, u'file': u'/data0/logs/clickstream/staytime.20171221160000'}

def check_size(model):
    size_ngixn_cmd = "du -sb " + get_last_file(model)[2] + "|awk '{print $1}'"
    size_flume_pos,size_nginx_log = int(get_last_file(model)[1]),int(ex_cmd(size_ngixn_cmd)[0])
    if  size_flume_pos and size_nginx_log:
        diff_num = size_nginx_log - size_flume_pos
        get_flag = "YES"
    else:
        get_flag = "NO"
        diff_num = 1000000
    return {"size_nginx_log": size_nginx_log, "size_flume_pos": size_flume_pos, "diff_num": diff_num, "get_flag": get_flag,"last_file":get_last_file(model)[2]}

def diff_model_allert(model):
    for i in range(3):
        size_list = check_size(model)
        if size_list["get_flag"] == "NO":
            printLog('''model,"未获取到对比数据,将会重试2次,间隔20秒"''',3)
            time.sleep(20)
            continue

    #print model + ": size_flume_pos :", size_list["size_flume_pos"], "  size_nginx_log:", size_list["size_nginx_log"], "diff_num:",size_list["diff_num"]
    if size_list["diff_num"] >= allert_num:
        err_mess = "%s 同步延迟超过%sB延迟大小(日志实际大小-flume读取大小)为:%sB延迟读取文件: %s"  % (model,allert_num,size_list["diff_num"],size_list["last_file"])
        printLog(err_mess,3)
        global read_err_model_list
        read_err_model_list.append({model:size_list["diff_num"]})
        global err_mess_list
        err_mess_list.append(err_mess)
    #print err_message_list,read_err_model_list
    return [read_err_model_list,err_mess_list]

def main(ps_cmd,):
    status = check_pro(ps_cmd)
    if status != 0:
        allert_mail('SUDA前端服务器:'+ip+'flume进程不存在 请检查',allert_users)
        printLog('flume进程不存在.')

        exit(127)
    else:
        for i in model_list:
            result = diff_model_allert(i)
        if result[0]:
            mess = '''suda 前 端 服 务 器 : %s, flume 数 据 读 取 有 延 迟 已 经 超 过 预 设 阀 值: %sB,模块:延迟值 分别为:%s,
                    参考文档:http://wiki.pso.sina.com.cn/pages/viewpage.action?pageId=8323362''' %(ip,allert_num,str(result[0]))

            allert_mail(mess,allert_users)

main("ps aux | grep flume-release|grep -v grep")







