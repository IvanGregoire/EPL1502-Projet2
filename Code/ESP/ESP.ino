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
  Serial.begin(250000);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Échec"));
    while (true);  // Boucle infinie si écran non détecté
  }

  display.clearDisplay();
  display.setTextSize(1.5);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("En attente...");
  display.display();
}

void loop() {
  // Lecture capteur
  valeur = analogRead(Mesure);
  int etat = (valeur > seuil) ? 0 : 1;
  Serial.println(etat);

  // Lecture série
  if (Serial.available()) {
    ligneSerial = Serial.readStringUntil('\n');
    ligneSerial.trim();

    if (ligneSerial.startsWith("FRQ")) {
      afficherTexte("Fréquence:", ligneSerial.substring(4));
    } 

    else if (ligneSerial.startsWith("CHR")) {
      afficherTexte("Chronomètre:", ligneSerial.substring(4));
    } 

    else if (ligneSerial.startsWith("CLK")) {
      afficherTexte("Heure:", ligneSerial.substring(4));
    }
    else if (ligneSerial.startsWith("ALM")) {
      afficherTexte("Alarme:", ligneSerial.substring(4));
    }

    else if (ligneSerial.startsWith("RIC")) {
      afficherTexte("Résultat:", ligneSerial.substring(4));
    }
  }
}

void afficherTexte(String titre, String valeur) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(titre);
  display.setTextSize(2);
  display.setCursor(0, 20);
  display.println(valeur);
  display.setTextSize(1);
  display.display();
}
