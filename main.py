import streamlit as st
import os
import urllib.parse
import datetime
from streamlit_mic_recorder import mic_recorder

# Force complete cache clear and set page config
st.set_page_config(
    page_title="ProMailer AI v2.0.1", 
    page_icon="✉️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# CRITICAL: Clear ALL caches to force fresh load
st.cache_data.clear()
st.cache_resource.clear()

# Force rerun marker
if 'app_version' not in st.session_state:
    st.session_state.app_version = "2.0.1"
    st.rerun()

# 2. Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_email' not in st.session_state:
    st.session_state.current_email = ""

# 3. Sidebar Implementation
with st.sidebar:
    st.markdown("# 📖 ProMailer AI")
    st.caption("v2.0.1 - Clean Version")
    st.markdown("**✍️ Type OR 🎤 Speak**")
    st.caption("⌨️ Type rough notes → Professional email")
    st.caption("🎤 Speak casually → Professional email")
    st.caption("🌍 Works in English, Marathi, Hindi")

    # Share App Link Button
    st.markdown("---")
    st.markdown("### 📲 Share this App")
    app_link = "https://promailer-ai.streamlit.app/"
    share_msg = urllib.parse.quote(
        f"Hey! Check out ProMailer AI - Converts rough notes into professional emails. Type or speak in any language: {app_link}"
    )
    
    st.markdown(f'''
        <a href="https://wa.me/?text={share_msg}" target="_blank" 
           style="text-decoration:none; display:block;">
            <div style="background-color:#25D366; color:white; border:none; 
                   padding:12px; border-radius:8px; text-align:center; 
                   font-weight:bold; font-size:14px; cursor:pointer;
                   margin-bottom:10px;">
                📱 Share App via WhatsApp
            </div>
        </a>
    ''', unsafe_allow_html=True)

    # History Section
    st.markdown("---")
    st.markdown("### 📜 Recent History")
    
    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        for i, item in enumerate(st.session_state.history):
            timestamp = item.get('timestamp', 'No date')
            
            with st.expander(f"📧 Email {i+1} - {timestamp}"):
                st.text_area("", value=item.get('email', ''), height=120, key=f"history_{i}", disabled=True, label_visibility="collapsed")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Use This", key=f"copy_{i}", use_container_width=True):
                        st.session_state.current_email = item.get('email', '')
                        st.success("✅ Loaded!")
                        st.rerun()
                with col2:
                    whatsapp_text = urllib.parse.quote(item.get('email', ''))
                    st.markdown(f'''
                        <a href="https://wa.me/?text={whatsapp_text}" target="_blank" 
                           style="text-decoration:none; display:block;">
                            <div style="background-color:#25D366; color:white; border:none; 
                                   padding:8px; border-radius:5px; text-align:center; 
                                   cursor:pointer; font-size:12px; font-weight:bold;">
                                📤 Share
                            </div>
                        </a>
                    ''', unsafe_allow_html=True)
    else:
        st.info("📭 No history yet. Generate your first email!")

    # Signature
    st.markdown("---")
    st.markdown("### 💚 ProMailer AI")
    st.caption("Built by Bhushan | Powered by AI")

# 4. Custom Styling
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%);
    }
    h1 { 
        color: #1b5e20 !important; 
        text-align: center; 
        font-weight: 700 !important;
        font-size: 2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem !important;
    }
    h3 {
        color: #2e7d32 !important;
        font-weight: 600 !important;
    }
    .stButton>button { 
        background-color: #2e7d32 !important; 
        color: white !important; 
        border-radius: 10px !important; 
        width: 100% !important; 
        height: 3em !important;
        font-weight: bold !important;
        border: none !important;
        font-size: 16px !important;
    }
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 2px solid #66bb6a !important;
        font-size: 16px !important;
    }
    .stRadio > label {
        font-weight: 600 !important;
        color: #2e7d32 !important;
        font-size: 16px !important;
    }
    .stSelectbox > label {
        font-weight: 600 !important;
        color: #2e7d32 !important;
        font-size: 14px !important;
    }
    hr {
        margin: 20px 0 !important;
        border-color: #66bb6a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. Initialize AI Client
try:
    if "GROQ_API_KEY" in st.secrets:
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        ai_provider = "groq"
        
    elif "HUGGINGFACE_API_KEY" in st.secrets:
        import requests
        hf_api_key = st.secrets["HUGGINGFACE_API_KEY"]
        ai_provider = "huggingface"
        
    elif "GEMINI_API_KEY" in st.secrets:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        ai_provider = "gemini"
        
    else:
        st.error("⚠️ Please configure at least one API key in Streamlit Secrets.")
        st.info("Supported APIs: GROQ_API_KEY (recommended), HUGGINGFACE_API_KEY, or GEMINI_API_KEY")
        st.stop()
        
except Exception as e:
    st.error(f"⚠️ API Configuration Error: {str(e)}")
    st.stop()

# 6. Main Application Content
st.markdown('<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />', unsafe_allow_html=True)

# Reduce top padding
st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("✉️ ProMailer AI")
st.markdown("<p style='text-align: center; color: #2e7d32; font-size: 16px; font-weight: 600; margin-top: -10px;'>⌨️ Type OR 🎤 Speak → Professional Emails!</p>", unsafe_allow_html=True)

# Language Selection
st.markdown("### 🌐 Language Settings")
col1, col2 = st.columns(2)

with col1:
    input_lang = st.selectbox(
        "🎤 Input Language:", 
        ["English", "Marathi", "Hindi", "Mix (Marathi+English)"],
        help="Language you'll speak or type in"
    )

with col2:
    target_lang = st.selectbox(
        "📧 Output Language:", 
        ["English", "Marathi"],
        help="Language for the final email"
    )

# Show helpful message
if input_lang == "Marathi" and target_lang == "English":
    st.success("✅ Perfect! Speak in Marathi, get email in English")
elif input_lang == "English" and target_lang == "Marathi":
    st.success("✅ Great! Speak in English, get email in Marathi")
elif input_lang == "English" and target_lang == "English":
    st.success("✅ Awesome! Convert rough English to professional English")
elif input_lang != target_lang:
    st.info(f"💡 Speak in {input_lang}, get email in {target_lang}")

# Quick feature showcase
st.markdown("""
<div style='background: #fff3e0; padding: 12px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ff9800;'>
    <div style='font-weight: bold; color: #e65100; font-size: 14px; margin-bottom: 8px;'>💡 What This App Does:</div>
    <div style='font-size: 13px; color: #333; line-height: 1.8;'>
        ✅ <strong>Type</strong> rough text → Get professional email<br>
        ✅ <strong>Speak</strong> your message → Get professional email<br>
        ✅ <strong>Multi-language</strong> support (English, Marathi, Hindi)<br>
        ✅ <strong>Choose tone & length</strong> for your email
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("---")
st.markdown("### ✍️ Step 1: Choose Your Input Method")

col1, col2 = st.columns(2)

with col1:
    if st.button("⌨️ Type", key="btn_type", use_container_width=True, help="Type your message"):
        st.session_state.input_method = "type"

with col2:
    if st.button("🎤 Speak", key="btn_speak", use_container_width=True, help="Record voice"):
        st.session_state.input_method = "speak"

if 'input_method' not in st.session_state:
    st.session_state.input_method = "type"

method_labels = {"type": "⌨️ Typing", "speak": "🎤 Speaking"}
st.info(f"📍 Current mode: **{method_labels.get(st.session_state.input_method, 'Typing')}**")

st.markdown("<br>", unsafe_allow_html=True)

# Show examples
st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%); 
     padding: 15px; border-radius: 10px; border: 2px solid #2e7d32; margin: 15px 0;'>
    <div style='font-weight: bold; color: #1b5e20; font-size: 18px; margin-bottom: 10px;'>
        💡 Examples - How it works
    </div>
""", unsafe_allow_html=True)

with st.expander("Click to see examples", expanded=False):
    st.markdown("""
    <style>
    .example-box {
        background: #ffffff !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 2px solid #66bb6a !important;
        margin: 10px 0 !important;
    }
    .example-title {
        font-weight: bold !important;
        color: #1b5e20 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    .example-text {
        color: #000000 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if input_lang == "Marathi" and target_lang == "English":
        st.markdown("""
        <div class="example-box">
        <div class="example-title">🎤 Marathi Input Example:</div>
        <div class="example-text">
        "नमस्कार, मला उद्याच्या मीटिंग बद्दल सांगायचे आहे की मी येऊ शकणार नाही. मला काही महत्वाचे काम आहे."
        </div>
        </div>
        
        <div class="example-box">
        <div class="example-title">📧 Professional English Email Output:</div>
        <div class="example-text">
        Subject: Unable to Attend Tomorrow's Meeting<br><br>
        Dear Sir/Madam,<br><br>
        I hope this email finds you well. I am writing to inform you that I will be unable to attend tomorrow's meeting due to some important prior commitments...
        </div>
        </div>
        """, unsafe_allow_html=True)
    elif input_lang == "English" and target_lang == "Marathi":
        st.markdown("""
        <div class="example-box">
        <div class="example-title">🎤 English Input Example:</div>
        <div class="example-text">
        "Hi, I want to tell about tomorrow's meeting that I cannot come. I have some important work."
        </div>
        </div>
        
        <div class="example-box">
        <div class="example-title">📧 Professional Marathi Email Output:</div>
        <div class="example-text">
        विषय: उद्याच्या बैठकीला उपस्थित राहू शकणार नाही<br><br>
        आदरणीय महोदय/महोदया,<br><br>
        मला तुम्हाला कळवायचे आहे की काही महत्त्वाच्या कामामुळे मी उद्याच्या बैठकीला उपस्थित राहू शकणार नाही...
        </div>
        </div>
        """, unsafe_allow_html=True)
    elif input_lang == "English" and target_lang == "English":
        st.markdown("""
        <div class="example-box">
        <div class="example-title">🎤 Rough English Input:</div>
        <div class="example-text">
        "hey boss need leave tomorrow got some family work cant come office"
        </div>
        </div>
        
        <div class="example-box">
        <div class="example-title">📧 Professional English Email Output:</div>
        <div class="example-text">
        Subject: Leave Request for Tomorrow<br><br>
        Dear Sir,<br><br>
        I hope this message finds you well. I am writing to request leave for tomorrow due to an important family commitment. I will be unable to attend the office.<br><br>
        I apologize for any inconvenience this may cause and will ensure all pending work is completed upon my return.<br><br>
        Thank you for your understanding.<br><br>
        Best regards
        </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="example-box">
        <div class="example-title">Example:</div>
        <div class="example-text">
        "Boss, please approve my leave for next week. Family function."
        </div>
        </div>
        
        <div class="example-box">
        <div class="example-title">Professional Email:</div>
        <div class="example-text">
        Subject: Leave Request for Next Week<br><br>
        Dear Sir,<br><br>
        I am writing to request leave for next week due to a family function...
        </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Voice Input
voice_text = ""
has_groq = "GROQ_API_KEY" in st.secrets

if has_groq:
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%); 
         padding: 15px; border-radius: 10px; border-left: 4px solid #2e7d32; margin: 10px 0;'>
        <div style='font-size: 18px; font-weight: bold; color: #1b5e20;'>
            🎤 Option 1: Record Your Voice
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    audio_input = mic_recorder(
        start_prompt="🎤 Click to Start Recording", 
        stop_prompt="🛑 Stop Recording", 
        key='recorder'
    )

    if audio_input:
        with st.spinner("🎧 Transcribing your voice..."):
            try:
                with open("temp.wav", "wb") as f:
                    f.write(audio_input['bytes'])
                
                with open("temp.wav", "rb") as af:
                    transcription = client.audio.transcriptions.create(
                        file=("temp.wav", af.read()), 
                        model="whisper-large-v3"
                    )
                    voice_text = transcription.text
                
                if os.path.exists("temp.wav"):
                    os.remove("temp.wav")
                
                st.success("✅ Voice transcribed successfully!")
                
            except Exception as e:
                st.error(f"❌ Voice error: {str(e)}")
                voice_text = ""
else:
    st.markdown("---")
    st.info("💡 Voice recording: Add GROQ_API_KEY in settings to enable.")

st.markdown("---")
st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%); 
     padding: 15px; border-radius: 10px; border-left: 4px solid #2e7d32; margin: 10px 0;'>
    <div style='font-size: 18px; font-weight: bold; color: #1b5e20;'>
        ⌨️ Option 2: Type Your Message
    </div>
</div>
""", unsafe_allow_html=True)

draft = st.text_area(
    f"📝 Your notes in {input_lang}:", 
    value=voice_text or st.session_state.current_email, 
    height=150,
    placeholder=f"Type or speak your message in {input_lang}...",
    help=f"Enter your draft in {input_lang}, we'll convert it to {target_lang}"
)

# Options
st.markdown("### ⚙️ Step 2: Customize")
col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox(
        "🎭 Tone", 
        ["Formal", "Friendly", "Urgent", "Casual"],
        help="Choose the tone"
    )

with col2:
    length = st.selectbox(
        "📏 Length", 
        ["Concise", "Detailed", "Very Brief"],
        help="Choose the length"
    )

# Generation Logic
st.markdown("---")
if st.button("✨ Generate Professional Email", use_container_width=True):
    if not draft or draft.strip() == "":
        st.warning("⚠️ Please enter some text or record a voice message first!")
    else:
        with st.spinner("🤖 Creating your email..."):
            try:
                prompt = f"""The user has provided notes in {input_lang}. 
Rewrite these notes into a professional email in {target_lang}.

Tone: {tone}
Length: {length}

Requirements:
- Translate accurately if input and output languages differ
- Include a relevant subject line
- Include an appropriate greeting
- Include a professional closing
- Format properly with spacing
- Maintain the original meaning and intent

Notes to rewrite:
{draft}"""

                if ai_provider == "groq":
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    result = response.choices[0].message.content
                    
                elif ai_provider == "huggingface":
                    import requests
                    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
                    headers = {"Authorization": f"Bearer {hf_api_key}"}
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 1024,
                            "temperature": 0.7,
                            "return_full_text": False
                        }
                    }
                    response = requests.post(API_URL, headers=headers, json=payload)
                    if response.status_code == 200:
                        result = response.json()[0]["generated_text"]
                    else:
                        st.error(f"Hugging Face API Error: {response.status_code}")
                        result = f"Subject: Professional Email\n\nDear Recipient,\n\n{draft}\n\nBest regards"
                    
                elif ai_provider == "gemini":
                    import google.generativeai as genai
                    response = model.generate_content(prompt)
                    result = response.text
                    
                else:
                    st.error("❌ No AI provider configured")
                    st.stop()
                
                timestamp = datetime.datetime.now().strftime("%d/%m %H:%M")
                st.session_state.history.insert(0, {
                    'email': result,
                    'timestamp': timestamp
                })
                
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]
                
                st.markdown("### ✅ Your Professional Email")
                st.markdown(f'<div style="background:#fff; padding:20px; border-radius:12px; border:2px solid #66bb6a;"><div style="color:#1b5e20; font-size:15px; line-height:1.6; white-space: pre-wrap;">{result}</div></div>', unsafe_allow_html=True)
                
                st.markdown("### 📋 Copy Email")
                st.code(result, language=None)
                st.info("👆 Tap and hold above text to copy")
                
                st.markdown("### 📤 Share Your Email")
                col1, col2 = st.columns(2)
                
                with col1:
                    whatsapp_text = urllib.parse.quote(result)
                    st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; cursor:pointer; font-weight:bold; font-size:15px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">📱 WhatsApp</div></a>', unsafe_allow_html=True)
                
                with col2:
                    email_subject = urllib.parse.quote("Professional Email")
                    email_body = urllib.parse.quote(result)
                    st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration:none; display:block;"><div style="background:#EA4335; color:white; padding:14px; border-radius:10px; text-align:center; cursor:pointer; font-weight:bold; font-size:15px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">📧 Email</div></a>', unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Please try again or check your API key")

# Footer
st.markdown("---")

ai_names = {
    "groq": "🚀 Groq (LLaMA 3.3)",
    "huggingface": "🤗 Hugging Face (LLaMA 3)",
    "gemini": "✨ Google Gemini"
}
if 'ai_provider' in locals():
    st.markdown(f'<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px; border: 2px solid #66bb6a;"><div style="font-weight: bold; color: #1b5e20; font-size: 14px;">AI Provider: {ai_names.get(ai_provider, ai_provider)}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #666; padding: 20px; font-size: 14px;'>ProMailer AI - Built with 💚 by Bhushan</div>", unsafe_allow_html=True)
