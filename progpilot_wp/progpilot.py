#!/usr/bin/env python3
import os
import subprocess
import json
from config import *

def main():
    cnt = 1
    for item in os.listdir(plugin_path):
        full_path = os.path.join(plugin_path, item)

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
            output_path = os.path.join(save_path, f"{str(cnt).rjust(6, '0')}_{os.path.basename(full_path)}") + ".json"
            with open(output_path, "w") as f:
                f.write(output)

            cnt += 1

if __name__ == "__main__":
    main()
