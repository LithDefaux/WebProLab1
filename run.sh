#!/bin/bash

echo "Starting WebPro Project..."

# Function to clean up background processes on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap Ctrl+C (SIGINT) and call the cleanup function
trap cleanup SIGINT

# 1. Manage Virtual Environment in Root
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in root directory..."
    python -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Ensuring backend dependencies are installed..."
pip install -r backend/requirements.txt

# 2. Start the Backend
echo "Starting FastAPI backend on port 8000..."
cd backend
# uvicorn runs using the activated root .venv
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# 3. Start the Frontend
echo "Starting Frontend static server on port 3000..."
cd frontend
# python http.server runs using the activated root .venv
python -m http.server 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "==================================================="
echo "Backend running at: http://localhost:8000"
echo "Frontend running at: http://localhost:3000/register.html"
echo "==================================================="
echo "Press Ctrl+C to stop both servers."

# Wait indefinitely so the script doesn't exit immediately
wait $BACKEND_PID
wait $FRONTEND_PID
