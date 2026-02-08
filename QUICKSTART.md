# 🚀 Quickstart Guide

## Erste Installation

Führe einmalig das Setup-Script aus:

```bash
./setup.sh
```

Das Script:
- ✅ Erstellt Python Virtual Environment (`.venv`)
- ✅ Installiert Python Dependencies
- ✅ Installiert Frontend Dependencies (npm)

## Anwendung starten

Nach dem Setup kannst du die Anwendung jederzeit starten mit:

```bash
./start.sh
```

Das Script:
- ✅ Aktiviert automatisch das Virtual Environment
- ✅ Installiert fehlende Dependencies (falls nötig)
- ✅ Startet Backend auf http://localhost:8000
- ✅ Startet Frontend auf http://localhost:3000

## Stoppen

Drücke `CTRL+C` um beide Server zu stoppen.

## Konfiguration

### Backend (.env)
```env
# Deine Backend Environment Variables
```

### Frontend (frontend/.env.local)
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Troubleshooting

### "Permission denied"
```bash
chmod +x start.sh setup.sh
```

### "python3: command not found"
Installiere Python 3:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-venv
```

### "npm: command not found"
Installiere Node.js:
```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt install nodejs npm
```

### Port bereits belegt
Wenn Port 8000 oder 3000 bereits belegt ist:
```bash
# Finde den Prozess
lsof -i :8000
lsof -i :3000

# Beende den Prozess
kill -9 <PID>
```

## Entwicklung

### Nur Backend starten
```bash
source .venv/bin/activate
cd backend
uvicorn main:app --reload --port 8000
```

### Nur Frontend starten
```bash
cd frontend
npm run dev
```

## Struktur

```
.
├── start.sh              # Start-Script (Backend + Frontend)
├── setup.sh              # Setup-Script (einmalig)
├── backend/              # Python Backend (FastAPI)
│   └── main.py
├── frontend/             # Next.js Frontend
│   ├── app/
│   ├── components/
│   └── lib/
└── requirements.txt      # Python Dependencies
```

## Nächste Schritte

1. ✅ Setup ausführen: `./setup.sh`
2. ✅ Environment Variables konfigurieren
3. ✅ Anwendung starten: `./start.sh`
4. ✅ Browser öffnen: http://localhost:3000

Viel Erfolg beim Hackathon! 🎉