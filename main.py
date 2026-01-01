import streamlit as st
import os
import urllib.parse
import datetime
from streamlit_mic_recorder import mic_recorder
import PIL.Image

# 1. Page Configuration
st.set_page_config(
    page_title="ProMailer AI", 
    page_icon="✉️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Initialize Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_email' not in st.session_state:
    st.session_state.current_email = ""
if 'emails_generated' not in st.session_state:
    st.session_state.emails_generated = 0
if 'session_start_time' not in st.session_state:
    st.session_state.session_start_time = datetime.datetime.now()

# 3. Sidebar Implementation
with st.sidebar:
    st.markdown("# 📖 App Menu")
    st.markdown("**✍️ Type | 🎤 Speak | 📸 Photo**")
    st.caption("⌨️ Type rough notes → Professional email")
    st.caption("🎤 Speak casually → Professional email")
    st.caption("📸 Photo of notes → Professional email")
    st.caption("🌍 Works in English, Marathi, Hindi")

    # Share App Link Button
    st.markdown("---")
    st.markdown("### 📲 Share this App")
    app_link = "https://promailer-ai.streamlit.app/"  # Update with your actual URL
    share_msg = urllib.parse.quote(
        f"Hey! Check out ProMailer AI - It converts rough notes into professional emails. Type or speak in any language: {app_link}"
    )
    
    # WhatsApp Share Button
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
        # Add clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        for i, item in enumerate(st.session_state.history):
            timestamp = item.get('timestamp', 'No date')
            preview = item.get('email', '')[:40] + "..." if len(item.get('email', '')) > 40 else item.get('email', '')
            
            with st.expander(f"📧 Email {i+1} - {timestamp}"):
                st.text_area("Email Content", value=item.get('email', ''), height=120, key=f"history_{i}", disabled=True, label_visibility="collapsed")
                
                # Individual email actions
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

    # Signature and Stats
    st.markdown("---")
    st.markdown("### 💚 ProMailer AI")
    st.caption("Built by Bhushan | Powered by Gemini AI")
    
    # Session Stats
    st.markdown("---")
    st.markdown("### 📊 Your Session Stats")
    
    # Calculate session duration
    session_duration = datetime.datetime.now() - st.session_state.session_start_time
    duration_mins = int(session_duration.total_seconds() / 60)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📧 Emails Generated", st.session_state.emails_generated)
    with col2:
        st.metric("⏱️ Session Time", f"{duration_mins} min")
    
    # History count
    st.metric("📜 History Count", len(st.session_state.history))

# 4. Custom Styling (Mobile Optimized)
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
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #66bb6a;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .result-text {
        color: #1b5e20;
        font-size: 15px;
        line-height: 1.6;
        white-space: pre-wrap;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    hr {
        margin: 20px 0 !important;
        border-color: #66bb6a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 5. Initialize AI Client
try:
    # Try to get Groq API key (import only when needed)
    if "GROQ_API_KEY" in st.secrets:
        from groq import Groq
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
        ai_provider = "groq"
    # Try Gemini if Groq not available
    elif "GEMINI_API_KEY" in st.secrets:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
        ai_provider = "gemini"
    else:
        st.error("⚠️ Please configure GROQ_API_KEY or GEMINI_API_KEY in Streamlit Secrets.")
        st.info("Get free Groq API key: https://console.groq.com/keys")
        st.stop()
except Exception as e:
    st.error(f"⚠️ API Configuration Error: {str(e)}")
    st.stop()

# 6. Main Application Content
st.title("✉️ ProMailer AI")
st.markdown("<p style='text-align: center; color: #2e7d32; font-size: 16px; font-weight: 600;'>⌨️ Type | 🎤 Speak | 📸 Photo → Professional Emails!</p>", unsafe_allow_html=True)

# Language Selection
st.markdown("### 🌐 Language Settings")
col1, col2 = st.columns(2)

with col1:
    input_lang = st.selectbox(
        "🎤 Input Language:", 
        ["English", "Marathi", "Hindi", "Mix (Marathi+English)"],  # English first now
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
        ✅ <strong>Photo</strong> of notes/whiteboard → Get professional email<br>
        ✅ <strong>Multi-language</strong> support (English, Marathi, Hindi)
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section
st.markdown("---")
st.markdown("### ✍️ Step 1: Choose Your Input Method")

# Input method selector buttons (interactive)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⌨️ Type", key="btn_type", use_container_width=True, help="Type your message"):
        st.session_state.input_method = "type"

with col2:
    if st.button("🎤 Speak", key="btn_speak", use_container_width=True, help="Record voice"):
        st.session_state.input_method = "speak"
        
with col3:
    if st.button("📸 Photo", key="btn_photo", use_container_width=True, help="Upload image"):
        st.session_state.input_method = "photo"

# Initialize input method if not set
if 'input_method' not in st.session_state:
    st.session_state.input_method = "type"

# Show current selection
method_labels = {"type": "⌨️ Typing", "speak": "🎤 Speaking", "photo": "📸 Photo Upload"}
st.info(f"📍 Current mode: **{method_labels.get(st.session_state.input_method, 'Typing')}**")

st.markdown("<br>", unsafe_allow_html=True)

# Show examples based on language selection
with st.expander("💡 See Examples - How it works"):
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

# Voice Input
voice_text = ""
photo_text = ""

# Check if we have Groq for voice
has_groq = "GROQ_API_KEY" in st.secrets

if has_groq:
    st.markdown("---")
    st.markdown("#### 🎤 Option 1: Record Your Voice")
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

# Photo/Image Input
st.markdown("---")
st.markdown("#### 📸 Option 2: Upload or Capture Photo")
st.markdown("""
<div style='background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%); 
     padding: 20px; border-radius: 12px; border: 2px solid #2196F3; 
     text-align: center; margin: 15px 0;'>
    <div style='font-size: 48px; margin-bottom: 10px;'>📸</div>
    <div style='font-weight: bold; color: #1565c0; font-size: 16px; margin-bottom: 8px;'>
        Upload Photo of Your Notes
    </div>
    <div style='color: #333; font-size: 13px; margin-bottom: 15px;'>
        Handwritten notes, whiteboard, documents - we'll extract the text!
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Choose an image file", 
    type=['png', 'jpg', 'jpeg'],
    help="Upload a clear photo of your notes for best results"
)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Your uploaded image", use_container_width=True)
    st.warning("⚠️ Photo text extraction requires GEMINI_API_KEY.")
    st.info("💡 For now, please type the text from the photo manually in the box below.")
    st.info("To enable photo upload: Add GEMINI_API_KEY in Streamlit Secrets")

st.markdown("#### ⌨️ Option 3: Type Your Message")

# Text Input
draft = st.text_area(
    f"📝 Your notes in {input_lang}:", 
    value=photo_text or voice_text or st.session_state.current_email, 
    height=150,
    placeholder=f"Type, speak, or upload a photo of your message in {input_lang}...",
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

# 7. Generation Logic
st.markdown("---")
if st.button("✨ Generate Professional Email", use_container_width=True):
    if not draft or draft.strip() == "":
        st.warning("⚠️ Please enter some text or record a voice message first!")
    else:
        with st.spinner("🤖 Creating your email..."):
            try:
                # Build prompt with language specification
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

                # Call API based on provider
                if ai_provider == "groq":
                    # Use Groq
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    result = response.choices[0].message.content
                    
                elif ai_provider == "gemini":
                    # Use Gemini
                    response = model.generate_content(prompt)
                    result = response.text
                else:
                    st.error("No AI provider configured")
                    return
                
                # Save to history
                timestamp = datetime.datetime.now().strftime("%d/%m %H:%M")
                st.session_state.history.insert(0, {
                    'email': result,
                    'timestamp': timestamp
                })
                
                # Increment email counter
                st.session_state.emails_generated += 1
                
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]
                
                # Display result
                st.markdown("### ✅ Your Professional Email")
                st.markdown(f'<div class="result-box"><div class="result-text">{result}</div></div>', unsafe_allow_html=True)
                
                # Copy to Clipboard
                st.markdown("### 📋 Copy Email")
                st.code(result, language=None)
                st.info("👆 Tap and hold above text to copy")
                
                # Share buttons
                st.markdown("### 📤 Share Your Email")
                col1, col2 = st.columns(2)
                
                with col1:
                    whatsapp_text = urllib.parse.quote(result)
                    st.markdown(f'''
                        <a href="https://wa.me/?text={whatsapp_text}" target="_blank" 
                           style="text-decoration:none; display:block;">
                            <div style="background-color:#25D366; color:white; border:none; 
                                   padding:14px; border-radius:10px; text-align:center; 
                                   cursor:pointer; font-weight:bold; font-size:15px;
                                   box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                📱 WhatsApp
                            </div>
                        </a>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    email_subject = urllib.parse.quote("Professional Email")
                    email_body = urllib.parse.quote(result)
                    st.markdown(f'''
                        <a href="mailto:?subject={email_subject}&body={email_body}" 
                           style="text-decoration:none; display:block;">
                            <div style="background-color:#EA4335; color:white; border:none; 
                                   padding:14px; border-radius:10px; text-align:center; 
                                   cursor:pointer; font-weight:bold; font-size:15px;
                                   box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                📧 Email
                            </div>
                        </a>
                    ''', unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Please try again or check your API key")

# Footer
st.markdown("---")

# Stats Section in Footer
st.markdown("### 📊 Session Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;">
            <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">{st.session_state.emails_generated}</div>
            <div style="font-size: 12px; color: #666;">Emails Generated</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    session_duration = datetime.datetime.now() - st.session_state.session_start_time
    duration_mins = int(session_duration.total_seconds() / 60)
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;">
            <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">{duration_mins}</div>
            <div style="font-size: 12px; color: #666;">Minutes Active</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div style="background: white; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;">
            <div style="font-size: 24px; font-weight: bold; color: #2e7d32;">{len(st.session_state.history)}</div>
            <div style="font-size: 12px; color: #666;">In History</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(
    f"<div style='text-align: center; color: #666; padding: 20px; font-size: 14px;'>"
    f"ProMailer AI - Built with 💚 by Bhushan | Powered by {ai_provider.upper()} AI"
    "</div>", 
    unsafe_allow_html=True
)