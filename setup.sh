#!/bin/bash

echo "🤖 Discord-Ollama Bot Setup"
echo "============================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Get a Discord bot token from https://discord.com/developers/applications"
echo "2. Edit .env file and add your DISCORD_TOKEN"
echo "3. Make sure Ollama is running: ollama serve"
echo "4. Run the bot: python bot.py"
echo ""
echo "💡 Tip: To activate virtual environment in future, run:"
echo "   source venv/bin/activate"
