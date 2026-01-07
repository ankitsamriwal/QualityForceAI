# Windows Setup Guide

## Quick Start (Easiest Method)

1. **Double-click `start-backend.bat`** - This will start the backend server
2. **Double-click `start-frontend.bat`** - This will start the frontend
3. Open your browser to http://localhost:5173

## Manual Setup

### Prerequisites
- Python 3.11+ installed
- Node.js 18+ installed
- Git installed

### Backend Setup

**Option 1: Using Command Prompt**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install fastapi uvicorn pydantic pydantic-settings python-multipart aiofiles httpx python-dotenv
python main.py
```

**Option 2: Using PowerShell**
```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic pydantic-settings python-multipart aiofiles httpx python-dotenv
python main.py
```

**Option 3: Using Git Bash**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install fastapi uvicorn pydantic pydantic-settings python-multipart aiofiles httpx python-dotenv
python main.py
```

The backend will start on: http://localhost:8000

### Frontend Setup

Open a **new terminal** and run:

```cmd
cd frontend
npm install
npm run dev
```

The frontend will start on: http://localhost:5173

## Troubleshooting

### PowerShell Execution Policy Error
If you get an error about scripts being disabled in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use
If port 8000 or 5173 is already in use:

**Backend (.env file):**
```
PORT=8001
```

**Frontend (vite.config.ts):**
```typescript
server: {
  port: 5174
}
```

### Python Not Found
Make sure Python is in your PATH:
```cmd
python --version
```

If not found, reinstall Python and check "Add Python to PATH" during installation.

### Node.js Not Found
Make sure Node.js is installed:
```cmd
node --version
npm --version
```

Download from: https://nodejs.org/

## Configuration

### No API Keys Required!
The application works out of the box without any external API keys. All agents use template-based test generation by default.

If you want to enable AI-powered generation later:
1. Edit `backend/.env`
2. Add your API keys (OpenAI, Anthropic, or Google)
3. Set `USE_AI_GENERATION=True`

## Using the Application

1. **Select Agents** - Choose one or more testing agents (Unit, Functional, Integration, Security, Load, Stress, Regression)
2. **Upload Documents** - Upload source code, requirements, specs, etc.
3. **Click Execute** - Start the testing process
4. **View Results** - See generated tests, test data, results, RCA, and recommendations

## File Structure
```
QualityForceAI/
├── backend/
│   ├── venv/              # Python virtual environment
│   ├── main.py            # FastAPI server
│   ├── .env               # Configuration (no API keys needed)
│   └── core/              # Core functionality
├── frontend/
│   ├── src/               # React source code
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
├── start-backend.bat      # Quick start backend (Windows)
└── start-frontend.bat     # Quick start frontend (Windows)
```

## Need Help?

- Check backend logs in the terminal where you ran `python main.py`
- Check frontend logs in the browser console (F12)
- Check `QUICK_START_DEBUG.md` for detailed troubleshooting
- Ensure both backend AND frontend are running simultaneously
