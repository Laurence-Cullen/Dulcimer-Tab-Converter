import requests

function_url = 'https://us-central1-dulcimer-tab.cloudfunctions.net/guitar_to_dulcimer_tab'

with open('tab.txt') as tab:
    guitar_tab_string = tab.read()

r = requests.post(function_url,  json={"tab": guitar_tab_string})

print(r.text)
