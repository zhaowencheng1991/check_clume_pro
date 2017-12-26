#!/bin/bash

python=`which python`

#echo $file_path
if [ $0 != start.sh ];then
    file_path=`echo $0 |awk -F 'start.sh' '{print $1}'`
else
    file_path=$0
fi
python $file_path/../lib/core.py