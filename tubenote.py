from dotenv import load_dotenv
import serpapi
import os, requests
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from datetime import date

load_dotenv()

def change_youtube_link_to_video_id(link: str):
    return link.replace("https://www.youtube.com/watch?v=", "")

def get_related_youtube_searches(query: str):
    client = serpapi.Client(api_key=os.getenv('SERPAPI_API_KEY'))

    results = client.search({
        'search_query': query,
        'engine': 'youtube'
    })

    youtube_links = [(video['title'], video['link'], change_youtube_link_to_video_id(video['link'])) for video in results['video_results']]
    return youtube_links[:1]

def format_transcripts(video_data: tuple[str, str]):
    ytt_api = YouTubeTranscriptApi()

    youtube_transcripts = []
    for title, link, video_id in video_data:
        transcripts = ytt_api.fetch(video_id)
        transcript_text = "\n".join([transcript.text for transcript in transcripts])

        youtube_transcripts.append(f'''Title: {title}\nLink: {link}\nTranscript:\n {transcript_text}\n''')
    
    return youtube_transcripts

def get_youtube_transcripts(query: str):
    try:
        video_data = get_related_youtube_searches(query)

        return format_transcripts(video_data)
    except:
        print('Could not fetch YouTube transcripts')


system_instruction = """
"You are an assistant that can give wholesome information based on YouTube transcripts"
"Use tools only when necessary, ensure the user catches a full picture when using transcripts."
"The user does not need to specify a YouTube link, YouTube is a resource for getting the user any information they need"
"If you decide to get information from YouTube, use the tools available"
"Don't tell the user about your plans to use the tools, just use it"
"Do not hallucinate"
"""

function_call_system_instruction = """
"You are an assistant that can perfectly the occurences from a YouTube transcript,"
" your users are able to understand a video from your description of the transcript"
"and would not need to watch the video to understand it's content"
"also provide the resources of the video incase the user chooses to check it"
"""

config = {
    "tools": [
        {
            "function_declarations": [
                {
                    "name": "get_youtube_transcripts",
                    "description": "Fetches YouTube transcripts for a given topic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The topic of interest for which transcripts should be retrieved.",
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        }
    ],

}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-1.5-pro",
    config=config,
    contents=f"{system_instruction}\n\n User Query: Understanding RAG" ,
)

print(f'First Response: {response}')

def call_function(function_call, functions):
    function_name = function_call.name  # Extract function name
    function_args = function_call.args  # Already a dictionary, no need for JSON parsing

    # Fetch the function from dictionary
    func = functions.get(function_name)

    if func:
        return func(**function_args)  # Call the function with unpacked arguments

    return f"Error: Function '{function_name}' not found."

def get_llm_final_response(response):
    if hasattr(response, "text") and response.text:
        return response.text
    
    part = response.candidates[0].content.parts[0]

    available_functions = {
        "get_youtube_transcripts": get_youtube_transcripts
    }

    result = ""
    if part.function_call:
        result = call_function(part.function_call, available_functions)

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        config=config,
        contents=f"{function_call_system_instruction}\n\n Video Transcript: {result}",
    )

    return response.text

print(f'Final Response: {get_llm_final_response(response)}')
