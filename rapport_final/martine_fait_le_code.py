import serial

# Configuration du port série
port = "COM3"  # À adapter selon ta machine
baud = 9600    # Débit en bauds
frequence = 10  # En Hz (oscillations par seconde) car 2 aimants
start = 0 # Nombre d'oscillations à ignorer avant de commencer le comptage

try:
    ser = serial.Serial(port, baud, timeout=1)
except serial.SerialException as e:
    print(f"Erreur d'ouverture du port série : {e}")
    exit(1)

etat_precedent = 0
oscillations_totales = 0
oscillations_utiles = 0  # Celles après le seuil

def mise_a_jour(oscillations_totales, oscillations_utiles, etat_precedent):
    try:
        ligne = ser.readline().decode().strip()
        
        if not ligne.isdigit():
            return oscillations_totales, oscillations_utiles, etat_precedent

        valeur = int(ligne)
        
        if valeur == 1 and etat_precedent == 0:
            oscillations_totales += 1
            print(f"Oscillation #{oscillations_totales}")
            
            if oscillations_totales > start:
                oscillations_utiles += 1
                temps_ecoule = oscillations_utiles / frequence
                print(f"Temps estimé : {temps_ecoule:.2f} secondes")
        
        return oscillations_totales, oscillations_utiles, valeur 
    
    except Exception as e:
        print(f"Erreur lors de la lecture ou de la mise à jour : {e}")
        return oscillations_totales , oscillations_utiles, etat_precedent

# Boucle principale
try:
    while True:
        oscillations_totales, oscillations_utiles, etat_precedent = mise_a_jour(
            oscillations_totales, oscillations_utiles, etat_precedent)
except KeyboardInterrupt:
    print("Arrêt manuel détecté.")
finally:
    if oscillations_totales > start:
        temps_final = oscillations_utiles / frequence
        print(f"\nTemps total estimé après les {start} premières oscillations ignorées : {temps_final:.2f} secondes")
        print(f"Nombre d'oscillations mesurées après seuil : {oscillations_utiles}")
    else:
        print(f"\nMoins de {start} oscillations détectées. Aucune mesure de temps effectuée.")
