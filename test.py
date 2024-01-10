import requests
import re 
from concurrent.futures import ThreadPoolExecutor, as_completed
from vaderSentiment. vaderSentiment import SentimentIntensityAnalyzer
import os 
import time
import sys
import matplotlib.pyplot as plt
import numpy as numpy
from IPython.display import clear_output



analyzer = SentimentIntensityAnalyzer()


def get_video_id(video_url):
      match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
      return  match.group(1) if match else None
    
def clean_text(text):
  return re.sub(r'<.*?>', '', text)

def analyze_sentiment(comment):
  sentiment = analyzer.polarity_scores(comment)
  compound_score = sentiment['compound']
  if compound_score >= 0.05:
    return "Positive"
  elif compound_score <= -0.05:
    return "Negative"
  else:
    return "Neutral"


def analyze_comments_in_batch(comments, batch_size=1000):
  sentiment_counts = {'Positive': 0, 'Negative': 0,'Neutral': 0} 
  with ThreadPoolExecutor(max_workers=20) as executor:
    for i in range(0, len(comments), batch_size):
      for i in range(0, len(comments), batch_size):
        batch = comments[i:i + batch_size]
        results = list(executor.map(analyze_sentiment, batch))
        for sentiment in results:
          sentiment_counts[sentiment] += 1
  return sentiment_counts
def retrieve_comments_page(url):
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    comments = [clean_text(item['snippet']['topLevelComment']['snippet']['textDisplay']) for item in  data['items']]
    return comments, data.get('nextPageToken')
  else:
    return [], None
# ...

def retrieve_comments(video_id, api_key, page_token=None, max_comments=5000):
    comments = []
    while len(comments) < max_comments:
        video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100'
        if page_token:
            video_comments_url += f'&pageToken={page_token}'
        response = requests.get(video_comments_url)
        if response.status_code == 200:
            data = response.json()
            comments.extend(data.get('items', []))
            page_token = data.get('nextPageToken', None)
            if not page_token:
                break
        else:
            break

    return comments[:max_comments]

# ...
video_url = input('Input Youtube URL: ')
video_id = get_video_id(video_url)
api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'

if video_id:
    try:
        # Retrieve the first batch of comments
        comments, next_page_token = retrieve_comments(video_id, api_key)
        positive_count, negative_count, neutral_count = print_comments(comments)

        # Retrieve more comments if they are available
        while next_page_token is not None:
            see_more = input('Type "See More" to load more comments, or press Enter to exit: ')
            if see_more.lower() == 'see more':
                more_comments, next_page_token = retrieve_comments(video_id, api_key, next_page_token)
                pos, neg, neu = print_comments(more_comments)
                positive_count += pos
                negative_count += neg
                neutral_count += neu
            else:
                break

        # Print totals after processing all comments
        print(f'Total Positive Comments: {positive_count}')
        print(f'Total Negative Comments: {negative_count}')
        print(f'Total Neutral Comments: {neutral_count}')

    except Exception as e:
        print(f'An error occurred: {e}')

# ...
