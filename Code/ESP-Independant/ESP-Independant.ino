#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int Mesure = 4;        // Pin analogique utilisé pour la mesure
int seuil = 3000;      // Seuil pour la détection
int valeur = 0;

String ligneSerial = "";  // Pour lire les lignes série

void setup() {
  Wire.begin(21, 22);     // I2C sur broches personnalisées
  Serial.begin(115200);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Échec"));
    while (true);  // Boucle infinie si écran non détecté
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0); // On affiche en haut à gauche
  display.println("En attente...");
  display.display();
}

void loop() {
  // Lecture bobine
  valeur = analogRead(Mesure);
  int etat = (valeur > seuil) ? 0 : 1;

  // Si l'état change, l'afficher et envoyer à la série
  static int dernierEtat = -1;  // Variable pour stocker l'état précédent
  if (etat != dernierEtat) {
    Serial.println(etat);  // Envoie de l'état via série uniquement lorsqu'il change
    dernierEtat = etat;    // Mise à jour de l'état précédent
  }

  // Lecture des données envoyées par le port
  if (Serial.available()) {
    ligneSerial = Serial.readStringUntil('\n');
    afficherTexte(ligneSerial);  // Affichage simple du message reçu
  }
}

void afficherTexte(String texte) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(texte);
  display.display();
}