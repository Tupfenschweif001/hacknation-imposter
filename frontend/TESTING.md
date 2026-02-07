# 🧪 Testing Guide - Voice AI Agent

Anleitung zum Testen der erweiterten Registrierung und aller Features.

## 🚀 Quick Start Testing

### 1. Development Server starten

```bash
cd frontend
npm run dev
```

Öffne: http://localhost:3000

## 📝 Registrierung testen

### Schritt 1: Zur Registrierung navigieren

1. Öffne http://localhost:3000
2. Du wirst automatisch zu `/login` weitergeleitet
3. Klicke auf **"Sign up"** Link unten

### Schritt 2: Registrierungsformular ausfüllen

Fülle alle Felder aus:

**Testdaten:**
```
Username: Max Mustermann
Email: test@example.com (oder deine echte Email)
Address: Musterstraße 123, 12345 Berlin
Phone Number: +49 123 456789 (optional)
Password: test123456
Confirm Password: test123456
```

### Schritt 3: Registrierung absenden

1. Klicke auf **"Sign up"**
2. Du solltest **NICHT** zum Login weitergeleitet werden
3. Stattdessen siehst du den **Email-Bestätigungs-Screen**

### Schritt 4: Email-Bestätigungs-Screen prüfen

Du solltest sehen:
- ✅ Titel: "Check Your Email"
- ✅ Deine Email-Adresse angezeigt
- ✅ Hinweis zur Email-Bestätigung
- ✅ Button "Go to Sign In"

## 📧 Email-Bestätigung

### Option A: Mit echter Email (Empfohlen für Produktion)

1. Prüfe dein Email-Postfach
2. Suche nach Email von Supabase
3. Klicke auf Bestätigungs-Link
4. Du wirst zu Supabase weitergeleitet
5. Gehe zurück zur App und logge dich ein

### Option B: Email-Bestätigung deaktivieren (Für Testing)

**Für schnelleres Testing:**

1. Gehe zu deinem **Supabase Dashboard**
2. Klicke auf **Authentication** > **Settings**
3. Scrolle zu **"Email Auth"**
4. Deaktiviere **"Confirm email"**
5. Klicke **"Save"**

Jetzt kannst du dich direkt nach der Registrierung einloggen!

## 🔍 Profil-Daten überprüfen

### In Supabase Dashboard:

1. Gehe zu **Table Editor**
2. Wähle **"profiles"** Tabelle
3. Du solltest deinen neuen User sehen mit:
   - ✅ username
   - ✅ default_callback_number
   - ✅ address
   - ✅ calendar_connected (false)

### In der App:

1. Logge dich ein
2. Gehe zu **Profile** (Sidebar)
3. Prüfe, ob alle Daten korrekt angezeigt werden

## 🧪 Test-Szenarien

### Test 1: Validierung

**Passwörter stimmen nicht überein:**
```
Password: test123
Confirm Password: test456
```
Erwartung: ❌ Error "Passwords do not match"

**Passwort zu kurz:**
```
Password: 12345
```
Erwartung: ❌ Error "Password must be at least 6 characters"

**Pflichtfelder leer:**
- Lasse Username leer
Erwartung: ❌ Browser-Validierung verhindert Submit

### Test 2: Optionales Feld

**Ohne Telefonnummer:**
```
Username: Test User
Email: test2@example.com
Address: Teststraße 1
Phone Number: (leer lassen)
Password: test123456
```
Erwartung: ✅ Registrierung erfolgreich, Telefonnummer bleibt leer

### Test 3: Doppelte Email

**Registriere zweimal mit gleicher Email:**
```
Email: test@example.com (bereits verwendet)
```
Erwartung: ❌ Error von Supabase "User already registered"

### Test 4: Login nach Registrierung

1. Registriere einen neuen User
2. Bestätige Email (oder deaktiviere Email-Bestätigung)
3. Klicke "Go to Sign In"
4. Logge dich mit den Credentials ein
Erwartung: ✅ Redirect zu Dashboard

## 🐛 Troubleshooting

### Problem: "Failed to create profile"

**Lösung:**
1. Prüfe Supabase Connection (`.env.local`)
2. Prüfe ob `profiles` Tabelle existiert
3. Prüfe RLS Policies in Supabase

### Problem: Keine Email erhalten

**Lösung:**
1. Prüfe Spam-Ordner
2. Prüfe Supabase Email-Settings
3. Für Testing: Deaktiviere Email-Bestätigung

### Problem: "radius_km column not found"

**Lösung:**
1. Gehe zu Supabase Dashboard
2. Settings > API > "Reload schema"
3. Oder führe aus:
```sql
ALTER TABLE requests DROP COLUMN IF EXISTS radius_km;
```

## 📊 Datenbank-Checks

### Prüfe User in Supabase:

```sql
-- Alle User anzeigen
SELECT * FROM auth.users;

-- Alle Profile anzeigen
SELECT * FROM profiles;

-- User mit Profil joinen
SELECT 
  u.email,
  p.username,
  p.address,
  p.default_callback_number
FROM auth.users u
LEFT JOIN profiles p ON u.id = p.user_id;
```

## 🎯 Vollständiger Test-Flow

### 1. Registrierung
- [ ] Formular ausfüllen
- [ ] Validierung testen
- [ ] Submit
- [ ] Email-Bestätigungs-Screen sehen

### 2. Email-Bestätigung
- [ ] Email erhalten
- [ ] Link klicken
- [ ] Oder: Email-Bestätigung deaktivieren

### 3. Login
- [ ] Zum Login navigieren
- [ ] Credentials eingeben
- [ ] Erfolgreich einloggen

### 4. Dashboard
- [ ] Dashboard sehen
- [ ] Kanban-Board leer (noch keine Requests)

### 5. Profil prüfen
- [ ] Zu Profile navigieren
- [ ] Username korrekt
- [ ] Address korrekt
- [ ] Phone Number korrekt (oder leer)

### 6. Request erstellen
- [ ] "New Request" klicken
- [ ] Formular ausfüllen
- [ ] Submit
- [ ] Request-Detail-Seite sehen

### 7. Dashboard aktualisiert
- [ ] Zurück zu Dashboard
- [ ] Request in "Open" Spalte sehen

## 🔄 Reset für neuen Test

### User löschen in Supabase:

```sql
-- User und Profil löschen
DELETE FROM profiles WHERE user_id = 'user-id-hier';
DELETE FROM auth.users WHERE id = 'user-id-hier';
```

Oder im Dashboard:
1. **Authentication** > **Users**
2. User auswählen
3. **Delete user**

## 💡 Testing-Tipps

1. **Nutze verschiedene Emails** für mehrere Tests
2. **Browser DevTools** öffnen (F12) für Console-Logs
3. **Network Tab** prüfen für API-Calls
4. **Supabase Dashboard** parallel offen haben
5. **Email-Bestätigung deaktivieren** für schnelleres Testing

## 🎨 UI-Testing

### Prüfe visuell:
- [ ] Lila-Gradient auf Buttons
- [ ] Rounded Cards (2xl)
- [ ] Pflichtfelder mit rotem Stern
- [ ] Loading-States (Spinner)
- [ ] Toast-Benachrichtigungen
- [ ] Responsive Design (Mobile)

## 📱 Mobile Testing

```bash
# Finde deine lokale IP
ipconfig getifaddr en0  # macOS
ip addr show           # Linux
ipconfig              # Windows

# Öffne auf Mobile:
http://DEINE-IP:3000
```

Teste auf Mobile:
- [ ] Formular ausfüllen
- [ ] Buttons klickbar
- [ ] Text lesbar
- [ ] Keine horizontalen Scrollbars