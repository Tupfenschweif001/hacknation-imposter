# 📱 Voice AI Agent - Projekt Dokumentation

## 🎯 Projekt Übersicht

**Name:** Hacknation Imposter - Voice AI Appointment Booking Agent

**Zweck:** Automatisierte Terminbuchung via Telefon mit KI-gestütztem Agenten

**Entwicklungszeit:** 24h Hackathon

**Status:** MVP / Demo-Version

---

## 🏗️ System Architektur

### Tech Stack

#### Frontend
- **Framework:** Next.js 15 (App Router)
- **UI Library:** React 19
- **Styling:** TailwindCSS + shadcn/ui
- **Sprache:** TypeScript
- **Icons:** lucide-react
- **Notifications:** Sonner (Toast)

#### Backend
- **API Server:** FastAPI (Python)
- **Call Server:** Flask (Python)
- **Datenbank:** Supabase (PostgreSQL)
- **Authentication:** Supabase Auth

#### AI Services
- **LLM:** Google Gemini 2.0 Flash
  - Contact Search
  - Conversation Agent
- **TTS:** ElevenLabs
- **Telephony:** Twilio Voice API

---

## 📊 Datenmodell

### Supabase Tabellen

#### `profiles`
```sql
CREATE TABLE profiles (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id),
  username TEXT,
  default_callback_number TEXT,
  street TEXT,
  house_number TEXT,
  postal_code TEXT,
  city TEXT,
  country TEXT DEFAULT 'Germany',
  calendar_connected BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `requests`
```sql
CREATE TABLE requests (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  callback_number TEXT,
  number_to_call TEXT,
  preferred_time TEXT NOT NULL,
  status TEXT DEFAULT 'queued',
  summary TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Status Werte:**
- `queued` - Wartet auf Bearbeitung
- `outside_business_hours` - Außerhalb Geschäftszeiten
- `calling` - Anruf läuft
- `in_progress` - In Bearbeitung
- `waiting_for_callback` - Wartet auf Rückruf
- `booked` - Termin gebucht
- `failed` - Fehlgeschlagen
- `canceled` - Abgebrochen

#### `events`
```sql
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  request_id UUID REFERENCES requests(id),
  type TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🔄 User Flow

### 1. Registrierung & Login
```
User → /register → Email + Passwort
     → Supabase Auth
     → /dashboard
```

### 2. Profil einrichten
```
User → /profile
     → Adresse eingeben (Straße, PLZ, Stadt)
     → Callback Nummer
     → Speichern
```

### 3. Neuen Request erstellen

#### Option A: Mit Contact Search (NEU!)
```
User → /new
     → Title: "Zahnarzt Termin"
     → Description: "Zahnreinigung"
     → Radius: 10 km
     → "Find Contacts Nearby"
     
Backend:
     → Lädt User Profile (Adresse)
     → Gemini API: Suche Zahnarztpraxen in 10km
     → Gibt 10 Vorschläge zurück
     
Frontend:
     → Modal mit Kontakten
     → User wählt Praxis
     → "Start Call with Dr. Müller"
     
     → Request wird erstellt
     → Call startet automatisch
```

#### Option B: Manuelle Nummer
```
User → /new
     → Füllt Form aus
     → Gibt Telefonnummer manuell ein
     → "Create Request"
     → Call startet
```

### 4. Request Tracking
```
User → /dashboard
     → Sieht Kanban Board:
        - Open (queued)
        - In Progress (calling)
        - Completed (booked/failed)
     
     → Klickt auf Request
     → /requests/:id
     → Sieht Details + Timeline
     → Auto-refresh alle 2-3 Sekunden
```

---

## 🤖 AI Agent Workflow

### Contact Search (Gemini)

**Input:**
- User Adresse (Straße, PLZ, Stadt)
- Description (z.B. "Zahnarzt Termin")
- Radius (5/10/20 km)

**Prompt:**
```
Gebe in einem JSON Format die 10 [Service-Typ] zurück,
die von der Entfernung am kürzesten von [Straße] in [PLZ]
entfernt sind (maximal [Radius] km).

Format:
[
  {"name": "Praxis Dr. Müller", "telefonnummer": "0721 123456"},
  ...
]
```

**Output:**
```json
[
  {
    "name": "Dr. Müller Zahnarztpraxis",
    "telefonnummer": "0721 123456"
  },
  {
    "name": "Praxis Dr. Schmidt",
    "telefonnummer": "0721 234567"
  }
]
```

### Conversation Agent (Gemini)

**System Prompt:**
```
Du bist ein freundlicher, professioneller Telefon-Assistent.

AUFGABE: [Request Title]
DETAILS: [Request Description]
ZEIT: [Preferred Time]

ZIEL:
1. Begrüße höflich
2. Erkläre Grund des Anrufs
3. Frage nach verfügbaren Terminen
4. Notiere Termin
5. Bedanke dich

REGELN:
- Maximal 2-3 kurze Sätze
- Nur EINE Frage pro Antwort
- Natürlich und freundlich
```

**Conversation Flow:**
```
Agent: "Guten Tag! Hier spricht der Termin-Service. 
        Ich rufe an, um einen Zahnarzttermin zu vereinbaren."

User: "Ja, gerne."

Agent: "Wunderbar! Wir suchen einen Termin für nächste Woche. 
        Welche Tage hätten Sie verfügbar?"

User: "Mittwoch um 14 Uhr."

Agent: "Perfekt! Mittwoch, 14 Uhr ist notiert. 
        Vielen Dank und einen schönen Tag!"
```

---

## 🔧 API Endpoints

### Backend (FastAPI - Port 8000)

#### `POST /api/get-contact-suggestions`
**Beschreibung:** Findet Kontakte in der Nähe

**Request:**
```json
{
  "user_id": "uuid",
  "description": "Zahnarzt Termin",
  "radius_km": 10
}
```

**Response:**
```json
{
  "success": true,
  "contacts": [
    {
      "name": "Dr. Müller Zahnarztpraxis",
      "telefonnummer": "0721 123456"
    }
  ],
  "metadata": {
    "location": "Hauptstraße 12a, 85044 Ingolstadt",
    "radius_km": 10,
    "count": 10
  }
}
```

#### `POST /api/process-request`
**Beschreibung:** Erstellt Request und startet Call

**Request:**
```json
{
  "request_id": "uuid",
  "user_id": "uuid",
  "title": "Zahnarzt Termin",
  "description": "Zahnreinigung",
  "callback_number": "+49 123 456789",
  "number_to_call": "0721 123456",
  "preferred_time": "nächste Woche",
  "user_profile": {
    "username": "Max Mustermann",
    "street": "Hauptstraße",
    "postal_code": "85044",
    "city": "Ingolstadt"
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "request_id": "uuid"
}
```

### Call Server (Flask - Port 5001)

#### `GET /start_conversation?request_id=xxx`
**Beschreibung:** Twilio Webhook - Startet Konversation

#### `POST /gather?request_id=xxx`
**Beschreibung:** Twilio Webhook - Verarbeitet User Input

---

## 🚀 Setup & Installation

### Voraussetzungen
- Node.js 18+
- Python 3.9+
- Supabase Account
- Google AI Studio Account (Gemini)
- ElevenLabs Account
- Twilio Account

### Installation

#### 1. Repository klonen
```bash
git clone https://github.com/Tupfenschweif001/hacknation-imposter.git
cd hacknation-imposter
```

#### 2. Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### 3. Frontend Dependencies
```bash
cd frontend
npm install
```

#### 4. Environment Variables

**Root `.env`:**
```env
# Gemini LLM
GOOGLE_API_KEY=your_gemini_api_key

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...

# ElevenLabs TTS
meinapitoken=your_elevenlabs_key

# Twilio
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+49xxx
TARGET_PHONE_NUMBER=+49xxx

# Public URL (ngrok)
PUBLIC_BASE_URL=https://xxx.ngrok.io
```

**Frontend `.env.local`:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

#### 5. Supabase Setup

**Tabellen erstellen:**
```sql
-- Siehe Datenmodell oben
```

**RLS Policies:**
```sql
-- profiles: Allow read for all
CREATE POLICY "Allow users to read all profiles"
ON profiles FOR SELECT
TO authenticated, anon
USING (true);

-- requests: Allow users to read own requests
CREATE POLICY "Users can read own requests"
ON requests FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

-- requests: Allow users to insert own requests
CREATE POLICY "Users can insert own requests"
ON requests FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);
```

#### 6. Starten

**Option A: Alles auf einmal**
```bash
./start.sh
```

**Option B: Manuell**
```bash
# Terminal 1: Backend
source .venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Call Server (optional)
source .venv/bin/activate
cd twillio
python call_server.py

# Terminal 4: Ngrok (für Twilio)
ngrok http 5001
```

---

## 🧪 Testing

### 1. Contact Search testen
```bash
cd llmcall_method
python callgemini.py
```

### 2. Backend API testen
```bash
curl -X POST http://localhost:8000/api/get-contact-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your-user-id",
    "description": "Zahnarzt Termin",
    "radius_km": 10
  }'
```

### 3. Frontend testen
```
1. http://localhost:3000/register
2. Registrieren
3. /profile → Adresse eingeben
4. /new → "Find Contacts" testen
```

---

## 🐛 Troubleshooting

### Problem: "Profile not found"
**Lösung:**
1. Prüfe RLS Policies in Supabase
2. Füge Policy hinzu: `using (true)`
3. Backend neu starten

### Problem: "Supabase URL not set"
**Lösung:**
1. Prüfe `.env` im Root
2. Backend neu starten
3. Env Vars mit `cat .env | grep SUPABASE` prüfen

### Problem: Hydration Error
**Lösung:**
- Bereits gefixt in `contact-suggestions-modal.tsx`
- `<div>` nicht in `<DialogDescription>` verschachteln

### Problem: Gemini API Error
**Lösung:**
1. Prüfe `GOOGLE_API_KEY` in `.env`
2. Prüfe API Quota in Google AI Studio
3. Teste mit `python callgemini.py`

---

## 📈 Performance

### Gemini API
- **Model:** gemini-2.0-flash-exp
- **Kosten:** Kostenlos (bis Limit)
- **Response Time:** ~2-5 Sekunden
- **Max Tokens:** 150 (für kurze Antworten)

### Contact Search
- **Durchschnitt:** 3-5 Sekunden
- **Caching:** Nicht implementiert
- **Optimierung:** Möglich durch Caching häufiger Suchen

### Frontend
- **Build:** Next.js Production Build
- **Deployment:** Vercel empfohlen
- **Performance:** Lighthouse Score 90+

---

## 🔐 Sicherheit

### Implementiert
- ✅ Supabase Auth (Email + Passwort)
- ✅ RLS Policies
- ✅ Environment Variables
- ✅ HTTPS (Production)

### TODO
- ⏳ Rate Limiting
- ⏳ Input Validation (Backend)
- ⏳ CSRF Protection
- ⏳ API Key Rotation

---

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway/Render)
```bash
# Dockerfile erstellen
# Railway/Render verbinden
# Environment Variables setzen
```

### Supabase
- Bereits in Cloud
- Production URL verwenden

---

## 📝 Bekannte Limitierungen

1. **Polling statt Websockets**
   - Status Updates alle 2-3 Sekunden
   - Nicht real-time

2. **Keine Concurrent Calls**
   - Ein Call pro Request
   - Keine Warteschlange

3. **Gemini Halluzinationen**
   - Kontakte können erfunden sein
   - Telefonnummern nicht verifiziert

4. **Keine Kalender Integration**
   - Nur UI Placeholder
   - Google Calendar TODO

5. **Development Only**
   - Nicht production-ready
   - Keine Tests

---

## 🎯 Roadmap

### Phase 1 (MVP) ✅
- [x] Frontend UI
- [x] Contact Search
- [x] Basic Call Flow
- [x] Supabase Integration

### Phase 2 (Verbesserungen)
- [ ] Websockets für Real-time Updates
- [ ] Kalender Integration
- [ ] Multi-Language Support
- [ ] Voice Recognition (STT)

### Phase 3 (Production)
- [ ] Unit Tests
- [ ] E2E Tests
- [ ] Error Monitoring (Sentry)
- [ ] Analytics
- [ ] Rate Limiting
- [ ] Caching

---

## 👥 Team

**Entwickler:** [Dein Name]

**Hackathon:** Hacknation 2026

**Zeitraum:** 24 Stunden

---

## 📄 Lizenz

MIT License

---

## 🙏 Credits

- **Next.js** - React Framework
- **Supabase** - Backend as a Service
- **Google Gemini** - LLM
- **ElevenLabs** - Text-to-Speech
- **Twilio** - Voice API
- **shadcn/ui** - UI Components

---

**Erstellt:** Februar 2026

**Version:** 1.0.0 (MVP)