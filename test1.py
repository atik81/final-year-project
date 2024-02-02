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

def retrieve_comments(video_id, api_key):
  all_comments = []
  initial_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&maxResults=100'

  with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_url ={executor.submit(retrieve_comments_page, initial_url): initial_url}
    while future_to_url :
      for future in  as_completed(future_to_url):
        comments, next_page_token = future.result()
        all_comments.extend(comments)
        if next_page_token and len(all_comments) < 10000:
          next_url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&textFormat=plainText&part=snippet&videoId={video_id}&pageToken={next_page_token}&maxResults=100'

          future_to_url[executor.submit(retrieve_comments_page, next_url)] = next_url
        del future_to_url[future]
        if  len(all_comments) >= 10000:
          return all_comments[:10000]
  return all_comments
def print_comments_show_graph(comments):
    global positive_count, negative_count, neutral_count
    positive_count, negative_count, neutral_count = 0, 0, 0

    for comment in comments:
        sentiment = analyze_sentiment(comment)

        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Negative':
            negative_count += 1
        else:
            neutral_count += 1

    # Print the final counts
    print(f'Total Positive Comments: {positive_count}')
    print(f'Total Negative Comments: {negative_count}')
    print(f'Total Neutral Comments: {neutral_count}')
    
    
    sentiment = ['Positive', 'Negative', 'Neutral' ]
    counts = [positive_count,negative_count,neutral_count]
    total_comments = positive_count + negative_count + neutral_count
    percentages = [count / total_comments for count in [positive_count, negative_count, neutral_count]]

    
    plt.bar(sentiment,percentages, color=['green','red','blue'])
    plt.xlabel('sentiment')
    plt.ylabel('Percentage  of comments')
    plt.title('Sentiment analysis of YouTube Comments')
    plt.show()
video_url = input('Input Youtube URL: ')
video_id = get_video_id(video_url)
api_key = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'

if video_id: 
  comments = retrieve_comments(video_id,api_key)
  if comments:
    print_comments_show_graph(comments)
  else:
    print('Failed to retrieve or no comments found. ')
else: 
  print('Video ID not found in the url.')