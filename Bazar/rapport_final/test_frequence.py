import serial
import time

# Configuration du port série
port = "COM3"  # À adapter selon ta machine
baud = 9600     # Débit en bauds
start = 0  # Nombre d'oscillations à ignorer avant de commencer le comptage

# Durée du test en secondes (5 minutes)
duree_test = 5 * 60

try:
    ser = serial.Serial(port, baud, timeout=1)
except serial.SerialException as e:
    print(f"Erreur d'ouverture du port série : {e}")
    exit(1)

etat_precedent = 0
oscillations_totales = 0
temps_debut = 0  # Temps au début du comptage

def mise_a_jour(oscillations_totales, etat_precedent):
    try:
        if ser.in_waiting > 0:  # Vérifie s'il y a des données disponibles
            ligne = ser.readline().decode('utf-8', errors='ignore').strip()  # Ignorer les erreurs de décodage
            
            if ligne.isdigit():
                valeur = int(ligne)
                
                if valeur == 1 and etat_precedent == 0:
                    oscillations_totales += 1
                    print(f"Oscillation #{oscillations_totales}")
                    
                return oscillations_totales, valeur
            else:
                print(f"Valeur non numérique reçue : {ligne}")
        else:
            pass  # Pas de données à lire, continuer la boucle
            
    except Exception as e:
        print(f"Erreur lors de la lecture ou de la mise à jour : {e}")
    
    return oscillations_totales, etat_precedent

# Boucle principale pour tester le temps d'un tour complet
try:
    print("Commencement du test pour mesurer la fréquence sur 5 minutes.")
    temps_debut = time.time()
    
    while True:
        # Mise à jour du comptage d'oscillations
        oscillations_totales, etat_precedent = mise_a_jour(oscillations_totales, etat_precedent)
        
        # Condition pour calculer après 5 minutes
        if time.time() - temps_debut >= duree_test:
            break
    
    # Calcul de la fréquence
    tours_complets = oscillations_totales // 3  # Nombre de tours (chaque tour correspond à 3 oscillations)
    temps_total = time.time() - temps_debut  # Temps total écoulé
    frequence = tours_complets / temps_total  # Fréquence en tours par seconde (Hz)

    print(f"Nombre d'oscillations : {oscillations_totales}")
    print(f"Nombre de tours complets : {tours_complets}")
    print(f"Temps écoulé : {temps_total:.2f} secondes")
    print(f"Fréquence mesurée : {frequence:.2f} tours par seconde (Hz)")

except KeyboardInterrupt:
    # Si l'utilisateur interrompt, afficher les données calculées jusqu'à ce point
    print("Arrêt manuel détecté.")
    temps_total = time.time() - temps_debut  # Calcul du temps écoulé
    tours_complets = oscillations_totales // 3  # Calcul des tours complets
    frequence = tours_complets / temps_total  # Calcul de la fréquence en tours par seconde (Hz)
    print(f"Nombre d'oscillations : {oscillations_totales}")
    print(f"Nombre de tours complets : {tours_complets}")
    print(f"Temps écoulé : {temps_total:.2f} secondes")
    print(f"Fréquence mesurée : {frequence:.2f} tours par seconde (Hz)")

finally:
    print("Test terminé.")
