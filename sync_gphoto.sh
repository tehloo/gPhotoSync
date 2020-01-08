#!/bin/bash

echo
echo "Starting GPhotoSync...."
date
echo

cd /home/jckim/Projects/gPhotos
. .venv/bin/activate

python3 gphotoSync.py
python3 imageConverter.py
