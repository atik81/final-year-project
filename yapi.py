import requests
import re

def get_video_id(video_url):
    match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
    if match:
        return match.group(1)
    else:
        return None

# Youtube API key
api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'

# Replace with the YouTube video URL you want to retrieve comments from
video_url = input('input youtube url:')
video_id = get_video_id(video_url)

# Extract the video ID from the URL
if video_id:

    try:
        # Make an API request to retrieve comments
        video_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'
        video_response = requests.get(video_url)
        

        if video_response.status_code == 200:
            data = video_response.json()
            comments = data['items']

        if video_response.status_code == 200:
            video_data = video_response.json()['items'][0]['snippet']
          
            

            # Get video details
            video_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}'
            video_response = requests.get(video_url)

            if video_response.status_code == 200:
                video_data = video_response.json()['items'][0]['statistics']
                like_count = video_data.get('likeCount', 0)
                title = video_response.json()['items'][0]['snippet']['title']
                print('\033[91m\033[1m' + f'Video Title: {title}' + '\033[0m')

                print('\033[91m\033[1m' + f'Like Count: {like_count}'  + '\033[0m')

                channel_id = video_response.json()['items'][0]['snippet']['channelId']

                # Get channel details
                channel_url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={api_key}'
                channel_response = requests.get(channel_url)

                if channel_response.status_code == 200:
                    channel_details = channel_response.json()['items'][0]['snippet']
                    subscriber_count = channel_response.json()['items'][0]['statistics']['subscriberCount']
                    
                    print('\033[91m\033[1m' + f'Channel Title: {channel_details["title"]}'+ '\033[0m')
                    print('\033[91m\033[1m' + f'Subscriber Count: {subscriber_count}'+ '\033[0m')

                else:
                    print('Failed to retrieve channel details. Check your API key and channel ID.')

            else:
                print('Failed to retrieve video details. Check your API key and video ID.')
                # Iterate through the comments and display author and comment text
          

            # Iterate through the comments and display the specified number
            

# Iterate through the comments and display the specified number
            for comment in comments:
                
                snippet = comment['snippet']['topLevelComment']['snippet']
                author = snippet.get('authorDisplayName', 'Unknown Author')
                text = snippet.get('textDisplay', 'No text')
                print(f'{author} - {text}\n')

                
            for comment in comments:
                snippet = comment['snippet']['topLevelComment']['snippet']
                author = snippet['authorDisplayName']
                text = snippet['textDisplay']
                print(f' {author} -  {text}\n')
                print(f'{author} - {text}\n')

        else:
            print('Failed to retrieve comments. Check your API key and video ID.')

    except Exception as e:
        print(f'An error occurred: {e}')

else:
    print('Video ID not found in the URL.')
