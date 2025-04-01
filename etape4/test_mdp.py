import requests


url = "http://192.168.137.146:5000/level"

json = {
    "level": input('Level - ')
}

res = requests.post(url=url, json=json, verify=False)

if res.status_code == 200:
    print(res.json())
else:
    print(res.text)


url = "http://192.168.137.146:5000/check"

while 1:
    json = {
        "password": input('Password - ')
    }

    res = requests.post(url=url, json=json, verify=False)

    if res.status_code == 200:
        print(res.json())
    else:
        print(res.text)