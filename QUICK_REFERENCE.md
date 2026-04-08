# Quick Reference

## Getting Started

```bash
# 1. Setup bot (run once)
bash setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Start oMLX (in another terminal)
mlx serve

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
| `!help_omlx` | Show help menu | `!help_omlx` |
| **Mention** | Ask naturally | `@bot explain quantum computing` |

## Common oMLX Models

```bash
# Fast models (recommended for Discord)
mlx pull deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
mlx pull microsoft/DialoGPT-medium

# Larger models (slower but better quality)
mlx pull meta-llama/Llama-2-7b-chat-hf

# List installed models
mlx list
```

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
DISCORD_TOKEN=your_bot_token
OMLX_HOST=http://localhost:8080
OMLX_MODEL=DeepSeek-R1-Distill-Qwen-1.5B
OMLX_API_KEY=your_api_key_here
```

## Troubleshooting

### Bot won't start
- ❌ `ModuleNotFoundError`: Run `pip install -r requirements.txt`
- ❌ `DISCORD_TOKEN not found`: Edit `.env` file with your token
- ❌ `ConnectionRefusedError`: oMLX not running, start with `mlx serve`

### Bot doesn't respond
- Check bot has message permissions in server settings
- Verify bot is online in Discord
- Check server console for error messages

### Slow responses
- Use smaller model: `mlx pull microsoft/DialoGPT-medium`
- Check machine resources (CPU, RAM)
- Increase request timeout in bot.py

### "Could not connect to oMLX"
```bash
# Test oMLX connection
curl -X POST http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", "prompt": "Hello", "max_tokens": 10}'

# If it fails, start oMLX:
mlx serve
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
    """Check oMLX connection"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{OMLX_HOST}/v1/models") as resp:
                await ctx.send("✅ oMLX is online")
    except:
        await ctx.send("❌ oMLX is offline")
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
