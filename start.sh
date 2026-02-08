#!/bin/bash

# Backend starten
cd backend
source language-output/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Zurück zum Root-Verzeichnis, dann ins Frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Backend running on http://localhost:8000 (PID: $BACKEND_PID)"
echo "✅ Frontend running on http://localhost:3000 (PID: $FRONTEND_PID)"

# Warten auf CTRL+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait