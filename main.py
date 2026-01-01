import streamlit as st
import requests
import datetime
import urllib.parse
from streamlit_mic_recorder import mic_recorder
import os
import time

# Page Configuration
st.set_page_config(
    page_title="ProMailer AI - Free Email Generator",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main container */
    .main-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin: 1rem auto;
        max-width: 900px;
    }
    
    /* Title styling */
    .title {
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* API status badges */
    .api-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 2px;
    }
    .api-badge.groq {
        background: #10B981;
        color: white;
    }
    .api-badge.hf {
        background: #FFD700;
        color: black;
    }
    
    /* Feature cards */
    .feature-card {
        background: #f8f9ff;
        padding: 1rem;
        border-radius: 15px;
        border: 2px solid #667eea;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Result box */
    .result-box {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #667eea;
        margin: 1rem 0;
        white-space: pre-wrap;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Language badges */
    .lang-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 4px 12px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    defaults = {
        'groq_key': "",
        'hf_key': "",
        'history': [],
        'current_email': "",
        'emails_generated': 0,
        'voice_text': "",
        'last_api_used': ""
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Sidebar - API Configuration
with st.sidebar:
    st.markdown("## 🔑 API Configuration")
    
    # Groq API Section
    st.markdown("### 1. Groq API (Primary)")
    with st.expander("How to get Groq key", expanded=False):
        st.markdown("""
        **Free & Fast:**
        1. Visit **[console.groq.com](https://console.groq.com)**
        2. Sign up with Google/GitHub
        3. Go to **API Keys**
        4. Click **Create API Key**
        5. Copy key (starts with `gsk_`)
        """)
    
    groq_key = st.text_input(
        "Groq API Key:",
        value=st.session_state.groq_key,
        type="password",
        placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Required for voice recording & best Marathi support"
    )
    
    if groq_key:
        st.session_state.groq_key = groq_key.strip()
        st.success("✅ Groq key saved!")
    
    # Hugging Face API Section
    st.markdown("---")
    st.markdown("### 2. Hugging Face (Backup)")
    with st.expander("How to get HF token", expanded=True):
        st.markdown("""
        **Free Backup API:**
        1. Go to **[huggingface.co](https://huggingface.co)**
        2. Sign up (free)
        3. Click **profile picture** → **Settings**
        4. Go to **Access Tokens**
        5. Click **"New token"**
        6. Name: `promailer-ai`
        7. Role: **Read**
        8. Click **Generate**
        9. **Copy token** (starts with `hf_`)
        
        ⚠️ **Save immediately!** Won't show again.
        """)
    
    hf_key = st.text_input(
        "Hugging Face Token:",
        value=st.session_state.hf_key,
        type="password",
        placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        help="Free backup if Groq fails"
    )
    
    if hf_key:
        st.session_state.hf_key = hf_key.strip()
        st.success("✅ Hugging Face token saved!")
    
    # API Status
    st.markdown("---")
    st.markdown("### 📊 API Status")
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        if st.session_state.groq_key:
            st.markdown('<span class="api-badge groq">✅ Groq Ready</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: orange">⚠️ Groq Needed</span>', unsafe_allow_html=True)
    
    with status_col2:
        if st.session_state.hf_key:
            st.markdown('<span class="api-badge hf">✅ HF Ready</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: gray">ℹ️ HF Optional</span>', unsafe_allow_html=True)
    
    # Stats
    st.markdown(f"**Emails Generated:** {st.session_state.emails_generated}")
    st.markdown(f"**History Items:** {len(st.session_state.history)}")
    
    # History
    st.markdown("---")
    st.markdown("### 📜 Email History")
    
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[:3]):
            with st.expander(f"📧 {item.get('time', '')} - {item.get('api', '')}"):
                st.text(item.get('email', '')[:120] + "...")
                if st.button(f"Use This", key=f"use_{i}"):
                    st.session_state.current_email = item.get('email', '')
                    st.rerun()
        
        if st.button("Clear History", type="secondary"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No emails generated yet")
    
    # Footer
    st.markdown("---")
    st.caption("ProMailer AI v1.0")
    st.caption("Made for Marathi/Hindi speakers")

# Main Content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="title">✉️ ProMailer AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Turn Marathi/Hindi thoughts into professional emails instantly!</p>', unsafe_allow_html=True)

# Language Support Badges
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <span class="lang-badge">Marathi</span>
    <span class="lang-badge">Hindi</span>
    <span class="lang-badge">English</span>
    <span class="lang-badge">Gujarati</span>
    <span class="lang-badge">Tamil</span>
    <span class="lang-badge">Telugu</span>
</div>
""", unsafe_allow_html=True)

# Features
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="feature-card">🎤<br>Voice Input</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="feature-card">🌍<br>Multi-Language</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="feature-card">⚡<br>Fast & Free</div>', unsafe_allow_html=True)

# Language Selection
st.markdown("---")
st.markdown("### 🌐 Choose Languages")

col_lang1, col_lang2 = st.columns(2)
with col_lang1:
    input_lang = st.selectbox(
        "🎤 Input Language:",
        ["Marathi", "Hindi", "English", "Gujarati", "Tamil", "Telugu"],
        index=0,
        help="Speak or type in this language"
    )

with col_lang2:
    target_lang = st.selectbox(
        "📧 Output Language:",
        ["English", "Marathi", "Hindi"],
        index=0,
        help="Professional email will be in this language"
    )

# Show language info
if input_lang == target_lang:
    st.success(f"✅ We'll polish your {input_lang} into professional {target_lang}")
else:
    st.info(f"💡 Input: **{input_lang}** → Output: **{target_lang}**")

# Voice Input (Groq Only)
if st.session_state.groq_key:
    st.markdown("---")
    st.markdown("### 🎤 Voice Input (Groq Only)")
    
    audio = mic_recorder(
        start_prompt="🎤 Click to Start Recording",
        stop_prompt="⏹️ Click to Stop",
        key="voice_recorder",
        format="wav"
    )
    
    if audio and 'bytes' in audio:
        with st.spinner("Transcribing your voice..."):
            try:
                from groq import Groq
                client = Groq(api_key=st.session_state.groq_key)
                
                # Save audio to temporary file
                temp_file = "temp_voice.wav"
                with open(temp_file, "wb") as f:
                    f.write(audio['bytes'])
                
                # Transcribe with Groq Whisper
                with open(temp_file, "rb") as f:
                    transcription = client.audio.transcriptions.create(
                        file=("voice.wav", f.read()),
                        model="whisper-large-v3",
                        language=input_lang.lower() if input_lang.lower() in ["marathi", "hindi", "english"] else None
                    )
                
                st.session_state.voice_text = transcription.text
                st.success(f"✅ Transcribed: *{st.session_state.voice_text[:100]}...*")
                
                # Clean up
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            except Exception as e:
                st.error(f"❌ Voice error: {str(e)[:100]}")
else:
    st.info("💡 Enable voice: Add Groq API key in sidebar")

# Text Input
st.markdown("---")
st.markdown("### 📝 Text Input")
draft = st.text_area(
    f"Type your message in {input_lang}:",
    value=st.session_state.voice_text or st.session_state.current_email,
    height=150,
    placeholder=f"Example in {input_lang}: 'मला उद्या सुट्टी हवी आहे कारण लग्नाचा कार्यक्रम आहे' or 'Need leave tomorrow for marriage function'",
    help="Type naturally in your language"
)

# Email Customization
st.markdown("---")
st.markdown("### ⚙️ Customize Your Email")

col_opt1, col_opt2, col_opt3 = st.columns(3)
with col_opt1:
    tone = st.selectbox("Tone", ["Professional", "Formal", "Friendly", "Urgent"], index=0)
with col_opt2:
    length = st.selectbox("Length", ["Concise", "Detailed", "Brief"], index=0)
with col_opt3:
    email_type = st.selectbox("Type", ["Leave Request", "Business", "Personal", "Official"], index=0)

# Generate Functions
def generate_with_groq(prompt):
    """Generate email using Groq API"""
    try:
        from groq import Groq
        client = Groq(api_key=st.session_state.groq_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Best for Marathi/Hindi
            messages=[
                {"role": "system", "content": "You are a professional email writer specializing in Indian languages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)

def generate_with_huggingface(prompt):
    """Generate email using Hugging Face API"""
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.hf_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.95
            }
        }
        
        # Use Mistral model (good for Indian languages)
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            headers=headers,
            json=payload,
            timeout=45
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Clean up the response
                if prompt in generated_text:
                    generated_text = generated_text.replace(prompt, "").strip()
                return generated_text, None
        else:
            error_msg = f"Status {response.status_code}"
            if response.status_code == 503:
                error_msg += " - Model loading, try again in 30 seconds"
            return None, error_msg
            
    except Exception as e:
        return None, str(e)

# Generate Button
st.markdown("---")
generate_disabled = not draft.strip() or (not st.session_state.groq_key and not st.session_state.hf_key)

if st.button("✨ Generate Professional Email", 
             type="primary", 
             use_container_width=True,
             disabled=generate_disabled):
    
    if not draft.strip():
        st.warning("⚠️ Please enter some text!")
    elif not st.session_state.groq_key and not st.session_state.hf_key:
        st.error("❌ Please add at least one API key in sidebar!")
    else:
        with st.spinner(f"🤖 Creating {target_lang} email..."):
            # Build the prompt
            prompt = f"""Convert the following message into a professional email.

INPUT LANGUAGE: {input_lang}
OUTPUT LANGUAGE: {target_lang}
TONE: {tone}
LENGTH: {length}
EMAIL TYPE: {email_type}

USER'S MESSAGE:
{draft}

INSTRUCTIONS:
1. Write the email in {target_lang}
2. Use a {tone.lower()} tone
3. Make it {length.lower()} in length
4. Include an appropriate subject line
5. Use proper email format (greeting, body, closing)
6. Keep the original meaning but make it professional
7. Add placeholders like [Your Name] where needed

EMAIL OUTPUT:"""

            # Try Groq first
            email_result = None
            error_msg = None
            api_used = ""
            
            if st.session_state.groq_key:
                email_result, error_msg = generate_with_groq(prompt)
                api_used = "Groq"
            
            # If Groq fails, try Hugging Face
            if not email_result and st.session_state.hf_key:
                st.info("🔄 Groq failed, trying Hugging Face backup...")
                email_result, error_msg = generate_with_huggingface(prompt)
                api_used = "Hugging Face"
            
            if email_result:
                # Save to history
                timestamp = datetime.datetime.now().strftime("%H:%M • %d/%m")
                st.session_state.history.insert(0, {
                    'email': email_result,
                    'time': timestamp,
                    'api': api_used,
                    'input_lang': input_lang,
                    'output_lang': target_lang
                })
                
                # Update counters
                st.session_state.emails_generated += 1
                st.session_state.last_api_used = api_used
                st.session_state.current_email = email_result
                
                # Display result
                st.markdown(f"### ✅ Email Generated with <span class='api-badge {api_used.lower().replace(' ', '')}'>{api_used}</span>", unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{email_result}</div>', unsafe_allow_html=True)
                
                # Action Buttons
                st.markdown("### 📋 Actions")
                action_cols = st.columns(4)
                
                with action_cols[0]:
                    if st.button("📋 Copy Text", use_container_width=True):
                        st.toast("✅ Copied to clipboard!", icon="✅")
                
                with action_cols[1]:
                    whatsapp_text = urllib.parse.quote(f"Professional Email:\n\n{email_result}")
                    st.markdown(f'''
                        <a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration: none;">
                            <button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">
                                WhatsApp
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                
                with action_cols[2]:
                    email_subject = urllib.parse.quote("Professional Email")
                    email_body = urllib.parse.quote(email_result)
                    st.markdown(f'''
                        <a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration: none;">
                            <button style="width:100%; background:#EA4335; color:white; border:none; padding:10px; border-radius:8px; font-weight:bold; cursor:pointer;">
                                Gmail
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                
                with action_cols[3]:
                    st.download_button(
                        label="📥 Download",
                        data=email_result,
                        file_name=f"email_{timestamp.replace(':', '').replace(' • ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                st.balloons()
            else:
                st.error(f"❌ Generation failed: {error_msg}")
                st.info("💡 Try: 1) Check API key 2) Use shorter text 3) Try again in 30 seconds")

# Examples Section
with st.expander("📚 Examples & Tips", expanded=False):
    st.markdown("### Marathi to English Example")
    
    example_col1, example_col2 = st.columns(2)
    with example_col1:
        st.markdown("**Input (Marathi):**")
        st.code("बॉस, मला उद्या सुट्टी हवी आहे. डॉक्टरची सल्ला आहे.", language=None)
    
    with example_col2:
        st.markdown("**Output (English):**")
        st.code("""Subject: Sick Leave Request for Tomorrow

Dear Sir/Madam,

I hope this email finds you well. I am writing to request sick leave for tomorrow as per my doctor's advice.

I apologize for any inconvenience caused and will ensure to complete my pending tasks before taking leave.

Thank you for your understanding.

Best regards,
[Your Name]""", language=None)
    
    st.markdown("---")
    st.markdown("### 💡 Tips for Best Results:")
    st.markdown("""
    1. **Be specific** - Include dates, reasons, and requirements
    2. **Mention context** - Who it's for, why it's needed
    3. **Keep natural** - Write as you'd speak in your language
    4. **Try different tones** - Professional, friendly, urgent, etc.
    5. **Review output** - Always check before sending
    """)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: white; padding: 2rem;">
    <p style="font-size: 0.9rem;">ProMailer AI • Free Professional Email Generator • 
    Using: Groq (Primary) + Hugging Face (Backup)</p>
    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.8);">
    Supports Marathi, Hindi, English, Gujarati, Tamil, Telugu
    </p>
</div>
""", unsafe_allow_html=True)