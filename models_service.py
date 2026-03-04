import os
from flask import Flask, jsonify, request

app = Flask(__name__)

MODELES = [
    {"id": "m1", "nom": "Aile-X", "pieces": ["p1"]}
]

INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "secret-token-123")

@app.route('/api/internal/used_pieces', methods=['GET'])
def obtenir_pieces_utilisees():
    en_tete_auth = request.headers.get("Authorization")
    
    if en_tete_auth != f"Bearer {INTERNAL_API_KEY}":
        return jsonify({"error": "Non autorisé"}), 401
        
    pieces_utilisees = set()
    for model in MODELES:
        pieces_utilisees.update(model["pieces"])
        
    return jsonify({"ids_pieces_utilisees": list(pieces_utilisees)}), 200

if __name__ == '__main__':
    app.run(port=5002)