#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng
# desc    :distcp

import subprocess

def ex_cmd(cmd):
    '''
    执行命令并返回结果列表
    :param cmd:所要执行的命令
    :return:结果列表
    '''
    run_cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = run_cmd.stdout.read()
    err = run_cmd.stderr.read()
    wait = int(run_cmd.wait())                  #退出状态码
    result_list = [res,err,wait,]
    return  result_list


def allert_mail(message,allert_users,):
    message = str(message)
    level = 'waring'
    service = '监控系统'
    subject = 'suda平台flume异常'
    mail='http://monitor.pso.sina.com.cn/monitor/index.php/interface/sendMail'
    receiver = allert_users
    curl_cmd = ("curl -d receivers=%s -d service=%s -d level=%s -d subject=%s -d content='%s', %s") % (receiver,service,level,subject,message,mail)
    ex_cmd(curl_cmd)





