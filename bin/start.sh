#!/bin/bash

python=`which python`
file_path=`echo $0 |awk -F 'start.sh' '{print $1}'`
echo $file_path
python $file_path/../lib/core.py