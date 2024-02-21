document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');

    analyzeButton.addEventListener('click', function() {
        analyzeButton.disabled = true;
        analyzeButton.textContent = "Analyzing..."
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const currentTabUrl = tabs[0].url;
            if (!currentTabUrl.includes('youtube.com/watch')) {
                outputElement.textContent = 'This tool is for YouTube videos only.';
                analyzeButton.disabled = false;
                analyzeButton.textContent = 'Analyze Video';
                return; // Legal use of return within a function
            }

            const apiKey = 'AIzaSyCF4V_xVhqlffr-XxgbuX2ELdo93yZxqtM';
            const requestUrl = `http://127.0.0.1:5000/analyze_comments?url=${encodeURIComponent(currentTabUrl)}&apiKey=${encodeURIComponent(apiKey)}`;

            fetch(requestUrl)
                .then(response => {
                    console.log(response)
                    if (!response.ok) {
                        throw new Error("Network response was not ok");

                    }
                    return response.json();

                })
                .then(data => {
                    if (data.results) {
                        displayResults(data.results); // Correct way to display results
                    } else {
                        document.getElementById('analyzeText').textContent = 'Error: ' + data.error;
                    }
                })


            .catch(error => {
                console.error('Error fetching analysis:', error);
                document.getElementById('analyzeText').textContent = 'Error fetching analysis: ' + error.message;
            })

            .finally(() => {
                analyzeButton.disabled = false;
                analyzeButton.textContent = 'analyze Video';
            });
        });
    });
});

function displayResults(results, outputElement) {
    document.getElementById('Result').style.display = 'block';
    document.getElementById('videoTitle').textContent = results.videoTitle || 'Not available';
    document.getElementById('likeCount').textContent =
        Number(results.likeCount).toLocaleString() || 'Not available';

    document.getElementById('commentCount').textContent =
        Number(results.commentCount).toLocaleString() || 'Not available';
    document.getElementById('subscriberCount').textContent =
        Number(results.subscriberCount).toLocaleString() || 'Not available';

    if (!results) {
        outputElement.textContent = "No results found. Please ensure the video URL is correct and try again.";
        return;
    }

    let analyzeText = `Video Title: ${results.videoTitle}\n` +
        `Like Count: ${results.likeCount}\n` +
        `Comment Count: ${results.commentCount}\n` +
        `Subscriber Count: ${results.subscriberCount}\n` +
        `Sentiment Analysis:\n` +
        `Positive: ${results.sentimentResults.positive}\n` +
        `Neutral: ${results.sentimentResults.neutral}\n` +
        `Negative: ${results.sentimentResults.negative}`;
    document.getElementById('positiveSentiment').textContent = `Positive: ${
            Number(results.sentimentResults.positive).toLocaleString() || 'Not available'
        }`;
    document.getElementById('neutralSentiment').textContent = `Neutral: ${
            Number(results.sentimentResults.neutral).toLocaleString() || 'Not available'
        }`;
    document.getElementById('negativeSentiment').textContent = `Negative: ${
            Number(results.sentimentResults.negative).toLocaleString() || 'Not available'
        }`;



}