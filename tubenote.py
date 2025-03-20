from dotenv import load_dotenv
import serpapi
import os, requests
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from datetime import date

load_dotenv()

def change_youtube_link_to_video_id(link: str):
    print('here')
    return link.replace("https://www.youtube.com/watch?v=", "")

def get_related_youtube_searches(query):
    print('here')

    client = serpapi.Client(api_key=os.getenv('SERPAPI_API_KEY'))

    results = client.search({
        'search_query': query,
        'engine': 'youtube'
    })

    youtube_links = [(video['title'], video['link'], change_youtube_link_to_video_id(video['link'])) for video in results['video_results']]
    return youtube_links[:1]

def format_transcripts(video_data: tuple[str, str]):
    print('here')
    ytt_api = YouTubeTranscriptApi()

    youtube_transcripts = []
    for title, link, video_id in video_data:
        transcripts = ytt_api.fetch(video_id)
        transcript_text = "\n".join([transcript.text for transcript in transcripts])

        youtube_transcripts.append(f'''Title: {title}\nLink: {link}\nTranscript:\n {transcript_text}\n''')
    
    return youtube_transcripts

# def get_youtube_transcripts(query: str) -> str:
#     video_data = get_related_youtube_searches(query)

#     transcripts = format_transcripts(video_data)

#     return "\n\n".join(transcripts) 


def get_youtube_transcripts(query):
    ''' returns relevant youtube transcripts about any fact'''

    print('here')
    client = serpapi.Client(api_key=os.getenv('SERPAPI_API_KEY'))

    results = client.search({
        'search_query': query,
        'engine': 'youtube'
    })

    youtube_links = [(video['title'], video['link'], video['link'].replace("https://www.youtube.com/watch?v=", "")) for video in results['video_results']]
    youtube_links[:1]

    ytt_api = YouTubeTranscriptApi()

    youtube_transcripts = []
    for title, link, video_id in youtube_links[:1]:
        transcripts = ytt_api.fetch(video_id)
        transcript_text = " ".join([transcript.text for transcript in transcripts])

        youtube_transcripts.append(f'''Title: {title}\nLink: {link}\nTranscript:\n {transcript_text}\n''')

    return "\n\n".join(youtube_transcripts) 


system_instruction = """
You are an AI that gives a comprehensive information to users. Refer to tools for using information, query might be a youtube video.
If a user request benefits from real-world video transcripts or fits video title perfectly use YouTube transcripts for additional context and return the resource used. 
If no relevant transcripts are found, proceed with the best available information.
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
    # 'system_instruction': system_instruction
}

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# chat = client.chats.create(
#     model="gemini-1.5-flash",
#     config = {
#         "tools": [get_youtube_transcripts],
#         "automatic_function_calling": {"disable": True} # This line is not needed as automatic_function_calling is enabled by default
#     }
# )

# Call Gemini to trigger function execution
response = client.models.generate_content(
    model="gemini-1.5-flash",
    config=config,
    contents=f"{system_instruction}\n\n User Query: What happened to Jimmy Carter video" ,
)

print(response.text)
print(response)

# def call_function(function_call, functions):
#     function_name = function_call.name
#     function_args = function_call.args
#     # Find the function object from the list based on the function name
#     for func in functions:
#         if func.__name__ == function_name:
#             return func(**function_args)

# if(response.candidates[0].content.parts[0]):
#     part = response.candidates[0].content.parts[0]

#     result = ''
#     # Check if it's a function call; in real use you'd need to also handle text
#     # responses as you won't know what the model will respond with.
#     if part.function_call:
#         result = call_function(part.function_call, get_youtube_transcripts)

#     print(result)
# response = chat.send_message(
#     f"{system_instruction}\n\n User Query: Jimmy Carter"
# )


def call_function(function_call, functions):
    function_name = function_call.get("name")
    function_args = function_call.get("parameters", {})
    
    for func in functions:
        if func.__name__ == function_name:
            return func(**function_args)
    return None

if response and response.candidates:
    candidate = response.candidates[0]

    if candidate and candidate.content and candidate.content.parts:
        part = candidate.content.parts[0]

        result = "No function call detected"
        if part.function_call:
            result = call_function(part.function_call, [get_youtube_transcripts])

        print(result)
# print(response.text)
# print(response)