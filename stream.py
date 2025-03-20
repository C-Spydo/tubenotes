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
in a concise way, providing important points within 1000 words,
emphasizing the most vital points. Here is the text to summarize:
"""

# Add app configuration
st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="wide")

# Display a logo
st.image("logo.jpg", width=200)  # Replace 'logo.jpg' with your logo file

# Title and instructions
st.markdown("<h1 style='text-align: center; color: #6c63ff;'>YouTube Video Summarizer 🎥</h1>", unsafe_allow_html=True)
st.write("📌 Provide a YouTube video URL to generate a detailed summary, analyze its sentiment, and create an audio summary with character-based voice customization!")

# User input
video_url = st.text_input("Enter YouTube Video URL:")

# Function to extract transcript from a YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for item in transcript_text:
            transcript += " " + item["text"]

        return transcript, video_id
    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        return None, None

# Function to generate a 1000-word summary using Google Gemini
def generate_gemini_content(transcript_text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")  # Replace with available model
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

# Function for text-to-speech conversion with avatar selection
def generate_audio(summary_text, avatar):
    try:
        tts = gTTS(text=summary_text, lang="en", slow=False)  # Currently supports basic TTS
        audio_file = f"{avatar}_summary_audio.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Error generating audio: {str(e)}")
        return None

# Function to perform sentiment analysis with explanation
def analyze_sentiment(summary_text):
    try:
        analysis = TextBlob(summary_text)
        explanation = (
            "Polarity indicates how positive or negative the content is "
            "on a scale from -1 (very negative) to 1 (very positive). "
            "Subjectivity measures whether the content is opinionated (1) or factual (0)."
        )
        return {
            "polarity": analysis.polarity,
            "subjectivity": analysis.subjectivity,
            "explanation": explanation,
        }
    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")
        return None

if st.button("Summarize"):
    if not video_url:
        st.error("Please provide a valid YouTube video URL.")
    else:
        with st.spinner("Processing..."):
            # Step 1: Extract transcript
            transcript, video_id = extract_transcript_details(video_url)

            if transcript and video_id:
                # Step 2: Generate summary
                summary = generate_gemini_content(transcript)

                if summary:
                    # Step 3: Perform sentiment analysis
                    sentiment = analyze_sentiment(summary)

                    # Step 4: Generate audio with avatar
                    avatar = st.selectbox(
                        "Choose your avatar for audio playback:",
                        ["Default", "Male - American", "Female - British", "Child - Neutral", "Senior - Australian"]
                    )
                    audio_file = generate_audio(summary, avatar)

                    # Display results
                    st.success("Summary generated successfully!")
                    st.subheader("Video Summary")
                    st.write(summary)

                    # Display sentiment analysis
                    if sentiment:
                        st.subheader("Sentiment Analysis")
                        st.write(f"**Polarity**: {sentiment['polarity']}")
                        st.write(f"**Subjectivity**: {sentiment['subjectivity']}")
                        st.info(sentiment["explanation"])

                    # Display YouTube thumbnail and link
                    st.subheader("Video Thumbnail")
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                    st.image(thumbnail_url, caption="YouTube Video Thumbnail")
                    st.write(f"[Watch the video on YouTube](https://www.youtube.com/watch?v={video_id})")

                    # Display audio summary with controls
                    if audio_file:
                        st.subheader("Audio Summary")
                        st.audio(audio_file)
                        st.download_button(
                            label="Download Audio Summary",
                            data=open(audio_file, "rb"),
                            file_name=f"{avatar}_summary_audio.mp3",
                            mime="audio/mpeg"
                        )
