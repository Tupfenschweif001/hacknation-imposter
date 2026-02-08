# 🧪 Contact Suggestions Feature - Test Guide

## ✅ Voraussetzungen

### 1. Environment Variables prüfen

**Backend (.env):**

```bash
cat .env | grep GOOGLE_API_KEY
```

Sollte zeigen: `GOOGLE_API_KEY=your_key_here`

**Frontend (frontend/.env.local):**

```bash
cat frontend/.env.local | grep BACKEND_URL
```

Sollte zeigen: `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`

### 2. User Profile muss Adresse haben

Gehe zu `/profile` und stelle sicher dass ausgefüllt ist:

- ✅ Street (z.B. "Nancystraße")
- ✅ House Number (z.B. "1")
- ✅ Postal Code (z.B. "76187")
- ✅ City (z.B. "Karlsruhe")

## 🚀 Schritt-für-Schritt Test

### Schritt 1: Backend starten

```bash
# Terminal 1
cd backend
source ../.venv/bin/activate  # Falls nicht schon aktiv
uvicorn main:app --reload --port 8000
```

**Erwartete Ausgabe:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```
