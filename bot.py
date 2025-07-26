import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
from youtube_functions import *
import webserver # using flask to run the bot on a web server
from datetime import datetime, timezone

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
    # error handling if the channel is not found
    if stats_channel is None:
        await interaction.response.send_message("Error: Bot cannot find the configured channel. Check channel ID and permissions.", ephemeral=True)
        return

    await stats_channel.send(embed=embed)
    await interaction.response.send_message(f"📊 Channel stats sent to {stats_channel.mention}")


@bot.tree.command(name='addchannel', description='Add a channel to the database with its latest video Id')
@app_commands.describe(channel_id="YouTube channel ID")
async def add_channel_command(interaction: discord.Interaction, channel_id: str):
    """Add a channel to the database with its latest video Id."""
    try:
        await interaction.response.defer(thinking=True, ephemeral=True)

        # Check if the channel ID is already being monitored
        if channel_id in Monitoring_Channels:
            await interaction.followup.send(f"Channel {channel_id} is already being monitored.", ephemeral=True)
            return

        channel = bot.get_channel(CHANNEL_ID)
        # error handling if the channel is not found
        if channel is None:
            await interaction.followup.send("Error: Bot cannot find the configured channel. Check channel ID and permissions.", ephemeral=True)
            return
        
        latest_video = get_latest_uploaded_videos(channel_id, max_results=1)
        if not latest_video:
            await interaction.followup.send("No videos found for this channel ID.", ephemeral=True)
            return

        Monitoring_Channels[channel_id] = latest_video[0]['videoId']

        stats = get_channel_stats(channel_id)
        if not stats:
            await interaction.followup.send("Could not fetch channel stats.", ephemeral=True)
            return
        stats = stats[0]

        video_id = latest_video[0]['videoId']
        published_at = latest_video[0]['publishedAt']
        title = latest_video[0]['title']
        thumbnail = latest_video[0]['thumbnail']

        embed = discord.Embed(title=title, description=f"Latest video uploaded by {stats['title']}", color=discord.Color.green())
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="Video Link", value=f"https://www.youtube.com/watch?v={video_id}", inline=False)
        embed.add_field(name="Video ID", value=video_id, inline=False)
        embed.timestamp = datetime.fromisoformat(published_at.replace("Z", "+00:00"))

        video_channel = bot.get_channel(LATEST_VIDEO_CHANNEL_ID)
        await channel.send(embed=embed)
        await interaction.followup.send(f"Latest videos will be added to {video_channel.mention}", ephemeral=True)
        print(Monitoring_Channels)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)
        print(f"Error in add_channel_command: {e}")

@bot.tree.command(name='removechannel', description='Remove a channel from the database')
@app_commands.describe(channel_id="YouTube channel ID") 
async def remove_channel_command(interaction: discord.Interaction, channel_id: str):
    """Remove a channel from the database."""
    if channel_id in Monitoring_Channels:
        del Monitoring_Channels[channel_id]
        await interaction.response.send_message(f"Channel {channel_id} removed from monitoring.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Channel {channel_id} not found in monitoring list.", ephemeral=True)


@bot.tree.command(name='listchannels', description='List all monitored channels')
async def list_channels_command(interaction: discord.Interaction):
    """List all monitored channels."""
    if not Monitoring_Channels:
        await interaction.response.send_message("No channels are currently being monitored.", ephemeral=True)
        return

    embed = discord.Embed(title="Monitored Channels", color=discord.Color.blue())
    for channel_id, video_id in Monitoring_Channels.items():
        embed.add_field(name=channel_id, value=f"Latest Video ID: {video_id}", inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name='transcript', description='Get the transcript of a YouTube video by video ID')
@app_commands.describe(video_id="YouTube video ID")
async def transcript_command(interaction: discord.Interaction, video_id: str):
    """Fetch and send the transcript of a YouTube video."""
    await interaction.response.defer(thinking=True, ephemeral=True)
    transcript_text = get_transcript(video_id)
    if not transcript_text:
        await interaction.followup.send("Transcript not available for this video.", ephemeral=True)
        return

    # Discord message limit is 2000 characters
    if len(transcript_text) < 1900:
        await interaction.followup.send(f"Transcript for `{video_id}`:\n```{transcript_text}```", ephemeral=True)
    else:
        # If too long, send as a text file
        filename = f"transcript_{video_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        await interaction.followup.send(
            content=f"Transcript for `{video_id}` is too long, sending as a file.",
            file=discord.File(filename),
            ephemeral=True
        )
        os.remove(filename)

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
                thumbnail = video['thumbnail']
                channel_name = video['channelName']

                embed = discord.Embed(title=channel_name, description=f"New video uploaded!", color=discord.Color.green())
                embed.set_thumbnail(url=thumbnail)
                embed.add_field(name="Title", value=title, inline=False)
                embed.add_field(name="Video Link", value=f"https://www.youtube.com/watch?v={video_id}", inline=False)
                embed.set_footer(text=f"Video ID: {video_id}")
                embed.timestamp = datetime.fromisoformat(published_at.replace("Z", "+00:00"))

                await channel.send(embed=embed)
                print(f'new video found for {channel_name}!')
            else:
                pass
            # Uncomment the following lines if you want to notify when no new videos are found  
                # await channel.send(f"No new videos found for channel ID: {channel_id}")
                # print(f"No new videos found for channel ID: {channel_id}")


webserver.keep_alive()  # Start the web server to keep the bot alive
bot.run(token)