"""
venv
pip install flask google-search-results youtube-transcript-api openai gtts
make frontend
"""
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import re
from gtts import gTTS
import os
from huggingface_hub import InferenceClient
import requests
import json
app = Flask(__name__)
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
client = InferenceClient(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    token=HUGGINGFACEHUB_API_TOKEN
)

# Function to extract YouTube video ID from a URL
def extract_video_id(url):
    match = re.search(r"v=([\w-]+)", url)
    return match.group(1) if match else None

# Function to search YouTube video
def search_youtube_video(title, api_key):
    params = {
        "engine": "youtube",
        "search_query": title,
        "api_key": api_key
    }
    
    # API request
    response = requests.get("https://serpapi.com/search", params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract video results
        video_results = data.get("video_results", [])
        
        # Return the link of the first video if any results exist
        if video_results and len(video_results) > 0:
            print('Link', video_results[0].get("link"))
            return video_results[0].get("link")
        else:
            print("No video results found for the given title.")
            return None
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        print(response.text)
        return None
    
# Function to get YouTube transcript
def get_video_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except Exception as e:
        return None
    

# Function to convert summary to speech
def text_to_speech(text, filename="summary.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# Available Functions
available_functions = {
    "search_youtube_video": search_youtube_video,
    "get_video_transcript": get_video_transcript,
    "text_to_speech": text_to_speech
}
# Function Specifications
function_descriptions = [
    {
        "name": "search_youtube_video",
        "description": "Search for a YouTube video by title and get its URL",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The title of the YouTube video to search for"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_video_transcript",
        "description": "Get the transcript from a YouTube video URL",
        "parameters": {
            "type": "object",
            "properties": {
                "video_url": {
                    "type": "string",
                    "description": "The URL of the YouTube video"
                }
            },
            "required": ["video_url"]
        }
    },
    {
        "name": "text_to_speech",
        "description": "Convert text to speech and save as an MP3 file",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to convert to speech"
                },
                "filename": {
                    "type": "string",
                    "description": "The filename to save the audio as (default: summary.mp3)"
                }
            },
            "required": ["text"]
        }
    }
]
def process_with_llm(prompt, model="mistral:latest"):
    try:
        system_message = (
            "You are an assistant that can search for YouTube videos, summarize their content, and generate audio summaries. "
            "Use tools only when necessary. Summarization should be done naturally."
        )
        
        full_prompt = f"{system_message}\n\nUser: {prompt}"
        response = client.text_generation(full_prompt, max_new_tokens=500, temperature=0.5)
        #response = response.lstrip("Assistant:").strip()

        return {
            "message": {
                "content": response
            }
        }
    except Exception as e:
        return {"error": f"Hugging Face API error: {str(e)}"}
    
def handle_llm_response(llm_response, correct_video_url):
    # Check if the response contains a tool call
    if "tool_calls" in llm_response:
        responses = []
        
        for tool_call in llm_response["tool_calls"]:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args)
                responses.append(f"Function {function_name} executed: {function_response}")
            else:
                responses.append(f"Error: Function {function_name} not found")
                
        # Now send the function responses back to the LLM for final processing
        final_response = process_with_llm("\n".join(responses))
        return f"Summary:\n{final_response}\n\n Video URL: {correct_video_url}"

    else:
        # Direct response with no function call
        return f'{llm_response["message"]["content"]}\n\n Video URL: {correct_video_url}'


@app.route("/summarize", methods=["POST"]) 
def summarize_video():
    data = request.json
    user_query = data.get("user_query")
    video_url = search_youtube_video(user_query, SERPAPI_API_KEY)

    if not video_url:
        return jsonify({"error": "No video found for the given query"}), 400

    # Process with LLM using tool calling
    response = process_with_llm(user_query)
    llm_output = handle_llm_response(response, video_url)
    return jsonify({
        "response": llm_output
    })

if __name__ == "__main__":
    app.run(debug=True)