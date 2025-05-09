 ##############################################################################################################################
##                                                                                                                            ##
##   Ce code python est conçu pour mesurer le temps grâce au mouvement rotatif d'un système à trois aimants.                  ##
##   Auteur : [Ivan G.]                                                                                                       ##
##   Date : 2025-05-07                                                                                                        ##
##   Version 0.1.8                                                                                                            ##
##                                                                                                                            ##
 ##############################################################################################################################

import serial

# Configuration du port série 1
port1 = "COM10"  # À adapter si besoin 
baud1 = 250000    # Débit (bauds)
frequence_systeme = 20  # En Hz (tours par seconde) 
duree_test_1 = 50
duree_test_2 = 100
facteur_discretisation = 2
erreur_lancement = False

try:
    ser1 = serial.Serial(port1, baud1, timeout=1)
except:
    print(f"Erreur d'ouverture du port {port1}")
    erreur_lancement = True


########################################################################### 
## Fonctions pour les microcontroleurs                                   ##   
########################################################################### 

def mise_a_jour(oscillations_totales, etat_precedent):
    if ser1.in_waiting > 0: 
        ligne = ser1.readline().decode('utf-8', errors='ignore').strip() 
        if ligne.isdigit(): 
            valeur = int(ligne) 
            if valeur == 1 and etat_precedent == 0: 
                oscillations_totales += 1  
            return oscillations_totales, valeur
    return oscillations_totales, etat_precedent
    
def envoyer_frequence(frequence):
    message = f"FRQ {frequence:.2f} Hz\n"
    ser1.write(message.encode('utf-8'))

def envoyer_chronometre(temps_chronometre):
    message = f"CHR {temps_chronometre:.2f} s\n"
    ser1.write(message.encode('utf-8'))

def envoyer_alarme(temps_alarme):
    message = f"ALM {temps_alarme:.2f} s \nDring !\n"
    ser1.write(message.encode('utf-8'))

def envoyer_horloge(temps_horloge):
    message = f"CLK {temps_horloge}\n"
    ser1.write(message.encode('utf-8'))

def envoyer_richardson(frequence_1, frequence_2=None, facteur=None):
    message = f"RIC {frequence_1:.2f} Hz {frequence_2:.2f} Hz {facteur}\n"
    ser1.write(message.encode('utf-8'))


########################################################################### 
## Fonctions pour le code python                                         ##   
########################################################################### 

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
                if etat_precedent == 0:
                    envoyer_frequence(frequence)
                else:
                    continue

            if temps_systeme >= duree_test:
                envoyer_frequence(frequence)
                print(f"\nFréquence mesurée : {frequence:.2f} Hz")
                break

    except KeyboardInterrupt:
        print("Interruption manuelle.")
        envoyer_frequence(frequence)

    temps_total = time.time() - temps_debut
    tours = oscillations_totales // 3
    if temps_total > 0:
        frequence = tours / temps_total
        resultat_frequence(frequence, liste_temps, liste_frequence, temps_total, oscillations_totales, tours)
    else:
        frequence = None
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
            if etat_precedent == 0:
                envoyer_chronometre(temps_projet)
            else:
                continue

            liste_temps_projet.append(temps_projet)
            liste_temps_reel.append(temps_reel)
            liste_erreur.append(temps_reel - temps_projet)



    except KeyboardInterrupt:
        resultat_chronometre(frequence_systeme, oscillations_totales, tours, temps_projet, temps_reel,
                                       liste_temps_reel, liste_temps_projet, liste_erreur)
        envoyer_chronometre(temps_projet)

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
            envoyer_horloge(heure_str)

    except KeyboardInterrupt:
        print("\n" + "-" * 40)
        print(f"{'Horloge arrêtée':^40}")
        print(f"Il était {heure_str}")
        print("-" * 40)
        envoyer_horloge(heure_str)

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

            temps_restant = temps_alarme - temps_projet

            if temps_projet < temps_alarme:
                print(f"Temps restant : {temps_restant:.2f} secondes", end="\r")
                if etat_precedent == 0:
                    envoyer_alarme(temps_restant)
            else:
                print("Temps écoulé !")
                envoyer_alarme(temps_restant)
                break
    except KeyboardInterrupt:
        print(f"Alarme arrêtée à {temps_restant:.2f} secondes")
        envoyer_alarme(temps_restant)

def mode_debug(frequence_systeme, port, baud, duree_test_1, duree_test_2, facteur_discretisation):
    texte = [
        "\n" + "-" * 40,
        f"{'DEBUG':^40}",
        "-" * 40,
        f"{'Fréquence':<25}: {frequence_systeme} Hz",
        f"{'Port':<25}: {port}",
        f"{'Baud':<25}: {baud}",
        f"{'duree_test_1':<25}: {duree_test_1}",
        f"{'duree_test_2':<25}: {duree_test_2}",
        f"{'facteur_discretisation':<25}: {facteur_discretisation}",
        "-" * 40  # correction de la ligne avec "\n-" * 40
    ]

    for i in texte:
        print(i)

    while True:
        code = input(">>> ")
        if code == "help":
            print("quit\nchanger_frequence\nchanger_port\nchanger_baud\nreset\ndebug\nchanger_temps_facteur")
        elif code == "quit":
            break
        elif code == "changer_frequence":
            try:
                frequence = float(input("Nouvelle fréquence (Hz) : "))
                print(f"Fréquence changée à {frequence} Hz")
            except:
                print("Erreur : nombre invalide.")
        elif code == "changer_port":
            port = input("Nouveau port : ")
            try:
                ser.close()
                ser = serial.Serial(port, baud, timeout=1)
                print(f"Port changé à {port}")
            except:
                print(f"Erreur d'ouverture du port {port}")
        elif code == "changer_baud":
            try:
                baud = int(input("Nouveau baud : "))
                ser.baudrate = baud
                print(f"Baud changé à {baud}")
            except:
                print("Erreur : doit être un entier.")
        elif code == "debug":
            for i in texte:
                print(i)
        elif code == "reset":
            frequence_systeme = 20
            duree_test_1 = 50
            duree_test_2 = 100
            facteur_discretisation = 2
            print(f"{code} : réinitialisation effectuée.")
        
        elif code == "changer_temps_facteur":
            try:
                duree_test_1 = float(input("Nouvelle durée test 1 (en secondes) : "))
                duree_test_2 = float(input("Nouvelle durée test 2 (en secondes) : "))
                facteur_discretisation = int(input("Nouveau facteur de discrétisation : "))
                print(f"Durées et facteur changés :")
                print(f"  duree_test_1 = {duree_test_1}s")
                print(f"  duree_test_2 = {duree_test_2}s")
                print(f"  facteur_discretisation = {facteur_discretisation}")
            except:
                print("Erreur : saisie invalide pour les durées ou le facteur.")

        else:
            print("Commande invalide. Tapez 'help' pour voir les options.")

########################################################################### 
## Methode d'extrapolation de Richardson                                 ##   
########################################################################### 

def extrapolation_richardson(frequence_1, frequence_2, facteur):
    #Si durée 1 = 10 et durée 2 = 5, facteur = 2
    return (frequence_2 * facteur**2 - frequence_1) / (facteur**2 - 1)

def tester_extrapolation_richardson(duree_test_1 , duree_test_2, facteur_discretisation):
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
    envoyer_richardson(frequence_1, frequence_2, facteur_discretisation)
    print(f"\nRésultats:")
    print(f"  Fréquence mesurée avec résolution faible : {frequence_1:.3f} Hz")
    print(f"  Fréquence mesurée avec résolution élevée : {frequence_2:.3f} Hz")
    print(f"  Fréquence extrapolée (Richardson) : {frequence_extrapolee:.3f} Hz")
    
    return frequence_extrapolee

########################################################################### 
## Boucle                                                                ##   
########################################################################### 
if erreur_lancement:
    pass
else:
    try:
        while True:
            print("=== Bienvenue dans le projet de mesure de temps ===")
            print("1. Chronomètre")
            print("2. Horloge")
            print("3. Alarme")
            print("4. Jeu")
            print("5. Calcul de la fréquence")
            print("6. Debug")
            print("7. Quitter le programme")

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
                while True:
                    print("1. Sans extrapolation")
                    print("2. Extrapolation de Richardson")
                    print("3. Revenir en arrière")
                    sous_choix  = input("Comment voulez vous la calculer ? ").strip()
                    if sous_choix  == "1":
                        frequence_systeme = mesurer_frequence(100)
                        print(f"Nouvelle fréquence du système établit à : {frequence_systeme}")
                    elif sous_choix  == "2":
                        frequence_systeme = tester_extrapolation_richardson(50, 100, 2)
                        print(f"Nouvelle fréquence du système établit à : {frequence_systeme}")
                    elif sous_choix  == "3":
                        break
                    else : 
                        print("Entrée invalide")

            elif choix == "6":
                mode_debug(frequence_systeme, port1, baud1, duree_test_1, duree_test_2, facteur_discretisation)
            elif choix == "7":
                print("Fermeture du programme.")
                break
            else:
                print("Entrée invalide. Veuillez taper un des choix proposés.")

    except KeyboardInterrupt:
        print("Interruption manuelle détectée. Fermeture du programme.")