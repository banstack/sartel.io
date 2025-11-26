#!/bin/bash

# Build script for Sartel.io
# This script builds the frontend and prepares the application for deployment

set -e  # Exit on error

echo "🔨 Building Sartel.io..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build completed successfully!"
echo ""
echo "To run the application:"
echo "  cd backend"
echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Then visit: http://localhost:8000"
