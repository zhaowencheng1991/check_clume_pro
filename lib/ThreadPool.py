#!/usr/bin/python
# coding: utf-8
# author  :zhaowencheng

import Queue
import threading
import time

class ThreadPool:
    def __init__(self,maxsize=3):
        '''
        构造方法 创建一个队列并且将执行类放到队列中
        :param maxsize:队列最大长度默认=5
        '''
        self.maxsize = maxsize
        self._q = Queue.Queue(maxsize)

        for i in range(maxsize):
            self._q.put(threading.Thread)

    def get_thread(self):
        return self._q.get()

    def add_thread(self):
        self._q.put(threading.Thread)

#pool = ThreadPool(8)

#def worker(num,p):
#    print num
#    time.sleep(1)
#    p.add_thread()
#
#def start():
#    cmd_list = []
#    for i in range(1,101):
#        cmd_list.append(i)
#    for i in cmd_list:
#        t=pool.get_thread()
#        obj = t(target=worker,args=(i,pool))
#        obj.start()

#start()
















