import os
import re

PATH_SOURCE = './images'
PATH_TARGET = './images/converted'


def doConvert(origin, target):
    CMD_CONVERT = f'convert {origin} \( -clone 0 -blur 0x100 -resize 1920x1080\! \) \( -clone 0 -resize 1920x1080 \) -delete 0 -gravity center -compose over -composite {target}'
    os.system(CMD_CONVERT)

file_list = os.listdir(PATH_SOURCE)

if not os.path.exists(PATH_TARGET):
    os.mkdir(PATH_TARGET)

for filename in file_list:

    target_name = filename.replace('.', '-converted.')
    target_name = f'{PATH_TARGET}/{target_name}'

    #target_name = re.sub('(S+)\.(S+)$', r'\1-converted.\2', filename)

    if os.path.exists(target_name):
        print(f'{filename} is already converted.')
    else:
        filename = f'{PATH_SOURCE}/{filename}'
        print(f"{filename} -> {target_name}")
        doConvert(filename, target_name)