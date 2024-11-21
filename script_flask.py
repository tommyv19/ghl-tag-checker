from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Configurazione API
API_BASE_URL = "https://rest.gohighlevel.com/v1"
API_KEY = "la-tua-api-key"  # Sostituisci con la tua chiave API

def check_tag_exists(tag_name):
    url = f"{API_BASE_URL}/tags"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tags = [tag['name'] for tag in response.json().get('data', [])]
        return tag_name in tags
    return False

@app.route('/')
def home():
    return "Server Flask attivo! Usa l'endpoint /create_tag per interagire."

@app.route('/create_tag', methods=['POST'])
def create_tag():
    data = request.json
    tag_name = data.get('tag_name')
    if check_tag_exists(tag_name):
        return jsonify({"status": "exists", "message": f"Il tag '{tag_name}' esiste già"}), 400
    # Logica per creare un nuovo tag
    url = f"{API_BASE_URL}/tags"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"name": tag_name}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return jsonify({"status": "success", "message": f"Tag '{tag_name}' creato"}), 201
    return jsonify({"status": "failed", "message": response.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Cambia la porta a 5001
