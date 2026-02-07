# Voice AI Agent - Hacknation Imposter

Demo-Webapp für einen Voice-AI-Agenten, der Telefonate führt und Termine bucht. Entwickelt für den Hacknation Hackathon 2026.

## 📁 Projektstruktur

```
hacknation-imposter/
├── frontend/           # Next.js Frontend-Anwendung
│   ├── app/           # Next.js App Router
│   ├── components/    # React-Komponenten
│   ├── lib/           # Utilities & Types
│   └── README.md      # Frontend-Dokumentation
├── requirements.txt   # Python Dependencies (Backend)
└── test.py           # Backend-Tests
```

## 🚀 Quick Start

### Frontend starten

```bash
cd frontend
npm install
npm run dev
```

Siehe [frontend/QUICKSTART.md](frontend/QUICKSTART.md) für eine detaillierte Anleitung.

## 📚 Dokumentation

- **Frontend**: [frontend/README.md](frontend/README.md)
- **Quick Start**: [frontend/QUICKSTART.md](frontend/QUICKSTART.md)
- **Supabase Schema**: [frontend/supabase-schema.sql](frontend/supabase-schema.sql)

## 🎯 Features

### ✅ Implementiert

- **Authentifizierung**: Login & Registrierung mit Supabase
- **Dashboard**: Kanban-Board mit 3 Spalten
- **Request-Management**: Erstellen und Verwalten von Terminanfragen
- **Live-Updates**: Polling alle 3 Sekunden für Echtzeit-Status
- **Timeline**: Event-Historie für jede Anfrage
- **Profil**: Persönliche Informationen verwalten
- **Modernes Design**: Lila-Akzent, rounded cards, minimalistisch

### 🚧 Geplant

- Darkmode Toggle
- Google Calendar Integration
- WebSocket statt Polling
- Request-Abbruch-Funktion
- Push-Benachrichtigungen

## 🛠️ Tech Stack

### Frontend
- Next.js 15 (App Router)
- TypeScript
- TailwindCSS
- shadcn/ui
- Supabase (Auth + Database)

### Backend (geplant)
- Python
- Voice AI Integration
- Telefonie-API

## 👥 Team

Hacknation Hackathon 2026

## 📝 Lizenz

MIT