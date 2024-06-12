import os
plugins = os.listdir('plugins')

for plugin in plugins:
    print('==================================================================')
    for (path, dir, files) in os.walk('plugins/'+plugin):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.php':
                print(path, filename)
