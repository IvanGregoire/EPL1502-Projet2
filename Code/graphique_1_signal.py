import numpy as np
import matplotlib.pyplot as plt

# Chemin vers le fichier de données
file_location = r"C:\Users\igrgr\Documents\EPL1502-Projet2\Code\graphiques_systeme\POST_CONCOURS\partie 2\test1\filtre1\filtre1_1.csv"  # Remplacez par le chemin correct si nécessaire

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

plt.xlabel("Temps [s]")
plt.ylabel("Tension [V]")
plt.title("Décharge du condensateur")
plt.grid(True)
plt.legend()
plt.xlim(0, 300)  # Ajustez les limites selon vos besoins
plt.ylim(-0.8, 10)  # Ajustez les limites selon vos besoins
plt.xlim(time.min(), time.max())
plt.show()