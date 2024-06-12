#!/usr/bin/env python3
import os
import subprocess
import json
import shutil
from config import *

def main():
    with open('./nopriv.json', 'r') as f:
        plugins = json.load(f)

    for item in os.listdir(plugin_path):
        full_path = os.path.join(plugin_path, item)

        if item in plugins:
            dest_path = os.path.join('./fplugins', item)
            shutil.copytree(full_path, dest_path)

if __name__ == "__main__":
    main()
