import numpy as np
import matplotlib.pyplot as plt

R = 0.05 #Rayon de la bobine
I = 0.500 #Courant Max
N = 176 #Nombre de spires dans notre bobine
B = 1.2 #Champ magnétique de notre aimant

def force(x):
    expr = 1 - ((x - R) / R) ** 2
    return np.where(expr >= 0, 2 * B * N * I * R * np.sqrt(expr), 0) #Si la force est négative (pour qu'on ait un graphe)

x_values = np.linspace(-0.5, 1, 1000)

y_values = force(x_values)

max_x = R
max_force = force(max_x)

plt.plot(x_values, y_values, label="Force F(x)", color='blue')
plt.scatter(max_x, max_force, color='red', zorder=5, label=f'Maximum à x = {max_x}')
plt.title("Graphe de la force en fonction de x")
plt.xlabel("x")
plt.ylabel("Force F(x)")
plt.grid(True)
plt.legend()
plt.show()