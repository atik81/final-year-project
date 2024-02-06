chrome.runtime.onInstalled.addListener(function() {
    // Perform on install tasks, such as setting default values
});

// You can listen for messages from your popup script if you need to perform actions in the background
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.action === "getApiKey") {
            // Implement a way to securely retrieve your API key
            sendResponse({ apiKey: "your-securely-stored-api-key" });
        }
        return true; // Return true to indicate you wish to send a response asynchronously
    }
);