from flask import Flask, request, jsonify
import logging
import traceback

app = Flask(__name__)

# Configura il logging per vedere tutti i dettagli
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s')

@app.route('/inbound_webhook', methods=['POST'])
def inbound_webhook():
    try:
        logging.info("=== Inizio gestione richiesta /inbound_webhook ===")
        
        # Loggare i dati ricevuti
        data = request.get_json()
        logging.debug(f"Dati ricevuti: {data}")
        
        # Controllare che il payload contenga il campo 'tag_name'
        if not data or 'tag_name' not in data:
            logging.error("Errore: 'tag_name' non trovato o dati mancanti.")
            return jsonify({"status": "failed", "message": "Dati non validi o mancanti"}), 400

        tag_name = data['tag_name']
        logging.info(f"Tag ricevuto: {tag_name}")
        
        # Simulazione di logica di gestione del tag
        if tag_name == "Test Tag":
            raise Exception("Errore simulato nella creazione del tag")

        # Successo simulato
            logging.info(f"Tag '{tag_name}' gestito con successo.")
        return jsonify({"status": "success", "message": f"Tag '{tag_name}' creato con successo"}), 200

    except Exception as e:
        # Loggare l'errore con il traceback completo
        logging.error("Errore durante la gestione della richiesta:")
        logging.error(traceback.format_exc())
        return jsonify({"status": "failed", "message": f"Errore nella gestione del webhook: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
