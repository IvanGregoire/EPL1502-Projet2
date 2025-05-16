import numpy as np
import matplotlib.pyplot as plt


X = np.array([10, 11, 12, 13, 14, 20]) #Résistances en K ohm
U = np.array([10.228, 9.791, 8.666, 8.228, 7.750, 0]) #Fréquence en Hz

n = 2 #Le degré du polynôme pour la régression (Si on met 5 on aura l'interpolation de Lagrange)
Phi = np.vander(X, N=n+1, increasing=True) 

a = np.linalg.lstsq(Phi, U, rcond=None)[0]

X_plot = np.linspace(min(X), max(X), 200)
Phi_plot = np.vander(X_plot, N=n+1, increasing=True)

U_plot = Phi_plot @ a

plt.scatter(X, U, label="Données expérimentales")
plt.plot(X_plot, U_plot, color='red', label=f"Régression polynomiale (degré {n})")
plt.xlabel("X")
plt.ylabel("U")
plt.title("Régression par moindres carrés")
plt.grid(True)
plt.legend()
plt.show()
