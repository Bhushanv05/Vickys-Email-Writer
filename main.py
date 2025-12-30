import streamlit as st
import os
import urllib.parse
from groq import Groq
from streamlit_mic_recorder import mic_recorder

# 1. Page Configuration
st.set_page_config(page_title="Vicky Email Writer", page_icon="✉️", layout="centered")

# 2. Sidebar Implementation
with st.sidebar:
    st.title("📖 App Menu")
    st.markdown("""
    **How to Use:**
    1. Select your target language.
    2. Click the 🎤 mic to speak or type your notes.
    3. Choose the tone and length.
    4. Click 'Generate' and share!
    """)
    
    st.divider()
    st.subheader("📜 Recent History")
    if 'history' not in st.session_state:
        st.session_state.history = []
        
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Email {i+1}"):
                st.text(item)
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No history in this session.")

    # Personalized Signature at the bottom
    st.divider()
    st.info("🎨 **Built by Vicky** | Free for friends")

# 3. Styling
st.markdown("""
    <style>
    .stApp { background-color: #f1f8e9; }
    h1 { color: #1b5e20; text-align: center; }
    .stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 10px; width: 100%; height: 3em; }
    .wa-button { background-color: #25D366 !important; color: white !important; text-decoration: none; padding: 10px; border-radius: 10px; display: block; text-align: center; font-weight: bold; margin-top: 10px; line-height: 2.5em; }
    </style>
    """, unsafe_allow_html=True)

# 4. Initialize Groq
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("API Key missing.")
    st.stop()

# 5. Main UI
st.title("✉️ Vicky_Email_writer")

target_lang = st.radio("Final Email Language:", ["English", "Marathi"], horizontal=True)

st.write("### Step 1: Speak or Type your message")
audio_input = mic_recorder(start_prompt="🎤 Click to Speak", stop_prompt="🛑 Stop", key='recorder')

voice_text = ""
if audio_input:
    with st.spinner("Processing voice..."):
        try:
            with open("temp.wav", "wb") as f: f.write(audio_input['bytes'])
            with open("temp.wav", "rb") as af:
                transcription = client.audio.transcriptions.create(file=("temp.wav", af.read()), model="whisper-large-v3")
                voice_text = transcription.text
        except: st.error("Voice processing error.")

draft = st.text_area("Your rough draft:", value=voice_text, height=150, placeholder="Marathi or English...")

col1, col2 = st.columns(2)
with col1: tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2: length = st.selectbox("Length", ["Concise", "Detailed"])

# 6. AI Logic
if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                prompt = f"Rewrite as a professional email in {target_lang}. Tone: {tone}, Length: {length}. Content: {draft}"
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                result = response.choices[0].message.content
                
                # Add to history
                st.session_state.history.insert(0, result)
                
                st.info(result)
                st.download_button("Download 💾", result, file_name="email.txt")
                
                whatsapp_text = urllib.parse.quote(result)
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" class="wa-button">Share to WhatsApp 📱</a>', unsafe_allow_html=True)
                st.balloons()
                st.rerun() 
            except Exception as e: st.error(f"Error: {e}")
