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

# Function to clean text (remove HTML tags and emojis)
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

# Input YouTube video URL
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    try:
        # Initialize sentiment counters and total comment count
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_comments = 0
        top_comments = []

        # Retrieve all video comments
        all_comments = []
        next_page_token = None

        while True:
            video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
            if next_page_token:
                video_comments_url += f'&pageToken={next_page_token}'
            
            video_comments_response = requests.get(video_comments_url)

            if video_comments_response.status_code == 200:
                data = video_comments_response.json()
                comments = data.get('items', [])
                all_comments.extend(comments)

                next_page_token = data.get('nextPageToken')

                if not next_page_token:
                    break

            else:
                print('Failed to retrieve comments. Check your API key and video ID.')
                break

        # Iterate through and analyze all comments
        for comment in all_comments:
            snippet = comment['snippet']['topLevelComment']['snippet']
            author = snippet['authorDisplayName']
            text = snippet['textDisplay']
            cleaned_comment = clean_text(text)
            sentiment = analyze_sentiment(cleaned_comment)

            # Update sentiment counters
            if sentiment == 'Positive':
                positive_count += 1
            elif sentiment == 'Negative':
                negative_count += 1
            else:
                neutral_count += 1

            # Count total comments
            total_comments += 1

            # Store comments for top sentiment analysis
            top_comments.append((author, cleaned_comment, sentiment))

        # Sort the top comments by sentiment score (positive sentiment first)
        top_comments.sort(key=lambda x: x[2] == 'Positive', reverse=True)
        top_comments = top_comments[:10]  # Select the top 10 comments

        # Print top sentiment comments
        print('Top 10  Sentiment Comments:')
        for i, (author, comment, sentiment) in enumerate(top_comments):
            print(f'{i + 1}. Author: {author}')
            print(f'   Comment: {comment}')
            print(f'   Sentiment: {sentiment}')
            print('-------------------')

        # Print total sentiment counts and total comment count
        print(f'Total Positive Comments: {positive_count}')
        print(f'Total Negative Comments: {negative_count}')
        print(f'Total Neutral Comments: {neutral_count}')
        print(f'Total Comments: {total_comments}')

    except Exception as e:
        print(f'An error occurred: {e}')

else:
    print('Video ID not found in the URL.')
