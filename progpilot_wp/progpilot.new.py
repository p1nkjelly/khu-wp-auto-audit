#!/usr/bin/env python3
import os
import subprocess
import json
import time
import sys
from config import *

update1 = int(sys.argv[1])
update2 = int(sys.argv[2])
active1 = int(sys.argv[3])
active2 = int(sys.argv[4])
download1 = int(sys.argv[5])
download2 = int(sys.argv[6])

if len(sys.argv) != 7:
    print("Insufficient arguments")
    sys.exit()

cnt = 1
outputdir_path = os.path.join(save_path + '/', time.strftime('%Y%m%d_%H_%M_%S', time.localtime(time.time())))
os.mkdir(outputdir_path)    

with open(outputdir_path+'/filter.txt', 'w') as f:
    f.write(str(update1) + ' ' + str(update2) + ' ' + str(active1) + ' ' + str(active2) + ' ' + str(download1) + ' ' + str(download2))

for item in os.listdir(plugin_path):

    full_path = os.path.join(plugin_path, item)

    with open(full_path+'/info.json', 'r') as f:
        info = json.load(f)
    
    if update1 != 0 or update2 != 0:
        year = int(info['last_updated'].split('-')[0])
        if not((2023-update1) <= year <= (2023-update2)):
            break
    
    if active1 != 0 or active2 != 0:
        if not(active1 <= info.active_installs <= active2):
            break
    
    if download1 != 0 or download2 != 0:
        if not(download1 <= info.downloaded <= download2):
            break

    with open(analysis_file, "w") as f:
       f.write(code.format(sanitizer_path, full_path))
    
    output_json = []

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        output_json = json.loads(output)
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8')
        print(f"Error occurred: {output}")
    
    if len(output_json) > 0:    
        output_path = os.path.join(outputdir_path, f"{str(cnt).rjust(6, '0')}_{os.path.basename(full_path)}") + ".json"
        with open(output_path, "w") as f:
            f.write(output)
        cnt += 1
