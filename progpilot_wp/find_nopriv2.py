import os
import json
import re


result = []

if __name__ == '__main__':
    with open('./nopriv.json', 'r') as f:
        plugins = json.load(f)

    for plugin in plugins:
        full_path = os.path.join('./plugins', plugin)

        print(plugin)

        flag = False
        functions = []

        for (path, dir, files) in os.walk(full_path):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if ext == ".php":
                    file_path = os.path.join(path, filename)

                    with open(file_path, errors="surrogateescape") as temp:
                        lines = temp.readlines()
                        for line in lines:
                            if "ajax_nopriv" in line:
                                matches = re.findall(r'"([^"]*)"|\'([^\']*)\'', line)
                                match_strings = [match[0] if match[0] else match[1] for match in matches]
                                if len(match_strings) == 2:
                                    functions.append(match_strings[1])


        if functions:
            flag = True
            for (path, dir, files) in os.walk(full_path):
                for filename in files:
                    ext = os.path.splitext(filename)[-1]
                    if ext == ".php":
                        file_path = os.path.join(path, filename)

                        with open(file_path, errors="surrogateescape") as temp:
                            lines = temp.readlines()
                            for func in functions:
                                func_start = False
                                cnt = 0
                                for line in lines:
                                    if func_start:
                                        if "wp_verify_nonce" in line:
                                            flag = False
                                        if "check_ajax_referer" in line:
                                            flag = False
                                        cnt += 1
                                    else:
                                        if "function " + func in line:
                                            func_start = True
                                    if cnt >= 30:
                                        break
        if flag:
            result.append(plugin)


with open("nopriv2.json", "w") as json_file:
    json.dump(result, json_file)
