# Voice AI Agent - Appointment Booking Demo

Eine moderne Demo-Webapp für einen Voice-AI-Agenten, der Telefonate führt und Termine bucht. Entwickelt für einen 24h Hackathon.

## 🚀 Features

- **Authentifizierung**: Login & Registrierung mit Supabase Auth
- **Dashboard**: Kanban-Board mit 3 Spalten (Offen, In Bearbeitung, Abgeschlossen)
- **Request-Erstellung**: Formular für neue Terminanfragen
- **Request-Details**: Live-Updates via Polling (alle 3 Sekunden)
- **Timeline**: Event-Historie für jede Anfrage
- **Profil-Verwaltung**: Persönliche Informationen bearbeiten
- **Modernes Design**: Lila-Akzent, rounded cards, minimalistisch

## 🛠️ Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Sprache**: TypeScript
- **Styling**: TailwindCSS
- **UI-Komponenten**: shadcn/ui
- **Icons**: lucide-react
- **Backend**: Supabase (Auth + PostgreSQL)
- **Toasts**: Sonner
- **Datum-Formatierung**: date-fns

## 📋 Voraussetzungen

- Node.js 18+ und npm
- Supabase Account und Projekt

## 🔧 Installation

1. **Repository klonen und in das Frontend-Verzeichnis wechseln**:
   ```bash
   cd frontend
   ```

2. **Dependencies installieren**:
   ```bash
   npm install
   ```

3. **Umgebungsvariablen konfigurieren**:
   
   Erstelle eine `.env.local` Datei im `frontend` Verzeichnis:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

4. **Supabase Datenbank einrichten**:
   
   Führe das SQL-Schema aus (siehe unten) in deinem Supabase SQL Editor aus.

5. **Development Server starten**:
   ```bash
   npm run dev
   ```

6. **App öffnen**:
   
   Öffne [http://localhost:3000](http://localhost:3000) im Browser.

## 🗄️ Supabase Setup

### SQL Schema

Führe folgendes SQL in deinem Supabase SQL Editor aus:

```sql
-- Profiles table
create table profiles (
  user_id uuid references auth.users primary key,
  username text,
  default_callback_number text,
  address text,
  calendar_connected boolean default false,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Requests table
create table requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  title text not null,
  description text not null,
  callback_number text not null,
  number_to_call text,
  preferred_time text not null,
  radius_km integer,
  status text not null default 'queued',
  summary text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Events table
create table events (
  id uuid primary key default gen_random_uuid(),
  request_id uuid references requests(id) on delete cascade not null,
  type text not null,
  message text not null,
  created_at timestamp with time zone default now()
);

-- Enable Row Level Security
alter table profiles enable row level security;
alter table requests enable row level security;
alter table events enable row level security;

-- Profiles policies
create policy "Users can view own profile"
  on profiles for select
  using (auth.uid() = user_id);

create policy "Users can insert own profile"
  on profiles for insert
  with check (auth.uid() = user_id);

create policy "Users can update own profile"
  on profiles for update
  using (auth.uid() = user_id);

-- Requests policies
create policy "Users can view own requests"
  on requests for select
  using (auth.uid() = user_id);

create policy "Users can create own requests"
  on requests for insert
  with check (auth.uid() = user_id);

create policy "Users can update own requests"
  on requests for update
  using (auth.uid() = user_id);

-- Events policies
create policy "Users can view events for own requests"
  on events for select
  using (
    exists (
      select 1 from requests
      where requests.id = events.request_id
      and requests.user_id = auth.uid()
    )
  );

create policy "Users can create events for own requests"
  on events for insert
  with check (
    exists (
      select 1 from requests
      where requests.id = events.request_id
      and requests.user_id = auth.uid()
    )
  );
```

### Supabase Auth Konfiguration

1. Gehe zu **Authentication** > **Providers** in deinem Supabase Dashboard
2. Aktiviere **Email** Provider
3. Optional: Deaktiviere Email-Bestätigung für schnelleres Testing (unter **Authentication** > **Settings**)

## 📁 Projektstruktur

```
frontend/
├── app/
│   ├── (auth)/              # Auth-Routen (Login, Register)
│   │   ├── login/
│   │   └── register/
│   ├── (app)/               # Geschützte App-Routen
│   │   ├── dashboard/       # Kanban-Board
│   │   ├── new/             # Neue Anfrage erstellen
│   │   ├── requests/[id]/   # Request-Details
│   │   ├── profile/         # Profil-Seite
│   │   └── layout.tsx       # App-Layout mit Sidebar
│   ├── layout.tsx           # Root-Layout
│   ├── page.tsx             # Redirect zu /login
│   └── globals.css          # Globale Styles
├── components/
│   ├── ui/                  # shadcn/ui Komponenten
│   ├── sidebar.tsx          # Navigation Sidebar
│   ├── status-badge.tsx     # Status-Badge Komponente
│   ├── request-card.tsx     # Request-Karte für Kanban
│   ├── kanban-column.tsx    # Kanban-Spalte
│   └── timeline.tsx         # Event-Timeline
├── lib/
│   ├── supabase.ts          # Supabase Client
│   ├── types.ts             # TypeScript Types
│   └── utils.ts             # Utility-Funktionen
├── middleware.ts            # Auth-Middleware
└── package.json
```

## 🎨 Design-System

### Farben
- **Primär**: Lila/Violett (`violet-600`, `purple-600`)
- **Neutral**: Grau-Töne
- **Success**: Grün (`green-600`)
- **Warning**: Gelb (`yellow-600`)
- **Error**: Rot (`red-600`)

### Status-Farben
- **Queued**: Grau
- **Outside Business Hours**: Blau
- **Calling/In Progress**: Lila
- **Waiting for Callback**: Gelb
- **Booked**: Grün
- **Failed**: Rot
- **Canceled**: Grau

## 🔄 Request Status Flow

```
queued → calling → in_progress → booked
   ↓         ↓          ↓            ↓
outside_  waiting_   failed      canceled
business  for_
hours     callback
```

## 📱 Routen

- `/` - Redirect zu `/login`
- `/login` - Login-Seite
- `/register` - Registrierungs-Seite
- `/dashboard` - Kanban-Board (geschützt)
- `/new` - Neue Anfrage erstellen (geschützt)
- `/requests/:id` - Request-Details (geschützt)
- `/profile` - Profil-Seite (geschützt)

## 🔐 Authentifizierung

Die App nutzt Supabase Auth mit Email/Password. Die Middleware schützt alle App-Routen und leitet nicht-authentifizierte User zu `/login` weiter.

## 🔄 Live-Updates

Die Request-Detail-Seite nutzt Polling (alle 3 Sekunden), um Status-Updates und neue Events in Echtzeit anzuzeigen.

## 🚧 Zukünftige Features

- [ ] Darkmode Toggle
- [ ] Google Calendar Integration
- [ ] Passwort-Reset-Funktion
- [ ] WebSocket statt Polling
- [ ] Request-Abbruch-Funktion
- [ ] Benachrichtigungen

## 📝 Lizenz

MIT

## 👥 Entwickelt für

Hacknation Hackathon 2026