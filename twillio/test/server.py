from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Start des Anrufs"""
    print("📞 ANRUF EMPFANGEN: Twilio hat angeklopft!")
    resp = VoiceResponse()

    # Gather 'speech' aktiviert die Spracherkennung
    # language='de-DE' sorgt dafür, dass Deutsch verstanden wird
    # action='/gather' sagt Twilio, wohin das Ergebnis gesendet werden soll
    gather = Gather(
        input='speech dtmf',
        action='/gather',
        language='de-DE',
        timeout=10,
        speech_timeout='auto',
        action_on_empty_result=True,
        num_digits=1
    )
    
    gather.say("Hallo! Dies ist der Termin-Assistent. Bitte sprich jetzt oder druecke eine Taste. Wann moechtest du einen Termin vereinbaren?", language='de-DE')
    
    resp.append(gather)
    
    # Fallback, falls nichts gesagt wurde
    resp.say("Ich habe leider nichts gehört. Auf Wiedersehen.", language='de-DE')
    return str(resp)

@app.route("/gather", methods=['GET', 'POST'])
def gather():
    """Verarbeitung der Antwort"""
    resp = VoiceResponse()
    print(f"📥 /gather params: {dict(request.values)}")
    
    # Das gesprochene Wort kommt hier an
    user_input = request.values.get('SpeechResult', '').lower()
    digits = request.values.get('Digits', '').strip()
    print(f"🗣️ SpeechResult: {user_input!r}")
    
    if user_input:
        # Hier würde normalerweise deine KI-Logik (OpenAI, etc.) stehen
        resp.say(f"Du hast gesagt: {user_input}. Ich schaue nach, ob das passt.", language='de-DE')
        resp.say("Das sieht gut aus. Der Termin ist notiert.", language='de-DE')
    elif digits:
        resp.say(f"Taste {digits} erkannt. Bitte sprich jetzt deinen Wunschtermin.", language='de-DE')
        resp.redirect('/voice')
    else:
        resp.say("Ich habe dich nicht verstanden.", language='de-DE')
        resp.redirect('/voice') # Versuche es nochmal

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
