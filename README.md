# Youtube-Transcript-Discord-Bot

## Overview

This project is a Discord bot that fetches YouTube channel statistics and notifies you in Discord when a new video is uploaded from a monitored channel.  
**Transcript fetching** will be added in a future version.

---

## Features

- Fetch YouTube channel statistics (title, description, subscriber count, video count, view count) via a Discord command.
- Add YouTube channels to a monitoring list via a Discord command.
- Automatically checks for new uploads every 5 minutes and posts a notification embed in your Discord server.
- Uses environment variables for API keys and Discord bot token.
- Modular code structure for easy extension (e.g., video transcripts).

---

## Setup

### Prerequisites

- Python 3.8+
- Discord bot token
- YouTube Data API v3 key

### Installation

1. Clone this repository.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Create a `.env` file in the project root with the following contents:
    ```
    DISCORD_TOKEN=your_discord_token_here
    YOUTUBE_API=your_youtube_api_key_here
    ```
4. Run the bot:
    ```sh
    python bot.py
    ```

---

## Usage

- Invite your bot to a Discord server.
- Use the command:
    ```
    !GetChannelStats <channel_id>
    ```
    Example:
    ```
    !GetChannelStats UCngIhBkikUe6e7tZTjpKK7Q
    ```
    The bot will reply with an embed containing the channel's statistics.

- Add a channel to monitor for new uploads:
    ```
    !AddChannel <channel_id>
    ```
    The bot will start monitoring this channel and post a notification in your server when a new video is uploaded.

---

## Roadmap

- [x] Notify when a new video is uploaded to a channel.
- [ ] Fetch and display video transcripts automatically.
- [ ] Add more notification and configuration options.

---

## Files

- `bot.py` — Main Discord bot logic.
- `youtube_functions.py` — Functions for interacting with the YouTube Data API.
- `requirements.txt` — Python dependencies.
- `.env` — Environment variables (not included, create your own).

---

## License

This project is for educational and