import serial

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200


def test(mdp: str):
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            # Envoyer le mot de passe candidat
            ser.write(b'U ' + mdp.encode() + b'\n')
            response = ser.readlines()
            if "[-]   Sorry, try again" in response[2].decode():
                return {"Valid": False, "time": response[1].decode()[25:-2]}
            else:
                return {"Valid": True, "time": response[1].decode()[25:-2]}
    except serial.SerialException as e:
        print(f"Erreur UART: {e}")
        return False
    

print(test(input('U ')))