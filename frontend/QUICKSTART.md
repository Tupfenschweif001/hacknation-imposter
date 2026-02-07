# 🚀 Quick Start Guide

Schnellanleitung zum Starten der Voice AI Agent Demo-App.

## ⚡ 5-Minuten Setup

### 1. Supabase Projekt erstellen

1. Gehe zu [supabase.com](https://supabase.com) und erstelle ein kostenloses Konto
2. Erstelle ein neues Projekt
3. Warte, bis das Projekt bereit ist (~2 Minuten)

### 2. Datenbank einrichten

1. Gehe zu **SQL Editor** in deinem Supabase Dashboard
2. Klicke auf **New Query**
3. Kopiere den Inhalt von `supabase-schema.sql` und füge ihn ein
4. Klicke auf **Run** (oder drücke Cmd/Ctrl + Enter)

### 3. API Keys holen

1. Gehe zu **Settings** > **API** in deinem Supabase Dashboard
2. Kopiere:
   - **Project URL** (z.B. `https://xxxxx.supabase.co`)
   - **anon public** Key

### 4. Environment Variables setzen

Erstelle `.env.local` im `frontend` Ordner:

```env
NEXT_PUBLIC_SUPABASE_URL=deine_project_url_hier
NEXT_PUBLIC_SUPABASE_ANON_KEY=dein_anon_key_hier
```

### 5. App starten

```bash
cd frontend
npm install
npm run dev
```

Öffne [http://localhost:3000](http://localhost:3000)

## 🎯 Erste Schritte

1. **Registrieren**: Erstelle einen Account auf der Register-Seite
2. **Dashboard**: Du wirst automatisch zum Dashboard weitergeleitet
3. **Neue Anfrage**: Klicke auf "Neue Anfrage" und fülle das Formular aus
4. **Details ansehen**: Klicke auf eine Karte im Dashboard, um Details zu sehen

## 🧪 Test-Daten erstellen

Da dies eine Demo ist, kannst du Test-Requests direkt in Supabase erstellen:

1. Gehe zu **Table Editor** > **requests** in Supabase
2. Klicke auf **Insert** > **Insert row**
3. Fülle die Felder aus (user_id muss deine User-ID sein)
4. Erstelle auch Test-Events in der **events** Tabelle

## 🐛 Troubleshooting

### "Failed to fetch" Fehler
- Überprüfe, ob die Supabase URL und Keys korrekt sind
- Stelle sicher, dass Row Level Security (RLS) aktiviert ist

### Login funktioniert nicht
- Gehe zu **Authentication** > **Settings** in Supabase
- Deaktiviere "Confirm email" für schnelleres Testing

### Requests werden nicht angezeigt
- Überprüfe die RLS Policies in Supabase
- Stelle sicher, dass du eingeloggt bist

## 📚 Weitere Infos

Siehe [README.md](./README.md) für detaillierte Dokumentation.

## 💡 Demo-Tipps

Für eine realistische Demo:

1. Erstelle mehrere Requests mit verschiedenen Status
2. Füge Events zu Requests hinzu, um die Timeline zu füllen
3. Teste das Polling, indem du den Status in Supabase änderst
4. Die App aktualisiert sich automatisch alle 3 Sekunden

## 🎨 Design anpassen

Die Hauptfarben findest du in:
- `app/globals.css` - CSS-Variablen
- `tailwind.config.ts` - Tailwind-Konfiguration
- Komponenten verwenden `violet-600` und `purple-600` für Akzente