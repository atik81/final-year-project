import requests
import re
from dotenv import load_dotenv

def configure():
    load_dotenv()
api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'

def get_video_id(video_url):
    match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
    if match:
        return match.group(1)
    else:
        return None
def video_and_channel_details(video_url, api_key):
    video_id = get_video_id(video_url)
    if video_id:
        try:
            details = {}

            # Get video details
            video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={creds.api_key}'
            video_response = requests.get(video_details_url)

            if video_response.status_code == 200:
                video_data = video_response.json()['items'][0]
                details['video_title'] = video_data['snippet']['title']
                details['like_count'] = video_data['statistics'].get('likeCount', 0)

                # Get channel details
                channel_id = video_data['snippet']['channelId']
                channel_url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={creds.api_key}'
                channel_response = requests.get(channel_url)

                if channel_response.status_code == 200:
                    channel_data = channel_response.json()['items'][0]
                    details['channel_title'] = channel_data['snippet']['title']
                    details['subscriber_count'] = channel_data['statistics'].get('subscriberCount', 0)

                return details
            else:
                print('Failed to retrieve video details. Check your API key and video ID.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Video ID not found in the URL.')
    return {}
def fetch_comments(video_url, api_key):
    video_id = get_video_id(video_url)
    if video_id:
        try:
            comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'
            response = requests.get(comments_url)
            if response.status_code == 200:
                data = response.json()
                comments = data['items']
                return comments
            else:
                print('Failed to retrieve comments. Check your API key and video ID.')
        except Exception as e:
            print(f'An error occurred: {e}')
    else:
        print('Video ID not found in the URL.')
    return []

# Usage Example


