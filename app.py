from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Conexión a Mongo Atlas
client = MongoClient("mongodb+srv://admin:admin123@cluster0.2owahcw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["adminDB"]  # Nombre de la DB
admins = db["admins"]   # Colección

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
