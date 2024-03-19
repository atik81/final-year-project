import requests
import re
from concurrent.futures import ThreadPoolExecutor
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'
analyzer = SentimentIntensityAnalyzer()

class TextStyle:
    HEADER = '\033[95m' # Light Purple
    OKBLUE = '\033[94m' # Blue
    OKGREEN = '\033[92m' #green
    OKRED = '\033[91m' #red
    
    OKYELLOW = '\033[93m' # YELLOW
    ENDC = '\033[0m' # reset to default
    BIGGER ='\033[1M'


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
def analyze_sentiment_vader_all(comment):
    global positive_count, negative_count, neutral_count
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score > 0:
        positive_count += 1

    elif compound_score < 0:
        negative_count += 1

    else:
        neutral_count += 1
def analyze_comments(comments):
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    for comment in comments:
        sentiment = analyze_sentiment_vader(comment)
        sentiment_counts[sentiment] += 1
    return sentiment_counts
# Function to analyze sentcaiment of a comment
def analyze_sentiment_vader(comment):
    global positive_count, negative_count, neutral_count
    sentiment = analyzer.polarity_scores(comment)
    compound_score = sentiment['compound']
    if compound_score > 0:
        positive_count += 1
        return  f'{TextStyle.OKGREEN}Positive{TextStyle.ENDC}'  # Green for positive

    elif compound_score < 0:
        negative_count += 1

        return f'{TextStyle.OKRED}Negative{TextStyle.ENDC}'
    else:
        neutral_count += 1

        return f'{TextStyle.OKBLUE}Neutral{TextStyle.ENDC}'
    
def retrieve_comments(video_id, api_key, page_token=None , max_comments =10):
    comments = []
    video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'
    if page_token:
        video_comments_url += f'&pageToken={page_token}'
    response = requests.get(video_comments_url)
    if response.status_code ==200:
        data = response.json()
        comments.extend(data.get('items', []))
        next_page_token = (data.get('nextPageToken', None))
        return comments, next_page_token
    else:
        return None, None
    

def print_comments(comments):
    for comment in comments:
                snippet = comment['snippet']['topLevelComment']['snippet']
                author = snippet['authorDisplayName']
                text = snippet['textDisplay']
                cleaned_comment = clean_text(text)
                sentiment = analyze_sentiment_vader(cleaned_comment)
                formatted_Author = f'{TextStyle.OKYELLOW}{author}{TextStyle.ENDC}'


                print(f'Author: {formatted_Author}')
                print(f'Comment: {cleaned_comment}')
                print(f'Sentiment: {sentiment}')
                print('-------------------------')
def print_all_comments(comments):
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        text = snippet['textDisplay']
        cleaned_comment = clean_text(text)
        analyze_sentiment_vader_all(cleaned_comment)
# Input YouTube video URL
video_url = input('Input YouTube URL: ')
video_id = get_video_id(video_url)

if video_id:
    
    try:
        positive_count =0
        negative_count = 0 
        neutral_count =0
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
                comment_count = video_details_response.json()['items'][0]['statistics'].get('commentCount', 0)

                title = video_data['title']
                formatted_title = f'{TextStyle.HEADER}{title}{TextStyle.ENDC}'
                formatted_like_count = f'{TextStyle.OKGREEN}{like_count}{TextStyle.ENDC}'
                formatted_comment_count = f'{TextStyle.OKGREEN}{comment_count}{TextStyle.ENDC}'

                
                print(f'Video Title: {formatted_title}')
                print(f'Like Count: {formatted_like_count}')
                print(f'Comment Count: {formatted_comment_count} ')

                channel_id = video_data['channelId']

                # Retrieve channel details
                channel_details_url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={channel_id}&key={api_key}'
                channel_details_response = requests.get(channel_details_url)
                 
                if channel_details_response.status_code == 200:
                    channel_details = channel_details_response.json()['items'][0]['snippet']
                    subscriber_count = channel_details_response.json()['items'][0]['statistics'].get('subscriberCount', 0)
                    title = channel_details['title']

                    formatted_title = f'{TextStyle.HEADER}{title}{TextStyle.ENDC}'
                    formatted_subscriber_count = f'{TextStyle.OKGREEN}{comment_count}{TextStyle.ENDC}'


                    
                    print(f'Channel Title: {formatted_title}')
                    print(f'Subscriber Count: {formatted_subscriber_count}')

                else:
                    print('Failed to retrieve channel details. Check your API key and channel ID.')

            else:
                print('Failed to retrieve video details. Check your API key and video ID.')

            # Iterate through and analyze comments
            
            

        else:
            print('Failed to retrieve comments. Check your API key and video ID.')
        
        
        comments, next_page_token = retrieve_comments(video_id, api_key)
        print_comments(comments)
        
        while next_page_token is not None:
            see_more = input('Type "See More" to load more comments, or press Enter to exit: ')
            if see_more.lower() == 'see more' :
                more_comments, next_page_token = retrieve_comments(video_id, api_key, next_page_token)
                print_comments(more_comments)
            else:
                break
        
        print_all_comments(comments)

# Print totals after processing all comments
        print(f'Total Positive Comments: {positive_count}')
        print(f'Total Negative Comments: {negative_count}')
        print(f'Total Neutral Comments: {neutral_count}')

    except Exception as e:
        print(f'An error occurred: {e}')

else:
    print('Video ID not found in the URL.')
