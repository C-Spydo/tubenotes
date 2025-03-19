import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from gtts import gTTS
from textblob import TextBlob

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
prompt = """
You are a YouTube video summarizer. Summarize the transcript text
in a concise way, providing important points within 350 words.
Here is the text to summarize:
"""

# Function to extract transcript from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for item in transcript_text:
            transcript += " " + item["text"]

        return transcript
    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        return None

# Function to generate summary using Google Gemini
def generate_gemini_content(transcript_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Replace with available model
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

# Function for text-to-speech conversion
def generate_audio(summary_text):
    try:
        tts = gTTS(summary_text)
        audio_file = "summary_audio.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# Function to perform sentiment analysis
def analyze_sentiment(summary_text):
    try:
        analysis = TextBlob(summary_text)
        return {
            "polarity": analysis.polarity,
            "subjectivity": analysis.subjectivity
        }
    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")
        return None
