from flask import Flask, request,jsonify
from googleapiclient.discovery import build
from transformers import pipeline
from flask_cors import CORS
import numpy as np
import os
import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
from waitress import serve
from googleapiclient.discovery import build
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
#environment variable 

API_key=os.getenv("API_key")


app = Flask(__name__)
CORS(app) 
analyzer = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def preprocess_text(text):
    """Simple preprocessing on the text to clean it up before summarization."""
    text = text.replace('\n', ' ').replace('\r', '')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_video_description(video_id):
    """Fetch the video description using YouTube Data API."""
    youtube = build('youtube', 'v3', developerKey=API_key)
    response = youtube.videos().list(part='snippet', id=video_id).execute()
    items = response.get('items')
    if not items:
        return None
    return items[0]['snippet']['description']

def summarize_text(text):
    """Generate a summary for the given text."""
    clean_text = preprocess_text(text)
    summary = summarizer(clean_text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

@app.route('/summarize_video', methods=['GET'])
def summarize_video():
    """API endpoint to summarize YouTube video descriptions."""
    url = request.args.get('url')
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v', [None])[0]

    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL provided.'}), 400

    description = get_video_description(video_id)
    if not description:
        return jsonify({'error': 'Video description not found.'}), 404

    summary = summarize_text(description)
    return jsonify({'summary': summary})
####################################################
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
      
def extract_video_id(url):
    parsed_url = urlparse(url)
    query_string = parse_qs(parsed_url.query)
    video_id = query_string.get("v", [None])[0]
    return video_id
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
           


def get_video_summary(video_id):
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=API_key)
    
    # Fetch video details
    request = youtube.videos().list(
        part="snippet",  # Retrieve the snippet part which contains the description
        id=video_id
    )
    response = request.execute()

    if not response['items']:
        return "No details available for the video."

    # Extract description from the video details
    video_description = response['items'][0]['snippet']['description']
    
    # Check if the description is sufficiently long for summarization
    if len(video_description) < 100:
        return video_description  # Return as is if too short to summarize

    # Initialize summarization model
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Generate summary
    summary = summarizer(video_description, max_length=130, min_length=30, do_sample=False)

    # Return the first summary text
    return summary[0]['summary_text']
@app.route('/analyze_comments', methods=['GET'])
def analyze_comments_api():
    url = request.args.get('url', '')
    

    api_key = request.args.get('apiKey', os.environ.get(API_key))  # Ensure you securely manage your API key

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
    results ={
        "videoTitle": video_title,
        "likeCount": like_count,
        "commentCount": comment_count,
        "subscriberCount": subscriber_count,
        "sentimentResults": sentiment_results

        
    }
    return {"results": results}, 200


if __name__ == '__main__':
    
    serve(app, host='0.0.0.0', port=8080)

    
