import requests
import re

# Replace with your own API key
api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'

# Replace with the YouTube video URL you want to retrieve comments from
video_url = 'https://www.youtube.com/watch?v=0bLptFf3EEE'

# Extract the video ID from the URL
match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
if match:
    video_id = match.group(1)
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'

    try:
        # Make an API request to retrieve comments
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            comments = data['items']

            # Iterate through the comments and display author and comment text
            for comment in comments:
                snippet = comment['snippet']['topLevelComment']['snippet']
                author = snippet['authorDisplayName']
                text = snippet['textDisplay']
                print(f' {author} -  {text}\n')
        else:
            print('Failed to retrieve comments. Check your API key and video ID.')
    except Exception as e:
        print(f'An error occurred: {e}')
else:
    print('Video ID not found in the URL.')
