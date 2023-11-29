from subprocess import call 
import openai
import time
from youtubeapi import fetch_comments, video_and_channel_details
import creds

def open_py_file():
    call(['python', 'youtubeapi.py'])

open_py_file()

# Set your OpenAI API key
openai.api_key = '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' # Replace with your actual OpenAI API key
def analyze_sentiment(comments,batch_size=10, delay=5):
    sentiments = []
    for i in range(0, len(comments), batch_size):
        batched_comments = comments[i:i+batch_size]
        all_comments_text = "\n\n".join([f"{c['snippet']['topLevelComment']['snippet']['authorDisplayName']} - {c['snippet']['topLevelComment']['snippet']['textDisplay']}" for c in batched_comments])
        

        prompt = f"Classify the sentiment of these comments as Positive, Negative, or Neutral:\n\n{all_comments_text}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )  
      
        analyzed_sentiments = response.choices[0].message['content'].split('\n')
        sentiments.extend(zip(batched_comments, analyzed_sentiments))
        time.sleep(delay)
    return sentiments
def calculate_sentiment_percentages(sentiments):
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    total_comments = len(sentiments)

    for _, sentiment in sentiments:
        if 'Positive' in sentiment:
            sentiment_counts['Positive'] += 1
        elif 'Negative' in sentiment:
            sentiment_counts['Negative'] += 1
        else:
            sentiment_counts['Neutral'] += 1

    percentages = {k: (v / total_comments) * 100 for k, v in sentiment_counts.items()}
    return percentages
api_key = 'AIzaSyClvvMYcdHGu4K_zoVlOvIhf5Z-ykT9IIE'  # Your YouTube API key
video_url = input('Input YouTube URL: ')
# Fetch video and channel details
details = video_and_channel_details(video_url,api_key)
if details:
    print(f"Video Title: {details['video_title']}")
    print('\033[91m\033[1m' +f"Video Title: {details['video_title']}"+ '\033[0m')

    print('\033[91m\033[1m' + f"Like Count: {details['like_count']}"+ '\033[0m')
    print('\033[91m\033[1m' +f"Channel Title: {details['channel_title']}"+ '\033[0m')
    print('\033[91m\033[1m' + f"Subscriber Count: {details['subscriber_count']}"+ '\033[0m')

comments = fetch_comments(video_url, api_key)[:50]  # Fetch comments using the function from youtubeapi.py

comment_sentiments = analyze_sentiment(comments)
sentiment_percentages = calculate_sentiment_percentages(comment_sentiments)

print("Sentiment Percentages:")
for sentiment, percentage in sentiment_percentages.items():
    print(f"{sentiment}: {percentage:.2f}%")