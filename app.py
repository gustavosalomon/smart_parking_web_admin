import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Leer la URI desde variable de entorno
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError(
        "ERROR: Debes definir la variable de entorno MONGO_URI en Render.\n"
        "Ej: mongodb+srv://admin:admin123@cluster0.2owahcw.mongodb.net/?retryWrites=true&w=majority"
    )

# Conectar a MongoDB Atlas
try:
    client = MongoClient(MONGO_URI)
    db = client["smart_parking_web"]  # tu base de datos
    admins = db["admin"]              # tu colección
    print("✅ Conexión a MongoDB Atlas exitosa")
except Exception as e:
    print("❌ Error conectando a MongoDB Atlas:", e)
    raise

@app.route("/api/admin/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
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
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Servidor arrancando en puerto {port}")
    app.run(host="0.0.0.0", port=port)
