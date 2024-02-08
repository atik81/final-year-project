chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "getApiKey") {
        chrome.storage.local.get("apiKey", function(result) {
            if (result.apiKey) {
                sendResponse({ apiKey: result.apiKey });
            } else {
                console.error("API Key not found in storage.");
                sendResponse({ error: "API Key not found in storage." });
            }
        });
        return true; // Indicates an asynchronous response is pending
    }
});