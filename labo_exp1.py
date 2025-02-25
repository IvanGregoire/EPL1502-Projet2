import numpy as np
import matplotlib.pyplot as plt

# Chemin vers le fichier de données
file_location = "1.2_48.csv"  # Remplacez par le chemin correct si nécessaire

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
plt.plot(time, signal1, label="V1", color="b")
plt.xlabel("Temps [us]")
plt.ylabel("Tension [V]")
plt.title("Signal Mesuré")
plt.plot(time, signal2, label="V2", color="r")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)
plt.xlim(-250, 250)  # Ajustez les limites selon vos besoins
plt.ylim(0, 5)  # Ajustez les limites selon vos besoins
plt.xlim(time.min(), time.max())
plt.show()


#Attention, interpréter les résultats !!!