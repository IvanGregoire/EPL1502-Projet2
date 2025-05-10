import numpy as np
import matplotlib.pyplot as plt

# Chemin vers le fichier de données
file_location = r"S8.csv"  # Remplacez par le chemin correct si nécessaire

# Fonction pour convertir les virgules en points
def convert_to_float(value):
    return float(value.replace(',', '.'))

# Chargement des données à partir du fichier avec conversion des virgules en points
data = np.genfromtxt(
    file_location,
    delimiter=";",
    skip_header=3,
    converters={0: convert_to_float, 1: convert_to_float, 2: convert_to_float}
)


# Sélection de la plage de données à tracer
time = data[0:3059, 0]  # Ajustez les indices selon vos besoins
signal1 = data[0:3059, 1]  # Ajustez les indices selon vos besoins
signal2 = data[0:3059, 2]
# Tracé du signal
plt.plot(time, signal1, label="Signal amplifié", color="b")
plt.xlabel("Temps [ms]")
plt.ylabel("Tension [mV]")
plt.title("Signal Mesuré")
plt.plot(time, signal2, label="Signal détecté", color="r")
plt.legend()
plt.xlim(-1, -.9102251)  # Ajustez les limites selon vos besoins
plt.show()
#Attention, interpréter les résultats !!!