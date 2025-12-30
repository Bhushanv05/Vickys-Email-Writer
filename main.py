import streamlit as st
import os
import urllib.parse
from groq import Groq
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration
st.set_page_config(page_title="Vicky Email Writer", page_icon="✉️", layout="centered")

# 2. Simple Styling
st.markdown("""
    <style>
    .stApp { background-color: #f1f8e9; }
    h1 { color: #1b5e20; text-align: center; }
    .stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 10px; width: 100%; height: 3em; }
    .wa-button { background-color: #25D366 !important; color: white !important; text-decoration: none; padding: 10px; border-radius: 10px; display: block; text-align: center; font-weight: bold; margin-top: 10px; line-height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Groq
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("API Key missing. Check your Streamlit Secrets.")
    st.stop()

# 4. Main UI
st.title("✉️ Vicky_Email_writer")

# Language Selection
target_lang = st.radio("Final Email Language:", ["English", "Marathi"], horizontal=True)

# Voice Input
st.write("### Step 1: Speak or Type your message")
audio_input = mic_recorder(start_prompt="🎤 Click to Speak", stop_prompt="🛑 Stop Recording", key='recorder')

voice_text = ""
if audio_input:
    with st.spinner("Processing voice..."):
        try:
            with open("temp.wav", "wb") as f: f.write(audio_input['bytes'])
            with open("temp.wav", "rb") as af:
                transcription = client.audio.transcriptions.create(file=("temp.wav", af.read()), model="whisper-large-v3")
                voice_text = transcription.text
        except: st.error("Voice processing error.")

# Text Input Area
draft = st.text_area("Your rough draft:", value=voice_text, height=150, placeholder="Marathi or English...")

col1, col2 = st.columns(2)
with col1: tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2: length = st.selectbox("Length", ["Concise", "Detailed"])

# 5. Generation Logic
if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                prompt = f"Rewrite as a professional email in {target_lang}. Tone: {tone}, Length: {length}. Content: {draft}"
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                result = response.choices[0].message.content
                
                st.info(result)
                
                # Action Buttons
                st.download_button("Download 💾", result, file_name="email.txt")
                
                whatsapp_text = urllib.parse.quote(result)
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" class="wa-button">Share to WhatsApp 📱</a>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e: st.error(f"Error: {e}")
    else:
        st.warning("Please provide a draft first!")
