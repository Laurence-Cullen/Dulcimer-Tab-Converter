import requests

function_url = 'https://us-central1-dulcimer-tab.cloudfunctions.net/cors_enabled_function'

with open('tab.txt') as tab:
    guitar_tab_string = tab.read()

r = requests.post(function_url,  json={"tab": guitar_tab_string})

print(r.text)
