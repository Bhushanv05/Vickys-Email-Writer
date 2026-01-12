import streamlit as st
import os
import urllib.parse
import datetime
from streamlit_mic_recorder import mic_recorder

# Page config
st.set_page_config(
    page_title="ProMailer AI - Enhanced", 
    page_icon="✉️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Clear caches
st.cache_data.clear()
st.cache_resource.clear()

# Initialize session state
if 'current_email' not in st.session_state:
    st.session_state.current_email = ""
if 'last_generated' not in st.session_state:
    st.session_state.last_generated = ""
if 'user_signature' not in st.session_state:
    st.session_state.user_signature = ""
if 'voice_new_email_text' not in st.session_state:
    st.session_state.voice_new_email_text = ""
if 'voice_received_email_text' not in st.session_state:
    st.session_state.voice_received_email_text = ""

# Sidebar
with st.sidebar:
    st.markdown("# 📖 ProMailer AI")
    st.caption("v2.4.0 - Simplified Edition 🚀")

    # Signature Manager
    st.markdown("---")
    st.markdown("### ✍️ Your Signature")
    user_sig = st.text_area(
        "Save your signature (optional):",
        value=st.session_state.user_signature,
        height=100,
        placeholder="Best regards,\nYour Name\nYour Title\nyour@email.com",
        help="This will be added to all emails automatically"
    )
    if user_sig != st.session_state.user_signature:
        st.session_state.user_signature = user_sig
        st.success("✅ Signature saved!")

    st.markdown("---")
    st.markdown("**✍️ Type OR 🎤 Speak**")
    st.caption("⌨️ Type rough notes → Professional email")
    st.caption("🎤 Speak in any language → Professional email")
    st.caption("🌍 Works in English, Marathi, Hindi")

    # Share button
    st.markdown("---")
    st.markdown("### 📲 Share this App")
    app_link = "https://promailer-ai-test.streamlit.app/"
    share_msg = urllib.parse.quote(f"Check out ProMailer AI Enhanced: {app_link}")
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; font-size:14px;">📱 Share via WhatsApp</div></a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💚 ProMailer AI")
    st.caption("Built by Bhushan | Powered by AI")
    
    # Instructions
    st.markdown("---")
    with st.expander("📱 App Tips & Instructions"):
        st.markdown("""
        **🏠 Add to Home Screen (Install as App):**
        
        **📱 On Android (Chrome):**
        1. Tap the **⋮** (three dots) menu
        2. Select **"Add to Home screen"**
        3. Tap **"Add"** or **"Install"**
        4. App icon will appear on your home screen!
        
        **📱 On iPhone (Safari):**
        1. Tap the **Share** button (box with arrow)
        2. Scroll and tap **"Add to Home Screen"**
        3. Tap **"Add"**
        4. Launch from home screen like any app!
        
        ---
        
        **🚀 How to Use:**
        
        **Write New Email:**
        - Type or speak what you want to say
        - AI makes it professional
        
        **Reply to Email:**
        - Type or speak the email you received
        - AI generates perfect reply
        - You just choose tone & type!
        """)


# Styling
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f1f8e9 0%, #e8f5e9 100%); }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; }
h1 { color: #1b5e20 !important; text-align: center; font-weight: 700 !important; font-size: 2rem !important; margin-bottom: 0.3rem !important; }
h3 { color: #2e7d32 !important; font-weight: 600 !important; }
.stButton>button { background-color: #2e7d32 !important; color: white !important; border-radius: 10px !important; width: 100% !important; font-weight: bold !important; border: none !important; font-size: 15px !important; padding: 0.5rem !important; }
.stButton>button:hover { background-color: #1b5e20 !important; box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important; }
.stTextArea textarea { border-radius: 10px !important; border: 2px solid #66bb6a !important; font-size: 15px !important; }
.stTextArea > label { font-weight: 700 !important; color: #1b5e20 !important; font-size: 16px !important; }
.stSelectbox > label { font-weight: 600 !important; color: #2e7d32 !important; font-size: 14px !important; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { 
    height: 50px;
    background-color: #c8e6c9 !important;
    border-radius: 10px 10px 0 0;
    color: #1b5e20 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 12px 20px !important;
    border: 2px solid #66bb6a !important;
}
.stTabs [aria-selected="true"] {
    background-color: #2e7d32 !important;
    color: white !important;
    border-bottom: 2px solid #2e7d32 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 20px;
}
</style>

<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CWEBJ8Q2BK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-CWEBJ8Q2BK');
</script>
""", unsafe_allow_html=True)

# Initialize AI
ai_provider = None
text_model = None
client = None

try:
    # Try Groq FIRST
    if "GROQ_API_KEY" in st.secrets:
        try:
            from groq import Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            ai_provider = "groq"
            st.sidebar.success("✅ Using Groq AI (Fast & Reliable)")
        except Exception as e:
            st.sidebar.warning(f"⚠️ Groq unavailable: {str(e)}")
    
    # Try Gemini as fallback
    if not ai_provider and "GEMINI_API_KEY" in st.secrets:
        try:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            
            model_names = ['gemini-1.5-flash', 'gemini-1.5-pro']
            
            for model_name in model_names:
                try:
                    text_model = genai.GenerativeModel(model_name)
                    ai_provider = "gemini"
                    st.sidebar.success(f"✅ Using {model_name}")
                    break
                except:
                    continue
        except Exception as e:
            st.sidebar.warning(f"⚠️ Gemini unavailable: {str(e)}")
    
    if not ai_provider:
        st.error("⚠️ No AI provider available. Please add GROQ_API_KEY or GEMINI_API_KEY in Streamlit Secrets")
        st.info("💡 **Get Free API Keys:**\n- Groq: https://console.groq.com (Recommended)\n- Gemini: https://makersuite.google.com/app/apikey")
        st.stop()

except Exception as e:
    st.error(f"⚠️ API Setup Error: {str(e)}")
    st.stop()

# Main content
st.title("✉️ ProMailer AI")
st.markdown("<p style='text-align: center; color: #2e7d32; font-size: 15px; font-weight: 600; margin-top: -8px;'>⌨️ Type OR 🎤 Speak → Professional Emails!</p>", unsafe_allow_html=True)

# Two tabs
tab1, tab2 = st.tabs(["📝 Write New Email", "📧 Reply to Email"])

# TAB 1: WRITE NEW EMAIL
with tab1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
         padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; margin: 10px 0;'>
        <div style='font-size: 16px; font-weight: bold; color: #1b5e20; margin-bottom: 8px;'>
            📝 Create Professional Email
        </div>
        <div style='font-size: 13px; color: #2e7d32;'>
            Speak or type what YOU want to say - AI makes it professional!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Language Settings
    st.markdown("### 🌍 Language Settings")
    col1, col2 = st.columns(2)

    with col1:
        input_lang = st.selectbox("🎤 Input:", ["English", "Marathi", "Hindi", "Mix"], help="Your input language", key="new_input_lang")

    with col2:
        target_lang = st.selectbox("📧 Output:", ["English", "Marathi"], help="Email language", key="new_target_lang")

    if input_lang == "English" and target_lang == "English":
        st.success("✅ Convert rough English to professional English")

    # Input Section
    st.markdown("---")
    st.markdown("### ✍️ Your Message")

    # Voice Option Card
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFF3CD 0%, #FFE69C 100%); 
         padding: 20px; border-radius: 12px; border: 3px solid #FFC107; margin: 15px 0;'>
        <div style='font-size: 18px; font-weight: bold; color: #856404; margin-bottom: 8px;'>
            🎤 VOICE OPTION - Record Your Message
        </div>
        <div style='font-size: 14px; color: #856404; margin-bottom: 10px;'>
            Speak your rough notes - AI will create a professional email!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    voice_text_new = ""
    if "GROQ_API_KEY" in st.secrets:
        audio_input = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="🛑 Stop Recording", key='recorder_new_email')
        if audio_input:
            with st.spinner("🎧 Transcribing..."):
                try:
                    from groq import Groq
                    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    with open("temp_new.wav", "wb") as f:
                        f.write(audio_input['bytes'])
                    with open("temp_new.wav", "rb") as af:
                        transcription = groq_client.audio.transcriptions.create(
                            file=("temp_new.wav", af.read()), 
                            model="whisper-large-v3"
                        )
                        voice_text_new = transcription.text
                    if os.path.exists("temp_new.wav"):
                        os.remove("temp_new.wav")
                    
                    st.session_state.voice_new_email_text = voice_text_new
                    
                    st.success("✅ Voice transcribed!")
                    st.markdown("**📝 What you said:**")
                    st.text_area(
                        "Your transcribed voice:",
                        value=voice_text_new,
                        height=100,
                        key="show_new_voice_transcript",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    st.info("👇 **Your voice text appears below.** Scroll down and click 'Generate Professional Email'.")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("🎤 Voice requires GROQ_API_KEY in secrets")

    st.markdown("<p style='text-align: center; font-size: 16px; font-weight: bold; color: #666; margin: 15px 0;'>OR</p>", unsafe_allow_html=True)

    # Type Option Card
    st.markdown("""
    <div style='background: linear-gradient(135deg, #D1ECF1 0%, #B6D4FE 100%); 
         padding: 20px; border-radius: 12px; border: 3px solid #17A2B8; margin: 15px 0;'>
        <div style='font-size: 18px; font-weight: bold; color: #0C5460; margin-bottom: 8px;'>
            ✍️ TYPE OPTION - Write Your Message
        </div>
        <div style='font-size: 14px; color: #0C5460; margin-bottom: 10px;'>
            Type your rough notes or paste content here
        </div>
    </div>
    """, unsafe_allow_html=True)

    if voice_text_new:
        display_text = voice_text_new
    elif st.session_state.voice_new_email_text:
        display_text = st.session_state.voice_new_email_text
    else:
        display_text = st.session_state.current_email
    
    draft = st.text_area(
        f"📝 Your message (voice or typed):",
        value=display_text,
        height=150,
        placeholder=f"Type your rough notes in {input_lang}... or use voice recording above",
        key="new_draft"
    )

    if draft:
        word_count = len(draft.split())
        char_count = len(draft)
        st.caption(f"📊 {word_count} words | {char_count} characters")

    # Options
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("🎭 Tone", ["Formal", "Friendly", "Urgent", "Casual"], key="new_tone")
    with col2:
        length = st.selectbox("📏 Length", ["Concise", "Detailed", "Very Brief"], key="new_length")

    # Generate button
    st.markdown("---")
    if st.button("✨ Generate Professional Email", use_container_width=True, key="gen_new"):
        actual_draft = draft or st.session_state.voice_new_email_text
        
        if not actual_draft or actual_draft.strip() == "":
            st.warning("⚠️ Please enter text or record voice first!")
        else:
            with st.spinner("🤖 Creating your email..."):
                try:
                    signature_text = f"\n\n{st.session_state.user_signature}" if st.session_state.user_signature else ""

                    prompt = f"""Convert these rough notes into a professional email in {target_lang}.

Tone: {tone}
Length: {length}

Requirements:
- Include subject line
- Professional greeting
- Well-formatted body
- Professional closing
{f"- Add this signature at end: {signature_text}" if signature_text else ""}

Notes: {actual_draft}"""

                    if ai_provider == "gemini":
                        response = text_model.generate_content(prompt)
                        result = response.text
                    elif ai_provider == "groq":
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7,
                            max_tokens=1024
                        )
                        result = response.choices[0].message.content

                    st.session_state.last_generated = result

                    # Track email generation
                    st.markdown("""<script>
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'email_generated', {
                            'event_category': 'engagement',
                            'event_label': 'write_new_email',
                            'value': 1
                        });
                    }
                    </script>""", unsafe_allow_html=True)

                    st.markdown("### ✅ Your Professional Email")
                    st.markdown(f'<div style="background:#fff; padding:20px; border-radius:12px; border:2px solid #66bb6a;"><div style="color:#1b5e20; font-size:15px; line-height:1.6; white-space: pre-wrap;">{result}</div></div>', unsafe_allow_html=True)

                    # Quick actions
                    st.markdown("### 📄 Quick Actions")
                    st.caption("Click to modify the email above")
                    action_col1, action_col2, action_col3 = st.columns(3)

                    with action_col1:
                        if st.button("✂️ Make Shorter", use_container_width=True, key="action_shorter"):
                            shorter_prompt = f"Make this email shorter and more concise while keeping the main message:\n\n{result}"
                            with st.spinner("✂️ Making it shorter..."):
                                try:
                                    if ai_provider == "gemini":
                                        response = text_model.generate_content(shorter_prompt)
                                        shorter_result = response.text
                                    elif ai_provider == "groq":
                                        response = client.chat.completions.create(
                                            model="llama-3.3-70b-versatile",
                                            messages=[{"role": "user", "content": shorter_prompt}],
                                            temperature=0.7,
                                            max_tokens=1024
                                        )
                                        shorter_result = response.choices[0].message.content
                                    
                                    if 'shorter_result' in locals():
                                        st.markdown("#### ✂️ Shorter Version:")
                                        st.markdown(f'<div style="background:#fff3cd; padding:15px; border-radius:10px; border:2px solid #ffc107;"><div style="color:#333; font-size:15px; line-height:1.6; white-space: pre-wrap;">{shorter_result}</div></div>', unsafe_allow_html=True)
                                        st.code(shorter_result, language=None)
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")

                    with action_col2:
                        if st.button("📝 Make Longer", use_container_width=True, key="action_longer"):
                            longer_prompt = f"Make this email more detailed and elaborate while maintaining professionalism:\n\n{result}"
                            with st.spinner("📝 Making it longer..."):
                                try:
                                    if ai_provider == "gemini":
                                        response = text_model.generate_content(longer_prompt)
                                        longer_result = response.text
                                    elif ai_provider == "groq":
                                        response = client.chat.completions.create(
                                            model="llama-3.3-70b-versatile",
                                            messages=[{"role": "user", "content": longer_prompt}],
                                            temperature=0.7,
                                            max_tokens=1024
                                        )
                                        longer_result = response.choices[0].message.content
                                    
                                    if 'longer_result' in locals():
                                        st.markdown("#### 📝 Longer Version:")
                                        st.markdown(f'<div style="background:#d1ecf1; padding:15px; border-radius:10px; border:2px solid #17a2b8;"><div style="color:#333; font-size:15px; line-height:1.6; white-space: pre-wrap;">{longer_result}</div></div>', unsafe_allow_html=True)
                                        st.code(longer_result, language=None)
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")

                    with action_col3:
                        if st.button("😊 Friendlier", use_container_width=True, key="action_friendly"):
                            friendly_prompt = f"Rewrite this email in a more friendly and warm tone while staying professional:\n\n{result}"
                            with st.spinner("😊 Making it friendlier..."):
                                try:
                                    if ai_provider == "gemini":
                                        response = text_model.generate_content(friendly_prompt)
                                        friendly_result = response.text
                                    elif ai_provider == "groq":
                                        response = client.chat.completions.create(
                                            model="llama-3.3-70b-versatile",
                                            messages=[{"role": "user", "content": friendly_prompt}],
                                            temperature=0.7,
                                            max_tokens=1024
                                        )
                                        friendly_result = response.choices[0].message.content
                                    
                                    if 'friendly_result' in locals():
                                        st.markdown("#### 😊 Friendlier Version:")
                                        st.markdown(f'<div style="background:#d4edda; padding:15px; border-radius:10px; border:2px solid #28a745;"><div style="color:#333; font-size:15px; line-height:1.6; white-space: pre-wrap;">{friendly_result}</div></div>', unsafe_allow_html=True)
                                        st.code(friendly_result, language=None)
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")

                    st.markdown("### 📋 Copy Email")
                    st.code(result, language=None)
                    st.info("👆 Tap and hold to copy")

                    st.markdown("### 📤 Share")
                    share_col1, share_col2 = st.columns(2)

                    with share_col1:
                        whatsapp_text = urllib.parse.quote(result)
                        st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📱 WhatsApp</div></a>', unsafe_allow_html=True)

                    with share_col2:
                        email_subject = urllib.parse.quote("Email from ProMailer AI")
                        email_body = urllib.parse.quote(result)
                        st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration:none; display:block;"><div style="background:#EA4335; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📧 Email</div></a>', unsafe_allow_html=True)
                    
                    st.info("💡 **Tip:** Email button works best on mobile. On desktop, use the copy section above.")

                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# TAB 2: REPLY TO EMAIL (SIMPLIFIED - NO STEP 2!)
with tab2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
         padding: 15px; border-radius: 10px; border: 2px solid #2196F3; margin: 10px 0;'>
        <div style='font-size: 16px; font-weight: bold; color: #1565c0; margin-bottom: 8px;'>
            📧 Smart Reply Generator
        </div>
        <div style='font-size: 13px; color: #333;'>
            Tell us what email you received - AI generates the perfect reply!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Language Settings
    st.markdown("### 🌍 Language Settings")
    col1, col2 = st.columns(2)

    with col1:
        reply_input_lang = st.selectbox("🎤 Input:", ["English", "Marathi", "Hindi", "Mix"], help="Language of received email", key="reply_input_lang")

    with col2:
        reply_target_lang = st.selectbox("📧 Output:", ["English", "Marathi"], help="Reply language", key="reply_target_lang")

    # Email You Received
    st.markdown("---")
    st.markdown("### 📥 What Email Did You Receive?")

    # Voice Option
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFF3CD 0%, #FFE69C 100%); 
         padding: 20px; border-radius: 12px; border: 3px solid #FFC107; margin: 15px 0;'>
        <div style='font-size: 18px; font-weight: bold; color: #856404; margin-bottom: 8px;'>
            🎤 VOICE OPTION - Read Email Aloud
        </div>
        <div style='font-size: 14px; color: #856404; margin-bottom: 10px;'>
            Speak or read the email you received - AI will generate reply!
        </div>
    </div>
    """, unsafe_allow_html=True)

    voice_received = ""
    if "GROQ_API_KEY" in st.secrets:
        audio_received = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="🛑 Stop", key='recorder_received_email')
        if audio_received:
            with st.spinner("🎧 Transcribing received email..."):
                try:
                    from groq import Groq
                    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                    
                    with open("temp_received.wav", "wb") as f:
                        f.write(audio_received['bytes'])
                    with open("temp_received.wav", "rb") as af:
                        transcription = groq_client.audio.transcriptions.create(
                            file=("temp_received.wav", af.read()), 
                            model="whisper-large-v3"
                        )
                        voice_received = transcription.text
                    if os.path.exists("temp_received.wav"):
                        os.remove("temp_received.wav")
                    
                    st.session_state.voice_received_email_text = voice_received
                    
                    st.success("✅ Email transcribed!")
                    st.markdown("**📝 What you said:**")
                    st.text_area(
                        "Received email:",
                        value=voice_received,
                        height=100,
                        key="show_received_voice",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    st.info("👇 Your voice appears in the text box below.")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    else:
        st.info("🎤 Voice requires GROQ_API_KEY in secrets")

    st.markdown("<p style='text-align: center; font-size: 16px; font-weight: bold; color: #666; margin: 15px 0;'>OR</p>", unsafe_allow_html=True)

    # Type Option
    st.markdown("""
    <div style='background: linear-gradient(135deg, #D1ECF1 0%, #B6D4FE 100%); 
         padding: 20px; border-radius: 12px; border: 3px solid #17A2B8; margin: 15px 0;'>
        <div style='font-size: 18px; font-weight: bold; color: #0C5460; margin-bottom: 8px;'>
            ✍️ TYPE OPTION - Paste Email Content
        </div>
        <div style='font-size: 14px; color: #0C5460; margin-bottom: 10px;'>
            Type or paste the email you received - AI will generate reply!
        </div>
    </div>
    """, unsafe_allow_html=True)

    if voice_received:
        display_received = voice_received
    elif st.session_state.voice_received_email_text:
        display_received = st.session_state.voice_received_email_text
    else:
        display_received = ""

    email_to_reply = st.text_area(
        "📧 Email content:",
        value=display_received,
        height=150,
        placeholder="Type or paste the email you received...",
        key="email_content_reply"
    )

    # Reply Settings
    st.markdown("---")
    st.markdown("### ⚙️ How Should We Reply?")
    
    reply_col1, reply_col2 = st.columns(2)
    with reply_col1:
        reply_tone = st.selectbox(
            "🎭 Reply Tone:",
            ["Professional", "Respectful", "Friendly", "Formal"],
            key="reply_tone_select",
            help="How formal should the reply be?"
        )
    with reply_col2:
        reply_type = st.selectbox(
            "📋 Reply Type:",
            ["Acknowledge", "Provide Info", "Request Clarification", "Agree/Confirm"],
            key="reply_type_select",
            help="What type of response?"
        )

    # Generate Reply Button
    st.markdown("---")
    if st.button("✨ Generate Professional Reply", use_container_width=True, key="generate_reply_btn"):
        # Check both text area AND session state for voice
        actual_email = email_to_reply or st.session_state.voice_received_email_text
        
        if not actual_email or not actual_email.strip():
            st.warning("⚠️ Please provide the email you received (type or record voice)!")
        else:
            with st.spinner("🤖 Generating your professional reply..."):
                try:
                    reply_prompt = f"""You received this email in {reply_input_lang}:

{actual_email}

Generate a {reply_tone.lower()} reply in {reply_target_lang} that will {reply_type.lower()}. 

Requirements:
- Match the sender's formality level
- Be concise but complete
- Include proper greeting and closing
- Professional tone
- Address all points raised
- Generate appropriate content based on the email context"""

                    # Generate reply using AI
                    if ai_provider == "gemini":
                        response = text_model.generate_content(reply_prompt)
                        reply_result = response.text
                    elif ai_provider == "groq":
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": reply_prompt}],
                            temperature=0.7,
                            max_tokens=1024
                        )
                        reply_result = response.choices[0].message.content

                    # Display result
                    st.markdown("### ✅ Your Professional Reply")
                    
                    # Track reply generation
                    st.markdown("""<script>
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'reply_generated', {
                            'event_category': 'engagement',
                            'event_label': 'reply_to_email',
                            'value': 1
                        });
                    }
                    </script>""", unsafe_allow_html=True)
                    
                    st.markdown(f'<div style="background:#e8f5e9; padding:20px; border-radius:12px; border:2px solid #4caf50;"><div style="color:#1b5e20; font-size:15px; line-height:1.6; white-space: pre-wrap;">{reply_result}</div></div>', unsafe_allow_html=True)

                    # Copy section
                    st.markdown("### 📋 Copy Reply")
                    st.code(reply_result, language=None)
                    st.info("👆 Tap and hold to copy, then paste in your email client")

                    # Share buttons
                    st.markdown("### 📤 Share Reply")
                    share_col1, share_col2 = st.columns(2)

                    with share_col1:
                        whatsapp_text = urllib.parse.quote(reply_result)
                        st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📱 WhatsApp</div></a>', unsafe_allow_html=True)

                    with share_col2:
                        email_subject = urllib.parse.quote("Reply from ProMailer AI")
                        email_body = urllib.parse.quote(reply_result)
                        st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration:none; display:block;"><div style="background:#EA4335; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📧 Email</div></a>', unsafe_allow_html=True)
                    
                    st.info("💡 **Tip:** Email button works best on mobile. On desktop, use the copy section above.")

                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error generating reply: {str(e)}")
                    st.info("Please try again or contact support if the issue persists.")

# Footer
st.markdown("---")
ai_names = {"gemini": "🤖 Google Gemini AI", "groq": "🚀 Groq AI"}
if 'ai_provider' in locals():
    st.markdown(f'<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 10px; border-radius: 8px; text-align: center; border: 2px solid #66bb6a; margin-bottom: 10px;"><div style="font-weight: bold; color: #1b5e20; font-size: 13px;">Powered by: {ai_names.get(ai_provider, ai_provider)}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #666; padding: 15px; font-size: 13px;'>ProMailer AI v2.4.0 - Built with 💚 by Bhushan</div>", unsafe_allow_html=True)
