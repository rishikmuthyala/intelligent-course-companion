#!/bin/bash

echo "🚀 Starting AI Course Companion Backend..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd "$(dirname "$0")"
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

