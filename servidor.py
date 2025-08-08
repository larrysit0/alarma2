import os
import requests
import json
from flask import Flask, request, jsonify, render_template

print("--- DEBUG: servidor.py: INICIO DEL SCRIPT ---")

app = Flask(__name__)

# 🔐 TOKEN del bot (configurado como variable de entorno en Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    print("--- DEBUG: Update de Telegram recibido:", json.dumps(update, indent=2))
    
    message = update.get('message')
    if message:
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text.startswith('/registrar') or text.startswith('/obtener_id'):
            print(f"--- DEBUG: Comando detectado: '{text}' en chat_id: {chat_id} ---")
            
            # URL de tu web app de registro en Railway
            webapp_url = "https://alarma2-production.up.railway.app"
            
            payload = {
                "chat_id": chat_id,
                "text": "Presiona el botón para obtener tu ID de Telegram.",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {
                                "text": "Obtener mi ID",
                                "web_app": { "url": webapp_url }
                            }
                        ]
                    ]
                }
            }
            
            send_telegram_message(chat_id, payload)
    
    return jsonify({"status": "ok"}), 200

@app.route('/api/register', methods=['POST'])
def register_id():
    data = request.json
    telegram_id = data.get('telegram_id')
    user_info = data.get('user_info', {})
    
    if telegram_id:
        print(f"--- DEBUG: ID de Telegram recibido: {telegram_id} ---")
        print(f"--- DEBUG: Información de usuario: {user_info} ---")
        return jsonify({"status": "ID recibido y registrado."}), 200
    else:
        print("--- DEBUG: Error: No se recibió ID de Telegram. ---")
        return jsonify({"error": "ID no proporcionado"}), 400

def send_telegram_message(chat_id, payload):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"--- DEBUG: Mensaje enviado exitosamente a {chat_id} (Telegram). ---")
    except requests.exceptions.RequestException as e:
        print(f"--- DEBUG: ERROR al enviar mensaje a Telegram {chat_id}: {e} ---")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
