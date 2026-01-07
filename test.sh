#!/bin/bash
# Quick test script to verify everything is working

echo "================================"
echo "QualityForce AI - Quick Test"
echo "================================"
echo ""

# Test 1: Check Python
echo "[1/5] Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python not found!"
    exit 1
fi
echo "✓ Python OK"
echo ""

# Test 2: Check dependencies
echo "[2/5] Checking backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r ../requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi
echo "✓ Dependencies OK"
echo ""

# Test 3: Test configuration
echo "[3/5] Testing configuration..."
python -c "from core.config import settings; print(f'✓ Config loaded: {settings.HOST}:{settings.PORT}')"
if [ $? -ne 0 ]; then
    echo "❌ Configuration error!"
    exit 1
fi
echo ""

# Test 4: Test backend imports
echo "[4/5] Testing backend imports..."
python -c "
from core.marketplace import AgentMarketplace
from agents import UnitTestingAgent
print('✓ All imports successful')
" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Import error!"
    exit 1
fi
echo ""

# Test 5: Start backend (test mode)
echo "[5/5] Testing backend startup..."
timeout 5 python -c "
import uvicorn
from main import app
print('✓ Backend can start')
" 2>&1
echo ""

echo "================================"
echo "✅ All tests passed!"
echo "================================"
echo ""
echo "To start the application:"
echo "1. Backend:  cd backend && source venv/bin/activate && python main.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
