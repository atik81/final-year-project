![Screenshot 2024-04-29 172525](https://github.com/atik81/final-year-project/assets/118019617/35291cf3-e934-4f26-88cd-c65a4ef0b70c)


Sure, here's a comprehensive README file for your YouTube Analyzer Chrome extension project without any AI-based content:

---

# YouTube Analyzer Chrome Extension

This project is a Chrome extension designed to analyze YouTube videos by fetching and analyzing comments for sentiment and summarizing video transcripts. It uses various technologies and APIs to achieve this, including Flask for the backend, Google APIs for data retrieval, and D3.js for visualizations.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Video Demo](#video-demo)
- [Report](#Report)

## Features

- **Analyze YouTube Video Comments**: Fetch and analyze comments from YouTube videos to determine the overall sentiment (positive, neutral, negative).
- **Summarize Video Transcripts**: Summarize the transcripts of YouTube videos.
- **Visual Representations**: Display sentiment analysis results in a donut chart.
- **Detailed Video Information**: Display video title, like count, comment count, and subscriber count.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, D3.js
- **Backend**: Flask
- **APIs**: Google YouTube Data API, Google YouTube Transcript API
- **Other Libraries**: VaderSentiment, Transformers

## Setup and Installation

### Prerequisites

- Python 3.x
- Node.js and npm (for building the Chrome extension)

### Backend Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/youtube-analyzer.git
   cd youtube-analyzer
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables. Create a `.env` file in the root directory and add your API key:
   ```env
   API_key=your_google_api_key
   ```

5. Run the Flask server:
   ```sh
   python app.py
   ```

### Frontend Setup

1. Navigate to the `extension` folder:
   ```sh
   cd extension
   ```

2. Install npm dependencies:
   ```sh
   npm install
   ```

3. Build the extension:
   ```sh
   npm run build
   ```

4. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`.
   - Enable Developer Mode.
   - Click on "Load unpacked" and select the `extension` folder.

## Usage

1. Open a YouTube video in your browser.
2. Click on the YouTube Analyzer extension icon.
3. Click the "Analyze Video" button to fetch and analyze the comments.
4. Click the "Summarize Video" button to get a summary of the video transcript.

## Folder Structure

```
youtube-analyzer/
├── app.py
├── requirements.txt
├── .env
├── extension/
│   ├── popup.html
│   ├── popup.js
│   ├── popup.css
│   ├── summariser.js
│   ├── d3.v6.min.js
│   ├── manifest.json
│   └── icons/
│       ├── icons16.png
│       ├── icons48.png
│       └── icons128.png
└── README.md
```

## API Endpoints

- **GET /analyze_comments**: Fetch and analyze comments from a YouTube video.
  - **Parameters**: `url` (YouTube video URL), `apiKey` (Google API key)
  - **Response**: JSON containing video details and sentiment analysis results.

- **GET /summarize_subtitles**: Summarize the subtitles of a YouTube video.
  - **Parameters**: `url` (YouTube video URL)
  - **Response**: JSON containing the summary of the video transcript.

## Screenshots
![chorem](https://github.com/user-attachments/assets/f5201a53-378b-444b-8bc9-df80138c0392)
![updated chorme](https://github.com/user-attachments/assets/402855e1-b4ac-4e04-a386-b9233af24494)
![updated sssss](https://github.com/user-attachments/assets/3b943a3d-a877-4fc2-b560-9f3383320d22)

## Video Demo

https://github.com/user-attachments/assets/5a2bb239-fcf6-4901-adc6-8a608defc6bb

## Report 



