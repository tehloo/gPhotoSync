#!/bin/bash

echo
echo "Starting GPhotoSync...."
date
echo

. .venv/bin/activate

python3 gphotoSync.py
python3 imageConverter.py
