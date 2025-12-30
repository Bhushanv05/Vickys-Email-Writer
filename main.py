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

# 2. Welcome Toast
if 'first_load' not in st.session_state:
    st.toast("Namaste! Welcome to Vicky's Email Writer! ✉️", icon="👋")
    st.session_state.first_load = True

# 3. Initialize History
if 'history' not in st.session_state:
    st.session_state.history = []

# 4. Styling: Green Theme & WhatsApp Button
st.markdown("""
    <style>
    .stApp { background-color: #f1f8e9; }
    h1 { color: #1b5e20; text-align: center; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 10px;
        width: 100%;
        height: 3em;
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
        line-height: 2.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. Sidebar: QR Code, History, and Feedback
with st.sidebar:
    st.title("📖 App Menu")
    st.markdown("Speak or type in Marathi/English to get professional emails.")
    
    # QR Code Section
    st.divider()
    st.subheader("📲 Share App")
    app_url = "https://vicky-email-writer.streamlit.app" 
    qr = qrcode.make(app_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    st.image(buf, caption="Scan to share!")
    
    # History Section
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

    # Feedback Section
    st.divider()
    st.subheader("💬 Feedback")
    fb = st.text_area("Suggestions?", placeholder="What should Vicky add next?")
    if st.button("Submit"):
        st.success("Thanks! I'll see this in the logs. 🙏")
        print(f"FEEDBACK FROM USER: {fb}")

# 6. Initialize Groq Client
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY missing in Secrets.")
    st.stop()

# 7. Main UI
st.title("✉️ Vicky_Email_writer")

# Language Selection
target_lang = st.radio("Final Email Language:", ["English", "Marathi"], horizontal=True)

# Step 1: Voice/Text Input
st.write("### Step 1: Speak or Type your message")
audio_input = mic_recorder(
    start_prompt="🎤 Click to Speak (Marathi/English)",
    stop_prompt="🛑 Stop Recording",
    key='recorder'
)

voice_text = ""
if audio_input:
    with st.spinner("Transcribing..."):
        try:
            with open("temp.wav", "wb") as f: f.write(audio_input['bytes'])
            with open("temp.wav", "rb") as af:
                transcription = client.audio.transcriptions.create(
                    file=("temp.wav", af.read()),
                    model="whisper-large-v3"
                )
                voice_text = transcription.text
        except Exception as e:
            st.error(f"Voice Error: {e}")

draft = st.text_area("Your rough draft:", value=voice_text, height=150, placeholder="Start typing or use the mic...")

# Step 2: Settings
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2:
    length = st.selectbox("Length", ["Concise", "Detailed"])

# Step 3: Generation Logic
if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                # Instruction to handle Marathi and English drafting
                prompt = f"""
                Draft: '{draft}'. 
                Rewrite this as a high-quality professional email in {target_lang}. 
                Tone: {tone}, Length: {length}.
                If input is Marathi and target is English, translate it professionally.
                """
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # Update History
                st.session_state.history.insert(0, result)
                if len(st.session_state.history) > 3: st.session_state.history.pop()
                
                # Results Display
                st.markdown("### 📄 Result:")
                st.info(result)
                
                # Action Buttons
                st.download_button("Download 💾", result, file_name="email.txt")
                
                whatsapp_text = urllib.parse.quote(result)
                whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="wa-button">Share to WhatsApp 📱</a>', unsafe_allow_html=True)
                
                st.balloons()
                st.rerun() # Refresh history immediately
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please provide a draft first!")
