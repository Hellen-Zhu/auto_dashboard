#!/bin/bash

# Crypto Test Admin - Stop Script
# This script stops both backend and frontend servers

echo "=========================================="
echo "  Crypto Test Admin - Stopping Services  "
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Read PIDs from files
BACKEND_PID_FILE="/tmp/crypto-admin-backend.pid"
FRONTEND_PID_FILE="/tmp/crypto-admin-frontend.pid"

stopped=0

# Stop backend
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo -e "${GREEN}✓ Backend stopped${NC}"
        stopped=$((stopped + 1))
    fi
    rm -f "$BACKEND_PID_FILE"
fi

# Stop frontend
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo -e "${GREEN}✓ Frontend stopped${NC}"
        stopped=$((stopped + 1))
    fi
    rm -f "$FRONTEND_PID_FILE"
fi

# Also try to stop by port
echo ""
echo "Checking for any remaining processes..."

# Kill any process on port 8000
BACKEND_PORT_PID=$(lsof -ti:8000)
if [ ! -z "$BACKEND_PORT_PID" ]; then
    echo "Found process on port 8000 (PID: $BACKEND_PORT_PID), killing..."
    kill $BACKEND_PORT_PID
    stopped=$((stopped + 1))
fi

# Kill any process on port 3000
FRONTEND_PORT_PID=$(lsof -ti:3000)
if [ ! -z "$FRONTEND_PORT_PID" ]; then
    echo "Found process on port 3000 (PID: $FRONTEND_PORT_PID), killing..."
    kill $FRONTEND_PORT_PID
    stopped=$((stopped + 1))
fi

echo ""
if [ $stopped -gt 0 ]; then
    echo -e "${GREEN}✓ Successfully stopped $stopped process(es)${NC}"
else
    echo "No running processes found"
fi

echo ""
echo "=========================================="
echo "  All services stopped"
echo "=========================================="
