document.addEventListener('DOMContentLoaded', function() {
    const summarizeButton = document.getElementById('summarizeButton'); // Make sure this ID matches the button's ID in popup.html
    const outputElement = document.getElementById('summaryText'); // Corrected to 'summaryText' based on your HTML

    summarizeButton.addEventListener('click', function() {
        chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
            const currentTabUrl = tabs[0].url;
            // WARNING: Do not expose API keys in client-side code like this.
            // I'm using the key you provided for demonstration purposes only.
            // Ideally, this key should be obtained securely from the server or environment variables.
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
                        outputElement.textContent = 'Analysis Results:\n' + JSON.stringify(data.results, null, 2);
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