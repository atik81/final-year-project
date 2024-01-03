import requests
import re
from concurrent.futures import ThreadPoolExecutor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji

api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'
analyzer = SentimentIntensityAnalyzer()
# Replace with your YouTube Data API key


class TextStyle:
    HEADER = '\033[95m'  # Light Purple
    OKBLUE = '\033[94m'  # Blue
    OKGREEN = '\033[92m'  # Green
    OKRED = '\033[91m'  # Red
    OKYELLOW = '\033[93m'  # Yellow
    ENDC = '\033[0m'  # Reset to default
    BIGGER = '\033[1M'


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
def analyze_sentiment_vader(comment):
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score > 0:
        return f'{TextStyle.OKGREEN}Positive{TextStyle.ENDC}'  # Green for positive
    elif compound_score < 0:
        return f'{TextStyle.OKRED}Negative{TextStyle.ENDC}'  # Red for negative
    else:
        return f'{TextStyle.OKBLUE}Neutral{TextStyle.ENDC}'  # Blue for neutral

def retrieve_comments(video_id, api_key, max_comments=10):
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'

        if next_page_token:
            video_comments_url += f'&pageToken={next_page_token}'
        video_comments_response = requests.get(video_comments_url)
        if video_comments_response.status_code == 200:
            data = video_comments_response.json()
            comments.extend(data.get('items', []))
            next_page_token = data.get('nextPageToken')
            if not next_page_token:
                break
    return comments[:max_comments]
def count_all_sentiments(video_id, api_key):
    sentiment_totals = {'positive': 0, 'negative': 0, 'neutral': 0}
    next_page_token = None

    while True:
        comments, next_page_token = retrieve_comments(video_id, api_key, next_page_token)
        if comments:
            for comment in comments:
                text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                cleaned_comment = clean_text(text)
                sentiment = analyze_sentiment_vader(cleaned_comment)

                if 'Positive' in sentiment:
                    sentiment_totals['positive'] += 1
                elif 'Negative' in sentiment:
                    sentiment_totals['negative'] += 1
                else:
                    sentiment_totals['neutral'] += 1

        if next_page_token is None:
            break

    return sentiment_totals

# Main script
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    try:
        sentiment_totals = count_all_sentiments(video_id, api_key)

        print(f"Total Positive Comments: {sentiment_totals['positive']}")
        print(f"Total Negative Comments: {sentiment_totals['negative']}")
        print(f"Total Neutral Comments: {sentiment_totals['neutral']}")

    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("Video ID not found in the URL.")
