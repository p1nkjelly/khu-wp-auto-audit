import os
import subprocess
import json
from config import *


result = []


def main():
    for item in os.listdir(plugin_path):
        full_path = os.path.join(plugin_path, item)
       
        flag = False

        for (path, dir, files) in os.walk(full_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == ".php":
                    file_path = os.path.join(path, filename)
                    
                    with open(file_path, errors="surrogateescape") as temp:
                        if "ajax_nopriv" in temp.read():
                            flag = True


        if flag:
          result.append(item)  


main()
with open("nopriv.json", "w") as json_file:
    json.dump(result, json_file)
