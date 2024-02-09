document.addEventListener('DOMContentLoaded', function() {
    const summarizeButton = document.getElementById('summarizeButton'); // Make sure this ID matches the button's ID in popup.html
    const outputElement = document.getElementById('summaryText'); // Corrected to 'summaryText' based on your HTML

    summarizeButton.addEventListener('click', function() {
        summarizeButton.disabled = true;
        summarizeButton.textContent = "Analyzing..."
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const currentTabUrl = tabs[0].url;
            if (!currentTabUrl.includes('youtube.com/watch')) {
                outputElement.textContent = 'This tool is for YouTube videos only.';
                summarizeButton.disabled = false;
                summarizeButton.textContent = 'Summarize Video';
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
                        displayResults(data.results, outputElement); // Correct way to display results
                    } else {
                        outputElement.textContent = 'Error: ' + data.error;
                    }
                })


            .catch(error => {
                console.error('Error fetching analysis:', error, requestUrl);
                outputElement.textContent = 'Error fetching analysis: ' + error.message;
            })

            .finally(() => {
                summarizeButton.disabled = false;
                summarizeButton.textContent = 'Summarize Video';
            });
        });
    });
});

function displayResults(results) {
    document.getElementById('Result').style.display = 'block'; // Make sure to show the container
    document.getElementById('videoTitle').textContent = results.videoTitle;
    // Repeat for other elements

    if (!results) {
        outputElement.textContent = "No results found. Please ensure the video URL is correct and try again.";
        return;
    }

    let summaryText = `Video Title: ${results.videoTitle}\n` +
        `Like Count: ${results.likeCount}\n` +
        `Comment Count: ${results.commentCount}\n` +
        `Subscriber Count: ${results.subscriberCount}\n` +
        `Sentiment Analysis:\n` +
        `Positive: ${results.sentimentResults.positive}\n` +
        `Neutral: ${results.sentimentResults.neutral}\n` +
        `Negative: ${results.sentimentResults.negative}`;

    outputElement.textContent = summaryText;
}