import requests



url = "http://10.0.2.15:5000/check"

json = {
    "password": 'Gaaaa'
}


res = requests.post(url=url, json=json, verify=False)

if res.status_code == 200:
    print(res.json())
else:
    print(res.text)