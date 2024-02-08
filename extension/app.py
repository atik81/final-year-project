from flask import Flask, request
from googleapiclient.discovery import build
from transformers import pipeline

app = Flask(__name__)

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline('sentiment-analysis')

# Function to fetch YouTube comments using the YouTube Data API
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,  # Adjust based on your needs. Be mindful of quota costs.
        textFormat="plainText"
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

# Function to analyze sentiment of comments
def analyze_sentiment(comments):
    # Prepare a dictionary to hold sentiment counts
    sentiment_counts = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }

    # Due to the transformers pipeline limitations, we might need to batch comments
    # or truncate them to avoid errors for long texts.
    # Here we are processing each comment individually.
    for comment in comments:
        try:
            # Analyze each comment sentiment
            result = sentiment_pipeline(comment)[0]
            # Increment the sentiment count based on the result
            if result['label'] == 'POSITIVE' and result['score'] > 0.55:  # You can adjust the threshold
                sentiment_counts['positive'] += 1
            elif result['label'] == 'NEGATIVE' and result['score'] > 0.55:  # You can adjust the threshold
                sentiment_counts['negative'] += 1
            else:
                sentiment_counts['neutral'] += 1
        except Exception as e:
            print(f"Error processing comment: {e}")
            continue  # Skip to the next comment if there's an error

    return sentiment_counts


@app.route('/analyze_comments', methods=['GET'])
def analyze_comments_api():
    url = request.args.get('url', '')
    api_key = request.args.get('apiKey', 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM')  # Ensure you securely manage your API key

    if not api_key:
        return {"error": "API key is required."}, 400

    video_id = url.split('=')[1]
    comments = fetch_comments(video_id, api_key)
    sentiment_results = analyze_sentiment(comments)
    return {"results": sentiment_results}, 200

if __name__ == '__main__':
    # It's a good practice to not include your actual API key in your script.
    # Consider using environment variables or other secure methods to handle them.
    app.run(debug=True)

