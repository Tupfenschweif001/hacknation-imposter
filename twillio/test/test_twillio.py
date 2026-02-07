import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# 1. Deine Zugangsdaten aus Umgebungsvariablen
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# 2. Der Anruf starten
# Damit Twilio mit deinem lokalen Server sprechen kann, brauchen wir die öffentliche URL (Dev Tunnel/Ngrok).
webhook_url = "https://v1h02wnp-5001.euw.devtunnels.ms".strip().rstrip('/')

# Sicherstellen, dass die Route stimmt
if not webhook_url.endswith('/voice'):
    webhook_url = f"{webhook_url}/voice"

print(f"Verwende Webhook URL: {webhook_url}")

call = client.calls.create(
    # Wohin soll angerufen werden? (Muss im Trial-Modus verifiziert sein!)
    to=os.getenv('TARGET_PHONE_NUMBER'), 
    
    # Von welcher Nummer kommt der Anruf? (Deine Twilio-Nummer)
    from_=os.getenv('TWILIO_PHONE_NUMBER'), 
    
    # Hier sagen wir Twilio: "Lade deine Anweisungen von dieser URL"
    url=webhook_url
)

print(f"Anruf gestartet! SID: {call.sid}")