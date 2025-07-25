import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from youtube_functions import *

# Get environment variables
load_dotenv()
# Add your token here!
token = os.getenv('DISCORD_TOKEN')

CHANNEL_ID = 1397987625456898058
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Bot is live")



bot.run(token)