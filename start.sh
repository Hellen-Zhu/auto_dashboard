#!/bin/bash

# Crypto Test Admin - Startup Script
# This script starts both backend and frontend servers

echo "=========================================="
echo "  Crypto Test Admin - Starting Services  "
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Backend directory
BACKEND_DIR="$SCRIPT_DIR/backend"
# Frontend directory
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Check if backend virtual environment exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${YELLOW}Warning: Backend virtual environment not found!${NC}"
    echo "Please run: cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start backend
echo -e "${BLUE}[1/2] Starting Backend API Server...${NC}"
cd "$BACKEND_DIR"
source venv/bin/activate
uvicorn main:app --reload --port 8000 > /tmp/crypto-admin-backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo "  - Health: http://localhost:8000/health"
echo ""

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${YELLOW}Warning: Backend may not be running properly${NC}"
    echo "Check logs: tail -f /tmp/crypto-admin-backend.log"
fi

# Start frontend
echo -e "${BLUE}[2/2] Starting Frontend Web Server...${NC}"
cd "$FRONTEND_DIR"
python3 -m http.server 3000 > /tmp/crypto-admin-frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo "  - Web UI: http://localhost:3000"
echo ""

echo "=========================================="
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo "=========================================="
echo ""
echo "Access the application:"
echo "  → Web UI: http://localhost:3000"
echo "  → API Docs: http://localhost:8000/docs"
echo ""
echo "To stop the services:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Or run:"
echo "  ./stop.sh"
echo ""
echo "Logs:"
echo "  Backend: /tmp/crypto-admin-backend.log"
echo "  Frontend: /tmp/crypto-admin-frontend.log"
echo ""

# Save PIDs to file for stop script
echo "$BACKEND_PID" > /tmp/crypto-admin-backend.pid
echo "$FRONTEND_PID" > /tmp/crypto-admin-frontend.pid

# Keep script running
echo "Press Ctrl+C to stop all services..."
wait
