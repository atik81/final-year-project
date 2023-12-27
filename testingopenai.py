import requests
import re
from textblob import TextBlob
import emoji

api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'

# Function to get video ID from YouTube URL
def get_video_id(video_url):
    match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
    if match:
        return match.group(1)
    else:
        return None

# Function to clean text (remove HTML tags)
def clean_text(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text

# Function to analyze sentiment of a comment
def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    sentiment_score = analysis.sentiment.polarity
    if sentiment_score > 0:
        return 'Positive'
    elif sentiment_score < 0:
        return 'Negative'
    else:
        return 'Neutral'
    emojis = [c for c in comment if c in emoji.UNICODE_EMOJI]
    if len(emojis) > 0:
      sentiment += f'with Emojis: {" ".join(emojis)}'
    return sentiment
# Replace with your YouTube API key
api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'


# Input YouTube video URL
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    try:
        # Retrieve video comments
        video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'
        video_comments_response = requests.get(video_comments_url)

        if video_comments_response.status_code == 200:
            data = video_comments_response.json()
            comments = data['items']

            # Retrieve video details
            video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={api_key}'
            video_details_response = requests.get(video_details_url)

            if video_details_response.status_code == 200:
                video_data = video_details_response.json()['items'][0]['snippet']
                like_count = video_details_response.json()['items'][0]['statistics'].get('likeCount', 0)
                title = video_data['title']
                print(f'Video Title: {title}')
                print(f'Like Count: {like_count}')

                channel_id = video_data['channelId']

                # Retrieve channel details
                channel_details_url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={api_key}'
                channel_details_response = requests.get(channel_details_url)

                if channel_details_response.status_code == 200:
                    channel_details = channel_details_response.json()['items'][0]['snippet']
                    subscriber_count = channel_details_response.json()['items'][0]['statistics'].get('subscriberCount', 0)
                    print(f'Channel Title: {channel_details["title"]}')
                    print(f'Subscriber Count: {subscriber_count}')

                else:
                    print('Failed to retrieve channel details. Check your API key and channel ID.')

            else:
                print('Failed to retrieve video details. Check your API key and video ID.')

            # Iterate through and analyze comments
            for comment in comments:
                snippet = comment['snippet']['topLevelComment']['snippet']
                author = snippet['authorDisplayName']
                text = snippet['textDisplay']
                cleaned_comment = clean_text(text)
                sentiment = analyze_sentiment(cleaned_comment)
                print(f'Author: {author}')
                print(f'Comment: {cleaned_comment}')
                print(f'Sentiment: {sentiment}')
                print('-------------------')

        else:
            print('Failed to retrieve comments. Check your API key and video ID.')

    except Exception as e:
        print(f'An error occurred: {e}')

else:
    print('Video ID not found in the URL.')
