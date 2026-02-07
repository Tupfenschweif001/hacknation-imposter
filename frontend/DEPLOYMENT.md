# 🚀 Deployment Guide

Anleitung zum Deployen der Voice AI Agent App.

## ⚠️ Wichtig vor dem Deployment

Die App benötigt gültige Supabase-Credentials in den Umgebungsvariablen. Der Build schlägt fehl, wenn diese nicht gesetzt sind.

## 🔧 Vorbereitung

1. **Supabase Projekt einrichten** (siehe QUICKSTART.md)
2. **Environment Variables setzen**
3. **Datenbank-Schema ausführen** (supabase-schema.sql)

## 📦 Vercel Deployment (Empfohlen)

### Schritt 1: Vercel Account

1. Gehe zu [vercel.com](https://vercel.com)
2. Melde dich mit GitHub an
3. Importiere dein Repository

### Schritt 2: Environment Variables

Füge in den Vercel Project Settings hinzu:

```
NEXT_PUBLIC_SUPABASE_URL=deine_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=dein_supabase_anon_key
```

### Schritt 3: Deploy

1. Vercel erkennt automatisch Next.js
2. Root Directory: `frontend`
3. Build Command: `npm run build`
4. Output Directory: `.next`
5. Klicke auf "Deploy"

## 🐳 Docker Deployment

### Dockerfile erstellen

```dockerfile
FROM node:18-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${NEXT_PUBLIC_SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${NEXT_PUBLIC_SUPABASE_ANON_KEY}
```

## 🌐 Andere Plattformen

### Netlify

1. Verbinde dein Repository
2. Build Command: `cd frontend && npm run build`
3. Publish Directory: `frontend/.next`
4. Setze Environment Variables

### Railway

1. Erstelle neues Projekt
2. Verbinde GitHub Repository
3. Root Directory: `frontend`
4. Setze Environment Variables
5. Deploy

## ✅ Post-Deployment Checklist

- [ ] Supabase URL und Keys sind korrekt gesetzt
- [ ] Datenbank-Schema ist ausgeführt
- [ ] RLS Policies sind aktiviert
- [ ] Email-Provider ist konfiguriert
- [ ] App ist erreichbar
- [ ] Login/Register funktioniert
- [ ] Dashboard lädt Daten

## 🔒 Sicherheit

### Produktions-Einstellungen

1. **Supabase**:
   - Aktiviere Email-Bestätigung
   - Setze Rate Limits
   - Konfiguriere CORS richtig

2. **Next.js**:
   - Nutze HTTPS
   - Setze Security Headers
   - Aktiviere CSP (Content Security Policy)

3. **Environment Variables**:
   - Niemals in Git committen
   - Nutze Secrets Management
   - Rotiere Keys regelmäßig

## 📊 Monitoring

### Empfohlene Tools

- **Vercel Analytics**: Automatisch bei Vercel
- **Sentry**: Error Tracking
- **LogRocket**: Session Replay
- **Supabase Dashboard**: Database Monitoring

## 🔄 CI/CD

### GitHub Actions Beispiel

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run build
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
```

## 🐛 Troubleshooting

### Build schlägt fehl

- Überprüfe Environment Variables
- Stelle sicher, dass alle Dependencies installiert sind
- Prüfe Node.js Version (18+)

### App lädt nicht

- Überprüfe Supabase Connection
- Prüfe Browser Console auf Fehler
- Verifiziere CORS-Einstellungen

### Authentifizierung funktioniert nicht

- Überprüfe Supabase Auth Settings
- Prüfe Redirect URLs in Supabase
- Verifiziere Email-Provider-Konfiguration