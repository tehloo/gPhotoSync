import os
import re

PATH_SOURCE = '/home/jckim/Pictures/jay'
PATH_TARGET = '/home/jckim/Pictures/wallpapers'

TARGET_RESOLUTION = '1920x1080'


def doConvert(origin, target):
    CMD_CONVERT = f'convert {origin} \( -clone 0 -blur 0x100 -resize {TARGET_RESOLUTION}\! \) \( -clone 0 -resize {TARGET_RESOLUTION} \) -delete 0 -gravity center -compose over -composite {target}'
    os.system(CMD_CONVERT)
    return



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