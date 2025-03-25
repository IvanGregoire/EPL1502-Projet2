import numpy as np
import matplotlib.pyplot as plt
import glob
from scipy.signal import butter, filtfilt

# 📂 Dossier contenant les fichiers CSV
folder_path = r"donnees\*.csv"

# 🔧 Fonction de conversion des virgules en points
def convert_to_float(value):
    return float(value.replace(',', '.'))

# 🔧 Fonction de filtrage passe-bas (Butterworth)
def lowpass_filter(data, cutoff=50, fs=1000, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# 🔧 Moyenne glissante pour lisser les données
def moving_average(data, window_size=10):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# 📂 Récupération des fichiers CSV
files = glob.glob(folder_path)

plt.figure(figsize=(10, 6))

signal2_plotted = False  # Pour tracer signal2 une seule fois

for file_location in files:
    # 📌 Chargement des données CSV
    data = np.genfromtxt(
        file_location,
        delimiter=";",
        skip_header=3,
        converters={0: convert_to_float, 1: convert_to_float, 2: convert_to_float}
    )

    # 📌 Sélection des données
    time = data[:, 0]
    signal1 = data[:, 1]
    signal2 = data[:, 2]

    # 🛠 Application du filtre passe-bas
    filtered_signal1 = lowpass_filter(signal1, cutoff=50, fs=1000, order=3)
    filtered_signal2 = lowpass_filter(signal2, cutoff=50, fs=1000, order=3)

    # 🛠 Lissage avec une moyenne glissante
    smooth_signal1 = moving_average(filtered_signal1, window_size=10)
    smooth_signal2 = moving_average(filtered_signal2, window_size=10)

    # Ajustement du temps (car les données lissées sont plus courtes)
    smooth_time = time[:len(smooth_signal1)]

    # 🎨 Tracé des signaux lissés
    plt.plot(smooth_time, smooth_signal1, label=f"V1 Lissé - {file_location}", linestyle="--")

    if not signal2_plotted:
        plt.plot(smooth_time, smooth_signal2, label="V2 Lissé (référence)", color="r")
        signal2_plotted = True

# 📊 Configuration du graphique
plt.xlabel("Temps [u]")
plt.xlim(0,1)
plt.ylim(0,10)
plt.ylabel("Tension [V]")
plt.title("Signaux Mesurés (Filtrés et Lissés)")
plt.legend()
plt.grid()
plt.show()
