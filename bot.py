import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from youtube_functions import *
import webserver # using flask to run the bot on a web server

# Get environment variables
load_dotenv()
token = os.getenv('DISCORD_TOKEN') # Add your token here!

# Channel Configuration
CHANNEL_ID = 1397987625456898058 # Default channel ID
STATS_CHANNEL_ID = 1398427572001574962 # Channel ID for stats
LATEST_VIDEO_CHANNEL_ID = 1398423889947922452 # Channel ID for latest video notifications

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Store a list of monitoring channels as dictionary with channel IDs and Latest video IDs
Monitoring_Channels = {}

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    channel = bot.get_channel(CHANNEL_ID)
    my_loop.start()
    await channel.send("Bot is live")


@bot.tree.command(name='getchannelstats', description='Get the latest uploaded videos from a channel by channel ID')
@app_commands.describe(channel_id="YouTube channel ID")
async def get_channel_stats_command(interaction: discord.Interaction, channel_id: str):
    """Get channel statistics by channel ID."""
    stats = get_channel_stats(channel_id)
    stats_list = stats[0]

    embed = discord.Embed(title=stats_list['title'] ,color=discord.Color.blue())
    embed.add_field(name="Description", value=stats_list['description'], inline=False)
    embed.add_field(name="Subscribers", value=stats_list['subscriberCount'], inline=True)
    embed.add_field(name="Videos", value=stats_list['videoCount'], inline=True)
    embed.add_field(name="Views", value=stats_list['viewCount'], inline=True)

    stats_channel = bot.get_channel(STATS_CHANNEL_ID)
    await stats_channel.send(embed=embed)
    await interaction.response.send_message(f"📊 Channel stats sent to {stats_channel.mention}")


@bot.tree.command(name='addchannel', description='Add a channel to the database with its latest video Id')
@app_commands.describe(channel_id="YouTube channel ID")
async def add_channel_command(interaction: discord.Interaction, channel_id: str):
    """Add a channel to the database with its latest video Id."""
    channel = bot.get_channel(CHANNEL_ID)
    
    # When adding a channel, we also fetch the latest video ID
    latest_video = get_latest_uploaded_videos(channel_id, max_results=1)
    Monitoring_Channels[channel_id]=latest_video[0]['videoId']

    # Get the channel stats
    stats = get_channel_stats(channel_id)
    stats = stats[0]

    # Get the latest video details
    video_id = latest_video[0]['videoId']
    published_at = latest_video[0]['publishedAt']
    title = latest_video[0]['title']

    embed = discord.Embed(title=title, description=f"Latest video uploaded at {published_at}", color=discord.Color.green())
    embed.add_field(name="Channel Name", value=stats['title'], inline=False)
    embed.add_field(name="Video Link", value=f"https://www.youtube.com/watch?v={video_id}", inline=False)
    
    video_channel = bot.get_channel(LATEST_VIDEO_CHANNEL_ID)
    await channel.send(embed=embed)
    await interaction.response.send_message(f"{stats['title']} Channel added to the database. \nLatest videos will be added to {video_channel.mention}")
    print(Monitoring_Channels)


@tasks.loop(minutes=5)
async def my_loop():
    """Check for new videos from monitored channels."""
    channel = bot.get_channel(LATEST_VIDEO_CHANNEL_ID)

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


webserver.keep_alive()  # Start the web server to keep the bot alive
bot.run(token)