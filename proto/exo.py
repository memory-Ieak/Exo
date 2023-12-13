import serial
import struct
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Définir le format de la structure
struct_format = '=fff'  # Trois flottants non alignés

# Configuration du port série
port = "/dev/ttyACM0"  # Assurez-vous de spécifier le bon port
baudrate = 115200

# Ouvrir le port série
ser = serial.Serial(port, baudrate, timeout=1)

# Initialiser les listes pour stocker les données
data_x = []
data_y = []
data_z = []

min_bound = 0.8
max_bound = 1.2

# Initialiser la figure avec trois sous-plots (signal temporel, FFT, spectre de fréquence)
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Initialiser les lignes des courbes pour le signal temporel
line_x, = ax1.plot([], [], label='accX')
line_min, = ax1.plot([], [], label='min', color='red')
line_max, = ax1.plot([], [], label='max', color='red')

# Initialiser les lignes des courbes pour la FFT
line_fft_x, = ax2.plot([], [], label='FFT accX')

# Spectre de fréquence
sampling_interval = 0.4
fs = 1 / sampling_interval

freq_spec, = ax3.plot([], [], label='spectre de fréquence accX')

# Fonction d'animation
def update(frame):
    # Lecture de données depuis le port série
    line = ser.readline().strip()  # Lire la ligne et supprimer les caractères de fin de ligne
    if len(line) != 12:
        print("Données incorrectes:", line)
        return

    data = struct.unpack(struct_format, line)

    print(data)

    # Ajouter les données aux listes
    data_x.append(data[0])

    if len(data_x) > 50:
        data_x.pop(0)

    # Temporal signal
    line_x.set_data(range(len(data_x)), data_x)
    line_min.set_data(range(len(data_x)), min_bound)
    line_max.set_data(range(len(data_x)), max_bound)
    ax1.relim()
    ax1.autoscale_view()

    # FFT
    if data[0] > max_bound or data[0] < min_bound:
        fft_x = np.fft.fft(data_x)
        line_fft_x.set_data(range(len(fft_x)), np.abs(fft_x))

        # Mettre à jour les barres pour le spectre de fréquence
        fft_freqs = np.fft.fftfreq(fft_x.size, sampling_interval)  # Utiliser l'intervalle d'échantillonnage
        idx = np.argsort(fft_freqs)
        freq_spec.set_data(fft_freqs[idx][fft_x.size//2:], np.abs(fft_x)[idx][fft_x.size//2:])

    ax2.relim()
    ax2.autoscale_view()

    ax3.relim()
    ax3.autoscale_view()

    # Ajouter des légendes
    ax1.legend()
    ax2.legend()
    ax3.legend()

# Créer l'animation
ani = FuncAnimation(fig, update, blit=False)

# Afficher le graphique en continu
plt.show()

# Fermer le port série à la fin
ser.close()