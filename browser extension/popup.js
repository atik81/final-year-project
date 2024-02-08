document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("submitButton").addEventListener("click", AnalyzeCommentsHandler);
});

// Function to retrieve comments from YouTube API
async function retrieveComments(videoId, apiKey) {
    const url = `https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=${videoId}&key=${apiKey}&textFormat=plainText&maxResults=100`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(`YouTube API error: ${data.error.message}`);
        }

        return data.items.map(item => item.snippet.topLevelComment.snippet.textDisplay);
    } catch (error) {
        console.error('Error retrieving comments:', error);
        throw error; // Rethrow the error to be caught by the calling function
    }
}

// Handler function for when the Analyze Comments button is clicked
async function AnalyzeCommentsHandler() {
    const videoUrl = document.getElementById("videoUrlInput").value;
    const videoId = getVideoId(videoUrl);

    if (videoId) {
        try {
            // Retrieve the API key
            const apiKey = await getApiKey();

            // Retrieve comments with the API key
            const comments = await retrieveComments(videoId, apiKey);
            if (comments && comments.length > 0) {
                const sentimentCounts = { positive: 0, negative: 0, neutral: 0 };
                for (const comment of comments) {
                    const sentiment = await AnalyzeSentiment(comment); // Assume this function is implemented elsewhere
                    sentimentCounts[sentiment]++;
                }
                updateChart(sentimentCounts); // Assume this function is implemented elsewhere
            } else {
                console.error("Failed to retrieve or no comments found.");
            }
        } catch (error) {
            console.error("An error occurred:", error);
        }
    } else {
        console.error("Video ID not found in the URL");
    }
}

// Function to extract the video ID from the YouTube URL
function getVideoId(url) {
    const urlObj = new URL(url);
    return urlObj.searchParams.get('v');
}

// Function to retrieve the API key securely
async function getApiKey() {
    return new Promise((resolve, reject) => {
        chrome.runtime.sendMessage({ action: "getApiKey" }, function(response) {
            if (response && response.apiKey) {
                resolve(response.apiKey);
            } else {
                reject("API Key not found.");
            }
        });
    });
}

// Placeholder functions that need to be implemented or integrated
async function AnalyzeSentiment(comment) {
    // Function should be defined in analyzeSentiment.js
    throw new Error('AnalyzeSentiment function is not implemented.');
}

function updateChart(sentimentCounts) {
    // Function should update the chart in the popup based on sentiment analysis
    console.log("Update your chart here", sentimentCounts);
}