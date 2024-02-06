// This content script would be injected into YouTube video pages
(function() {
    // Function to extract the video ID from the URL
    function getVideoIdFromUrl() {
        const videoIdMatch = window.location.search.match(/v=([A-Za-z0-9_-]+)/);
        return videoIdMatch ? videoIdMatch[1] : null;
    }

    // Send a message to the background script or popup script with the video ID
    function sendVideoIdToPopup(videoId) {
        chrome.runtime.sendMessage({ videoId: videoId });
    }

    // When the DOM is fully loaded, check if this is a YouTube video page
    if (document.readyState === "complete" || document.readyState === "interactive") {
        const videoId = getVideoIdFromUrl();
        if (videoId) {
            sendVideoIdToPopup(videoId);
        }
    } else {
        document.addEventListener("DOMContentLoaded", function() {
            const videoId = getVideoIdFromUrl();
            if (videoId) {
                sendVideoIdToPopup(videoId);
            }
        });
    }
})();