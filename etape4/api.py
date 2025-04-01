import serial
import random
from flask import Flask, request, jsonify

# Initialisation de l'API Flask
app = Flask(__name__)

# Configuration UART (à adapter selon votre matériel)
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
MAX_PASS_LENGTH = 16

def U1(mdp: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            # Envoyer le mot de passe candidat
            ser.write(b'U ' + mdp.encode() + b'\n')
            response = ser.readlines()
            for i in response:
                print(i.decode())
            if "[-]   Sorry, try again" in response[2].decode():
                return {"Valid": False, "time": response[1].decode()[25:-2]}
            else:
                return {"Valid": True, "time": response[1].decode()[25:-2]}
    except serial.SerialException as e:
        print(f"Erreur UART: {e}")
        return False

# Route API pour vérifier un mot de passe
@app.route('/check', methods=['POST'])
def api_check_password():
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Mot de passe requis dans le corps de la requête'
        })
    
    candidate = data['password']
    if len(candidate) > MAX_PASS_LENGTH:
        return jsonify({
            'status': 'error',
            'message': f'Le mot de passe ne doit pas dépasser {MAX_PASS_LENGTH} caractères'
        })
        
    
    # Vérification avec temporisation côté cible
    result = U1(candidate)
    
    return jsonify({
        'status': 'success',
        'result': result
    })


MDP = open('etape4/mdp.txt','r').read()

def test_password(mp):
    temps = 0
    tmp_mdp = MDP
    tmp_mp = mp
    if len(mp) > len(MDP):
        tmp_mdp = MDP + ('*' * (len(mp) - len(MDP)))
        tmp_mp = mp
    elif len(mp) < len(MDP):
        tmp_mp = mp + ('*' * (len(MDP) - len(mp)))
        tmp_mdp = MDP
    for i, j in zip(tmp_mp, tmp_mdp):
        temps += random.randint(40, 60)
        if i != j:
            return {"Valid": False, "time": temps}
    return {"Valid": True, "time": temps}

# Route API pour vérifier un mot de passe
@app.route('/test', methods=['POST'])
def api_test_password():
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Mot de passe requis dans le corps de la requête'
        })
    
    candidate = data['password']
    if len(candidate) > MAX_PASS_LENGTH:
        return jsonify({
            'status': 'error',
            'message': f'Le mot de passe ne doit pas dépasser {MAX_PASS_LENGTH} caractères'
        })
    
    # Vérification avec temporisation côté cible
    result = test_password(candidate)
    
    return jsonify({
        'status': 'success',
        'result': result
    })




if __name__ == '__main__':
    print("Lancement de l'API de vérification...")
    app.run(host='0.0.0.0', port=5000, debug=True)