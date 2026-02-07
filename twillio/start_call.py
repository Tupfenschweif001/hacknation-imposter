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
webhook_url = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:5001").strip().rstrip('/')

# Sicherstellen, dass die Route stimmt
if not webhook_url.endswith('/voice'):
    webhook_url = f"{webhook_url}/voice"




def start_call(number=None):
    to_number = number or os.getenv('TARGET_PHONE_NUMBER')
    if not to_number:
        raise ValueError("TARGET_PHONE_NUMBER ist nicht gesetzt und keine Nummer wurde übergeben.")

    call = client.calls.create(
        # Wohin soll angerufen werden? (Muss im Trial-Modus verifiziert sein!)
        to=to_number,
        # Von welcher Nummer kommt der Anruf? (Deine Twilio-Nummer)
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        # Hier sagen wir Twilio: "Lade deine Anweisungen von dieser URL"
        url=webhook_url
    )

    print(f"Anruf gestartet! SID: {call.sid}")
    return call


if __name__ == "__main__":
    start_call()





