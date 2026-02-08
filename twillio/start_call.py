import os
import urllib.parse
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




def start_call(number=None, request_id=None, title=None, description=None):
    to_number = os.getenv('TARGET_PHONE_NUMBER')
    if not to_number:
        raise ValueError("TARGET_PHONE_NUMBER ist nicht gesetzt und keine Nummer wurde übergeben.")

    # Parameter vorbereiten
    params = {}
    if request_id:
        params['request_id'] = request_id
    if title:
        params['title'] = title
    if description:
        # Achtung: Zu lange Beschreibungen können die URL-Länge sprengen!
        params['description'] = description

    # URL zusammenbauen
    call_url = webhook_url
    if params:
        # urlencode kümmert sich um Sonderzeichen (Leerzeichen -> %20 etc.)
        query_string = urllib.parse.urlencode(params)
        call_url = f"{webhook_url}?{query_string}"

    call = client.calls.create(
        # Wohin soll angerufen werden? (Muss im Trial-Modus verifiziert sein!)
        to=to_number,
        # Von welcher Nummer kommt der Anruf? (Deine Twilio-Nummer)
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        # Hier sagen wir Twilio: "Lade deine Anweisungen von dieser URL"
        url=call_url
    )

    print(f"Anruf gestartet! SID: {call.sid}")
    return call


if __name__ == "__main__":
    # Test request_id mit Daten
    start_call(
        request_id="test_request_id",
        title="Heizung kaputt",
        description="Wasser läuft aus dem Heizkörper im Wohnzimmer."
    )





