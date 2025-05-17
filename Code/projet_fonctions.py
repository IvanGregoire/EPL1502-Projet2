 ##############################################################################################################################
##                                                                                                                            ##
##   Ce code Python est conçu pour mesurer le temps grâce au mouvement rotatif d'un système à trois aimants.                v ##
##                                                                                                                            ##
##   Auteurs : Ivan G., Grégoire C., Charline C., Martin S., Guillaume J., Grâce De V.                                        ##
##   Date : 2025-05-13                                                                                                        ##
##                                                                                                                            ##
##   Sources :                                                                                                                ##
##     - Documentation PySerial : https://pyserial.readthedocs.io/en/latest/pyserial.html                                     ##
##     - Tutoriel Arduino-Python (Arduino Project Hub) :                                                                      ##
##         https://projecthub.arduino.cc/ansh2919/serial-communication-between-python-and-arduino-663756                      ##
##     - Tutoriel vidéo de communication série Arduino ↔ Python :                                                             ##
##         https://www.youtube.com/watch?v=iKGYbMD3NT8&list=PLb1SYTph-GZJb1CFM7ioVY9XJYlPVUBQy&index=1                        ##
##     - Documentation officielle du module `datetime` de Python :                                                            ##
##         https://docs.python.org/3/library/datetime.html                                                                    ##                                  
##     - Github Copilot pour les corrections d'erreurs récurrentes et pour des explications approfondies sur l'optimisation   ##                                                                                                       ##
##                                                                                                                            ##
 ##############################################################################################################################

import serial

# Configuration des ports

port1 = "COM11" #Parfois il change
baud1 = 9600    
port2 = "COM10"  
baud2 = 115200  

frequence_systeme = 10 #Il faut lancer la fonction de mesure, sinon on a une mauvaise fréquence
duree_test_1 = 180  
duree_test_2 = 180
facteur_discretisation = 2
delta_t = 0.01  # Délai entre les mesures (Utile pour le bouton)
erreur_lancement = False

try:
    ser1 = serial.Serial(port1, baud1, timeout=1)
    ser2 = serial.Serial(port2, baud2, timeout=1)
except:
    print(f"Erreur d'ouverture du port {port1} ou {port2}.")
    erreur_lancement = True

########################################################################### 
## Fonctions pour les microcontroleurs                                   ##   
########################################################################### 

def mise_a_jour(detections_totales, etat_precedent):
    if ser1.in_waiting > 0:
        derniere_ligne = None
        # Lire toutes les lignes disponibles, mais ne garder que la dernière 
        #Sinon on a un problème de lecture et le programme se met à lire toutes les nouvelles et anciennes valeurs (Problème durant le concours...)
        while ser1.in_waiting > 0:
            derniere_ligne = ser1.readline().decode('utf-8', errors='ignore').strip()
        # Si la dernière ligne est un chiffre, la traiter (Vérification qui, dans l'absolue, ne sert à rien puisque ça ne renvoie que des 1 et des 0)
        if derniere_ligne and derniere_ligne.isdigit():
            valeur = int(derniere_ligne)
            if valeur == 1 and etat_precedent == 0:
                detections_totales += 1
            return detections_totales, valeur
    return detections_totales, etat_precedent

def safe_write(message): #En cas de problème d'envoi (Si on tire sur un câble etc...)
    try:
        ser2.write(message.encode('utf-8'))
    except:
        print(f"Problème lors de l’envoi série")

def envoyer_richardson(frequence_1, facteur, frequence_systeme,frequence_2=None):
    message = f"RIC 1 : {frequence_1:.2f} Hz | 2 : {frequence_2:.2f} Hz | {facteur} Final : {frequence_systeme:.2f} Hz\n"
    safe_write(message)

def message_str(message):
    message = f"{message}\n" #Les \n sont importants. Sinon ça s'affiche mal
    safe_write(message)

def recevoir_message():
    try:
        if ser2.in_waiting > 0:
            ligne = ser2.readline().decode('utf-8', errors='ignore').strip()
            if ligne:  # si on a bien une ligne non vide
                return ligne

        return None  # rien reçu
    except :
        print("Erreur de réception du message. PORT 2")
        return

def envoyer_message(type_msg, valeur):
    if isinstance(valeur, float):
        message = f"{type_msg} {valeur:.2f}\n"
    else:
        message = f"{type_msg} {valeur}\n"
    safe_write(message)
########################################################################### 
## Fonctions pour le code python                                         ##   
########################################################################### 

import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

def mesurer_frequence(duree_test):
    etat_precedent = 0
    detections_totales = 0
    temps_debut = time.time()
    #Partie pour le graphique
    liste_temps = []
    liste_frequence = []

    print("Début du test...")
    try:
        while True:
            detections_totales, etat_precedent = mise_a_jour(detections_totales, etat_precedent)

            temps_systeme = time.time() - temps_debut

            if temps_systeme > 0:
                tours = detections_totales // 3
                frequence = tours / temps_systeme
                liste_temps.append(temps_systeme)
                liste_frequence.append(frequence)
                print(f"{temps_systeme:.1f}s : {frequence:.2f} Hz | détections {detections_totales}", end="\r")
                if etat_precedent == 0:
                    envoyer_message("FRQ", frequence)
                else:
                    continue

            if temps_systeme >= duree_test:
                envoyer_message("FRQ", frequence)
                print(f"\nFréquence mesurée : {frequence:.2f} Hz | détections {detections_totales}", end="\r")
                break

    except KeyboardInterrupt:
        print("Interruption manuelle.")
        envoyer_message("FRQ", frequence)

    temps_total = time.time() - temps_debut
    tours = detections_totales // 3
    if temps_total > 0:
        frequence = tours / temps_total
        resultat_frequence(frequence, liste_temps, liste_frequence, temps_total, detections_totales, tours)
    else:
        frequence = None
        return frequence
    return frequence

def resultat_frequence(frequence, liste_temps, liste_frequence, temps_total, detection_totales, tours):
    print("-" * 40)
    print("\n--- Récapitulatif ---")
    print("-" * 40)
    print(f"Durée totale de mesure : {temps_total:.2f} s")
    print(f"Nombre total de détections : {detection_totales}")
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
    envoyer_message("FRQ", frequence)

def chronometre(frequence_systeme):
    print("\nChronométrage en cours...\n")
    detections_totales = 0
    detections_utiles = 0
    etat_precedent = 0
    temps_depart = time.time()
    start = 0

    liste_temps_reel = []
    liste_temps_projet = []
    liste_erreur = []

    try:
        while True:
            detections_totales, etat_precedent = mise_a_jour( detections_totales, etat_precedent)

            if detections_totales > start:
                detections_utiles = detections_totales - start
                tours = detections_utiles // 3
                temps_projet = tours / frequence_systeme
                temps_reel = time.time() - temps_depart

                print(f"Temps mesuré : {temps_projet:.2f} s | {detections_totales} détections | {tours} tours", end="\r")

                if etat_precedent == 0:
                    envoyer_message("CHR", temps_projet)

                liste_temps_projet.append(temps_projet)
                liste_temps_reel.append(temps_reel)
                liste_erreur.append(temps_reel - temps_projet)


    except KeyboardInterrupt:
        print("\nArrêt manuel détecté.")
        if detections_totales > start:
            resultat_chronometre(frequence_systeme, detections_totales, tours, temps_projet, temps_reel,
                                 liste_temps_reel, liste_temps_projet, liste_erreur)
            envoyer_message("CHR", temps_projet)
        else:
            print("Pas assez de détections utiles détectées.")

def resultat_chronometre(frequence, detections, tours, temps_projet, temps_reel, liste_t_reel, liste_t_projet, liste_t_erreur):
    print("\n" + "-" * 40)
    print(f"{'RÉCAPITULATIF':^40}")
    print("-" * 40)
    print(f"{'Fréquence':<25}: {frequence} Hz")
    print(f"{'Détections détectées':<25}: {detections}")
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
    detections_totales = 0
    etat_precedent = 0
    heure_depart = datetime.now()

    try:
        while True:
            detections_totales, etat_precedent = mise_a_jour(detections_totales, etat_precedent)
            tours = detections_totales // 3
            temps_projet = tours / frequence_systeme
            heure_approx = heure_depart + timedelta(seconds=temps_projet)
            heure_str = heure_approx.strftime("%H:%M:%S") # Format pour afficher l'heure
            print(f"Horloge : {heure_str}", end="\r")
            envoyer_message("HOR", heure_str)
    except KeyboardInterrupt:
        print("\n" + "-" * 40)
        print(f"{'Horloge arrêtée':^40}")
        print(f"Il était {heure_str}")
        print("-" * 40)
        envoyer_message("HOR", heure_str)

def alarme(frequence_systeme):
    try:
        temps_alarme = float(input("Entrez le temps de l'alarme (en secondes) : "))
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    etat_precedent = 0
    detections_totales = 0

    try:
        while True:
            detections_totales, etat_precedent = mise_a_jour(detections_totales, etat_precedent)
            tours = detections_totales // 3
            temps_projet = tours / frequence_systeme

            temps_restant = temps_alarme - temps_projet

            if temps_projet < temps_alarme:
                print(f"Temps restant : {temps_restant:.2f} secondes", end="\r")
                envoyer_message("ALR", temps_restant)
            else:
                print("Temps écoulé !")
                envoyer_message("ALR", 0)
                message_str("DRING")  # Envoi d'un signal pour le son
                break

    except KeyboardInterrupt:
        print(f"Alarme arrêtée à {temps_restant:.2f} secondes")
        envoyer_message("ALR", temps_restant)

def jeu1(frequence_systeme):

    minus = 3  # Affichage du temps pendant 10 sec
    maximus = 15      # Objectif à atteindre
    texte = [
        "-" * 40,
        f"{'Jeu 1':^40}",
        "-" * 40,
        f"Le but est simple : essayez d'estimer {maximus} secondes dans notre système.",
        f"Le temps écoulé sera affiché durant les {minus} premières secondes.",
        "Pour commencer, appuyez sur le bouton.",
        "Appuyez à nouveau pour arrêter le chronomètre.",
        "Bonne chance !",
        "-" * 40,
    ]
    for i in texte:
        print(i)

    print("Appuyez sur le bouton pour commencer...")
    while True:
        message = recevoir_message()
        if message == "BEGIN":
            break
        print("En attente de l'appui sur le bouton...", end="\r")

    #Premier appui reçu pour démarrer le chrono
    etat_precedent = 0
    detections_totales = 0
    temps_projet = 0
    tours = 0

    print("Chronomètre lancé ! Appuyez à nouveau pour l’arrêter.")

    while True:
        detections_totales, etat_precedent = mise_a_jour(detections_totales, etat_precedent)
        tours = detections_totales // 3
        temps_projet = tours / frequence_systeme

        if temps_projet <= minus:
            print(f"Temps écoulé : {temps_projet:.2f} secondes", end="\r")
            envoyer_message("JEU", temps_projet)
        else:
            print(f"Bonne chance !", end="\r")

        if message == "BEGIN":     
            envoyer_message("JEU", temps_projet) #Si on appuie encore une fois, c'est pour l'arrêter
            break 
    ecart = temps_projet - maximus

    if abs(ecart) < 0.5:
        while True:
            print(f"{ecart:+.2f} | Bien joué ! Vous étiez proche des {maximus} secondes.", end="\r")
            ligne = recevoir_message()
            if ligne == "BEGIN":
                return 
    elif ecart > 0:
        while True:
            print(f"Temps écoulé : {temps_projet:.2f} secondes. Vous avez dépassé.", end="\r")
            ligne = recevoir_message()
            if ligne == "BEGIN":
                return 
    elif ecart < 0:
        while True:
            print(f"Temps écoulé : {temps_projet:.2f} secondes. Trop court.", end="\r")
            ligne = recevoir_message()
            if ligne == "BEGIN":
                return 
    else:
        while True:
            print("Bien joué", end="\r")
            ligne = recevoir_message()
            if ligne == "BEGIN":
                return 

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
    envoyer_richardson(frequence_1, facteur_discretisation, frequence_extrapolee, frequence_2)
    print("-" * 40)
    print(f"\n--- Résultats de l'extrapolation ---")
    print(f"  Fréquence mesurée avec résolution faible : {frequence_1:.3f} Hz")
    print(f"  Fréquence mesurée avec résolution élevée : {frequence_2:.3f} Hz")
    print(f"  Fréquence extrapolée (Richardson) : {frequence_extrapolee:.3f} Hz")
    print("-" * 40)
    
    return frequence_extrapolee

########################################################################### 
## Boucle                                                                ##   
########################################################################### 
def main(frequence_systeme, port1, baud1, duree_test_1, duree_test_2, facteur_discretisation, erreur_lancement):

    if erreur_lancement:
        pass
    else:
        try:
            while True:
                message_str("Bienvenue dans notre projet de mesure du temps !")
                print("=== Bienvenue dans le projet de mesure de temps ===")
                print("1. Chronomètre")
                print("2. Horloge")
                print("3. Alarme")
                print("4. Jeu")
                print("5. Calcul de la fréquence")
                print("6. Quitter")

                choix = input("Votre choix : ").strip()

                if choix == "1":
                    chronometre(frequence_systeme)
                elif choix == "2":
                    horloge(frequence_systeme)
                elif choix == "3":
                    alarme(frequence_systeme)
                elif choix == "4":
                    jeu1(frequence_systeme)
                elif choix == "5":
                    while True:
                        print("1. Sans extrapolation")
                        print("2. Extrapolation de Richardson")
                        print("3. Revenir en arrière")
                        sous_choix  = input("Comment voulez vous la calculer ? ").strip()
                        if sous_choix  == "1":
                            frequence_systeme = mesurer_frequence(duree_test_2)
                            print(f"Nouvelle fréquence du système établit à : {frequence_systeme}")
                        elif sous_choix  == "2":
                            frequence_systeme = tester_extrapolation_richardson(duree_test_1, duree_test_2, facteur_discretisation)
                            print(f"Nouvelle fréquence du système établit à : {frequence_systeme}")
                        elif sous_choix  == "3":
                            break
                        else : 
                            print("Entrée invalide")
                elif choix == "6":
                    print("Fermeture du programme.")
                    break
                else:
                    print("Entrée invalide. Veuillez taper un des choix proposés.")

        except KeyboardInterrupt:
            print("Interruption manuelle détectée. Fermeture du programme.")
            ser1.close()
            ser2.close()
        finally:
            ser1.close()
            ser2.close()

if __name__ == "__main__":
    main(frequence_systeme, port1, baud1, duree_test_1, duree_test_2, facteur_discretisation, erreur_lancement)
    ser1.close()
    ser2.close()