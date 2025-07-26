# Youtube-Transcript-Discord-Bot

## Overview

This Discord bot monitors YouTube channels and notifies your Discord server when a new video is uploaded.  
You can add or remove channels from monitoring, list all monitored channels, fetch channel statistics, and get the transcript of any YouTube video (if available).  
The bot is designed to run 24/7 on platforms like Render, using a lightweight Flask web server to keep the process alive.

---

## Features

- **Add a channel:** `/addchannel <channel_id>` — Start monitoring a YouTube channel for new uploads.
- **Remove a channel:** `/removechannel <channel_id>` — Stop monitoring a channel.
- **List channels:** `/listchannels` — See all currently monitored channels.
- **Fetch channel stats:** `/getchannelstats <channel_id>` — Get YouTube channel statistics (title, description, subscriber count, video count, view count).
- **Get transcript:** `/transcript <video_id>` — Fetch and display the transcript of a YouTube video (as a message or file, depending on length).
- **Automatic notifications:** Posts an embed in your Discord server when a new video is uploaded.
- **Hosted on Render:** Uses a Flask web server (`webserver.py`) to keep the bot alive on hosting platforms.

---

## Setup

### Prerequisites

- Python 3.8+
- Discord bot token
- YouTube Data API v3 key
- (For hosting) A Render.com account or similar

### Installation

1. Clone this repository.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root with:
    ```
    DISCORD_TOKEN=your_discord_token_here
    YOUTUBE_API=your_youtube_api_key_here
    ```
4. (If hosting) Make sure your environment variables are set in your Render dashboard.
5. Run the bot locally:
    ```sh
    python bot.py
    ```
   Or deploy to Render following their Python/Flask deployment instructions.

---

## Usage

- **Add a channel to monitor:**
    ```
    /addchannel <channel_id>
    ```
- **Remove a channel from monitoring:**
    ```
    /removechannel <channel_id>
    ```
- **List all monitored channels:**
    ```
    /listchannels
    ```
- **Get channel statistics:**
    ```
    /getchannelstats <channel_id>
    ```
- **Get transcript of a video:**
    ```
    /transcript <video_id>
    ```

The bot will automatically check for new uploads every 5 minutes and post a notification in your configured Discord channel.

---

## Files

- `bot.py` — Main Discord bot logic and commands.
- `youtube_functions.py` — Functions for interacting with the YouTube Data API and fetching transcripts.
- `webserver.py` — Flask server to keep the bot alive on Render.
- `requirements.txt` — Python dependencies.
- `.env` — Environment variables (not included, create your own).

---

## License

This project is for educational and personal use.
