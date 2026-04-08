# 🤖 Discord Bot with oMLX Integration

A Discord bot that integrates with oMLX to provide AI-powered responses using local language models on Apple Silicon.

## Features

- **AI Responses**: Ask questions and get responses from oMLX AI models
- **Multiple Models**: Support for any oMLX model (DeepSeek, Llama, etc.)
- **Flexible API**: Automatically detects and works with different oMLX server API formats
- **Commands**:
  - `!ask <question>` - Ask the AI a question
  - `!model` - View available models and current model
  - `!help_omlx` - Show help menu
  - **Mention**: Just mention the bot and ask a question naturally

## Requirements

- Python 3.8+
- Discord Bot Token
- oMLX running locally (Apple Silicon Macs)

## Setup

### 1. Install Prerequisites

```bash
# Install oMLX from https://github.com/ml-explore/mlx
pip install mlx
# Install the model you want to use
mlx pull deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
# Start oMLX server (typically runs on port 8080)
mlx serve
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
OMLX_HOST=http://localhost:8080
OMLX_MODEL=DeepSeek-R1-Distill-Qwen-1.5B
OMLX_API_KEY=your_api_key_here
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

## oMLX Models

Popular models you can use:
- `DeepSeek-R1-Distill-Qwen-1.5B` - Fast and capable (currently configured)
- `DeepSeek-Coder-V2-Lite-Instruct` - Code-focused model
- `Qwen2.5-Coder-1.5B-Instruct` - Another coding model

Check your oMLX server for available models: `curl http://localhost:8000/v1/models -H "Authorization: Bearer YOUR_API_KEY"`

## Troubleshooting

**Bot doesn't respond:**
- Check if oMLX is running: `curl http://localhost:8080/v1/models`
- Verify `DISCORD_TOKEN` is correct
- Check bot has message permissions in your server

**"Could not connect to oMLX":**
- Make sure oMLX is running: `mlx serve`
- Check `OMLX_HOST` in `.env` matches your oMLX location
- The bot automatically tries multiple API formats, but verify your oMLX server supports one of: `/v1/completions`, `/generate`, or `/v1/chat/completions`

**Request times out:**
- Large models take longer, increase wait time or use a smaller model
- Check your system resources (memory is critical for ML models)
- Response length is limited to 200 tokens to prevent memory issues

## Environment Variables

- `DISCORD_TOKEN` - Your Discord bot token (required)
- `OMLX_HOST` - oMLX server address (default: `http://localhost:8080`)
- `OMLX_MODEL` - Which model to use (default: `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`)
- `OMLX_API_KEY` - API key for authentication (optional)

## License

MIT
