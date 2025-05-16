#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


int START = 4; // PIN D4
int valeur = 0; 
int Buzzer = 5; // PIN D5 
int etat_precedent = 0; 
bool pression = false;  

String ligneSerial = "";  // Pour lire les lignes série

void setup() {
  Wire.begin(21, 22);     // SDA et SCL
  Serial.begin(115200);  
  pinMode(Buzzer, OUTPUT);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("Échec"));
    while (true);  // Boucle infinie si écran non détecté
  }

  display.clearDisplay(); // Efface l'écran s'il y a réinitialisation (ça évite de débrancher et rebrancher l'écran)
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0); // On affiche en haut à gauche
  display.println("En attente...");
  display.display();
}

void loop() {
  // Lecture bouton
  valeur = analogRead(START);

  if (valeur > 3000 && !pression) {  
    pression = true;
    Serial.println("BEGIN");
  }
  else if (valeur <= 3000 && pression) {  // La vérification de la pression est faite pour éviter les appuis trop longs
    pression = false;
  }
}

void afficherTexte(String texte) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println(texte);
  display.display();
}