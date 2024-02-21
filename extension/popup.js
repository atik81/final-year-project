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
                        displayResults(data.results);
                        drawSentimentAnalysisDonutChart(data.results.sentimentResults);
                        // Correct way to display results
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

function drawSentimentAnalysisDonutChart(sentimentResults) {
    if (!sentimentResults || !sentimentResults.positive || !sentimentResults.neutral || !sentimentResults.negative) {
        console.error("Sentiment results are not properly formatted", sentimentResults);
        return; // Exit the function if data is not valid
    }
    console.log('Sentiment Results:', sentimentResults);


    const data = [
        { label: "Positive", value: sentimentResults.positive, color: "#008000" },
        { label: "Neutral", value: sentimentResults.neutral, color: "#808080" },
        { label: "Negative", value: sentimentResults.negative, color: "#FF0000" },
    ];
    console.log('Chart Data:', data);


    const width = 180,
        height = 90,
        radius = Math.min(width, height * 2) / 2,
        donutWidth = 50;

    const svgContainer = d3.select("#sentimentAnalysisDonutChart");
    if (!svgContainer.node()) {
        console.error("The element #sentimentAnalysisDonutChart does not exist in the DOM.");
        return; // Exit the function because the element is not present
    }
    const svg = svgContainer.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height})`);

    const arc = d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius)
        .startAngle(-Math.PI / 2)
        .endAngle(Math.PI / 2);
    const labelArc = d3.arc()
        .outerRadius(radius - donutWidth / 2)
        .innerRadius(radius - donutWidth / 2);

    const pie = d3.pie()
        .value(d => d.value)
        .sort(null)
        .startAngle(-Math.PI / 2)
        .endAngle(Math.PI / 2);
    const path = svg.selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', d => d.data.color);
    svg.selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', d => d.data.color);

    path.each(function(d) {
        console.log(`Color for ${d.data.label}: `, d3.select(this).attr('fill'));
    });

    // mouseover event
    path.on('mouseover', function(event, d) {
        d3.select(this)
            .transition()
            .duration(300)
            .attr('fill', d3.rgb(d.data.color).brighter(0.9));
    })


    .on('mouseout', function(event, d) {
        d3.select(this)
            .transition()
            .duration(300)
            .attr('fill', d.data.color);
    });
    const total = d3.sum(data.map(d => d.value)); // Calculate the total sum of the data values

    svg.selectAll('.label')
        .data(pie(data))
        .enter()
        .append('text')
        .attr('class', 'label') // Add class for CSS if needed
        .attr('transform', d => {
            const [x, y] = labelArc.centroid(d);
            return `translate(${x}, ${y})`;
        })
        .attr('text-anchor', 'middle')
        .text(d => `${d.data.label}: ${(100 * d.data.value / total).toFixed(1)}%`)
        .style('fill', 'black') // Change color as needed
        .style('font-size', '10px');





}