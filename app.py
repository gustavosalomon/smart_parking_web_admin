import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexión a Mongo Atlas
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["smart_parking_web"]  # Nombre de la DB
admins = db["admin"]   # Colección

@app.route("/api/admin/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    admin = admins.find_one({"username": username, "password": password})
    
    if admin:
        return jsonify({"success": True, "message": "Login exitoso"})
    else:
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401


@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "ok", "message": "Servicio de admin funcionando"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
