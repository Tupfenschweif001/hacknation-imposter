g# 🔌 Backend API Specification

## Übersicht

Das Frontend sendet Requests an das Backend, welches die Voice-AI-Anrufe durchführt und die Datenbank aktualisiert.

## 🎯 Architektur

```
Frontend (Next.js)
    ↓ 1. Speichert Request in Supabase
    ↓ 2. Sendet JSON an Backend
Backend (Python/FastAPI)
    ↓ 3. Prüft Öffnungszeiten
    ↓ 4. Führt Anruf aus
    ↓ 5. Aktualisiert Supabase
Frontend
    ↓ 6. Pollt Supabase für Updates
```

## 📡 API Endpoints

### **POST /api/process-request**

Verarbeitet einen neuen Request und startet den Voice-AI-Anruf.

#### Request Body:
```json
{
  "request_id": "uuid-string",
  "user_id": "uuid-string",
  "title": "Zahnarzttermin buchen",
  "description": "Ich brauche einen Termin für eine Zahnreinigung",
  "callback_number": "+49 123 456789",
  "number_to_call": "+49 987 654321",
  "preferred_time": "nächste Woche, Montag 10-12 Uhr",
  "user_profile": {
    "username": "Max Mustermann",
    "street": "Musterstraße",
    "house_number": "123",
    "postal_code": "12345",
    "city": "Berlin",
    "country": "Germany"
  }
}
```

#### Response (Sofort):
```json
{
  "status": "accepted",
  "request_id": "uuid-string",
  "message": "Request is being processed"
}
```

#### Response (Bei Fehler):
```json
{
  "status": "error",
  "request_id": "uuid-string",
  "error": "Error message"
}
```

## 🔄 Status-Flow

Das Backend aktualisiert den Status in Supabase während der Verarbeitung:

### 1. **queued** (Initial)
- Request wurde erstellt
- Wartet auf Verarbeitung

### 2. **outside_business_hours**
- Außerhalb Geschäftszeiten (Mo-Fr 08:00-18:00)
- Wird für nächsten Werktag geplant

### 3. **calling**
- Anruf wird gerade durchgeführt
- Voice-AI ist aktiv

### 4. **in_progress**
- Gespräch läuft
- Termin wird gebucht

### 5. **waiting_for_callback**
- Anruf fehlgeschlagen
- Wartet auf Rückruf

### 6. **booked** (Erfolg)
- Termin erfolgreich gebucht
- Summary enthält Details

### 7. **failed** (Fehler)
- Anruf fehlgeschlagen
- Grund in Events gespeichert

### 8. **canceled**
- User hat abgebrochen

## 📝 Events

Das Backend loggt Events während der Verarbeitung:

```json
{
  "request_id": "uuid",
  "type": "call_started",
  "message": "Voice AI started calling +49 987 654321"
}
```

### Event-Types:
- `request_received` - Request vom Frontend empfangen
- `scheduled` - Für später geplant (außerhalb Öffnungszeiten)
- `call_started` - Anruf gestartet
- `call_connected` - Verbindung hergestellt
- `booking_in_progress` - Termin wird gebucht
- `booking_confirmed` - Termin bestätigt
- `call_failed` - Anruf fehlgeschlagen
- `call_completed` - Anruf abgeschlossen

## 🕐 Öffnungszeiten-Check

```python
def is_business_hours():
    """
    Prüft ob aktuell Geschäftszeiten sind.
    Montag-Freitag, 08:00-18:00 Uhr
    """
    now = datetime.now()
    
    # Wochenende
    if now.weekday() >= 5:  # 5=Samstag, 6=Sonntag
        return False
    
    # Außerhalb 08:00-18:00
    if now.hour < 8 or now.hour >= 18:
        return False
    
    return True
```

## 🔐 Authentifizierung

Das Backend sollte die Requests authentifizieren:

```python
from fastapi import Header, HTTPException

async def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing authorization header")
    
    # Supabase JWT Token verifizieren
    token = authorization.replace("Bearer ", "")
    # ... Token-Validierung
```

## 📊 Supabase Updates

Das Backend aktualisiert Supabase direkt:

### Status Update:
```python
supabase.table('requests').update({
    'status': 'calling',
    'updated_at': datetime.now().isoformat()
}).eq('id', request_id).execute()
```

### Event hinzufügen:
```python
supabase.table('events').insert({
    'request_id': request_id,
    'type': 'call_started',
    'message': 'Voice AI started calling...',
    'created_at': datetime.now().isoformat()
}).execute()
```

### Summary speichern:
```python
supabase.table('requests').update({
    'status': 'booked',
    'summary': 'Termin gebucht für Montag, 10:00 Uhr bei Dr. Müller',
    'updated_at': datetime.now().isoformat()
}).eq('id', request_id).execute()
```

## 🚀 Beispiel Backend-Implementierung (Python/FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase import create_client
import os

app = FastAPI()

# Supabase Client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")  # Service Key für Backend!
)

class RequestData(BaseModel):
    request_id: str
    user_id: str
    title: str
    description: str
    callback_number: str
    number_to_call: str | None
    preferred_time: str
    user_profile: dict

@app.post("/api/process-request")
async def process_request(data: RequestData):
    try:
        # 1. Event loggen
        add_event(data.request_id, 'request_received', 
                 f'Request received: {data.title}')
        
        # 2. Öffnungszeiten prüfen
        if not is_business_hours():
            update_status(data.request_id, 'outside_business_hours')
            add_event(data.request_id, 'scheduled',
                     'Scheduled for next business day at 08:00')
            return {"status": "scheduled", "request_id": data.request_id}
        
        # 3. Anruf starten (asynchron)
        update_status(data.request_id, 'calling')
        add_event(data.request_id, 'call_started',
                 f'Calling {data.number_to_call or "practice"}')
        
        # 4. Voice-AI aufrufen (hier deine AI-Integration)
        result = await call_voice_ai(data)
        
        # 5. Ergebnis speichern
        if result['success']:
            update_status(data.request_id, 'booked')
            save_summary(data.request_id, result['summary'])
            add_event(data.request_id, 'booking_confirmed',
                     'Appointment successfully booked')
        else:
            update_status(data.request_id, 'failed')
            add_event(data.request_id, 'call_failed',
                     result['error'])
        
        return {"status": "completed", "request_id": data.request_id}
        
    except Exception as e:
        update_status(data.request_id, 'failed')
        add_event(data.request_id, 'error', str(e))
        raise HTTPException(500, str(e))

def is_business_hours():
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    if now.hour < 8 or now.hour >= 18:
        return False
    return True

def update_status(request_id: str, status: str):
    supabase.table('requests').update({
        'status': status,
        'updated_at': datetime.now().isoformat()
    }).eq('id', request_id).execute()

def add_event(request_id: str, event_type: str, message: str):
    supabase.table('events').insert({
        'request_id': request_id,
        'type': event_type,
        'message': message
    }).execute()

def save_summary(request_id: str, summary: str):
    supabase.table('requests').update({
        'summary': summary
    }).eq('id', request_id).execute()

async def call_voice_ai(data: RequestData):
    # Hier deine Voice-AI Integration
    # z.B. OpenAI Realtime API, Twilio, etc.
    pass
```

## 🧪 Testing

### Mit curl:
```bash
curl -X POST http://localhost:8000/api/process-request \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "test-uuid",
    "user_id": "user-uuid",
    "title": "Test Request",
    "description": "Test",
    "callback_number": "+49 123 456789",
    "number_to_call": "+49 987 654321",
    "preferred_time": "ASAP",
    "user_profile": {
      "username": "Test User",
      "city": "Berlin"
    }
  }'
```

## 📦 Environment Variables

Backend benötigt:
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGc...  # Service Role Key!
OPENAI_API_KEY=sk-...  # Für Voice-AI
PORT=8000
```

## 🔒 Security

⚠️ **Wichtig:**
- Backend nutzt **Service Role Key** (nicht anon key!)
- Service Key hat volle DB-Rechte
- Niemals im Frontend verwenden!
- Nur auf Backend-Server

## 📚 Nächste Schritte

1. Backend-Server aufsetzen (Python/FastAPI)
2. Voice-AI Integration implementieren
3. Frontend anpassen (Request ans Backend senden)
4. Testing & Deployment