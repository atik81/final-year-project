import openai

def analyze_sentiment(text):
    openai.api_key = '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'  # Replace with your actual OpenAI API key

    response = openai.Completion.create(
      engine="text-davinci-003",  # You can change the model as needed
      prompt=f"Analyze the sentiment of this text: \"{text}\". Is it positive, negative, or neutral?",
      max_tokens=60
    )

    return response.choices[0].text.strip()

# Test the function
test_text = "I love spending time with my family on the weekends!"
result = analyze_sentiment(test_text)
print(f"Sentiment Analysis Result: {result}")
