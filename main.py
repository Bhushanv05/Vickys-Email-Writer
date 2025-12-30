import streamlit as st
import os
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Vicky Email Writer",
    page_icon="✉️",
    layout="centered"
)

# 2. Professional Green Theme CSS
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f1f8e9;
    }
    /* Text Area Styling */
    .stTextArea textarea {
        border: 2px solid #2e7d32 !important;
        border-radius: 10px;
    }
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background-color: #2e7d32 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    /* Headers */
    h1 {
        color: #1b5e20;
        text-align: center;
    }
    /* Info Box */
    .stInfo {
        background-color: #ffffff;
        border-left: 5px solid #2e7d32;
        border-radius: 5px;
    }
    </style>
    """, unsafe_content_allowed=True)

# 3. App Header
st.title("✉️ Vicky_Email_writer")
st.markdown("<p style='text-align: center;'>Transform your rough notes into polished, professional emails instantly.</p>", unsafe_content_allowed=True)

# 4. Initialize Groq Client
try:
    # Looks for secret in Streamlit Cloud Settings
    api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ GROQ_API_KEY missing! Go to App Settings > Secrets and add your key.")
    st.stop()

# 5. Input UI
st.markdown("---")
draft = st.text_area("Step 1: Paste your rough message or ideas here:", 
                    height=180, 
                    placeholder="Example: boss i want leave for 2 days because family function...")

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("Step 2: Choose Tone", ["Formal & Professional", "Friendly & Polite", "Direct", "Urgent"])
with col2:
    length = st.selectbox("Step 3: Choose Length", ["Concise (Short)", "Detailed (Standard)"])

# 6. AI Logic and Results
if st.button("Refine My Email ✨"):
    if draft.strip():
        with st.spinner("Vicky is writing... please wait."):
            try:
                # Instruction for the AI
                system_instruction = f"""
                You are a Professional Communication Expert.
                Your job is to rewrite the user's input into a high-quality email.
                Tone: {tone}
                Length: {length}
                
                Requirements:
                - Fix all grammar and spelling errors.
                - Create an effective 'Subject:' line.
                - Use professional greetings (Dear...) and closings (Sincerely, Regards...).
                - After the email text, add a '---' separator.
                - Add a section '💡 Grammar Lessons for You' where you explain 2 errors found in the original draft.
                """
                
                # Call Groq AI
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": draft}
                    ],
                    temperature=0.7
                )
                
                refined_email = completion.choices[0].message.content
                
                # Display Output
                st.markdown("### 📄 Your Refined Email")
                st.info(refined_email)
                
                # Download Option
                st.download_button(
                    label="Download as Text File 💾",
                    data=refined_email,
                    file_name="Vicky_Email.txt",
                    mime="text/plain"
                )
                
                st.success("You can now copy the text above or download the file!")

            except Exception as e:
                st.error(f"AI Error: {e}")
    else:
        st.warning("Please type something in the box above first!")

# 7. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Vicky_Email_writer v1.0 | No more grammar mistakes!</p>", unsafe_content_allowed=True)