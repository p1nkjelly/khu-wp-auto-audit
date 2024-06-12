import requests
import json
import zipfile
import os
import time
import numpy
from multiprocessing import Process, Queue


def download(threadnum, plugins):
    for plugin in plugins:
        cnt = 0
        while True:
            if os.path.exists('./plugins/{0}'.format(plugin['slug'])):
                print('[+] already downloaded, pass! : ' + plugin['slug'])
                break
            try:
                with open('./tmp{0}.zip'.format(threadnum), 'wb') as f:
                    response = requests.get(plugin['download_link'])
                    f.write(response.content)
                with zipfile.ZipFile('./tmp{0}.zip'.format(threadnum), 'r') as zip_file:
                    zip_file.extractall('./plugins')
                    with open('./plugins/{0}/info.json'.format(plugin['slug']), 'w') as json_file:
                        json.dump(plugin, json_file)
                break
            except:
                if cnt < 10:
                    time.sleep(10)
                    cnt += 1
                else:
                    print('[!] download failed! : ' + plugin['slug'])
                    break
            time.sleep(.1)


if __name__ == '__main__':
    with open('./wordpress_plugins.json', 'r') as f:
        plugins = json.load(f)
        print(len(plugins))
    
    threads = []
    chunked_plugins = numpy.array_split(plugins, 18) 
    print(len(chunked_plugins))
    for i in range(0, 18):
        threads.append(Process(target=download, args=(i, chunked_plugins[i])))
    print(threads)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    for i in range(0, 18):
        file_name = './tmp{0}.zip'.format(i)
        if os.path.isfile(file_name):
            os.remove(file_name)
