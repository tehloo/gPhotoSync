#!/bin/bash

echo
echo "Starting GPhotoSync...."
date
echo

cd /home/jckim/works/1226_gPhotos
. .venv/bin/activate

python3 gphotoSync.py
python3 imageConverter.py
