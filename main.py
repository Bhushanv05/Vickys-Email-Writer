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
    st.markdown("Turn rough Marathi or English notes into professional emails.")
    
    # NEW: Share App Link Button
    st.divider()
    st.subheader("📲 Share this App")
    app_link = "https://vicky-email-writer.streamlit.app/"
    share_msg = urllib.parse.quote(f"Hey! Check out Vicky's AI Email Writer. It converts Marathi/English voice notes into professional emails: {app_link}")
    st.markdown(f'''
        <a href="https://wa.me/?text={share_msg}" target="_blank" 
           style="text-decoration:none;">
            <button style="background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; width:100%; cursor:pointer; font-weight:bold;">
                Share App via WhatsApp 📱
            </button>
        </a>
    ''', unsafe_allow_html=True)

    st.divider()
    st.subheader("📜 Recent History")
    if 'history' not in st.session_state:
        st.session_state.history = []
        
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Email {i+1}"):
                st.text(item)
    else:
        st.write("No history yet.")

    # Your Personalized Signature (As requested)
    st.divider()
    st.markdown("### Built by Vicky")

# 3. Custom Styling (Green Theme)
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
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("Please check your Streamlit Secrets.")
    st.stop()

# 5. Main Application Content
st.title("✉️ Vicky_Email_writer")
target_lang = st.radio("Final Email Language:", ["English", "Marathi"], horizontal=True)

st.write("### Step 1: Speak or Type your message")
audio_input = mic_recorder(start_prompt="🎤 Click to Speak", stop_prompt="🛑 Stop Recording", key='recorder')

voice_text = ""
if audio_input:
    with st.spinner("Vicky is listening..."):
        try:
            with open("temp.wav", "wb") as f: f.write(audio_input['bytes'])
            with open("temp.wav", "rb") as af:
                transcription = client.audio.transcriptions.create(file=("temp.wav", af.read()), model="whisper-large-v3")
                voice_text = transcription.text
        except: st.error("Voice processing error.")

draft = st.text_area("Your rough notes:", value=voice_text, height=150)

col1, col2 = st.columns(2)
with col1: tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2: length = st.selectbox("Length", ["Concise", "Detailed"])

# 6. Generation Logic
if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                prompt = f"Rewrite the following notes into a professional email in {target_lang}. Tone: {tone}, Length: {length}. Notes: {draft}"
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                result = response.choices[0].message.content
                
                st.session_state.history.insert(0, result)
                st.info(result)
                
                # WhatsApp Result Sharing
                whatsapp_text = urllib.parse.quote(result)
                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" class="wa-button">Share Email to WhatsApp 📱</a>', unsafe_allow_html=True)
                
                st.balloons()
                st.rerun() 
            except: st.error("AI Error.")
