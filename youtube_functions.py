import os
import json
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('YOUTUBE_API')


service = build('youtube', 'v3', developerKey=api_key)

def get_channel_stats(channel_id):
    '''Get channel statistics by channel ID.'''
    request = service.channels().list(
        part='snippet,contentDetails,statistics', id=channel_id
        )
    response = request.execute()

    #filter channel stats
    filtered_stats = []
    for item in response.get('items', []):
        filtered_stats.append({
            'channelId': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'subscriberCount': item['statistics'].get('subscriberCount', 'N/A'),
            'videoCount': item['statistics'].get('videoCount', 'N/A'),
            'viewCount': item['statistics'].get('viewCount', 'N/A')
        })
    return filtered_stats

def get_latest_uploaded_videos(channel_id, max_results=1):
    '''Get the latest videos uploaded by a specific channel.'''

    # Get the uploads playlist ID from the API response
    request = service.channels().list(
        part='contentDetails', id=channel_id
    )
    response = request.execute()
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get videos from the uploads playlist
    playlist_response = service.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=max_results
    ).execute()

    # filter and format the video data
    videos = []
    for item in playlist_response.get('items', []):
        snippet = item['snippet']
        videos.append({
            'videoId': snippet['resourceId']['videoId'],
            'publishedAt': snippet['publishedAt'],
            'title': snippet['title']
        })
    return videos


# Uncomment the following lines to run the script continuously
# Note: This will run indefinitely until stopped manually.

# channel_id = 'UCngIhBkikUe6e7tZTjpKK7Q'
# latest_video_id = None
# while True:
#     latest_video = get_latest_uploaded_videos(channel_id, max_results=1)
#     if latest_video:
#         latest_video = latest_video[0]
#         if latest_video['videoId'] != latest_video_id:
#             print("New video detected!")
#             print(json.dumps(get_latest_uploaded_videos(channel_id, max_results=1), indent=4, ensure_ascii=False))
#             latest_video_id = latest_video['videoId']
#         else:
#             print("No new video detected.")
#     # Check every 5 minutes
#     time.sleep(300)