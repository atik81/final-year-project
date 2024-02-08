from flask import Flask, request
from googleapiclient.discovery import build
from transformers import pipeline
from flask_cors import CORS
import os
import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app) 
# Initialize the sentiment analysis pipeline
analyzer = SentimentIntensityAnalyzer()
# Function to fetch YouTube comments using the YouTube Data API
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
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
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
      

# Function to analyze sentiment of comments
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
           


@app.route('/analyze_comments', methods=['GET'])
def analyze_comments_api():
    url = request.args.get('url', '')
    

    api_key = request.args.get('apiKey', os.environ.get('AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM'))  # Ensure you securely manage your API key

    if not api_key:
        return {"error": "API key is required."}, 400

    video_id = None
    try:
        video_id = url.split('=')[1]
    except IndexError:
        return {"error": "Invalid URL provided."}, 400

    comments = fetch_comments(video_id, api_key)
    if not comments:
        return {"error": "Could not fetch comments or no comments found."}, 500

    sentiment_results = analyze_sentiment_vadar(comments)
    return {"results": sentiment_results}, 200


if __name__ == '__main__':
    # It's a good practice to not include your actual API key in your script.
    # Consider using environment variables or other secure methods to handle them.
    app.run(debug=True)

