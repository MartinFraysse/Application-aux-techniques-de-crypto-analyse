import serial
import time
from flask import Flask, request, jsonify

# Initialisation de l'API Flask
app = Flask(__name__)

MAX_PASS_LENGTH = 16

MDP = open('etape4/mdp.txt').write()


def check_password(candidate):
    pass

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
    result = check_password(candidate)
    
    return jsonify({
        'status': 'success',
        'result': result
    })

if __name__ == '__main__':
    print("Lancement de l'API de vérification...")
    app.run(host='0.0.0.0', port=5000, debug=True)