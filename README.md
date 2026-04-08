# 🤖 Discord Bot with Ollama Integration

A Discord bot that integrates with Ollama to provide AI-powered responses from local Ollama models.

## Features

- **AI Responses**: Ask questions and get responses from Ollama AI models
- **Multiple Models**: Support for any Ollama model installed locally
- **Simple API**: Uses Ollama's local REST API at `http://localhost:11434`
- **Commands**:
  - `!ask <question>` - Ask the AI a question
  - `!model` - View current model information
  - `!help_ollama` - Show help menu
  - **Mention**: Just mention the bot and ask a question naturally

## Requirements

- Python 3.8+
- Discord Bot Token
- Ollama running locally

## Setup

### 1. Install Prerequisites

```bash
# Install Ollama from https://ollama.ai
ollama pull qwen3.5:9b  # or any other model
ollama serve  # Start Ollama (runs on localhost:11434 by default)
```

### 2. Clone and Setup Bot

```bash
cd "Discord bot testing"
pip install -r requirements.txt
```

### 3. Configure Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the token and paste it in `.env` file as `DISCORD_TOKEN`
5. Under "OAuth2" → "URL Generator", select:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Messages/View Channels`, `Read Message History`
6. Use the generated URL to invite the bot to your server

### 4. Update Configuration

Edit `.env` file:
```env
DISCORD_TOKEN=your_token_here
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3.5:9b
```

### 5. Run the Bot

```bash
python bot.py
```

## Usage

### Commands

- **Ask a question**: `!ask What is the capital of France?`
- **See available models**: `!model`
- **Interactive**: Just mention the bot in a message and ask naturally

### Example

```
User: !ask What are the benefits of machine learning?
Bot: > Machine learning provides numerous benefits...
```

## Ollama Models

Popular models you can use:
- `qwen3.5:9b` - Recommended for this bot setup
- `llama2` - Meta's Llama 2 chat model
- `orca-mini` - Smaller and faster model

Check your Ollama installation for available models: `ollama list`

## Troubleshooting

**Bot doesn't respond:**
- Check if Ollama is running: `curl http://localhost:11434/api/tags`
- Verify `DISCORD_TOKEN` is correct
- Check bot has message permissions in your server

**"Could not connect to Ollama":**
- Make sure Ollama is running: `ollama serve`
- Check `OLLAMA_HOST` in `.env` matches your Ollama location

**Request times out:**
- Large models take longer, increase wait time or use a smaller model
- Check your system resources

## Environment Variables

- `DISCORD_TOKEN` - Your Discord bot token (required)
- `OLLAMA_HOST` - Ollama server address (default: `http://localhost:11434`)
- `OLLAMA_MODEL` - Which model to use (default: `qwen3.5:9b`)

## License

MIT
