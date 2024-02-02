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

class TextStyle:
    HEADER = '\033[95m' # Light Purple
    OKBLUE = '\033[94m' # Blue
    OKGREEN = '\033[92m' #green
    OKRED = '\033[91m' #red
    
    OKYELLOW = '\033[93m' # YELLOW
    ENDC = '\033[0m' # reset to default
    BIGGER ='\033[1M'




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
def print_comments(comments):
    for comment in comments:
        try:
            snippet = comment['snippet']['topLevelComment']['snippet']
            author = snippet['authorDisplayName']
            text = snippet['textDisplay']
            cleaned_comment = clean_text(text)
            sentiment = analyze_sentiment_vader(cleaned_comment)
            formatted_author = f'{TextStyle.OKYELLOW}{author}{TextStyle.ENDC}'

            print(f'Author: {formatted_author}')
            print(f'Comment: {cleaned_comment}')
            print(f'Sentiment: {sentiment}')
            print('-------------------------')

        except KeyError as e:
            print(f"Error processing comment: {e}")

def print_all_comments(comments):
    global positive_count, negative_count, neutral_count
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        text = snippet['textDisplay']
        cleaned_comment = clean_text(text)
        sentiment = analyze_sentiment_vader(cleaned_comment)
        
        # Print each comment with its sentiment
        print(f'Comment: {cleaned_comment}\nSentiment: {sentiment}\n-------------------------')
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
    

def print_all_comments(comments):
    for comment in comments:
        snippet = comment['snippet']['topLevelComment']['snippet']
        text = snippet['textDisplay']
        cleaned_comment = clean_text(text)
        analyze_sentiment_vader_all(cleaned_comment)

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
    
    try:
        
        # Retrieve video comments
        video_comments_url = f'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}'
        video_comments_response = requests.get(video_comments_url)


        if video_comments_response.status_code == 200:

            data = video_comments_response.json()
            comments = data['items']
            comments = retrieve_comments(video_id,api_key)


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
                    print_comments_show_graph(comments)

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