document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');
    if (commentsContainer) {
        commentsContainer.innerHTML = ''
    }
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
                    console.log(data); // This will show you the entire response object
                    if (data.results) {
                        displayResults(data.results);
                        drawSentimentAnalysisDonutChart(data.results.sentimentResults);
                        displayComments(data.results.comments)
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

    function applyTextStyles(element, color) {
        element.style.color = color;
        element.style.fontSize = '15px'; // Set font size to be larger
        element.style.fontWeight = 'bold'; // Make the font weight bold
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
    applyTextStyles(positiveSentiment, 'green');

    document.getElementById('neutralSentiment').textContent = `Neutral: ${
        Number(results.sentimentResults.neutral).toLocaleString() || 'Not available'
    }`;
    applyTextStyles(neutralSentiment, 'blue');

    document.getElementById('negativeSentiment').textContent = `Negative: ${
        Number(results.sentimentResults.negative).toLocaleString() || 'Not available'
    }`;
    applyTextStyles(negativeSentiment, 'red');


}
const commentsContainer = document.getElementById('commentsContainer');


function displayComments(comments) {
    const commentsContainer = document.getElementById('commentsContainer');
    commentsContainer.innerHTML = ''; // Clear the container before adding new comments

    if (!comments || comments.length === 0) {
        // No comments found, display the message
        const noCommentsMessage = document.createElement('p');
        noCommentsMessage.textContent = 'No Comments found.';
        noCommentsMessage.style.textAlign = 'center';
        commentsContainer.appendChild(noCommentsMessage);
    } else {
        // Comments exist, display them
        comments.forEach(comment => {
            const commentElement = document.createElement('div');
            commentElement.classList.add('comment');

            // Assuming commentText is an object with author, text, and sentiment properties
            const authorElement = document.createElement('p');
            authorElement.textContent = `Author: ${comment.author}`;
            commentElement.appendChild(authorElement);

            const textElement = document.createElement('p');
            textElement.textContent = `Comment: ${comment.text}`;
            commentElement.appendChild(textElement);

            const sentimentElement = document.createElement('p');
            sentimentElement.textContent = `Sentiment: ${comment.sentiment}`;
            commentElement.appendChild(sentimentElement);

            commentsContainer.appendChild(commentElement);
        });
    }
}

// Directly after defining commentsContainer
commentsContainer.innerHTML = '<p>Test Comment</p>';


const legendRectSize = 18; // defines the size of the legend color box
const legendSpacing = 4;

function drawSentimentAnalysisDonutChart(sentimentResults) {

    function getLabelText(d) {
        const percentage = (100 * d.value / total).toFixed(1);
        return `${d.data.label}: ${percentage}%`; // Return label with percentage
    }
    const colors = {
        positive: '#2ca02c', // Correct hex code for green
        neutral: '#0000FF', // Correct hex code for grey
        negative: '#d62728' // Correct hex code for red
    };

    if (!sentimentResults || !sentimentResults.positive || !sentimentResults.neutral || !sentimentResults.negative) {
        console.error("Sentiment results are not properly formatted", sentimentResults);
        return; // Exit the function if data is not valid
    }
    console.log('Sentiment Results:', sentimentResults);


    const data = [
        { label: "Positive", value: sentimentResults.positive, color: colors.positive },
        { label: "Neutral", value: sentimentResults.neutral, color: colors.neutral },
        { label: "Negative", value: sentimentResults.negative, color: colors.negative },
    ];
    console.log('Chart Data:', data);


    const width = 120,
        height = 70,
        radius = Math.min(width, height * 2) / 2,
        donutWidth = 30;

    const svgContainer = d3.select("#sentimentAnalysisDonutChart");
    svgContainer.selectAll("svg").remove();

    const svg = svgContainer.append("svg")
        .attr("width", width)
        .attr("height", height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${radius + 10})`); // Adjusted for proper centering

    const arc = d3.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius);
    const labelArc = d3.arc()
        .outerRadius(radius - donutWidth / 2)
        .innerRadius(radius - donutWidth / 2);

    const pie = d3.pie()
        .value(d => d.value)
        .sort(null)



    const path = svg.selectAll('path')
        .data(pie(data))
        .enter()
        .append('path')
        .attr('d', arc)
        .attr('fill', d => d.data.color)
        .attr('stroke', '#fff')
        .attr('stroke-width', '2px') // Width of the stroke for separation effect
        .style('filter', 'url(#drop-shadow)')
        .each(function(d) { this._current = d; })
        .on('mouseover', function(event, d) {
            // Scale up the segment on hover
            d3.select(this).transition()
                .duration(200)
                .attr('transform', function(d) {
                    const centroid = arc.centroid(d);
                    return `translate(${centroid[0] * 0.1}, ${centroid[1] * 0.1})`;
                });
        })
        .on('mouseout', function(event, d) {
            // Scale down the segment on mouse out
            d3.select(this).transition()
                .duration(200)
                .attr('transform', 'translate(0,0)');
        });
    path.transition()
        .duration(750)
        .attrTween('d', function(d) {
            const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
            return function(t) {
                return arc(interpolate(t));
            };
        });


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

    const total = d3.sum(data.map(d => d.value)); // Calculate the total sum of the data values
    const legendStartingPoint = width / 2 - (data.length * (legendRectSize + legendSpacing + 100)) / 2;


    const legend = svg.selectAll('.legend')
        .data(data)
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, i) {
            const horz = i * (legendRectSize + legendSpacing + 100) + legendStartingPoint; // 100 is additional spacing between items
            const vert = radius + donutWidth / 2 + 40; // 40 is the space below the donut chart
            return `translate(${horz}, ${vert})`;
        });

    // Append a rectangle to each legend item
    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', d => d.color)
        .style('stroke', d => d.color);

    // Append the text to each legend item





    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background", "white")
        .style("border", "1px solid #ddd")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("box-shadow", "2px 2px 10px rgba(0,0,0,0.5)")
        .style("text-align", "center");

    path.on('mouseover', function(event, d) {
            tooltip.html(getLabelText(d)) // Tooltip will now show label and percentage
                .style("visibility", "visible")
                .style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on('mousemove', function(event) {
            tooltip.style("left", (event.pageX) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
        .on('mouseout', function() {
            tooltip.style("visibility", "hidden");
        });


}