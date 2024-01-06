import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to get video ID from YouTube URL
def get_video_id(video_url):
    match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
    return match.group(1) if match else None

# Function to clean text (remove HTML tags)
def clean_text(text):
    return re.sub(r'<.*?>', '', text)

# Function to analyze sentiment of a comment
def analyze_sentiment(comment):
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"
# ... [previous parts of the code remain unchanged]

def retrieve_comments(video_id, api_key):
    all_comments = []
    initial_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100'
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(retrieve_comments_page, initial_url): initial_url}
        while future_to_url:
            for future in as_completed(future_to_url):
                comments, next_page_token = future.result()
                all_comments.extend(comments)
                # Commented out to avoid printing the count of retrieved comments
                # print(f"Retrieved {len(all_comments)} comments so far...")  
                if next_page_token and len(all_comments) < 10000:
                    next_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&pageToken={next_page_token}&maxResults=100'
                    future_to_url[executor.submit(retrieve_comments_page, next_url)] = next_url
                del future_to_url[future]
                if len(all_comments) >= 10000:
                    return all_comments[:10000]
    return all_comments

def analyze_comments_in_batch(comments, batch_size=100):
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            results = list(executor.map(analyze_sentiment, batch))
            for sentiment in results:
                sentiment_counts[sentiment] += 1
            
            # Print only the updated sentiment counts
            print(f"Total Positive Comments: {sentiment_counts['Positive']}, "
                  f"Total Negative Comments: {sentiment_counts['Negative']}, "
                  f"Total Neutral Comments: {sentiment_counts['Neutral']}")

  
    return sentiment_counts
def retrieve_comments_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        comments = []
        for item in data['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(clean_text(comment))
        return comments, data.get('nextPageToken')
    else:
        print('Failed to retrieve comments on this page, stopping.')
        return [], None

# Updated Function to retrieve up to 10,000 comments from a YouTube video
def retrieve_comments(video_id, api_key):
    all_comments = []
    initial_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100'
    
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        future_to_url = {executor.submit(retrieve_comments_page, initial_url): initial_url}
        while future_to_url:
            for future in as_completed(future_to_url):
                comments, next_page_token = future.result()
                all_comments.extend(comments)
                if next_page_token and len(all_comments) < 10000:
                    next_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&pageToken={next_page_token}&maxResults=100'
                    future_to_url[executor.submit(retrieve_comments_page, next_url)] = next_url
                del future_to_url[future]
                if len(all_comments) >= 10000:
                    return all_comments[:10000]
    return all_comments

# Input YouTube video URL
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'

    comments = retrieve_comments(video_id, api_key)

    if comments:
        sentiment_counts = analyze_comments_in_batch(comments)
        

        # Print the sentiment counts
        print(f"Total Positive Comments: {sentiment_counts['Positive']}")
        print(f"Total Negative Comments: {sentiment_counts['Negative']}")
        print(f"Total Neutral Comments: {sentiment_counts['Neutral']}")
    else:
        print("Failed to retrieve comments or no comments found.")
else:
    print('Video ID not found in the URL.')
