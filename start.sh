#!/bin/bash

set -e  # Stop bei Fehler

echo "🚀 Starting Hacknation Imposter..."
echo ""

# 1. Python Virtual Environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# 2. Python Dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt
echo "✅ Python dependencies installed"

# 3. Backend starten
echo ""
echo "🚀 Starting Backend on http://localhost:8000..."
cd backend
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 4. Frontend Dependencies
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Frontend dependencies (this may take a while)..."
    npm install
    echo "✅ Frontend dependencies installed"
fi

# 5. Frontend starten
echo ""
echo "🚀 Starting Frontend on http://localhost:3000..."
npm run dev &
FRONTEND_PID=$!
cd ..

# Status
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
echo "✅ Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press CTRL+C to stop both servers"
echo ""

# Cleanup bei CTRL+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Servers stopped'; exit" INT

# Warten
wait