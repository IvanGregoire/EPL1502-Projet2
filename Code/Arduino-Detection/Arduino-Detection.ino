const int Mesure = A0;      // Pin analogique utilisé pour la mesure
const int seuil = 300;      // Seuil de détection
int valeur = 0;
int etat = -1;              // État précédent
int nouvelEtat = -1;        // État actuel

void setup() {
  Serial.begin(9600);       // Initialisation de la communication série
}

void loop() {
  // Lecture de la valeur analogique
  valeur = analogRead(Mesure);

  // Détermination de l'état actuel
  if (valeur > seuil) {
    nouvelEtat = 0;
  } else {
    nouvelEtat = 1;
  }

  if (nouvelEtat != etat) {
    etat = nouvelEtat;
    Serial.println(etat);
  }
}
