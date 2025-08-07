import os
import requests
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

print("--- DEBUG: servidor.py: INICIO DEL SCRIPT ---")

app = Flask(__name__, static_folder='static')
CORS(app)

print("--- DEBUG: servidor.py: Instancia de Flask creada ---")

# 🔐 TOKEN del bot (configurado como variable de entorno en Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    print("--- DEBUG: ADVERTENCIA: TELEGRAM_BOT_TOKEN NO está configurado. Esto podría causar problemas. ---")
else:
    print("--- DEBUG: TELEGRAM_BOT_TOKEN detectado. ---")

COMUNIDADES_DIR = 'comunidades'
print(f"--- DEBUG: COMUNIDADES_DIR establecida a: {COMUNIDADES_DIR} ---")


@app.route('/healthz')
def health_check():
    print("--- DEBUG: Ruta /healthz fue accedida. Retornando OK. ---")
    return "OK", 200


@app.route('/')
def index():
    print("--- DEBUG: Ruta / fue accedida. Sirviendo index.html. ---")
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    print(f"--- DEBUG: Ruta /static/{filename} fue accedida. ---")
    return send_from_directory(app.static_folder, filename)


def load_community_json(comunidad_nombre):
    print(f"--- DEBUG: Intentando cargar JSON para la comunidad: {comunidad_nombre} ---")
    filepath = os.path.join(COMUNIDADES_DIR, f"{comunidad_nombre.lower()}.json")
    if not os.path.exists(filepath):
        print(f"--- DEBUG: Archivo JSON NO encontrado: {filepath} ---")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            comunidad_info = json.load(f)
            print(f"--- DEBUG: JSON para '{comunidad_nombre}' cargado exitosamente desde '{filepath}'. ---")
            return comunidad_info
    except json.JSONDecodeError as e:
        print(f"--- DEBUG: ERROR JSONDecodeError para '{filepath}': {e} ---")
        return None
    except Exception as e:
        print(f"--- DEBUG: ERROR General al cargar '{filepath}': {e} ---")
        return None


@app.route('/api/comunidad/<comunidad>', methods=['GET'])
def get_comunidad_data(comunidad):
    print(f"--- DEBUG: Ruta /api/comunidad/{comunidad} fue accedida. ---")
    comunidad_info = load_community_json(comunidad)
    if comunidad_info:
        return jsonify(comunidad_info)
    return jsonify({}), 404


@app.route('/api/alert', methods=['POST'])
def handle_alert():
    print("--- DEBUG: Ruta /api/alert fue accedida (POST). ---")
    data = request.json
    print("--- DEBUG: Datos recibidos para la alerta:", data)

    comunidad_nombre = data.get("comunidad")
    mensaje = data.get("mensaje")

    if not comunidad_nombre or not mensaje:
        print("--- DEBUG: Faltan datos en la alerta. ---")
        return jsonify({"error": "Faltan datos"}), 400

    comunidad_info = load_community_json(comunidad_nombre)
    if not comunidad_info:
        print("--- DEBUG: Comunidad no encontrada. ---")
        return jsonify({"error": "Comunidad no encontrada"}), 404

    chat_id = comunidad_info.get("chat_id")
    if not chat_id:
        print("--- DEBUG: chat_id no encontrado en el JSON. ---")
        return jsonify({"error": "chat_id no encontrado"}), 400

    send_telegram_message(chat_id, mensaje)

    print(f"--- DEBUG: Finalizando handle_alert. Status: Alerta enviada a la comunidad {comunidad_nombre} ---")
    return jsonify({"status": f"Alerta enviada a la comunidad {comunidad_nombre}"})


def send_telegram_message(chat_id, text, parse_mode='HTML'):
    print(f"--- DEBUG: Intentando enviar mensaje a Telegram para chat_id: {chat_id} ---")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"--- DEBUG: Mensaje enviado exitosamente a {chat_id} (Telegram). ---")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- DEBUG: ERROR al enviar mensaje a Telegram {chat_id}: {e} ---")
        return None


# 💡 ESTA PARTE ES CLAVE PARA RAILWAY
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto que Railway asigna
    print(f"--- DEBUG: Iniciando servidor Flask en puerto {port} ---")
    app.run(host='0.0.0.0', port=port)
