import tkinter as tk
import threading
from projet_fonctions import *


def window_ouverture():
    
    window = tk.Tk()  
    window.title("Projet Q2")
    window.geometry("800x600")
    window.configure(bg="white")

    titre = tk.Label(window,text="Projet Q2- Groupe 11.28", font=("Arial", 20), bg="white")
    titre.pack(pady=20)
    
    def lancer_en_thread(fonction):
        threading.Thread(target=fonction, daemon=True).start()

    liste_bouttons = [
        ("Mesurer la fréquence", lambda: lancer_en_thread(lambda: mesurer_frequence(10))),
        ("Chronomètre", lambda: lancer_en_thread(lambda: chronometre(frequence_systeme))),
        ("Horloge", lambda: lancer_en_thread(lambda: horloge(frequence_systeme))),
        ("Alarme", lambda: lancer_en_thread(lambda: alarme(frequence_systeme))),
        ("Debug", lambda: lancer_en_thread(lambda: mode_debug(frequence_systeme, port, baud))),
        ("Quitter", window.quit)
    ]

    for nom,fonctions in liste_bouttons:
        bouton = tk.Button(window, text=nom,font=("Arial", 15), bg="lightblue", command=fonctions)
        bouton.pack(pady=10, padx=20, fill=tk.X)
    window.mainloop()

    
if erreur_lancement:
    tk.messagebox.showerror("Erreur", f"Erreur de lancement du programme. Vérifiez le port {port}")
else:
    window_ouverture()
