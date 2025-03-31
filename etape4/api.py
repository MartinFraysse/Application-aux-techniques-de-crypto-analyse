import serial
import time
from flask import Flask, request, jsonify

# Initialisation de l'API Flask
app = Flask(__name__)

# Configuration UART (à adapter selon votre matériel)
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
MAX_PASS_LENGTH = 16

def test(mdp: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            # Envoyer le mot de passe candidat
            ser.write(b'U ' + mdp.encode() + b'\n')
            response = ser.readlines()
            if response[2].decode() == "[-]   Sorry, try again":
                return {"Valid": False, "time": response[1].decode()}
            else:
                return {"Valid": True, "time": response[1].decode()}
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
    result = test(candidate)
    
    return jsonify({
        'status': 'success',
        'result': result
    })

if __name__ == '__main__':
    print("Lancement de l'API de vérification...")
    app.run(host='0.0.0.0', port=5000, debug=True)