# YouTube Notification Discord Bot

## Overview
This Discord bot monitors YouTube channels and automatically notifies your Discord server when new videos are uploaded. It features robust error handling, automatic recovery, and comprehensive channel management capabilities. The bot is designed to run 24/7 on platforms like Render, using a lightweight Flask web server to maintain uptime.

---

## Features

### Core Functionality
- **Channel Monitoring:** Automatically checks for new video uploads every 5 minutes
- **Smart Notifications:** Posts rich embeds with video details when new content is detected
- **Channel Management:** Add, remove, and list monitored YouTube channels
- **Channel Statistics:** Fetch detailed YouTube channel analytics
- **Video Transcripts:** Extract and display video transcripts (when available)

### Advanced Features
- **Robust Error Handling:** Automatic loop recovery and error reporting
- **Manual Controls:** Admin commands for loop management and status monitoring
- **Multiple Channel Support:** Configure separate Discord channels for different notification types
- **Memory Persistence:** Maintains monitoring state during bot runtime
- **Rich Embeds:** Beautiful Discord embeds with thumbnails, timestamps, and formatted information

---

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/addchannel` | Start monitoring a YouTube channel | `/addchannel <channel_id>` |
| `/removechannel` | Stop monitoring a channel | `/removechannel <channel_id>` |
| `/listchannels` | View all monitored channels | `/listchannels` |
| `/getchannelstats` | Get channel statistics | `/getchannelstats <channel_id>` |
| `/transcript` | Fetch video transcript | `/transcript <video_id>` |
| `/status` | Check bot and loop status | `/status` |
| `/restartloop` | Manually restart monitoring loop | `/restartloop` |

---

## Setup

### Prerequisites
- Python 3.8+
- Discord bot token with appropriate permissions
- YouTube Data API v3 key
- Discord server with proper channel configuration

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd youtube-notification-discord-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file in the project root:
   ```env
   DISCORD_TOKEN=your_discord_token_here
   YOUTUBE_API=your_youtube_api_key_here
   ```

4. **Channel Configuration:**
   Update the channel IDs in `bot.py`:
   ```python
   CHANNEL_ID = 1397987625456898058              # Default notifications
   STATS_CHANNEL_ID = 1398427572001574962        # Channel statistics
   LATEST_VIDEO_CHANNEL_ID = 1398423889947922452 # New video notifications
   ```

5. **Run the bot:**
   ```bash
   python bot.py
   ```

### Discord Bot Permissions
Ensure your bot has the following permissions:
- Send Messages
- Use Slash Commands
- Embed Links
- Attach Files
- Read Message History

---

## Configuration

### Channel Setup
The bot uses three separate Discord channels for different purposes:

1. **Default Channel (`CHANNEL_ID`):** General bot status messages
2. **Stats Channel (`STATS_CHANNEL_ID`):** Channel statistics displays
3. **Latest Video Channel (`LATEST_VIDEO_CHANNEL_ID`):** New video notifications

### Monitoring Frequency
The bot checks for new videos every 5 minutes. This can be adjusted by modifying the `@tasks.loop(minutes=5)` decorator in the code.

---

## Deployment

### Render.com Deployment
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `python bot.py`
5. Add environment variables in the Render dashboard:
   - `DISCORD_TOKEN`
   - `YOUTUBE_API`

### Other Platforms
The bot includes `webserver.py` for platforms requiring HTTP endpoints. Ensure your hosting platform supports:
- Python 3.8+
- Persistent processes
- Environment variables
- Network access for Discord and YouTube APIs

---

## Error Handling & Recovery

The bot features comprehensive error handling:

- **Automatic Loop Recovery:** If the monitoring loop crashes, it automatically restarts
- **Individual Channel Error Isolation:** Issues with one channel don't affect others
- **Discord Notifications:** Error messages are sent to the configured channel
- **Graceful Degradation:** Bot continues operating even if some features fail
- **Manual Recovery Commands:** Admin commands for manual intervention

---

## File Structure

```
├── bot.py                  # Main Discord bot logic and commands
├── youtube_functions.py    # YouTube API interactions and transcript fetching
├── webserver.py           # Flask server for hosting platform compatibility
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create your own)
└── README.md             # This file
```

---

## API Rate Limits

- **YouTube API:** 10,000 quota units per day (default)
- **Discord API:** Built-in rate limiting handled by discord.py
- **Monitoring Frequency:** 5-minute intervals to conserve API quota

---

## Troubleshooting

### Common Issues

**Bot doesn't respond to commands:**
- Check bot permissions in Discord
- Verify the bot is online and slash commands are synced
- Ensure channel IDs are correct

**No new video notifications:**
- Verify YouTube channel IDs are correct
- Check API quota usage
- Use `/status` command to verify loop is running

**Transcript not available:**
- Not all videos have transcripts
- Some channels disable transcript access
- Auto-generated transcripts may not be available immediately

### Debug Commands
- `/status` - Check overall bot health
- `/restartloop` - Manually restart monitoring
- `/listchannels` - Verify monitored channels

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is for educational and personal use. Please respect YouTube's Terms of Service and API usage guidelines.

---

## Support

For issues and feature requests, please create an issue in the GitHub repository or refer to the troubleshooting section above.
