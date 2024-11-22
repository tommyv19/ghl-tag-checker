from flask import Flask, request, jsonify
import traceback

app = Flask(__name__)

# Simulazione di un archivio di tag già esistenti
existing_tags = ["Test Tag", "Sample Tag"]  # Puoi sostituire con un database o altro sistema di archiviazione

@app.route('/inbound_webhook', methods=['POST'])
def inbound_webhook():
    try:
        print("=== Inizio gestione richiesta /inbound_webhook ===")
        
        # Log dei dati ricevuti
        data = request.json
        print(f"Dati ricevuti: {data}")

        # Controlla se i dati e il campo 'tag_name' sono presenti
        if not data or 'tag_name' not in data:
            print("Errore: 'tag_name' non trovato o dati mancanti.")
            return jsonify({"status": "failed", "message": "Dati non validi o mancanti"}), 400

        tag_name = data['tag_name']
        print(f"Tag ricevuto: {tag_name}")

        # Controlla se il tag è già presente
        if tag_name in existing_tags:
            print(f"Errore: Il tag '{tag_name}' esiste già.")
            return jsonify({
                "status": "failed",
                "message": f"Il tag '{tag_name}' esiste già",
                "is_duplicate": True
            }), 409  # 409: Conflict

        # Procedi con la creazione del tag (simulata)
        existing_tags.append(tag_name)
        print(f"Tag '{tag_name}' creato con successo.")
        return jsonify({
            "status": "success",
            "message": f"Tag '{tag_name}' creato con successo",
            "is_duplicate": False
        }), 200

    except Exception as e:
        # Log dell'errore
        print("Errore durante la gestione della richiesta:")
        traceback.print_exc()
        return jsonify({"status": "failed", "message": f"Errore nella gestione del webhook: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
