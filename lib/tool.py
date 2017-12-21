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
    wait = int(run_cmd.wait())
    result_list = [res,err,wait,]
    return  result_list



result= ex_cmd("uname ")
print result
