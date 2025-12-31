import streamlit as st
import os
import urllib.parse
import datetime
import google.generativeai as genai
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

# 5. Initialize Gemini AI
try:
    # Try Gemini first (recommended)
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        ai_provider = "gemini"
    # Fallback to Groq if Gemini not available
    elif "GROQ_API_KEY" in st.secrets:
        from groq import Groq
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        ai_provider = "groq"
    else:
        st.error("⚠️ Please configure GEMINI_API_KEY or GROQ_API_KEY in Streamlit Secrets.")
        st.info("Get free Gemini API key: https://aistudio.google.com/app/apikey")
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

# Prominent input method selector - Now with 3 options
input_method_col1, input_method_col2, input_method_col3 = st.columns(3)
with input_method_col1:
    st.markdown("""
    <div style='background: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;'>
        <div style='font-size: 28px; margin-bottom: 5px;'>⌨️</div>
        <div style='font-weight: bold; color: #1b5e20; font-size: 13px;'>Type It</div>
        <div style='font-size: 11px; color: #666;'>Write below</div>
    </div>
    """, unsafe_allow_html=True)

with input_method_col2:
    st.markdown("""
    <div style='background: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;'>
        <div style='font-size: 28px; margin-bottom: 5px;'>🎤</div>
        <div style='font-weight: bold; color: #1b5e20; font-size: 13px;'>Speak It</div>
        <div style='font-size: 11px; color: #666;'>Use mic</div>
    </div>
    """, unsafe_allow_html=True)

with input_method_col3:
    st.markdown("""
    <div style='background: #e8f5e9; padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #66bb6a;'>
        <div style='font-size: 28px; margin-bottom: 5px;'>📸</div>
        <div style='font-weight: bold; color: #1b5e20; font-size: 13px;'>Photo It</div>
        <div style='font-size: 11px; color: #666;'>Capture notes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Show examples based on language selection
with st.expander("💡 See Examples - How it works"):
    if input_lang == "Marathi" and target_lang == "English":
        st.markdown("""
        **🎤 Marathi Input Example:**
        > "नमस्कार, मला उद्याच्या मीटिंग बद्दल सांगायचे आहे की मी येऊ शकणार नाही. मला काही महत्वाचे काम आहे."
        
        **📧 Professional English Email Output:**
        > Subject: Unable to Attend Tomorrow's Meeting
        > 
        > Dear Sir/Madam,
        > 
        > I hope this email finds you well. I am writing to inform you that I will be unable to attend tomorrow's meeting due to some important prior commitments...
        """)
    elif input_lang == "English" and target_lang == "Marathi":
        st.markdown("""
        **🎤 English Input Example:**
        > "Hi, I want to tell about tomorrow's meeting that I cannot come. I have some important work."
        
        **📧 Professional Marathi Email Output:**
        > विषय: उद्याच्या बैठकीला उपस्थित राहू शकणार नाही
        > 
        > आदरणीय महोदय/महोदया,
        > 
        > मला तुम्हाला कळवायचे आहे की काही महत्त्वाच्या कामामुळे मी उद्याच्या बैठकीला उपस्थित राहू शकणार नाही...
        """)
    elif input_lang == "English" and target_lang == "English":
        st.markdown("""
        **🎤 Rough English Input:**
        > "hey boss need leave tomorrow got some family work cant come office"
        
        **📧 Professional English Email Output:**
        > Subject: Leave Request for Tomorrow
        > 
        > Dear Sir,
        > 
        > I hope this message finds you well. I am writing to request leave for tomorrow due to an important family commitment. I will be unable to attend the office.
        > 
        > I apologize for any inconvenience this may cause and will ensure all pending work is completed upon my return.
        > 
        > Thank you for your understanding.
        > 
        > Best regards
        """)
    else:
        st.markdown("""
        **Example:**
        > "Boss, please approve my leave for next week. Family function."
        
        **Professional Email:**
        > Subject: Leave Request for Next Week
        > 
        > Dear Sir,
        > 
        > I am writing to request leave for next week due to a family function...
        """)

# Voice Input (only works with Groq for transcription)
voice_text = ""
photo_text = ""

if ai_provider == "groq":
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
    st.info("💡 Voice input requires GROQ_API_KEY. Add it in secrets to enable voice recording.")

# Photo/Image Input
st.markdown("#### 📸 Option 2: Upload or Capture Photo")
st.caption("Upload a photo of handwritten notes, whiteboard, or any document")

uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=['png', 'jpg', 'jpeg'],
    help="Take a photo of your notes or upload an existing image"
)

if uploaded_file is not None:
    # Display the image
    st.image(uploaded_file, caption="Your uploaded image", use_container_width=True)
    
    with st.spinner("🔍 Extracting text from image..."):
        try:
            # Use Gemini Vision API if available, otherwise use Groq
            if ai_provider == "gemini":
                # Prepare image for Gemini
                import PIL.Image
                img = PIL.Image.open(uploaded_file)
                
                # Use Gemini's vision capability
                vision_model = genai.GenerativeModel('gemini-1.5-flash')
                response = vision_model.generate_content([
                    "Extract all text from this image. If it's handwritten notes or rough text, transcribe it exactly as written. Include all text you can see:",
                    img
                ])
                photo_text = response.text
                st.success("✅ Text extracted from image!")
                
            else:
                st.warning("⚠️ Image text extraction requires GEMINI_API_KEY. Please add it to secrets.")
                st.info("💡 For now, you can type the text manually in the box below.")
                
        except Exception as e:
            st.error(f"❌ Image processing error: {str(e)}")
            st.info("💡 Try typing the text manually in the box below.")

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
                if ai_provider == "gemini":
                    response = model.generate_content(prompt)
                    result = response.text
                else:  # groq
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=1024
                    )
                    result = response.choices[0].message.content
                
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
