#!/bin/bash
# QualityForce AI - Startup Script for Linux/Mac

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         🚀 Starting QualityForce AI Application...          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if backend virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend virtual environment not found!"
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -q fastapi uvicorn pydantic pydantic-settings python-multipart aiofiles httpx python-dotenv
    cd ..
    echo "✅ Virtual environment created"
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies not found!"
    echo "Installing npm packages..."
    cd frontend
    npm install
    cd ..
    echo "✅ Dependencies installed"
fi

echo ""
echo "Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         ✅ QualityForce AI is now running!                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Backend:  http://localhost:8000"
echo "🖥️  Frontend: http://localhost:5173"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers, run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers..."
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
