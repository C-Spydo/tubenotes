import streamlit as st
import requests
import os
import base64
from gtts import gTTS

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://127.0.0.1:5000")

st.set_page_config(page_title="YOUTUBE ZETA", layout="wide")
st.title("🤖 ZETA-AI")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to call the Flask backend
def chat_with_ai(user_input):
    response = requests.post(f"{FLASK_API_URL}/summarize", json={"user_query": user_input})
    if response.status_code == 200:
        return response.json().get("response", "Error: No response from API")
    return "Error: Unable to fetch response"

# Function to generate speech from text
def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# Function to encode audio for Streamlit playback
def get_audio_player(audio_file):
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    encoded_audio = base64.b64encode(audio_bytes).decode()
    return f'<audio controls><source src="data:audio/mp3;base64,{encoded_audio}" type="audio/mpeg"></audio>'

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            audio_file = text_to_speech(msg["content"])
            audio_html = get_audio_player(audio_file)
            st.markdown("🔊 Click below to hear:", unsafe_allow_html=True)
            st.markdown(audio_html, unsafe_allow_html=True)

# User input area
user_input = st.chat_input("Type a message...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response from Flask
    ai_response = chat_with_ai(user_input)

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    with st.chat_message("assistant"):
        st.markdown(ai_response)
        
        # Generate and display speech
        audio_file = text_to_speech(ai_response)
        audio_html = get_audio_player(audio_file)
        st.markdown("🔊 Click below to hear:", unsafe_allow_html=True)
        st.markdown(audio_html, unsafe_allow_html=True)