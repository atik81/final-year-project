import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Analyzer and TextStyle class as before...


# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

class TextStyle:
    HEADER = '\033[95m' # Light Purple
    OKBLUE = '\033[94m' # Blue
    OKGREEN = '\033[92m' # Green
    OKRED = '\033[91m' # Red
    OKYELLOW = '\033[93m' # Yellow
    ENDC = '\033[0m' # Reset to default

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

# Updated function to analyze sentiment and keep track of counts
def analyze_sentiment_vader(comment, sentiment_counts):
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score > 0:
        sentiment_counts['positive'] += 1
        return f'{TextStyle.OKGREEN}Positive{TextStyle.ENDC}'
    elif compound_score < 0:
        sentiment_counts['negative'] += 1
        return f'{TextStyle.OKRED}Negative{TextStyle.ENDC}'
    else:
        sentiment_counts['neutral'] += 1
        return f'{TextStyle.OKBLUE}Neutral{TextStyle.ENDC}'

# Function to retrieve comments
def retrieve_comments(video_id, api_key, page_token=None):
    comments = []
    video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
    if page_token:
        video_comments_url += f'&pageToken={page_token}'
    response = requests.get(video_comments_url)
    if response.status_code == 200:
        data = response.json()
        comments.extend(data.get('items', []))
        next_page_token = data.get('nextPageToken', None)
        return comments, next_page_token
    else:
        return None, None

# Updated function to print comments and analyze sentiments
def print_comments(comments, sentiment_counts):
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        author = snippet['authorDisplayName']
        text = snippet['textDisplay']
        cleaned_comment = clean_text(text)
        sentiment = analyze_sentiment_vader(cleaned_comment, sentiment_counts)
        formatted_Author = f'{TextStyle.OKYELLOW}{author}{TextStyle.ENDC}'

        print(f'Author: {formatted_Author}')
        print(f'Comment: {cleaned_comment}')
        print(f'Sentiment: {sentiment}')
        print('-------------------------')

# Main part of the program
api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    try:
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}

        comments, next_page_token = retrieve_comments(video_id, api_key)
        print_comments(comments, sentiment_counts)

        while next_page_token is not None:
            see_more = input('Type "See More" to load more comments, or press Enter to exit: ')
            if see_more.lower() == 'see more':
                more_comments, next_page_token = retrieve_comments(video_id, api_key, next_page_token)
                print_comments(more_comments, sentiment_counts)
            else:
                break

        print(f'Total Positive Comments: {sentiment_counts["positive"]}')
        print(f'Total Negative Comments: {sentiment_counts["negative"]}')
        print(f'Total Neutral Comments: {sentiment_counts["neutral"]}')

    except Exception as e:
        print(f'An error occurred: {e}')
else:
    print('Video ID not found in the URL.')
