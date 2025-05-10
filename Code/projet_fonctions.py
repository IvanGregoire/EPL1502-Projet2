 ##############################################################################################################################
##                                                                                                                            ##
##   Ce code python est conçu pour mesurer le temps grâce au mouvement rotatif d'un système à trois aimants.                  ##
##   Auteur : [Ivan G.]                                                                                                       ##
##   Date : 2025-05-07                                                                                                        ##
##   Version 0.1.8                                                                                                            ##
##                                                                                                                            ##
 ##############################################################################################################################

import serial

# Configuration du port série
port = "COM3"  # À adapter si besoin
baud = 9600    # Débit (bauds)
frequence_systeme = 9.63  # En Hz (tours par seconde) 

erreur_lancement = False

try:
    ser = serial.Serial(port, baud, timeout=1)
except:
    print(f"Erreur d'ouverture du port {port}")
    erreur_lancement = True

# Fonction de mise à jour du nombre d'oscillations (Identique à celle de frequence.py)
def mise_a_jour(oscillations_totales, etat_precedent):
    if ser.in_waiting > 0: 
        ligne = ser.readline().decode('utf-8', errors='ignore').strip() 
        if ligne.isdigit(): 
            valeur = int(ligne) 
            if valeur == 1 and etat_precedent == 0: 
                oscillations_totales += 1  
            return oscillations_totales, valeur
    return oscillations_totales, etat_precedent

import matplotlib.pyplot as plt
import time
from threading import Thread, Event
from datetime import datetime, timedelta

def mesurer_frequence(duree_test):
    etat_precedent = 0
    oscillations_totales = 0
    temps_debut = time.time()
    #Partie pour le graphique
    liste_temps = []
    liste_frequence = []

    print("Début du test...")
    try:
        while True:
            oscillations_totales, etat_precedent = mise_a_jour(oscillations_totales, etat_precedent)

            temps_systeme = time.time() - temps_debut
            if temps_systeme > 0:
                tours = oscillations_totales // 3
                frequence = tours / temps_systeme
                liste_temps.append(temps_systeme)
                liste_frequence.append(frequence)
                print(f"{temps_systeme:.1f}s : {frequence:.2f} Hz")

            if temps_systeme >= duree_test:
                break

    except KeyboardInterrupt:
        print("Interruption manuelle.")

    temps_total = time.time() - temps_debut
    tours = oscillations_totales // 3
    if temps_total > 0:
        frequence = tours / temps_total
        resultat_frequence(frequence, liste_temps, liste_frequence, temps_total, oscillations_totales, tours)
    else:
        frequence = 0
        return frequence
    return frequence

def resultat_frequence(frequence, liste_temps, liste_frequence, temps_total, oscillations_totales, tours):
    print("-" * 40)
    print("\n--- Récapitulatif ---")
    print("-" * 40)
    print(f"Durée totale de mesure : {temps_total:.2f} s")
    print(f"Nombre total d'oscillations : {oscillations_totales}")
    print(f"Nombre de tours complets : {tours}")
    print(f"Fréquence moyenne : {frequence:.3f} Hz")
    print("-" * 40)

    plt.figure(figsize=(10, 5))
    plt.plot(liste_temps, liste_frequence, label='Fréquence (Hz)', color='blue')
    plt.title('Fréquence en fonction du temps')
    plt.xlabel('Temps (s)')
    plt.ylabel('Fréquence (Hz)')
    plt.grid()
    plt.legend()
    plt.show()

def chronometre(frequence_systeme):
    print("\nChronométrage en cours...\n")
    oscillations_totales = 0
    etat_precedent = 0
    temps_depart = time.time()
    liste_temps_reel = []
    liste_temps_projet = []
    liste_erreur = []

    try:
        while True:
            oscillations_totales, etat_precedent = mise_a_jour(oscillations_totales, etat_precedent)
            tours = oscillations_totales // 3
            temps_projet = tours / frequence_systeme
            temps_reel = time.time() - temps_depart

            print(f"Temps mesuré : {temps_projet:.2f} s", end="\r")

            liste_temps_projet.append(temps_projet)
            liste_temps_reel.append(temps_reel)
            liste_erreur.append(temps_reel - temps_projet)


    except KeyboardInterrupt:
        resultat_chronometre(frequence_systeme, oscillations_totales, tours, temps_projet, temps_reel,
                                       liste_temps_reel, liste_temps_projet, liste_erreur)

def resultat_chronometre(frequence, oscillations, tours, temps_projet, temps_reel, liste_t_reel, liste_t_projet, liste_t_erreur):
    print("\n" + "-" * 40)
    print(f"{'RÉCAPITULATIF':^40}")
    print("-" * 40)
    print(f"{'Fréquence':<25}: {frequence} Hz")
    print(f"{'Oscillations détectées':<25}: {oscillations}")
    print(f"{'Tours complets':<25}: {tours}")
    print(f"{'Temps mesuré':<25}: {temps_projet:.2f} s")
    print(f"{'Temps réel écoulé':<25}: {temps_reel:.2f} s")
    print("-" * 40)

    plt.subplot(2, 1, 1)
    plt.plot(liste_t_reel, liste_t_projet, label="Temps mesuré", color='blue')
    plt.plot(liste_t_reel, liste_t_reel, label="Temps réel (référence)", linestyle='--', color='green')
    plt.title("Évolution du temps mesuré vs temps réel")
    plt.xlabel("Temps réel (s)")
    plt.ylabel("Temps (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    plt.plot(liste_t_reel, liste_t_erreur, label="Erreur (mesuré - réel)", color='red')
    plt.title("Erreur entre temps mesuré et réel")
    plt.xlabel("Temps réel (s)")
    plt.ylabel("Erreur (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def horloge(frequence_systeme):
    oscillations_totales = 0
    etat_precedent = 0
    heure_depart = datetime.now()

    try:
        while True:
            oscillations_totales, etat_precedent = mise_a_jour(oscillations_totales, etat_precedent)
            tours = oscillations_totales // 3
            temps_projet = tours / frequence_systeme
            heure_approx = heure_depart + timedelta(seconds=temps_projet)
            heure_str = heure_approx.strftime("%H:%M:%S") # Format pour afficher l'heure
            print(f"Horloge : {heure_str}", end="\r")

    except KeyboardInterrupt:
        print("\n" + "-" * 40)
        print(f"{'Horloge arrêtée':^40}")
        print(f"Il était {heure_str}")
        print("-" * 40)

def alarme(frequence_systeme):
    try:
        temps_alarme = float(input("Entrez le temps de l'alarme (en secondes) : "))
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    etat_precedent = 0
    oscillations_totales = 0

    try:
        while True:
            oscillations_totales, etat_precedent = mise_a_jour(oscillations_totales, etat_precedent)
            tours = oscillations_totales // 3
            temps_projet = tours / frequence_systeme

            if temps_projet < temps_alarme:
                print(f"Temps restant : {temps_alarme - temps_projet:.2f} secondes", end="\r")
            else:
                print("Temps écoulé !")
                break
    except KeyboardInterrupt:
        print(f"Alarme arrêtée à {temps_alarme-temps_projet:.2f} secondes")

def mode_debug(frequence_system, port, baud):
    print("\n" + "-" * 40)
    print(f"{'DEBUG':^40}")
    print("-" * 40)
    print(f"{'Fréquence':<25}: {frequence_system} Hz")
    print(f"{'Port':<25}: {port}")
    print(f"{'Baud':<25}: {baud}")
    print("-" * 40)

    while True:
        code = input(">>> ")
        if code == "help":
            print("quit\nchanger_frequence\nchanger_port\nchanger_baud\nreset")
        elif code == "quit":
            break
        elif code == "changer_frequence":
            try:
                frequence = float(input("Nouvelle fréquence (Hz) : "))
                print(f"Fréquence changée à {frequence} Hz")
            except ValueError:
                print("Erreur : nombre invalide.")
        elif code == "changer_port":
            port = input("Nouveau port : ")
            try:
                ser.close()
                ser = serial.Serial(port, baud, timeout=1)
                print(f"Port changé à {port}")
            except serial.SerialException as e:
                print(f"Erreur d'ouverture du port : {e}")
        elif code == "changer_baud":
            try:
                baud = int(input("Nouveau baud : "))
                ser.baudrate = baud
                print(f"Baud changé à {baud}")
            except ValueError:
                print("Erreur : doit être un entier.")
        elif code == "reset":
            print(f"{code} : réinitialisation effectuée.")
        else:
            print("Commande invalide. Tapez 'help' pour voir les options.")

########################################################################### 
## Methode d'extrapolation de Richardson                                 ##   
########################################################################### 

def extrapolation_richardson(frequence_1, frequence_2, facteur):
    #Si durée 1 = 10 et durée 2 = 5, facteur = 2
    return (frequence_2 * facteur**2 - frequence_1) / (facteur**2 - 1)

def tester_extrapolation_richardson(duree_test_1, duree_test_2, facteur_discretisation):
    print(f"Mesure 1 (résolution faible, durée {duree_test_1} secondes) :")
    frequence_1 = mesurer_frequence(duree_test_1)
    if frequence_1 is None:
        print("Erreur de mesure pour la première fréquence.")
        return None  
    time.sleep(3)
    print(f"Mesure 2 (résolution élevée, durée {duree_test_2} secondes) :")
    frequence_2 = mesurer_frequence(duree_test_2)
    if frequence_2 is None:
        print("Erreur de mesure pour la deuxième fréquence.")
        return None  
    
    frequence_extrapolee = extrapolation_richardson(frequence_1, frequence_2, facteur_discretisation)

    print(f"\nRésultats:")
    print(f"  Fréquence mesurée avec résolution faible : {frequence_1:.3f} Hz")
    print(f"  Fréquence mesurée avec résolution élevée : {frequence_2:.3f} Hz")
    print(f"  Fréquence extrapolée (Richardson) : {frequence_extrapolee:.3f} Hz")
    
    return frequence_extrapolee

########################################################################### 
## Boucle                                                                ##   
########################################################################### 

try:
    while True:
        print("=== Bienvenue dans le projet de mesure de temps ===")
        print("1. Chronomètre")
        print("2. Horloge")
        print("3. Alarme")
        print("4. Jeu")
        print("5. Debug")
        print("6. Quitter le programme")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            chronometre(frequence_systeme)
        elif choix == "2":
            horloge(frequence_systeme)
        elif choix == "3":
            alarme(frequence_systeme)
        elif choix == "4":
            print("Jeu non implémenté.")
        elif choix == "5":
            mode_debug(frequence_systeme, port, baud)
        elif choix == "6":
            print("Fermeture du programme.")
            break
        else:
            print("Entrée invalide. Veuillez taper un des choix proposés.")

except KeyboardInterrupt:
    print("Interruption manuelle détectée. Fermeture du programme.")