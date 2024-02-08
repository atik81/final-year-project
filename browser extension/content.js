(function() {
    // Function to extract the video ID from the URL
    function getVideoIdFromUrl() {
        const videoIdMatch = window.location.search.match(/v=([A-Za-z0-9_-]+)/);
        return videoIdMatch ? videoIdMatch[1] : null;
    }

    // Send a message to the background script or popup script with the video ID
    function sendVideoIdToPopup(videoId) {
        console.log("Sending video ID to popup/background:", videoId);
        chrome.runtime.sendMessage({ videoId: videoId });
    }

    // Function to request and log the API key from the background script
    chrome.runtime.sendMessage({ action: "getApiKey" }, function(response) {
        if (response && response.apiKey) {
            console.log("Received API key:", response.apiKey);
            // You can now use the API key for making authenticated requests, etc.
        } else if (response && response.error) {
            console.error("API key retrieval error:", response.error);
            // Handle the error (e.g., show a message to the user)
        } else {
            console.error("Unexpected error in receiving API key.");
            // Additional error handling
        }
    });


    // When the DOM is fully loaded, check if this is a YouTube video page and request the API key
    if (document.readyState === "complete" || document.readyState === "interactive") {
        const videoId = getVideoIdFromUrl();
        if (videoId) {
            sendVideoIdToPopup(videoId);
        }
        requestApiKey(); // Request the API key
    } else {
        document.addEventListener("DOMContentLoaded", function() {
            const videoId = getVideoIdFromUrl();
            if (videoId) {
                sendVideoIdToPopup(videoId);
            }
            requestApiKey(); // Request the API key
        });
    }
})();