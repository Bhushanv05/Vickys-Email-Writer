import streamlit as st
import os
import urllib.parse
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Initialize History in Session State
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. Sidebar with Help Guide and History
with st.sidebar:
    st.title("📖 App Menu")
    st.markdown("""
    **How to Use:**
    1. Paste your rough notes.
    2. Choose tone and length.
    3. Click Generate!
    4. Share via WhatsApp or Download.
    """)
    
    st.divider()
    
    # History Section
    st.subheader("📜 Recent History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"Email {i+1}"):
                st.text(item)
    else:
        st.write("No history in this session yet.")
    
    st.divider()
    st.info("Built by Vicky | Free for friends")

# 4. Fixed CSS for Green Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f8e9;
    }
    h1 {
        color: #1b5e20;
        text-align: center;
    }
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
    }
    </style>
    """, unsafe_allow_html=True) # Corrected parameter

# 5. App Header
st.title("✉️ Vicky_Email_writer")
st.write("Professional emails made easy.")

# 6. Initialize Groq Client
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY not found in Secrets.")
    st.stop()

# 7. Main Input Section
draft = st.text_area("Step 1: Paste your rough message here:", height=150)
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2:
    length = st.selectbox("Length", ["Concise", "Detailed"])

# 8. AI Generation Logic
if st.button("Generate Professional Email ✨"):
    if draft:
        with st.spinner("Vicky is writing..."):
            try:
                prompt = f"Rewrite this as a professional email. Tone: {tone}, Length: {length}. Content: {draft}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # Save to History (Keep last 3)
                st.session_state.history.insert(0, result)
                if len(st.session_state.history) > 3:
                    st.session_state.history.pop()
                
                # Display Results
                st.markdown("### 📄 Result:")
                st.info(result)
                
                # Action Buttons
                st.download_button("Download Email 💾", result, file_name="email.txt")
                
                whatsapp_text = urllib.parse.quote(result)
                whatsapp_url = f"https://wa.me/?text={whatsapp_text}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="wa-button">Share to WhatsApp 📱</a>', unsafe_allow_html=True)
                
                st.rerun() # Refresh sidebar to show new history
                
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please enter text first.")
