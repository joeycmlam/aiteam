#!/bin/bash

# Quick Setup Script for AI Agents
# This gets everything working quickly!

echo "🚀 AI Agents Quick Setup"
echo "================================"

# 1. Add VS Code to PATH (optional - for using Copilot in VS Code)
echo ""
echo "📌 Step 1: Add VS Code to PATH (optional)"
echo "Run this command to add VS Code CLI:"
echo ""
echo 'export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"'
echo ""
echo "Add it to your ~/.zshrc or ~/.bash_profile to make it permanent:"
echo 'echo '\''export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"'\'' >> ~/.zshrc'
echo ""

# 2. Make sure Ollama is running
echo "================================"
echo "📌 Step 2: Start Ollama"
echo ""

if pgrep -x "ollama" > /dev/null; then
    echo "✅ Ollama is already running"
else
    echo "⚠️  Starting Ollama..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "✅ Ollama started"
fi

# 3. Check if model is available
echo ""
echo "📌 Step 3: Check Ollama Model"
echo ""
ollama list

echo ""
echo "================================"
echo "🎯 You're Ready!"
echo "================================"
echo ""
echo "Run your AI agents:"
echo "  python3 workflows/migration_pipeline.py"
echo ""
echo "Test LLM connection:"
echo "  python3 test_llm.py"
echo ""
echo "For GitHub Copilot in VS Code:"
echo "  1. Open VS Code manually (from Applications)"
echo "  2. Install extensions from the Extensions panel (Cmd+Shift+X)"
echo "  3. Search for 'GitHub Copilot' and install"
echo ""
echo "✨ Happy coding!"
echo ""
