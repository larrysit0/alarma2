import os
from flask import Flask, request, jsonify, render_template

print("--- DEBUG: servidor.py: INICIO DEL SCRIPT ---")

app = Flask(__name__)

print("--- DEBUG: servidor.py: Instancia de Flask creada ---")

@app.route('/')
def index():
    print("--- DEBUG: Ruta / fue accedida. Sirviendo index.html. ---")
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register_id():
    data = request.json
    telegram_id = data.get('telegram_id')
    user_info = data.get('user_info', {})
    
    if telegram_id:
        print(f"--- DEBUG: ID de Telegram recibido: {telegram_id} ---")
        print(f"--- DEBUG: Información de usuario: {user_info} ---")
        # Aquí es donde verás el ID en los logs de Railway
        return jsonify({"status": "ID recibido y registrado."}), 200
    else:
        print("--- DEBUG: Error: No se recibió ID de Telegram. ---")
        return jsonify({"error": "ID no proporcionado"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"--- DEBUG: Iniciando servidor Flask en puerto {port} ---")
    app.run(host='0.0.0.0', port=port)
