int Mesure = A5;      // Pin analogique pour la mesure
int valeur = 0;       // Valeur lue
int seuil = 100;      // Seuil de détection
int etat_precedent = 0; // État précédent (0 ou 1)
// Il faut faire attention à intervertir l'état 0 et 1 entre les tests avec bouton et avec aimant
// Les deux sont inversés
void setup() {
  Serial.begin(9600);  // Il me semble que 9600 c'est bien assez
}

void loop() {
  valeur = analogRead(Mesure);  
  int etat_actuel = (valeur > seuil) ? 1 : 0; // 1 si au-dessus du seuil, 0 sinon

  // Envoie uniquement si changement d'état
  if (etat_actuel != etat_precedent) {
    Serial.println(etat_actuel);
    etat_precedent = etat_actuel;
  }
}