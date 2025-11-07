#!/bin/bash

echo "🚀 Starting Legacy Migration AI System"

# Start Ollama in background
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!
echo "✅ Ollama started (PID: $OLLAMA_PID)"

# Wait for Ollama to be ready
sleep 3

# Activate venv and run pipeline
cd ~/Documents/aiteam
source venv/bin/activate

echo "🤖 Running migration pipeline..."
python workflows/migration_pipeline.py

# Cleanup
echo "🧹 Cleaning up..."
kill $OLLAMA_PID
