import serial
from flask import Flask, request, jsonify

# Initialisation de l'API Flask
app = Flask(__name__)

# Configuration UART
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
MAX_PASS_LENGTH = 16

def U(mdp: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.3) as ser:
            # Envoyer le mot de passe testé
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

def L(level: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.3) as ser:
            # Envoyer le level
            ser.write(b'L ' + level.encode() + b'\n')
            response = ser.readlines()
            for i in response:
                print(i.decode())
            if 'Not a valid level' in response[1].decode():
                return False
            return True
    except serial.SerialException as e:
        print(f"Erreur UART: {e}")
        return False

# Route API pour changer de level
@app.route('/level', methods=['POST'])
def api_level():
    data = request.get_json()
    level: str = data.get('level', '0')
    if not data or 'level' not in data or not level.isdigit():
        return jsonify({
            'status': 'error',
            'message': 'Level requis dans le corps de la requête'
        })
    
    result = L(data.get('level'))

    return jsonify({
        'status': 'success',
        'result': result
    })

# Route API pour vérifier le mot de passe
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
    
    result = U(candidate)
    
    return jsonify({
        'status': 'success',
        'result': result
    })

if __name__ == '__main__':
    print("Lancement de l'API...")
    app.run(host='0.0.0.0', port=5000)