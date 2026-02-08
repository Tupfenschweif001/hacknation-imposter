#!/bin/bash

set -e  # Stop bei Fehler

echo "🔧 Setting up Hacknation Imposter..."
echo ""

# Python venv
echo "📦 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
echo "✅ Virtual environment created"

# Python Dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Frontend Dependencies
echo ""
echo "📦 Installing Frontend dependencies (this may take a while)..."
cd frontend
npm install
cd ..
echo "✅ Frontend dependencies installed"

# Success
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Configure your .env files:"
echo "   - Root .env (Backend config)"
echo "   - frontend/.env.local (Supabase config)"
echo ""
echo "2. Start the application:"
echo "   ./start.sh"
echo ""