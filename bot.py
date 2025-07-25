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

# List of monitoring channels
Monitoring_Channels = []

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Bot is live")

@bot.command(name='GetChannelStats')
async def get_channel_stats_command(ctx, channel_id: str):
    """Get channel statistics by channel ID."""
    stats = get_channel_stats(channel_id)
    stats_list = stats[0]

    embed = discord.Embed(title=stats_list['title'] ,color=discord.Color.blue())
    embed.add_field(name="Description", value=stats_list['description'], inline=False)
    embed.add_field(name="Subscribers", value=stats_list['subscriberCount'], inline=True)
    embed.add_field(name="Videos", value=stats_list['videoCount'], inline=True)
    embed.add_field(name="Views", value=stats_list['viewCount'], inline=True)

    await ctx.send(embed=embed)

@bot.command(name='AddChannel')
async def add_channel_command(ctx, channel_id: str):
    """Add a channel to the database (not implemented)."""
    Monitoring_Channels.append(channel_id)
    stats = get_channel_stats(channel_id)
    stats = stats[0]
    await ctx.send(f"Channel {stats['title']} added to the database.")
    print(Monitoring_Channels)

bot.run(token)