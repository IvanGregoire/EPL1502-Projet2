import numpy as np
import matplotlib.pyplot as plt

# Chemin vers le fichier de données
file_location = r"Pico\graphe-2\Détection-Amplifiée\Détection-Amplifiée_22.csv"  # Remplacez par le chemin correct si nécessaire

# Fonction pour convertir les virgules en points
def convert_to_float(value):
    return float(value.replace(',', '.'))

# Chargement des données à partir du fichier avec conversion des virgules en points
data = np.genfromtxt(
    file_location,
    delimiter=";",
    skip_header=2,
    converters={0: convert_to_float, 1: convert_to_float}
)


# Sélection de la plage de données à tracer
time = data[:, 0]  # Ajustez les indices selon vos besoins
signal1 = data[:, 1]  # Ajustez les indices selon vos besoins
# Tracé du signal
plt.plot(time, signal1, label="V1", color="b")

plt.xlabel("Temps [ms]")
plt.ylabel("Tension [V]")
plt.title("Signal Mesuré")
plt.legend()
plt.xlim(0, 300)  # Ajustez les limites selon vos besoins
plt.ylim(-0.8, 5)  # Ajustez les limites selon vos besoins
plt.xlim(time.min(), time.max())
plt.show()