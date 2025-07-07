# Cars.co.za Sentiment Analysis API Documentation

## Base URL
- **Production**: `https://cars-co-za-sentiment-analysis-dashboard.onrender.com/`
- **Development**: `http://localhost:8000`

## Authentication
Currently no authentication required. API keys are managed server-side.

## CORS Configuration
The API is configured to accept requests from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)
- `https://your-frontend-domain.com` (Production)

## API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

### 2. Root Endpoint
**GET** `/`

Get basic API information.

**Response:**
```json
{
  "message": "Welcome to Cars.co.za Sentiment API",
  "version": "1.0.0",
  "status": "running",
  "cors_origins": 4
}
```

### 3. CORS Test
**GET** `/cors-test`

Test CORS configuration (useful for debugging frontend connectivity).

**Response:**
```json
{
  "message": "CORS is working!",
  "allowed_origins": [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://your-frontend-domain.com"
  ]
}
```

### 4. Fetch Video Comments
**POST** `/youtube/comments`

Fetch comments from a YouTube video.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "video_id": "VIDEO_ID",
  "comments": [
    "This car review was so helpful!",
    "Why didn't you test the fuel economy?",
    "Best car channel on YouTube!"
  ]
}
```

**Error Responses:**
- `400`: Invalid YouTube URL
- `500`: Failed to fetch comments

### 5. Fetch Video Metadata
**POST** `/youtube/metadata`

Get video metadata (title, views, likes, etc.).

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "videoId": "VIDEO_ID",
  "title": "2024 BMW X5 Review - Is it worth it?",
  "description": "Complete review of the 2024 BMW X5...",
  "publishedAt": "2024-01-15T10:00:00Z",
  "channelTitle": "Cars.co.za",
  "viewCount": 125000,
  "likeCount": 3500,
  "commentCount": 245
}
```

### 6. Fetch Video Transcript
**POST** `/youtube/transcript`

Get the video's transcript if available.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "video_id": "VIDEO_ID",
  "transcript": "Welcome to Cars.co.za. Today we're reviewing the 2024 BMW X5..."
}
```

**If no transcript available:**
```json
{
  "video_id": "VIDEO_ID",
  "transcript": null,
  "message": "No transcript available."
}
```

### 7. Complete Video Analysis
**POST** `/analyze/video`

Perform complete sentiment analysis on a YouTube video (comments + metadata + AI report).

**Request Body:**
```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "video_id": "VIDEO_ID",
  "sentiment_results": [
    {
      "text": "This car review was amazing!",
      "label": "POSITIVE",
      "score": 0.92,
      "error": null
    },
    {
      "text": "Why didn't you test highway driving?",
      "label": "NEUTRAL",
      "score": 0.65,
      "error": null
    },
    {
      "text": "Terrible camera work",
      "label": "NEGATIVE",
      "score": 0.87,
      "error": null
    }
  ],
  "categories": {
    "most_interesting": [
      "I've owned this car for 2 years and here's my honest opinion..."
    ],
    "hot_takes": [
      "BMW is overpriced garbage!",
      "Best luxury SUV ever made!"
    ],
    "questions": [
      "What's the fuel economy like?",
      "How does it compare to the Mercedes GLE?"
    ]
  },
  "report": "VIDEO ANALYSIS REPORT\n\nThe 2024 BMW X5 review received overwhelmingly positive feedback from viewers, with 78% positive sentiment across 245 comments. Key strengths highlighted include build quality, driving dynamics, and luxury features.\n\nViewers particularly appreciated the detailed interior walkthrough and performance testing segments. Common questions focused on fuel economy, maintenance costs, and comparisons with competing models.\n\nRecommendations:\n1. Address fuel economy concerns in future reviews\n2. Include more comparison content with Mercedes and Audi\n3. Continue the detailed interior coverage format",
  "metadata": {
    "videoId": "VIDEO_ID",
    "title": "2024 BMW X5 Review - Is it worth it?",
    "description": "Complete review...",
    "publishedAt": "2024-01-15T10:00:00Z",
    "channelTitle": "Cars.co.za",
    "viewCount": 125000,
    "likeCount": 3500,
    "commentCount": 245
  }
}
```

## Frontend Integration Examples

### React/JavaScript Example

```javascript
// Base API client
const API_BASE_URL = 'https://your-render-app.onrender.com';

// Analyze a video
async function analyzeVideo(videoUrl) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze/video`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        video_url: videoUrl
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing video:', error);
    throw error;
  }
}

// Get video metadata only
async function getVideoMetadata(videoUrl) {
  try {
    const response = await fetch(`${API_BASE_URL}/youtube/metadata`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: videoUrl
      })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching metadata:', error);
    throw error;
  }
}

// Usage in React component
function VideoAnalyzer() {
  const [videoUrl, setVideoUrl] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const result = await analyzeVideo(videoUrl);
      setAnalysis(result);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <input 
        type="text" 
        value={videoUrl} 
        onChange={(e) => setVideoUrl(e.target.value)}
        placeholder="Enter YouTube URL"
      />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Video'}
      </button>
      
      {analysis && (
        <div>
          <h3>{analysis.metadata.title}</h3>
          <p>Sentiment: {analysis.sentiment_results.filter(r => r.label === 'POSITIVE').length} positive, {analysis.sentiment_results.filter(r => r.label === 'NEGATIVE').length} negative</p>
          <p>Questions: {analysis.categories.questions.length}</p>
          <pre>{analysis.report}</pre>
        </div>
      )}
    </div>
  );
}
```

### Axios Example

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-render-app.onrender.com',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analyze video
export const analyzeVideo = async (videoUrl) => {
  const response = await api.post('/analyze/video', {
    video_url: videoUrl
  });
  return response.data;
};

// Get comments only
export const getComments = async (videoUrl) => {
  const response = await api.post('/youtube/comments', {
    url: videoUrl
  });
  return response.data;
};
```

## Data Types

### Sentiment Labels
- `POSITIVE` - Positive sentiment
- `NEGATIVE` - Negative sentiment  
- `NEUTRAL` - Neutral sentiment
- `Unknown` - Analysis failed

### Comment Categories
- `most_interesting` - Long, detailed comments
- `hot_takes` - Strong opinions (love/hate)
- `questions` - Comments containing questions

## Error Handling

All endpoints return standard HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid URL, missing parameters)
- `404` - Not Found (video not found)
- `500` - Server Error (API failures, processing errors)

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

The API processes YouTube requests in batches to avoid rate limits. For large videos with many comments, expect response times of 10-30 seconds.

## Tips for Frontend Development

1. **Loading States**: Always show loading indicators - analysis can take 10-30 seconds
2. **Error Handling**: Wrap all API calls in try-catch blocks
3. **URL Validation**: Validate YouTube URLs on the frontend before sending
4. **Caching**: Consider caching results for the same video URL
5. **CORS Testing**: Use the `/cors-test` endpoint to verify connectivity

## Environment Variables for Deployment

Make sure these are set in your Render.com environment:
- `YOUTUBE_API_KEY` - Google YouTube Data API key
- `COHERE_API_KEY` - Cohere API key for sentiment analysis
- `FRONTEND_URL` - Your frontend domain for CORS (optional)
- `DEBUG` - Set to "false" for production

## Example Full Integration

```javascript
// Complete video analysis component
import React, { useState } from 'react';

const VideoAnalyzer = () => {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const analyzeVideo = async () => {
    if (!url) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('https://your-render-app.onrender.com/analyze/video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_url: url })
      });
      
      if (!response.ok) {
        throw new Error('Analysis failed');
      }
      
      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="video-analyzer">
      <h2>YouTube Video Sentiment Analysis</h2>
      
      <div>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://www.youtube.com/watch?v=..."
          style={{ width: '400px', padding: '8px' }}
        />
        <button onClick={analyzeVideo} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
      
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      {analysis && (
        <div>
          <h3>{analysis.metadata.title}</h3>
          <p>Views: {analysis.metadata.viewCount.toLocaleString()}</p>
          <p>Likes: {analysis.metadata.likeCount.toLocaleString()}</p>
          
          <div>
            <h4>Sentiment Breakdown:</h4>
            <p>Positive: {analysis.sentiment_results.filter(r => r.label === 'POSITIVE').length}</p>
            <p>Negative: {analysis.sentiment_results.filter(r => r.label === 'NEGATIVE').length}</p>
            <p>Neutral: {analysis.sentiment_results.filter(r => r.label === 'NEUTRAL').length}</p>
          </div>
          
          <div>
            <h4>Top Questions:</h4>
            {analysis.categories.questions.map((q, i) => (
              <p key={i}>• {q}</p>
            ))}
          </div>
          
          <div>
            <h4>Analysis Report:</h4>
            <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f5f5f5', padding: '10px' }}>
              {analysis.report}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoAnalyzer;
```