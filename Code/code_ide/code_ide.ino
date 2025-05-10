// Déclaration des variables globales
int Mesure = A0;   // Le pin analogique utilisé pour la mesure (A5)
int valeur = 0;     // Variable pour stocker la valeur lue par le capteur
int seuil = 700;    // Seuil pour la détection (par exemple, pour détecter un aimant ou un changement de valeur)

void setup() {
  // Initialisation de la communication série pour l'affichage des données sur le moniteur série
  Serial.begin(9600);  
}

void loop() {
  // Lecture de la valeur analogique provenant du capteur connecté à A5
  valeur = analogRead(Mesure);  
  
  // Vérification si la valeur lue dépasse le seuil défini
  if (valeur > seuil) {
    // Si la valeur dépasse le seuil, envoyer "0" sur le port série (indique un état particulier, ici le passage d'un aimant)
    Serial.println(0);   
  } else {
    // Si la valeur est inférieure au seuil, envoyer "1" sur le port série
    Serial.println(1);   
  }
  // Aucun délai n'est inclus afin d'éviter de passer des oscillations en cas d'une vitesse élevée
}