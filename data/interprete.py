import sys
import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score




filename = "obstacle/data6.json"
filename2 = "normal/data6.json"

label_dict = {
    "human": 0,
    "normal": 1,
    "obstacle": 2
}

if len(sys.argv) > 1:
    filename = sys.argv[1]

def recuperer_de_json(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        donnees = json.load(fichier)
    return donnees

# Charger les données depuis le fichier JSON
data_x = recuperer_de_json(filename)
data_z = recuperer_de_json(filename2)

def histogramme(data_x, label) :
    # Calculer la transformée de Fourier
    fft_x = np.fft.fft(data_x)
    fft_freqs = np.fft.fftfreq(len(fft_x), d=1)  # fréquences associées à la transformée de Fourier

    # Trier les indices pour un tracé correct
    idx = np.argsort(fft_freqs)

    # Sélectionner les fréquences positives seulement
    positive_freqs = fft_freqs[idx][fft_freqs[idx] >= 0]
    positive_fft = np.abs(fft_x)[idx][fft_freqs[idx] >= 0]

    # Discrétiser en 20 plages
    num_bins = 20
    hist, bin_edges = np.histogram(positive_freqs, bins=num_bins, weights=positive_fft)
    hist = np.append(hist, label_dict[label])
    return hist[1:]


    

# Créer un DataFrame avec les noms de colonnes
noms_colonnes = [f'Range{i}' for i in range(1, 20)] + ['Label']
df = pd.DataFrame(columns=noms_colonnes)


folders = ["human", "normal", "obstacle"]
i = 0
for folder in folders:
    directory = os.fsencode(folder)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        data = recuperer_de_json(f'{folder}/{filename}')
        df.loc[i] = histogramme(data, folder)
        i += 1


 
df["Label"] = df["Label"].astype(int)


X = df.drop("Label", axis=1).values
y = df["Label"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



## Entraîner un modèle (exemple avec une forêt aléatoire)
model = RandomForestClassifier()
model.fit(X_train, y_train)





data = histogramme(recuperer_de_json("human/test1.json"), "normal" )[:-1]
num_features = 19  # Replace with the correct number of features
X_new = np.reshape(data, (1, num_features))


print(model.predict(X_new))


