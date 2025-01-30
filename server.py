import os
from flask import Flask, request, jsonify
from twilio.rest import Client
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

app = Flask(__name__)

# Credenziali Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Messaggio di risposta automatica
AUTO_REPLY_MESSAGE = ("Grazie per averci scritto!\n"
                      "Purtroppo questo numero non è abilitato alla ricezione di messaggi e non abbiamo modo di leggere quello che ci hai scritto\n"
                      "\n"
                      "Per ricevere assistenza, contattaci tramite:\n"
                      "\n"
                      "📧 assistenza@grelli.it\n"
                      "\n"
                      "📲 +39 3791988758\n"
                      "\n"
                      "📞 +39 0758040747\n"
                      "\n"
                      "Grazie mille,\n" 
                      "\n"
                      "*Ferramenta Grelli*")


# 📩 Webhook per ricevere messaggi WhatsApp
@app.route('/whatsapp_webhook', methods=['POST'])
def whatsapp_webhook():
    # Twilio invia i dati in formato application/x-www-form-urlencoded
    sender_number = request.form.get('From', '').replace('whatsapp:', '')
    received_message = request.form.get('Body', '')

    print(f"📩 Messaggio ricevuto da {sender_number}: {received_message}")

    if sender_number:
        try:
            # Invia la risposta automatica
            message = twilio_client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=f'whatsapp:{sender_number}',
                body=AUTO_REPLY_MESSAGE
            )
            print(f"✅ Risposta inviata a {sender_number}: {AUTO_REPLY_MESSAGE}")
        except Exception as e:
            print(f"❌ Errore nell'invio del messaggio: {e}")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002, debug=True)
