// analyzeSentiment.js
async function AnalyzeSentiment(comment) {
    // Define simple keyword-based sentiment analysis
    const positiveKeywords = ['love', 'great', 'fantastic', 'perfect', 'wonderful', 'happy', 'amazing'];
    const negativeKeywords = ['hate', 'terrible', 'awful', 'worst', 'horrible', 'sad', 'bad'];

    // Normalize the comment to lower case for comparison
    const commentLowerCase = comment.toLowerCase();

    // Check for positive and negative keywords
    const hasPositive = positiveKeywords.some(keyword => commentLowerCase.includes(keyword));
    const hasNegative = negativeKeywords.some(keyword => commentLowerCase.includes(keyword));

    // Determine sentiment
    if (hasPositive && !hasNegative) {
        return "positive";
    } else if (!hasPositive && hasNegative) {
        return "negative";
    } else {
        return "neutral";
    }
}