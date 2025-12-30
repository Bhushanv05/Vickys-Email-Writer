import streamlit as st
import os
import urllib.parse
import qrcode
from PIL import Image
from io import BytesIO
from groq import Groq
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Welcome Message
if 'first_load' not in st.session_state:
    st.toast("Welcome to Vicky's Email Writer! ✉️", icon="👋")
    st.session_state.first_load = True

# 3. Initialize History
if 'history' not in st.session_state:
    st.session_state.history = []

# 4. Sidebar: Menu, QR Code, and History
with st.sidebar:
    st.title("📖 App Menu")
    st.markdown("Polish your thoughts into professional emails.")
    
    # QR Code Section
    st.divider()
    st.subheader("📲 Share App")
    app_url = "https://vicky-email-writer.streamlit.app" 
    qr = qrcode.make(app_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf, caption="Scan to share!")
    
    st.divider()
    st.subheader("📜 Recent History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Email {i+1}"):
                st.text(item)
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No history yet.")

# 5. Styling
st.markdown("""
    <style>
    .stApp { background-color: #f1f8e9; }
    h1 { color: #1b5e20; text-align: center; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        width: 100%;
    }
    .wa-button {
        background-color: #25D366 !important;
        color: white !important;
        text-decoration: none;
        padding: 10px;
        border-radius: 10px;
        display: block;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 6. Initialize Groq
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY missing.")
    st.stop()

# 7. Main UI
st.title("✉️ Vicky_Email_writer")

# VOICE INPUT SECTION
st.write("### Step 1: Speak or Type your message")
audio_input = mic_recorder(
    start_prompt="🎤 Click to Speak Draft",
    stop_prompt="🛑 Stop Recording",
    key='recorder'
)

# Logic to handle transcribed voice
voice_text = ""
if audio_input:
    # Use Groq's Whisper model for high-quality transcription
    with st.spinner("Transcribing your voice..."):
        try:
            # Save audio to temp file for Groq Whisper API
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_input['bytes'])
            
            with open("temp_audio.wav", "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=("temp_audio.wav", audio_file.read()),
                    model="whisper-large-v3",
                )
                voice_text = transcription.text
        except Exception as e:
            st.error(f"Transcription Error: {e}")

# TEXT AREA
draft = st.text_area("Your rough draft:", value=voice_text, height=150, placeholder="Type here or use the mic above...")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2:
    length = st.selectbox("Length", ["Concise", "Detailed"])

if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                prompt = f"Rewrite as a professional email. Tone: {tone}, Length: {length}. Content: {draft}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                st.session_state.history.insert(0, result)
                if len(st.session_state.history) > 3: st.session_state.history.pop()
                
                st.markdown("### 📄 Result:")
                st.info(result)
                st.download_button("Download Email 💾", result, file_name="email.txt")
                
                whatsapp_text = urllib.parse.quote(result)
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" class="wa-button">Share to WhatsApp 📱</a>', unsafe_allow_html=True)
                
                st.balloons()
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please provide a draft first!")
