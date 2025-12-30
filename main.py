import streamlit as st
import os
import urllib.parse
import qrcode
from PIL import Image
from io import BytesIO
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Welcome Message (Shows on every load)
st.toast("Welcome to Vicky's Email Writer! ✉️", icon="👋")

# 3. Initialize History
if 'history' not in st.session_state:
    st.session_state.history = []

# 4. Sidebar: Menu, QR Code, and History
with st.sidebar:
    st.title("📖 App Menu")
    st.markdown("Easily polish your rough notes into professional emails.")
    
    # QR Code Section
    st.divider()
    st.subheader("📲 Share App")
    # Replace with your actual Streamlit URL
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

# 5. Fixed CSS for Green Theme
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

# 6. Initialize Groq Client
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY missing.")
    st.stop()

# 7. Main UI
st.title("✉️ Vicky_Email_writer")
draft = st.text_area("Step 1: Paste your rough message here:", height=150)
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
                
                st.balloons() # Fun celebration effect!
                st.rerun()
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please enter text first.")
