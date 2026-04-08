import discord
from discord.ext import commands
import aiohttp
import asyncio
import os
import sys
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

# oMLX configuration
OMLX_HOST = os.getenv("OMLX_HOST", "http://localhost:8080")
OMLX_MODEL = os.getenv("OMLX_MODEL", "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
OMLX_API_KEY = os.getenv("OMLX_API_KEY")

@bot.event
async def on_ready():
    print(f'✅ Bot logged in as {bot.user}')
    print(f'🔗 Connected to oMLX at: {OMLX_HOST}')
    print(f'🤖 Using model: {OMLX_MODEL}')

@bot.command(name='ask')
async def ask(ctx, *, question):
    """Ask a question to the oMLX AI model"""
    async with ctx.typing():
        try:
            # Show that bot is thinking
            response_text = await query_omlx(question)
            
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
        # For oMLX, we'll just show the current model since the API structure is different
        await ctx.send(f"**Current Model:** `{OMLX_MODEL}`\n**oMLX Host:** {OMLX_HOST}")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

@bot.command(name='help_omlx')
async def help_omlx(ctx):
    """Show help for oMLX bot commands"""
    embed = discord.Embed(title="🤖 oMLX Bot Help", color=discord.Color.blue())
    embed.add_field(name="!ask <question>", value="Ask the AI model a question", inline=False)
    embed.add_field(name="!model", value="Show current model information", inline=False)
    embed.add_field(name="!help_omlx", value="Show this help message", inline=False)
    embed.set_footer(text=f"Connected to {OMLX_HOST}")
    await ctx.send(embed=embed)

async def query_omlx(prompt: str) -> str:
    """Query the oMLX API and return the response"""
    # Try different API endpoints that oMLX might support
    endpoints = [
        (f"{OMLX_HOST}/v1/completions", {
            "model": OMLX_MODEL,
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.7,
            "stream": False
        }),
        (f"{OMLX_HOST}/generate", {
            "model": OMLX_MODEL,
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.7
        }),
        (f"{OMLX_HOST}/v1/chat/completions", {
            "model": OMLX_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.7
        })
    ]
    
    for url, payload in endpoints:
        try:
            headers = {"Content-Type": "application/json"}
            if OMLX_API_KEY:
                headers["Authorization"] = f"Bearer {OMLX_API_KEY}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        # Try different response formats
                        if 'choices' in data and data['choices']:
                            choice = data['choices'][0]
                            if 'text' in choice:
                                return choice['text']
                            elif 'message' in choice and 'content' in choice['message']:
                                return choice['message']['content']
                        elif 'response' in data:
                            return data['response']
                        elif 'generated_text' in data:
                            return data['generated_text']
                        else:
                            return 'Response received but format not recognized'
                    
                    # If this endpoint returns 404, try the next one
                    if resp.status == 404:
                        continue
                    else:
                        return f"Error from oMLX ({url}): Status {resp.status}"
        
        except aiohttp.ClientConnectorError:
            return "❌ Could not connect to oMLX. Make sure it's running at " + OMLX_HOST
        except asyncio.TimeoutError:
            return "❌ Request timed out. The model is taking too long to respond."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    return "❌ No compatible oMLX API endpoint found. Please check your oMLX server configuration."

# Handle message content
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check if bot is mentioned and respond
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            response = await query_omlx(message.content)
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
