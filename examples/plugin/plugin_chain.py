from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import pdb
import os

ai_plugin_data = {
    "schema_version": "v1",
    "name_for_human": "Youtube Transcript Plugin",
    "name_for_model": "youtube_transcript",
    "description_for_human": "Plugin that finds a youtube video and returns the transcript based on a search query.",
    "description_for_model": "Plugin that finds a youtube video and returns the transcript based on a search query.",
    "auth": {
        "type": "none"
    },
    "api": {
        "type": "openapi",
        "url": "http://127.0.0.1:4444/openapi.yaml",
        "is_user_authenticated": False
    },
    "logo_url": "https://d1yjjnpx0p53s8.cloudfront.net/styles/logo-original-577x577/s3/0016/4231/brand.gif?itok=cOeuUIp-",
    "contact_email": "support@example.com",
    "legal_info_url": "http://www.example.com/legal"
}

openapi_yaml_content = """
openapi: 3.0.0
info:
  title: YouTube API
  version: 1.0.0
paths:
  /youtube/transcripts:
    get:
      summary: Get YouTube video transcript
      parameters:
        - in: query
          name: video_id
          required: true
          schema:
            type: string
          description: The YouTube video ID
      responses:
        '200':
          description: Transcript of the YouTube video
          content:
            application/json:
              schema:
                type: object
                properties:
                  text:
                    type: string
                    description: Transcript text
                  start:
                    type: number
                    description: Start time of each sentence in seconds
                  duration:
                    type: number
                    description: Duration of each sentence in seconds
                  speaker:
                    type: string
                    description: Speaker name (if available)
                required:
                  - text
                  - start
                  - duration
      description: |
        This endpoint returns the transcript of a YouTube video using the YouTubeTranscriptApi.

  /youtube/search:
    get:
      summary: Search for a YouTube video
      parameters:
        - in: query
          name: query
          required: true
          schema:
            type: string
          description: The search query
      responses:
        '200':
          description: URL of the first video search result
          content:
            application/json:
              schema:
                type: object
                properties:
                  video_url:
                    type: string
                    description: URL of the first video search result
                required:
                  - video_url
      description: |
        This endpoint searches for a video on YouTube using the SerpApi service and returns the URL of the first search result.
"""

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:4444", "https://chat.openai.com"])

# Testing example
# http://127.0.0.1:4444/youtube/transcripts?video_id=C_78DM8fG6E
@app.route('/youtube/transcripts')
def youtube_transcripts():
    video_id = request.args.get('video_id')
    if video_id is None:
        return jsonify({
            "error": "video_id is required"
        })
    return jsonify(YouTubeTranscriptApi.get_transcript(video_id))

# Testing example
# http://127.0.0.1:4444/youtube/search?query=Ted+Talk+Greg+Brockman
@app.route('/youtube/search', methods=['GET'])
def youtube_search():
    query = request.args.get('query')
    params = {
        'search_query': query,
        'engine': 'youtube',
        'gl': 'us',
        'hl': 'en',
        'api_key': os.environ['SERPAPI_API_KEY'],
    }
    response = requests.get('https://serpapi.com/search', params=params)
    data = response.json()
    video_url = data['video_results'][0]['link']
    return jsonify({'video_url': video_url})

@app.route('/.well-known/ai-plugin.json')
def ai_plugin_json():
    return jsonify(ai_plugin_data)

@app.route('/openapi.yaml')
def openapi_yaml():
    return Response(openapi_yaml_content, mimetype='application/x-yaml')

if __name__ == '__main__':
    app.run(port=4444)
