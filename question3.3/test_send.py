import serial

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200


def test(mdp: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            # Envoyer le mot de passe candidat
            ser.write(mdp.encode() + b'\n')
            # Attendre la réponse (suppose que la cible renvoie '1' pour vrai, '0' pour faux)
            response = ser.readline().decode().strip()
            print(response)
            return response
    except serial.SerialException as e:
        print(f"Erreur UART: {e}")
        return False
    

test('test')