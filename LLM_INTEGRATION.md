# 🤖 LLM Integration - Dokumentation

## Übersicht

Diese Dokumentation beschreibt die Integration des Gemini LLM in den Telefon-Agenten für automatische Terminbuchungen.

## 📋 Aktueller Status

### ✅ Implementiert:
- `AppointmentAgent` Klasse mit Gemini LLM
- Kontext-aware Prompts
- Conversation History Management
- Fallback-Mechanismen
- Test-Funktion

### ⚠️ Noch zu implementieren:
- Integration in `call_server.py`
- Request-Daten Übergabe via Twilio
- Supabase Integration für Request-Daten
- Summary zurück an Frontend

## 🏗️ Architektur

### Workflow:

```
Frontend (New Request)
    ↓
Backend (FastAPI) - POST /api/process-request
    ↓
start_call() mit request_id
    ↓
Twilio Call → webhook_url?request_id=xxx
    ↓
Flask Server - /start_conversation
    ↓
AppointmentAgent.set_context(request_data)
    ↓
AppointmentAgent.get_response() → Gemini LLM
    ↓
TTS (ElevenLabs) → Audio
    ↓
Twilio spielt Audio ab
    ↓
User spricht
    ↓
/gather → AppointmentAgent.get_response(user_input)
    ↓
... Konversation continues ...
    ↓
get_conversation_summary() → Zurück an Frontend
```

## 📝 AppointmentAgent Klasse

### Initialisierung:

```python
from llmcall_method.agent import AppointmentAgent

agent = AppointmentAgent()
```

### Kontext setzen:

```python
request_data = {
    'title': 'Arzttermin vereinbaren',
    'description': 'Allgemeine Untersuchung',
    'preferred_time': 'nächste Woche vormittags',
    'user_profile': {
        'username': 'Max Mustermann',
        'city': 'Berlin'
    }
}

agent.set_context(request_data)
```

### Konversation:

```python
# Erste Nachricht (Begrüßung)
greeting = agent.get_response()
print(greeting)
# → "Guten Tag! Hier spricht der Termin-Service..."

# User Antwort verarbeiten
response = agent.get_response("Ja, gerne.")
print(response)
# → "Wunderbar! Wir suchen einen Termin für..."

# Zusammenfassung erstellen
summary = agent.get_conversation_summary()
print(summary)
# → "Termin wurde vereinbart für Mittwoch, 14 Uhr..."
```

## 🔧 Integration in call_server.py

### Schritt 1: Import

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llmcall_method.agent import AppointmentAgent
from language_output.language_output import talk
```

### Schritt 2: Global Agent

```python
# Global agent instance (wird pro Call neu erstellt)
agents = {}  # request_id -> AppointmentAgent
```

### Schritt 3: /start_conversation updaten

```python
@app.route("/start_conversation", methods=['GET', 'POST'])
def start_conversation():
    """Start the conversation with LLM context."""
    
    # Hole request_id aus Query Params
    request_id = request.args.get('request_id')
    
    if not request_id:
        # Fallback ohne Kontext
        resp = VoiceResponse()
        resp.say("Guten Tag! Hier spricht der Termin-Service.")
        resp.append(build_gather())
        return str(resp)
    
    try:
        # Lade Request-Daten aus Supabase
        request_data = load_request_from_supabase(request_id)
        
        # Erstelle neuen Agent mit Kontext
        agent = AppointmentAgent()
        agent.set_context(request_data)
        agents[request_id] = agent
        
        # Generiere erste Nachricht
        greeting = agent.get_response()
        
        # TTS
        audio_file = talk(greeting)
        
        # Twilio Response
        resp = VoiceResponse()
        resp.play(f"/audio/{audio_file}")
        resp.append(build_gather())
        return str(resp)
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        # Fallback
        resp = VoiceResponse()
        resp.say("Entschuldigung, es gab ein technisches Problem.")
        return str(resp)
```

### Schritt 4: /gather updaten

```python
@app.route("/gather", methods=['GET', 'POST'])
def gather():
    """Process user reply with LLM."""
    
    request_id = request.args.get('request_id')
    user_input = request.values.get('SpeechResult', '').strip()
    
    if not user_input:
        # Kein Input
        resp = VoiceResponse()
        resp.append(build_gather("Ich habe Sie nicht verstanden. Könnten Sie das wiederholen?"))
        return str(resp)
    
    # Hole Agent für diesen Request
    agent = agents.get(request_id)
    
    if not agent:
        # Kein Agent gefunden - Fallback
        resp = VoiceResponse()
        resp.say("Entschuldigung, die Verbindung wurde unterbrochen.")
        return str(resp)
    
    try:
        # Generiere Antwort mit LLM
        agent_response = agent.get_response(user_input)
        
        # TTS
        audio_file = talk(agent_response)
        
        # Twilio Response
        resp = VoiceResponse()
        resp.play(f"/audio/{audio_file}")
        
        # Prüfe ob Gespräch beendet
        if "vielen dank" in agent_response.lower() or "auf wiedersehen" in agent_response.lower():
            # Gespräch beenden
            resp.hangup()
            
            # Summary erstellen und speichern
            summary = agent.get_conversation_summary()
            save_summary_to_supabase(request_id, summary)
            
            # Agent aufräumen
            del agents[request_id]
        else:
            # Konversation fortsetzen
            resp.append(build_gather())
        
        return str(resp)
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
        resp = VoiceResponse()
        resp.say("Entschuldigung, es gab ein Problem.")
        resp.hangup()
        return str(resp)
```

## 🗄️ Supabase Integration

### Request-Daten laden:

```python
from supabase import create_client
import os

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")  # Service Key für Backend!
)

def load_request_from_supabase(request_id: str) -> dict:
    """Lade Request-Daten aus Supabase"""
    
    # Request laden
    response = supabase.table('requests').select('*').eq('id', request_id).single().execute()
    request = response.data
    
    # User Profile laden
    profile_response = supabase.table('profiles').select('*').eq('user_id', request['user_id']).single().execute()
    profile = profile_response.data
    
    return {
        'title': request['title'],
        'description': request['description'],
        'preferred_time': request['preferred_time'],
        'user_profile': {
            'username': profile['username'],
            'city': profile['city']
        }
    }

def save_summary_to_supabase(request_id: str, summary: str):
    """Speichere Konversations-Summary in Supabase"""
    
    supabase.table('requests').update({
        'summary': summary,
        'status': 'booked',  # oder 'failed' je nach Summary
        'updated_at': 'now()'
    }).eq('id', request_id).execute()
    
    # Event erstellen
    supabase.table('events').insert({
        'request_id': request_id,
        'type': 'call_completed',
        'message': f'Call completed. {summary}'
    }).execute()
```

## 🔐 Environment Variables

Füge zu `.env` hinzu:

```env
# Gemini LLM
GOOGLE_API_KEY=your_gemini_api_key_here

# Supabase (für Backend)
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key_here

# ElevenLabs TTS
meinapitoken=your_elevenlabs_api_key

# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
TARGET_PHONE_NUMBER=target_number

# Public URL (ngrok/dev tunnel)
PUBLIC_BASE_URL=https://your-ngrok-url.ngrok.io
```

## 🧪 Testing

### Test 1: Agent direkt testen

```bash
cd llmcall_method
python agent.py
```

### Test 2: Mit Flask Server

```bash
# Terminal 1: Flask Server starten
cd twillio
python call_server.py

# Terminal 2: Test Call
python start_call.py
```

### Test 3: End-to-End

```bash
# 1. Backend starten
./start.sh

# 2. Ngrok starten
ngrok http 5001

# 3. PUBLIC_BASE_URL in .env setzen

# 4. Request im Frontend erstellen

# 5. Call wird automatisch gestartet
```

## 📊 Prompt Template Analyse

### ✅ Stärken:
- **Kontext-aware**: Nutzt Request-Daten
- **Strukturiert**: Klare Ziele und Regeln
- **Kurz**: Erzwingt präzise Antworten
- **Beispiele**: Few-shot learning
- **Fallbacks**: Error Handling

### 🔧 Verbesserungsmöglichkeiten:
1. **Multi-Language**: Deutsch/Englisch je nach User
2. **Tone Anpassung**: Formell/Informell je nach Kontext
3. **Domain-specific**: Arzt/Friseur/Restaurant Templates
4. **Learning**: Feedback Loop für bessere Prompts

## 🚀 Nächste Schritte

1. ✅ AppointmentAgent implementiert
2. ⏳ call_server.py Integration
3. ⏳ Supabase Helper Functions
4. ⏳ Request-ID Übergabe via Twilio
5. ⏳ Summary zurück an Frontend
6. ⏳ Testing & Debugging
7. ⏳ Production Deployment

## 📝 Notizen

- Gemini 2.0 Flash ist kostenlos und schnell
- Max 150 Tokens pro Response für kurze Antworten
- Temperature 0.7 für natürliche aber konsistente Antworten
- Conversation History auf 6 Nachrichten limitiert (Kontext-Fenster)
- Fallback-Mechanismen für Fehlerbehandlung

## 🐛 Known Issues

1. **Agent Cleanup**: Agents werden nicht automatisch gelöscht bei abgebrochenen Calls
2. **Concurrent Calls**: Keine Limitierung für gleichzeitige Calls
3. **Error Handling**: Mehr Logging nötig
4. **Testing**: Keine Unit Tests vorhanden

## 📚 Weitere Ressourcen

- [Gemini API Docs](https://ai.google.dev/docs)
- [Twilio Voice Docs](https://www.twilio.com/docs/voice)
- [ElevenLabs API](https://elevenlabs.io/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python)