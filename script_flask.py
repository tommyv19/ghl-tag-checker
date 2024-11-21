from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configurazione API di GHL
API_BASE_URL = "https://rest.gohighlevel.com/v1"  # Base URL dell'API GHL
API_KEY = "la-tua-api-key"  # Sostituisci con la tua chiave API

# Endpoint per gestire il webhook
@app.route('/inbound_webhook', methods=['POST'])
def inbound_webhook():
    """Gestisce i dati inviati da GHL tramite un Inbound Webhook."""
    try:
        # Ricezione dati JSON dal webhook
        data = request.json
        print(f"Dati ricevuti dal webhook: {data}")

        # Estrai il nome del tag dai dati
        tag_name = data.get("tag_name", "Default Tag")
        if not tag_name:
            return jsonify({"error": "Nessun nome del tag fornito"}), 400

        # Verifica se il tag esiste già
        url = f"{API_BASE_URL}/tags"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tags = [tag['name'] for tag in response.json().get('data', [])]
            if tag_name in tags:
                return jsonify({"status": "exists", "message": f"Il tag '{tag_name}' esiste già"}), 200

        # Creazione del nuovo tag se non esiste
        payload = {"name": tag_name}
        create_response = requests.post(url, headers=headers, json=payload)
        if create_response.status_code == 201:
            return jsonify({"status": "success", "message": f"Tag '{tag_name}' creato con successo"}), 201

        return jsonify({"status": "failed", "message": "Errore nella creazione del tag"}), 500

    except Exception as e:
        # Gestione errori
        return jsonify({"error": str(e)}), 500

# Avvia il server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
