import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from youtube_functions import *

# Get environment variables
load_dotenv()
# Add your token here!
token = os.getenv('DISCORD_TOKEN')

CHANNEL_ID = 1397987625456898058
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Store a list of monitoring channels as dictionary with channel IDs and Latest video IDs
Monitoring_Channels = {}

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    my_loop.start()
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
    """Add a channel to the database with its latest video Id."""
    channel = bot.get_channel(CHANNEL_ID)
    
    latest_video = get_latest_uploaded_videos(channel_id, max_results=1)
    Monitoring_Channels[channel_id]=latest_video[0]['videoId']

    stats = get_channel_stats(channel_id)
    stats = stats[0]

    video_id = latest_video[0]['videoId']
    published_at = latest_video[0]['publishedAt']
    title = latest_video[0]['title']

    embed = discord.Embed(title=title, description=f"Latest video uploaded at {published_at}", color=discord.Color.green())
    embed.add_field(name="Video Link", value=f"https://www.youtube.com/watch?v={video_id}", inline=False)
    await channel.send(embed=embed) 

    await ctx.send(f"Channel {stats['title']} added to the database.")
    print(Monitoring_Channels)

@tasks.loop(minutes=5)
async def my_loop():
    """Check for new videos from monitored channels."""
    channel = bot.get_channel(CHANNEL_ID)

    for channel_id in Monitoring_Channels:
        latest_video = get_latest_uploaded_videos(channel_id, max_results=1)
        if latest_video:
            video = latest_video[0]
            if video['videoId'] != Monitoring_Channels[channel_id]:
                Monitoring_Channels[channel_id] = video['videoId']
                video_id = video['videoId']
                published_at = video['publishedAt']
                title = video['title']

                embed = discord.Embed(title=title, description=f"New video uploaded at {published_at}", color=discord.Color.green())
                embed.add_field(name="Video Link", value=f"https://www.youtube.com/watch?v={video_id}", inline=False)

                await channel.send(embed=embed)
            else:
                pass
            # Uncomment the following lines if you want to notify when no new videos are found  
                # await channel.send(f"No new videos found for channel ID: {channel_id}")
                # print(f"No new videos found for channel ID: {channel_id}")
bot.run(token)