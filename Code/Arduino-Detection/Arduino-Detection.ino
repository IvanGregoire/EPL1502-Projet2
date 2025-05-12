int Mesure = A0;        // Pin analogique utilisé pour la mesure
int seuil = 700;   // seuil de détection
int valeur = 0;

void setup() {

  Serial.begin(9600);

}

void loop() {
  // Lecture bobine
  valeur = analogRead(Mesure);
  static int etat = -1;         
  static int dernierEtat = -1;  

  if (valeur > seuil) etat = 0;
  else if (valeur < seuil) etat = 1;

  // Si l'état change, l'afficher et envoyer à la série
    Serial.println(etat);  // Envoie de l'état via série uniquement lorsqu'il change
    dernierEtat = etat;    // Mise à jour de l'état précédent
}