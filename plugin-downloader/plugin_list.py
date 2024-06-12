import requests
import json


plugins = []

for i in range(1, 221):
    url = "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[page]={0}&request[per_page]=250".format(i)
    response = requests.get(url).json()
    for plugin in response['plugins']:
        plugins.append({'name':plugin['name'], 'last_updated':plugin['last_updated'], 'added':plugin['added'], 'active_installs':plugin['active_installs'], 'downloaded':plugin['downloaded'], 'download_link':plugin['download_link'], 'slug':plugin['slug']})
    print(plugins)
    print(len(plugins))

with open("wordpress_plugins.json", "w") as json_file:
    json.dump(plugins, json_file)
