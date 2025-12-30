import streamlit as st
import os
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Sidebar with Help Guide
with st.sidebar:
    st.title("📖 How to Use")
    st.markdown("""
    1. **Draft:** Paste your rough notes in the main box.
    2. **Tone:** Choose formal or friendly.
    3. **Generate:** Click the button to see the result.
    4. **Download:** Save it as a text file!
    
    ---
    **Note:** This app is 100% free for friends.
    """)
    st.info("Built by Vicky")

# 3. Fixed CSS (Using the correct 'unsafe_allow_html' parameter)
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
    </style>
    """, unsafe_allow_html=True) # TYPO FIXED HERE

# 4. App Header
st.title("✉️ Vicky_Email_writer")
st.write("Professional emails made easy.")

# 5. Initialize Groq Client
try:
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY not found in Secrets.")
    st.stop()

# 6. Main Input Section
draft = st.text_area("Paste your rough message here:", height=150)
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2:
    length = st.selectbox("Length", ["Concise", "Detailed"])

# 7. AI Logic
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
                st.markdown("### 📄 Result:")
                st.info(result)
                
                st.download_button("Download Email 💾", result, file_name="email.txt")
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please enter text first.")
