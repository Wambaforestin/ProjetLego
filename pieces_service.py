import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

TOUTES_LES_PIECES = [
    {"id": "p1", "couleur": "rouge", "type": "brique 2x4"},
    {"id": "p2", "couleur": "bleu", "type": "brique 2x2"},
    {"id": "p3", "couleur": "jaune", "type": "plaque 1x1"}
]

MODELS_SERVICE_URL = os.getenv("MODELS_SERVICE_URL", "http://localhost:5002")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "secret-token-123")

@app.route('/pieces/available', methods=['GET'])
def obtenir_pieces_disponibles():
    en_tetes = {"Authorization": f"Bearer {INTERNAL_API_KEY}"}
    response = requests.get(f"{MODELS_SERVICE_URL}/api/internal/used_pieces", headers=en_tetes)
    
    if response.status_code != 200:
        return jsonify({"error": "Service models indisponible"}), 502
        
    used_ids = response.json().get("ids_pieces_utilisees", [])
    pieces_disponibles = [p for p in TOUTES_LES_PIECES if p["id"] not in used_ids]
    
    return jsonify(pieces_disponibles), 200

if __name__ == '__main__':
    app.run(port=5001)