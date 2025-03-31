import requests



url = "http://127.0.0.1:5000/check"

json = {
    "password": 'aest'
}


res = requests.post(url=url, json=json, verify=False)

if res.status_code == 200:
    print(res.json())
else:
    print(res.text)