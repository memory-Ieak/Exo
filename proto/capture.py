import serial
import struct
import json
import sys

filename = "data"
datafolder = "human"

if len(sys.argv) > 1:
    filename = sys.argv[1]

if len(sys.argv) > 2:
    datafolder = sys.argv[2]

def sauvegarder_en_json(nom_fichier, liste):
    with open(nom_fichier, 'w+') as fichier:
        json.dump(liste, fichier)

# Définir le format de la structure
struct_format = '=fff'  # Trois flottants non alignés

# Configuration du port série
port = "/dev/ttyACM0"  # Assurez-vous de spécifier le bon port
baudrate = 115200

ser = serial.Serial(port, baudrate, timeout=1)

data_x = []

try:
    i = 0
    while True:


        # Lecture de données depuis le port série
        line = ser.readline().strip()  # Lire la ligne et supprimer les caractères de fin de ligne
        if len(line) != 12:
            print("UART error")
            continue

        data = struct.unpack(struct_format, line)

        # Ajouter les données aux listes
        data_x.append(data[0])

        if (len(data_x) > 2680):
            sauvegarder_en_json(f"../data/{datafolder}/" + filename + str(i) + ".json", data_x)
            i += 1
            data_x.clear()

except KeyboardInterrupt:
    pass
    
