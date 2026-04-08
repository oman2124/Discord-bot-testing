# Quick Reference

## Getting Started

```bash
# 1. Setup bot (run once)
bash setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start Ollama (in another terminal)
ollama serve

# 4. Edit .env with your Discord token
nano .env

# 5. Run bot
python bot.py
```

## Bot Commands

| Command | Usage | Example |
|---------|-------|---------|
| `!ask` | Ask the AI a question | `!ask What is Python?` |
| `!model` | Show available models | `!model` |
| `!help_ollama` | Show help menu | `!help_ollama` |
| **Mention** | Ask naturally | `@bot explain quantum computing` |

## Common Ollama Models

```bash
# Recommended model for this setup
ollama pull qwen3.5:9b

# Fast models
ollama pull orca-mini

# Larger models (slower but better quality)
ollama pull llama2

# List installed models
ollama list
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
DISCORD_TOKEN=your_bot_token
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3.5:9b
```

## Troubleshooting

### Bot won't start
- ❌ `ModuleNotFoundError`: Run `pip install -r requirements.txt`
- ❌ `DISCORD_TOKEN not found`: Edit `.env` file with your token
- ❌ `ConnectionRefusedError`: Ollama not running, start with `ollama serve`

### Bot doesn't respond
- Check bot has message permissions in server settings
- Verify bot is online in Discord
- Check server console for error messages

### Slow responses
- Use a smaller Ollama model like `orca-mini` or `llama2`
- Check machine resources (CPU, RAM)
- Increase request timeout in bot.py

### "Could not connect to Ollama"
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# If it fails, start Ollama:
ollama serve
```

## File Structure

```
Discord bot testing/
├── bot.py              # Main bot code
├── .env                # Your configuration (keep private!)
├── .env.example        # Configuration template
├── requirements.txt    # Python dependencies
├── README.md          # Full documentation
├── ADVANCED.md        # Advanced features
├── setup.sh           # Setup script
└── .gitignore         # Git ignore rules
```

## Admin Commands (Add to bot.py)

```python
@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency"""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='status')
async def status(ctx):
    """Check Ollama connection"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{OLLAMA_HOST}/api/tags") as resp:
                if resp.status == 200:
                    await ctx.send("✅ Ollama is online")
                else:
                    await ctx.send("⚠️ Ollama returned status {resp.status}")
    except Exception:
        await ctx.send("❌ Ollama is offline")
```

## Performance Tips

1. **Use streaming models**: `neural-chat`, `orca-mini` are fast
2. **Increase timeout**: Large models need more time
3. **Monitor memory**: Larger models need more RAM
4. **Add caching**: Cache common questions to reduce load
5. **Limit concurrent requests**: Prevent server overload

## Security

- **Never commit `.env`**: It's in `.gitignore` for a reason
- **Restrict bot token**: Treat like password
- **Limit bot permissions**: Only give needed permissions
- **Monitor resource usage**: Prevent DoS attacks
