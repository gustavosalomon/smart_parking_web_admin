import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Leer la URI desde variable de entorno (Render)
MONGO_URI = os.getenv("MONGO_URI")

# Conectar a tu base de datos
client = MongoClient(MONGO_URI)
db = client["smart_parking_web"]   # 👈 nombre de tu base
admins = db["admin"]               # 👈 nombre de la colección

@app.route("/api/admin/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    # Buscar usuario en la colección admin
    admin = admins.find_one({"username": username, "password": password})

    if admin:
        return jsonify({"success": True, "message": "Login exitoso"})
    else:
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "ok", "message": "Servicio de admin funcionando"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
