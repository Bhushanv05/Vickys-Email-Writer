import streamlit as st
import os
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Simplified CSS for the "Green" look (Fixed for Streamlit)
st.markdown("""
    <style>
    .stApp {
        background-color: #f1f8e9;
    }
    h1 {
        color: #1b5e20;
    }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
    }
    </style>
    """, unsafe_content_allowed=True)

# 3. App Header
st.title("✉️ Vicky_Email_writer")
st.write("Professional emails made easy.")

# 4. Initialize Groq Client
try:
    # This looks for the secret in Streamlit Cloud Settings
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("Error: GROQ_API_KEY not found in Secrets.")
    st.stop()

# 5. Input Section
draft = st.text_area("Paste your rough message here:", height=150)
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Tone", ["Formal", "Friendly", "Urgent"])
with col2:
    length = st.selectbox("Length", ["Concise", "Detailed"])

# 6. Logic
if st.button("Generate Email ✨"):
    if draft:
        with st.spinner("Writing..."):
            try:
                prompt = f"Rewrite this as a professional email. Tone: {tone}, Length: {length}. Message: {draft}"
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.markdown("### Your Result:")
                st.info(result)
                
                st.download_button("Download Text", result, file_name="email.txt")
            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please enter text.")
