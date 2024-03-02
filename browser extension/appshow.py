from flask import Flask, request
from googleapiclient.discovery import build
from transformers import pipeline
from flask_cors import CORS
import os
import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs



app = Flask(__name__)
CORS(app) 
# Initialize the sentiment analysis pipeline
analyzer = SentimentIntensityAnalyzer()
# Function to fetch YouTube comments using the YouTube Data API
def analyze_sentiment_vadar(comments):
    sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
    for comment in comments:
        # Analyze each comment sentiment
        sentiment = analyzer.polarity_scores(comment)
        compound_score = sentiment['compound']
        if compound_score >= 0.05:
            sentiment_counts['positive'] += 1
        elif compound_score <= -0.05:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1
    # Return the counts after analyzing all comments
    return sentiment_counts
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    nextPageToken =None
    try:
        while len(comments) < 10000:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,  # Max allowed by the API
                pageToken=nextPageToken,
                textFormat="plainText"
            ).execute()

            
            for item in response['items']:
                comment_snippet = item['snippet']['topLevelComment']['snippet']
                comment_text = comment_snippet['textDisplay']
                comment_author = comment_snippet['authorDisplayName']
                sentiment_score = analyzer.polarity_scores(comment_text)


    # You need to define a function analyze_sentiment that will return sentiment of the text
                comment = {
                    'author': comment_author,
                    'text': comment_text,
                    'sentiment': sentiment_score,
                    
                }

                comments.append(comment)
                if len(comments) >= 10000:
                    break
            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break
            
            
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
        return []
    
    return comments
      
def extract_video_id(url):
    parsed_url = urlparse(url)
    query_string = parse_qs(parsed_url.query)
    video_id = query_string.get("v", [None])[0]
    return video_id
# Function to analyze sentiment of comments

           


@app.route('/analyze_comments', methods=['GET'])
def analyze_comments_api():
    url = request.args.get('url', '')
    

    api_key = request.args.get('apiKey', os.environ.get('AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'))  # Ensure you securely manage your API key

    if not api_key:
        return {"error": "API key is required."}, 400

    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid URL provided."}, 400

    youtube = build('youtube', 'v3', developerKey=api_key)
    # fetch comments
    comments = fetch_comments(video_id, api_key)
    if not comments:
        return {"error": "Could not fetch comments or no comments found."}, 500
    
    # fetch video details 
    video_response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()
    if not video_response["items"]:
        return {"error": "Could not fetch video details."},500
    video_details = video_response["items"][0]
    video_title = video_details["snippet"]["title"]
    like_count = video_details["statistics"].get("likeCount",0)
    comment_count = video_details['statistics'].get("commentCount",0)
    # fetch channel details 
    channel_id = video_details["snippet"]["channelId"]
    channel_response = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    ).execute()
    if not channel_response['items']:
        return{"error", "Could not fetch channel details."},500
    channel_details= channel_response["items"][0]
    subscriber_count = channel_details["statistics"].get('subscriberCount',0)
    
    sentiment_results = analyze_sentiment_vadar(comments)
    sample_comments = comments[:3]  # Sending only the first 20 comments for brevity

    results ={
        "videoTitle": video_title,
        "likeCount": like_count,
        "commentCount": comment_count,
        "subscriberCount": subscriber_count,
        "sentimentResults": sentiment_results,
        "comments": sample_comments 

        
    }
    return {"results": results}, 200


if __name__ == '__main__':
    # It's a good practice to not include your actual API key in your script.
    # Consider using environment variables or other secure methods to handle them.
    app.run(debug=True)

