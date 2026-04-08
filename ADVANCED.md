# Advanced Features Guide

## 1. Streaming Responses (Long Responses)

For models that produce lengthy responses, you can implement streaming to send responses as they're generated:

```python
@bot.command(name='ask_stream')
async def ask_stream(ctx, *, question):
    """Ask a question with streaming response"""
    async with ctx.typing():
        try:
            url = f"{OMLX_HOST}/v1/completions"
            payload = {
                "model": OMLX_MODEL,
                "prompt": question,
                "max_tokens": 200,
                "temperature": 0.7,
                "stream": False
            }
            
            full_response = ""
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    async for line in resp.content:
                        data = json.loads(line)
                        full_response += data.get('response', '')
            
            if len(full_response) > 2000:
                chunks = [full_response[i:i+1900] for i in range(0, len(full_response), 1900)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(full_response)
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")
```

## 2. Custom System Prompts

Make the AI behave differently by setting system prompts:

```python
SYSTEM_PROMPTS = {
    "assistant": "You are a helpful Discord bot assistant.",
    "pirate": "You are a pirate. Respond in pirate speak!",
    "tutor": "You are a patient tutor. Explain concepts clearly."
}

@bot.command(name='ask_as')
async def ask_as(ctx, persona, *, question):
    """Ask with a specific persona"""
    if persona not in SYSTEM_PROMPTS:
        await ctx.send(f"Available personas: {', '.join(SYSTEM_PROMPTS.keys())}")
        return
    
    prompt = f"{SYSTEM_PROMPTS[persona]}\n\nUser question: {question}"
    response = await query_omlx(prompt)
    await ctx.send(response)
```

## 3. Chat History

Keep track of conversation context:

```python
conversation_history = {}

@bot.command(name='chat')
async def chat(ctx, *, message):
    """Have a conversation with context"""
    user_id = ctx.author.id
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    # Add user message to history
    conversation_history[user_id].append(f"User: {message}")
    
    # Build context from history
    context = "\n".join(conversation_history[user_id][-5:])  # Last 5 messages
    
    async with ctx.typing():
        response = await query_omlx(context)
        conversation_history[user_id].append(f"Assistant: {response}")
        await ctx.send(response)

@bot.command(name='clear_chat')
async def clear_chat(ctx):
    """Clear conversation history"""
    user_id = ctx.author.id
    if user_id in conversation_history:
        conversation_history[user_id] = []
    await ctx.send("✅ Chat history cleared")
```

## 4. Rate Limiting

Prevent spam and manage resources:

```python
from datetime import datetime, timedelta

user_last_query = {}
QUERY_COOLDOWN = 2  # seconds

@bot.command(name='ask')
async def ask(ctx, *, question):
    """Ask with rate limiting"""
    user_id = ctx.author.id
    now = datetime.now()
    
    if user_id in user_last_query:
        if now - user_last_query[user_id] < timedelta(seconds=QUERY_COOLDOWN):
            await ctx.send(f"⏳ Please wait before asking another question")
            return
    
    user_last_query[user_id] = now
    # ... rest of ask command
```

## 5. Model Switching

Allow users to switch between different models:

```python
current_model = OMLX_MODEL

@bot.command(name='switch_model')
async def switch_model(ctx, model_name):
    """Switch to a different oMLX model"""
    global current_model
    
    # For oMLX, we'll just set the model (no verification needed)
    current_model = model_name
    await ctx.send(f"✅ Switched to model: `{model_name}`")
```

## 6. Error Handling with Retry Logic

Add resilience to API calls:

```python
async def query_omlx_with_retry(prompt: str, max_retries: int = 3) -> str:
    """Query oMLX with retry logic"""
    for attempt in range(max_retries):
        try:
            response = await query_omlx(prompt)
            if "Error" not in response:
                return response
        except Exception as e:
            if attempt == max_retries - 1:
                return f"❌ Failed after {max_retries} attempts: {str(e)}"
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## 7. Command Cooldowns

Built-in Discord.py cooldown system:

```python
@bot.command(name='ask')
@commands.cooldown(1, 5, commands.BucketType.user)  # 1 use per 5 seconds per user
async def ask(ctx, *, question):
    # Your ask command code here
    pass

@ask.error
async def ask_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Please wait {error.retry_after:.1f}s before asking again")
```

## 8. Logging

Track bot activity:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.command(name='ask')
async def ask(ctx, *, question):
    logger.info(f"Query from {ctx.author}: {question[:50]}...")
    # ... rest of command
```

## Tips

- Use smaller models for faster responses (orca-mini, neural-chat)
- Implement caching for common questions
- Add embeds for better Discord formatting
- Use Discord's thread feature for long conversations
- Monitor bot response times and adjust timeout values
