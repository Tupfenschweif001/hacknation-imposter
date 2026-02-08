# Voice AI Agent - Hacknation Imposter

Demo-Webapp of a Voice-Agent that manages phone calls and appointments. Developed for the hack-nation hackathon 2026.

## 🚀 Quick Start

1. clone the git repository

2. pip install -r equirements.txt
3. pip install node
4. ./setup.sh
5. add a local .env file in the outer scope
6. add the nessecary api-tokens in the following format:
     - TWILIO_ACCOUNT_SID= ## add you twilio account id
     - TWILIO_AUTH_TOKEN= ## add your twilio authentication token 
     - TWILIO_PHONE_NUMBER=+17348758446
     - TARGET_PHONE_NUMBER=+4917645628259 ##
     - ELEVENLABS_API_TOKEN= ## add your elevenlabs_token_here
     - PUBLIC_BASE_URL=https://hacknation-imposter.onrender.com ## this stays as it is
     - GOOGLE_API_KEY=   ## add your google_api_token pip install node
7. ./start.sh


## 🎯 Features

### ✅ Implementet

- **Authentification**: login & registration with Supabase
- **Request-management**: creating and managing of appointments
- **Timeline**: Event-history for every request
- **Profil**: access and change profile information
- **Modern design**: purple-accent, rounded cards, minimalistic design
- **Darkmode toggle**
- **nearest doctor search**: prototype of an integrated search for the nearest doctor including their phonenumber

### 🚧 planed
- Google Calendar Integration
- WebSocket instead of polling
- Request-cancel-function
- Push-notification

## 🛠️ Tech Stack

### Frontend
- Next.js 15 (App Router)
- TypeScript
- TailwindCSS
- shadcn/ui
- Supabase (Auth + Database)

### Backend ()
- Python
- Voice AI Integration
- integration of the ElevenLabs-API

## 👥 Team

Hacknation Hackathon 2026
