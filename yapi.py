
import requests
import re
import spacy
import emoji
from concurrent.futures import ThreadPoolExecutor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()

api_key = 'AIzaSyCMQt_THIlXaS-pyHF_aeItcCPhse4p3Fg'

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
def analyze_sentiment_vader(comment):
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    

    if compound_score>= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Function to process a batch of comments
def process_comment_batch(comments):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    total_comments = len(comments)

    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        text = snippet['textDisplay']
        cleaned_comment = clean_text(text)
        sentiment = analyze_sentiment_vader(cleaned_comment)

        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Negative':
            negative_count += 1
        else:
            neutral_count += 1

    return positive_count, negative_count, neutral_count, total_comments

# Input YouTube video URL
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    try:
        total_comments_to_analyze =  input ('Enter the number of Comments to analyze try to get less then 10,000 comments for  quicker  result (e.g., 10000for 10,000 comments, "all" for all comments): ')
        if total_comments_to_analyze.lower() =='all':
            total_comments_to_analyze = float('inf')
        else :
            total_comments_to_analyze = int(total_comments_to_analyze)
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
                next_page_token = data.get('nextPageToken')

                if not next_page_token:
                    break
            else:
                print(f'Failed to retrieve comments. HTTP Status Code: {video_comments_response.status_code}')
                break

        # Adjust batch size and max workers as needed
        batch_size = 2000  # Increase the batch size
        max_workers = 8    # Increase the number of workers based on your system's capacity

        # Split comments into batches for parallel processing
        comment_batches = [all_comments[i:i+batch_size] for i in range(0, len(all_comments), batch_size)]

        # Process comment batches in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(process_comment_batch, comment_batches))

        # Aggregate results
        total_positive = sum(result[0] for result in results)
        total_negative = sum(result[1] for result in results)
        total_neutral = sum(result[2] for result in results)
        total_comments = sum(result[3] for result in results)

        # Print total sentiment counts and total comment count
        print(f'Total Positive Comments: {total_positive}')
        print(f'Total Negative Comments: {total_negative}')
        print(f'Total Neutral Comments: {total_neutral}')
        print(f'Total Comments: {total_comments}')

    except Exception as e:
        print(f'An error occurred: {e}')

else:
    print('Video ID not found in the URL.')
