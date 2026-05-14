import discord
from discord.ext import commands
import aiohttp
import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Check Python version
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
LOG_FILE = os.getenv("AI_LOG_FILE", "ai_interactions.log")

def log_interaction(message_text: str, response_text: str, source: str = "unknown") -> None:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = (
        f"[{timestamp}] Source: {source}\n"
        f"Message: {message_text}\n"
        f"AI Response: {response_text}\n"
        "---\n"
    )
    print(log_entry, end="")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"⚠️ Failed to write log file: {e}")

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🔗 Connected to Ollama at: {OLLAMA_HOST}')
    print(f'🤖 Using model: {OLLAMA_MODEL}')

@bot.command(name='ask')
async def ask(ctx, *, question):
    """Ask a question to the Ollama AI model"""
    async with ctx.typing():
        try:
            # Show that bot is thinking
            response_text = await query_ollama(question)
            log_interaction(question, response_text, source="ask command")
            
            # Split response if too long for Discord (2000 char limit)
            if len(response_text) > 2000:
                chunks = [response_text[i:i+1900] for i in range(0, len(response_text), 1900)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(response_text)
                
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='model')
async def model(ctx):
    """Show current model information"""
    try:
        await ctx.send(f"**Current Model:** `{OLLAMA_MODEL}`\n**Ollama Host:** {OLLAMA_HOST}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='help_ollama')
async def help_ollama(ctx):
    """Show help for Ollama bot commands"""
    embed = discord.Embed(title="🤖 Ollama Bot Help", color=discord.Color.blue())
    embed.add_field(name="!ask <question>", value="Ask the AI model a question", inline=False)
    embed.add_field(name="!model", value="Show current model information", inline=False)
    embed.add_field(name="!help_ollama", value="Show this help message", inline=False)
    embed.set_footer(text=f"Connected to {OLLAMA_HOST}")
    await ctx.send(embed=embed)

async def query_ollama(prompt: str) -> str:
    """Query the Ollama API and return the response"""
    url = f"{OLLAMA_HOST}/api/generate"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', 'No response received')
                else:
                    return f"Error from Ollama: Status {resp.status}"
    except aiohttp.ClientConnectorError:
        return "❌ Could not connect to Ollama. Make sure it's running at " + OLLAMA_HOST
    except asyncio.TimeoutError:
        return "❌ Request timed out. The model is taking too long to respond."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Handle message content
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check if bot is mentioned and respond
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            response = await query_ollama(message.content)
            log_interaction(message.content, response, source="mention reply")
            if len(response) > 2000:
                chunks = [response[i:i+1900] for i in range(0, len(response), 1900)]
                for chunk in chunks:
                    await message.reply(chunk)
            else:
                await message.reply(response)
    
    await bot.process_commands(message)

def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("❌ DISCORD_TOKEN not found in .env file")
    
    bot.run(token)

if __name__ == "__main__":
    main()
