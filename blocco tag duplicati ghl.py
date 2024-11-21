import requests

# Configurazione delle credenziali API
API_BASE_URL = "https://rest.gohighlevel.com/v1"  # URL base dell'API
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6IlJ0S1NEcWU2OEFhZlZTQXpvRUtjIiwidmVyc2lvbiI6MSwiaWF0IjoxNzI3OTUwNzI0MTY4LCJzdWIiOiJQU3FJbXRuSDJvMTlnQkpqWlR3ZyJ9.SNTu5ocqIOF6Vvpd4QDyn4dpGxV_ojwLo-sdIhzsww0"  # Inserisci la tua chiave API

def get_existing_tags():
    """
    Recupera l'elenco dei tag esistenti tramite l'API.
    """
    url = f"{API_BASE_URL}/tags"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tags = response.json()
            return [tag['name'] for tag in tags.get('data', [])]
        else:
            print(f"Errore nel recupero dei tag: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        print(f"Errore durante la connessione all'API: {e}")
        return []

def create_tag(tag_name):
    """
    Crea un nuovo tag se non esiste già.
    """
    existing_tags = get_existing_tags()

    if tag_name in existing_tags:
        print(f"Il tag '{tag_name}' esiste già. Creazione annullata.")
        return {"status": "exists", "message": "Tag duplicato"}

    url = f"{API_BASE_URL}/tags"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"name": tag_name}

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Tag '{tag_name}' creato con successo!")
            return {"status": "success", "message": "Tag creato"}
        elif response.status_code == 422:  # Il tag esiste già secondo l'API
            print(f"Errore: Il tag '{tag_name}' esiste già. Messaggio: {response.json()}")
            return {"status": "exists", "message": response.json()}
        else:
            print(f"Errore nella creazione del tag: {response.status_code}, {response.text}")
            return {"status": "failed", "message": response.text}
    except Exception as e:
        print(f"Errore durante la connessione all'API: {e}")
        return {"status": "failed", "message": str(e)}

# Esempio di utilizzo
if __name__ == "__main__":
    # Sostituisci "Nuovo Tag" con il nome del tag desiderato
    nuovo_tag = "nuovo tag"
    risultato = create_tag(nuovo_tag)
    print(risultato)
