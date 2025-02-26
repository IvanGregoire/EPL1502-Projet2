import numpy as np
import matplotlib.pyplot as plt

# Chemin vers le fichier de données
file_location = r"données\prise_en_main.csv"  # Remplacez par le chemin correct si nécessaire

# Fonction pour convertir les virgules en points
def convert_to_float(value):
    return float(value.replace(',', '.'))

# Chargement des données à partir du fichier avec conversion des virgules en points
data = np.genfromtxt(
    file_location,
    delimiter=";",
    skip_header=3,
    converters={0: convert_to_float, 1: convert_to_float}
)

# Sélection de la plage de données à tracer
time = data[0:5000, 0]  # Ajustez les indices selon vos besoins
signal1 = data[0:5000, 1]  # Ajustez les indices selon vos besoins

# Tracé du signal
plt.plot(time, signal1, label="V1", color="b")
plt.xlabel("Temps [us]")
plt.ylabel("Tension [V]")
plt.title("Signal Mesuré")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
plt.xlim(-25, 25)  # Ajustez les limites selon vos besoins
plt.ylim(-0.5, 0.8)  # Ajustez les limites selon vos besoins
plt.show()
