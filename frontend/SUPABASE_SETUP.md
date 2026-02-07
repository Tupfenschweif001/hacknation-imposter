# 🔑 Supabase API Keys finden - Schritt für Schritt

## 📍 Wo finde ich die API Keys?

### Schritt 1: Supabase Dashboard öffnen

1. Gehe zu [supabase.com](https://supabase.com)
2. Melde dich an (oder erstelle einen Account)
3. Du siehst eine Liste deiner Projekte

### Schritt 2: Projekt auswählen oder erstellen

**Falls du noch kein Projekt hast:**
1. Klicke auf **"New Project"**
2. Wähle eine Organisation (oder erstelle eine neue)
3. Gib deinem Projekt einen Namen (z.B. "voice-ai-agent")
4. Wähle ein Passwort für die Datenbank
5. Wähle eine Region (z.B. "Frankfurt" für Deutschland)
6. Klicke auf **"Create new project"**
7. ⏳ Warte ~2 Minuten, bis das Projekt bereit ist

**Falls du bereits ein Projekt hast:**
1. Klicke auf dein Projekt in der Liste

### Schritt 3: API Keys finden

Jetzt bist du im Projekt-Dashboard. So findest du die Keys:

1. **In der linken Sidebar**, klicke auf das **Zahnrad-Symbol** (⚙️) ganz unten
2. Oder klicke direkt auf **"Settings"**
3. Im Settings-Menü, klicke auf **"API"**

### Schritt 4: Keys kopieren

Auf der API-Seite siehst du:

#### 📋 Project URL
```
https://xxxxxxxxxxxxx.supabase.co
```
- Das ist deine `NEXT_PUBLIC_SUPABASE_URL`
- Klicke auf das Kopier-Symbol rechts neben der URL

#### 🔑 API Keys

Du siehst mehrere Keys. Du brauchst den **"anon public"** Key:

```
Project API keys
├── anon public    ← DEN BRAUCHST DU!
├── service_role   ← NICHT DIESEN!
└── ...
```

- Der **anon public** Key ist sicher für Frontend-Nutzung
- Klicke auf das Kopier-Symbol neben dem **anon public** Key
- Das ist deine `NEXT_PUBLIC_SUPABASE_ANON_KEY`

⚠️ **WICHTIG**: Nutze NICHT den `service_role` Key im Frontend!

### Schritt 5: Keys in .env.local einfügen

1. Öffne die Datei `frontend/.env.local`
2. Ersetze die Platzhalter:

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🗄️ Datenbank einrichten

Nachdem du die Keys hast:

1. Gehe zurück zum Supabase Dashboard
2. Klicke in der linken Sidebar auf **"SQL Editor"** (Symbol: 📝)
3. Klicke oben rechts auf **"New query"**
4. Öffne die Datei `frontend/supabase-schema.sql` in deinem Code-Editor
5. Kopiere den gesamten Inhalt
6. Füge ihn in den SQL Editor ein
7. Klicke auf **"Run"** (oder drücke `Cmd/Ctrl + Enter`)
8. ✅ Du solltest "Success. No rows returned" sehen

## ✅ Testen

Um zu testen, ob alles funktioniert:

1. Gehe zu **"Table Editor"** in der Sidebar
2. Du solltest jetzt 3 Tabellen sehen:
   - `profiles`
   - `requests`
   - `events`

## 🔐 Auth konfigurieren (Optional für schnelleres Testing)

Für die Demo kannst du Email-Bestätigung deaktivieren:

1. Gehe zu **"Authentication"** in der Sidebar
2. Klicke auf **"Providers"**
3. Stelle sicher, dass **"Email"** aktiviert ist
4. Gehe zu **"Settings"** (unter Authentication)
5. Scrolle zu **"Email Auth"**
6. Deaktiviere **"Confirm email"** (für schnelleres Testing)
7. Klicke auf **"Save"**

## 🎯 Fertig!

Jetzt kannst du die App starten:

```bash
cd frontend
npm install
npm run dev
```

Öffne http://localhost:3000 und registriere einen Account!

## 🐛 Troubleshooting

### "Invalid supabaseUrl" Fehler
- Überprüfe, ob die URL mit `https://` beginnt
- Stelle sicher, dass keine Leerzeichen in der `.env.local` sind
- Die URL sollte auf `.supabase.co` enden

### "Invalid API key" Fehler
- Stelle sicher, dass du den **anon public** Key verwendest
- Der Key sollte mit `eyJ` beginnen
- Kopiere den kompletten Key (er ist sehr lang!)

### Tabellen werden nicht erstellt
- Überprüfe, ob das SQL-Script komplett ausgeführt wurde
- Schaue in den SQL Editor für Fehlermeldungen
- Stelle sicher, dass du im richtigen Projekt bist

### Login funktioniert nicht
- Überprüfe, ob Email-Provider aktiviert ist
- Schaue in **Authentication** > **Users**, ob der User erstellt wurde
- Prüfe die Browser-Console auf Fehler

## 📸 Visuelle Hilfe

### Wo ist was?

```
Supabase Dashboard
├── 🏠 Home (Projekt-Übersicht)
├── 📝 SQL Editor (hier SQL ausführen)
├── 📊 Table Editor (Daten ansehen/bearbeiten)
├── 🔐 Authentication (User-Verwaltung)
│   ├── Users
│   ├── Providers
│   └── Settings
└── ⚙️ Settings (ganz unten)
    ├── General
    ├── API ← HIER SIND DIE KEYS!
    ├── Database
    └── ...
```

## 💡 Tipps

1. **Speichere die Keys sicher**: Füge sie zu deinem Passwort-Manager hinzu
2. **Teile sie nicht**: Die Keys sollten nicht in Git committed werden
3. **Für Produktion**: Nutze Environment Variables in deinem Hosting-Provider
4. **Backup**: Notiere dir die Keys, falls du sie später brauchst

## 🆘 Weitere Hilfe

- [Supabase Dokumentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- Siehe auch: `QUICKSTART.md` in diesem Projekt