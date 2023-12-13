import numpy as np
import matplotlib.pyplot as plt

# Création d'un signal temporel
t = np.linspace(0, 1, 1000, endpoint=False)
x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.randn(1000)  # Signal sinusoïdal avec bruit

# Calcul de la DSP
frequencies, Pxx = plt.psd(x, NFFT=1024, Fs=1000)

# Affichage du résultat
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Densité Spectrale de Puissance (dB/Hz)')
plt.show()