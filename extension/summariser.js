document.addEventListener('DOMContentLoaded', function() {
    const summarizeButton = document.getElementById('summarizeButton');
    const outputElement = document.getElementById('output'); // Ensure there's an element with id="output" in your HTML

    summarizeButton.addEventListener('click', function() {
        summarizeButton.disabled = true;
        summarizeButton.textContent = "Summarizing...";

        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            const activeTab = tabs[0];
            const videoUrl = encodeURIComponent(activeTab.url);
            fetch(`http://127.0.0.1:5000/summarize_video?url=${videoUrl}`)
                .then(response => response.json())
                .then(data => {
                    if (data.summary) {
                        outputElement.textContent = data.summary;
                    } else {
                        outputElement.textContent = data.error || 'Summary not available.';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    outputElement.textContent = 'Failed to fetch summary.';
                })
                .finally(() => {
                    summarizeButton.disabled = false;
                    summarizeButton.textContent = "Summarize";
                });
        });
    });
});
