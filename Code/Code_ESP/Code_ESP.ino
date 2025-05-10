#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ESP32_Network";  // Nom du réseau Wi-Fi créé par l'ESP32
const char* password = "123456789";  // Mot de passe du réseau Wi-Fi

WebServer server(80);  // Crée un serveur HTTP sur le port 80

// Fonction pour gérer les requêtes POST
void handlePost() {
  if (server.hasArg("message")) {
    String message = server.arg("message");  // Récupère le paramètre 'message' de la requête POST
    Serial.println("Message reçu : " + message);
    server.send(200, "text/plain", "Données reçues avec succès");
  } else {
    server.send(400, "text/plain", "Aucune donnée 'message' reçue");
  }
}

void setup() {
  // Initialisation du moniteur série
  Serial.begin(115200);

  // Initialisation de l'ESP32 en mode point d'accès
  WiFi.softAP(ssid, password);

  // Affichage de l'adresse IP du point d'accès
  Serial.println("");
  Serial.print("Point d'accès créé. L'adresse IP est : ");
  Serial.println(WiFi.softAPIP());

  // Définir la route et la fonction qui gère la requête POST
  server.on("/post", HTTP_POST, handlePost);

  // Démarrer le serveur
  server.begin();
}

void loop() {
  // Le serveur HTTP écoute les requêtes entrantes
  server.handleClient();
}
