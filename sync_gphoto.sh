#!/bin/bash

cd /home/jckim/works/1226_gPhotos
. .venv/bin/activate

echo "Log starts " >> sync.log
date >> sync.log

nohup python3 -u gphotoSync.py >> sync.log 2>&1
nohup python3 -u imageConverter.py >> sync.log 2>&1