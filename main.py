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
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_email' not in st.session_state:
    st.session_state.current_email = ""
if 'last_generated' not in st.session_state:
    st.session_state.last_generated = ""
if 'user_signature' not in st.session_state:
    st.session_state.user_signature = ""

# Email templates
EMAIL_TEMPLATES = {
    "📅 Meeting Request": "Hi, I would like to schedule a meeting to discuss the project progress. Please let me know your available time slots.",
    "🏖️ Leave Application": "I am writing to request leave from [start date] to [end date] due to personal reasons. I will ensure all my work is completed before I leave.",
    "📧 Follow-up": "I wanted to follow up on my previous email regarding [topic]. Please let me know if you need any additional information.",
    "🎉 Thank You": "Thank you very much for your time and consideration. I really appreciate your help with this matter.",
    "❓ Information Request": "I am writing to request information about [topic]. Could you please provide details on this?",
    "📋 Status Update": "I wanted to update you on the progress of [project]. Here is the current status and next steps."
}

# Sidebar
with st.sidebar:
    st.markdown("# 📖 ProMailer AI")
    st.caption("v2.1.0 - Enhanced Edition 🚀")

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
    st.caption("📋 Use templates for quick start")

    # Share button
    st.markdown("---")
    st.markdown("### 📲 Share this App")
    app_link = "https://promailer-ai-test.streamlit.app/"
    share_msg = urllib.parse.quote(f"Check out ProMailer AI Enhanced: {app_link}")
    st.markdown(f'<a href="https://wa.me/?text={share_msg}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:bold; font-size:14px;">📱 Share via WhatsApp</div></a>', unsafe_allow_html=True)

    # History
    st.markdown("---")
    st.markdown("### 📜 Recent History")

    if st.session_state.history:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

        for i, item in enumerate(st.session_state.history[:5]):
            timestamp = item.get('timestamp', 'No date')
            with st.expander(f"📧 Email {i+1} - {timestamp}"):
                st.text_area("", value=item.get('email', ''), height=100, key=f"hist_{i}", disabled=True, label_visibility="collapsed")
                if st.button("📋 Reuse", key=f"reuse_{i}", use_container_width=True):
                    st.session_state.current_email = item.get('email', '')
                    st.rerun()
    else:
        st.info("📭 No history yet")

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
        
        **😴 About App Sleep:**
        
        This free app may sleep after a few hours of inactivity to save resources. If you see a "wake up" screen, just click the button - it takes only 10-30 seconds to restart!
        
        💡 **Tip:** Once the app loads, it stays active while you're using it. No interruptions during your work!
        
        ---
        
        **🚀 Quick Start Guide:**
        
        1. **Choose template** or start from scratch
        2. **Type or speak** your rough notes
        3. **Select language** & tone
        4. **Generate** professional email
        5. **Copy & share** instantly!
        
        **For Email Replies:**
        - Upload screenshot of received email
        - Choose reply tone
        - Get perfect response in seconds!
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
/* Fix tab styling - make both tabs equally visible */
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

<script>
// Keep app awake by simulating activity every 4 minutes
setInterval(function() {
    // Create a small interaction to prevent sleep
    var event = new Event('streamlit:rerun');
    window.dispatchEvent(event);
}, 240000); // 4 minutes
</script>
""", unsafe_allow_html=True)

# Initialize AI
try:
    # Priority 1: Gemini (Best for vision + multilingual including Marathi)
    if "GEMINI_API_KEY" in st.secrets:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        ai_provider = "gemini"
        
        # Try different model names for text generation
        model_names = [
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-2.0-flash-exp'
        ]
        
        text_model = None
        for model_name in model_names:
            try:
                text_model = genai.GenerativeModel(model_name)
                break
            except:
                continue
        
        if not text_model:
            raise Exception("No Gemini model available")
    
    # Priority 2: Groq (Fast fallback for text)
    elif "GROQ_API_KEY" in st.secrets:
        from groq import Groq
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        ai_provider = "groq"
    
    # Priority 3: HuggingFace (Last resort)
    elif "HUGGINGFACE_API_KEY" in st.secrets:
        import requests
        hf_api_key = st.secrets["HUGGINGFACE_API_KEY"]
        ai_provider = "huggingface"
    
    else:
        st.error("⚠️ Please add API key in Streamlit Secrets")
        st.stop()

    # Check for Gemini vision features separately
    has_vision = False
    if "GEMINI_API_KEY" in st.secrets:
        import google.generativeai as genai
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # Try different model names for vision
        vision_model_names = [
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-2.0-flash-exp'
        ]
        
        vision_model = None
        for model_name in vision_model_names:
            try:
                vision_model = genai.GenerativeModel(model_name)
                has_vision = True
                st.sidebar.success(f"✅ Using {model_name}")
                break
            except:
                continue

except Exception as e:
    st.error(f"⚠️ API Error: {str(e)}")
    st.stop()

# Main content
st.title("✉️ ProMailer AI")
st.markdown("<p style='text-align: center; color: #2e7d32; font-size: 15px; font-weight: 600; margin-top: -8px;'>⌨️ Type OR 🎤 Speak → Professional Emails!</p>", unsafe_allow_html=True)

# Email Templates Section
st.markdown("### 📋 Quick Start")
tab1, tab2 = st.tabs(["📝 Write New Email", "📧 Reply to Email"])

with tab1:
    st.caption("Click a template to auto-fill, then customize!")
    cols = st.columns(3)
    template_keys = list(EMAIL_TEMPLATES.keys())

    for idx, template_name in enumerate(template_keys):
        col_idx = idx % 3
        with cols[col_idx]:
            if st.button(template_name, key=f"template_{idx}", use_container_width=True):
                st.session_state.current_email = EMAIL_TEMPLATES[template_name]
                st.rerun()

with tab2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
         padding: 15px; border-radius: 10px; border: 2px solid #2196F3; margin: 10px 0;'>
        <div style='font-size: 16px; font-weight: bold; color: #1565c0; margin-bottom: 8px;'>
            📧 Smart Reply Generator
        </div>
        <div style='font-size: 13px; color: #333;'>
            Got an email from your boss/senior? Upload screenshot and we'll generate the perfect reply!
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_email = st.file_uploader(
        "📸 Upload email screenshot (PNG, JPG)",
        type=['png', 'jpg', 'jpeg'],
        help="Take a screenshot of the email you received",
        key="email_reply_upload"
    )

    if uploaded_email:
        st.image(uploaded_email, caption="Email to reply to", use_container_width=True)

        reply_col1, reply_col2 = st.columns(2)
        with reply_col1:
            reply_tone = st.selectbox("Reply Tone:", ["Professional", "Respectful", "Friendly", "Formal"], key="reply_tone")
        with reply_col2:
            reply_type = st.selectbox("Reply Type:", ["Acknowledge", "Provide Info", "Request Clarification", "Agree/Confirm"], key="reply_type")

        if st.button("✨ Generate Reply", use_container_width=True, key="gen_reply"):
            with st.spinner("📧 Analyzing email and generating reply..."):
                try:
                    email_content = ""

                    # Try to extract text using Gemini Vision if available
                    if has_vision:
                        try:
                            import PIL.Image
                            uploaded_email.seek(0)  # Reset file pointer
                            img = PIL.Image.open(uploaded_email)

                            extract_response = vision_model.generate_content([
                                "Extract all text from this email screenshot. Return ONLY the email text content, no explanations:",
                                img
                            ])
                            email_content = extract_response.text

                            st.success("✅ Email text extracted automatically!")
                            st.markdown("**Extracted Email:**")
                            st.info(email_content)

                        except Exception as e:
                            st.warning(f"⚠️ Auto-extraction failed: {str(e)}")
                            email_content = ""

                    # Fallback: Ask user to paste text if extraction failed
                    if not email_content or not email_content.strip():
                        st.warning("💡 Please paste the email content below:")
                        email_content = st.text_area(
                            "Email content:",
                            height=150,
                            placeholder="Paste the email you received here...",
                            key="email_paste"
                        )

                    # Generate reply if we have content
                    if email_content and email_content.strip():
                        with st.spinner("✍️ Generating your reply..."):
                            reply_prompt = f"""You received this email:

{email_content}

Generate a {reply_tone.lower()} reply that will {reply_type.lower()}. 

Requirements:
- Match the sender's formality level
- Be concise but complete
- Include proper greeting and closing
- Professional tone
- Address all points raised"""

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
                            else:
                                reply_result = f"Reply: {email_content}"

                            st.markdown("### ✅ Your Reply Draft")
                            st.markdown(f'<div style="background:#e8f5e9; padding:20px; border-radius:12px; border:2px solid #4caf50;"><div style="color:#1b5e20; font-size:15px; line-height:1.6; white-space: pre-wrap;">{reply_result}</div></div>', unsafe_allow_html=True)

                            st.markdown("### 📋 Copy Reply")
                            st.code(reply_result, language=None)
                            st.info("👆 Tap and hold to copy")

                            # Share buttons for reply
                            st.markdown("### 📤 Share Reply")
                            share_col1, share_col2 = st.columns(2)

                            with share_col1:
                                whatsapp_text = urllib.parse.quote(reply_result)
                                st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📱 WhatsApp</div></a>', unsafe_allow_html=True)

                            with share_col2:
                                email_subject = urllib.parse.quote("Reply from ProMailer AI")
                                email_body = urllib.parse.quote(reply_result)
                                st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration:none; display:block;"><div style="background:#EA4335; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📧 Email</div></a>', unsafe_allow_html=True)
                            
                            st.info("💡 **Tip:** Email button works best on mobile. If it doesn't open on desktop, use the copy section above to paste into your email client.")

                            # Save to session
                            st.session_state.last_generated = reply_result

                            st.balloons()
                    else:
                        st.error("❌ No email content to generate reply from. Please paste the email text above.")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Feature status indicator
    if has_vision:
        st.success("✅ **Auto-extraction enabled** - Just upload and click generate!")
    else:
        st.info("💡 **Manual mode** - Upload image, then paste text to generate reply")



# Language Settings
st.markdown("---")
st.markdown("### 🌐 Language Settings")
col1, col2 = st.columns(2)

with col1:
    input_lang = st.selectbox("🎤 Input:", ["English", "Marathi", "Hindi", "Mix"], help="Your input language")

with col2:
    target_lang = st.selectbox("📧 Output:", ["English", "Marathi"], help="Email language")

# Show message
if input_lang == "English" and target_lang == "English":
    st.success("✅ Convert rough English to professional English")

# Input Section
st.markdown("---")
st.markdown("### ✍️ Your Message")

# Voice input
voice_text = ""
if "GROQ_API_KEY" in st.secrets:
    audio_input = mic_recorder(start_prompt="🎤 Record", stop_prompt="🛑 Stop", key='recorder')
    if audio_input:
        with st.spinner("🎧 Transcribing..."):
            try:
                # Import Groq for transcription
                from groq import Groq
                groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                with open("temp.wav", "wb") as f:
                    f.write(audio_input['bytes'])
                with open("temp.wav", "rb") as af:
                    transcription = groq_client.audio.transcriptions.create(
                        file=("temp.wav", af.read()), 
                        model="whisper-large-v3"
                    )
                    voice_text = transcription.text
                if os.path.exists("temp.wav"):
                    os.remove("temp.wav")
                
                st.success("✅ Voice transcribed!")
                
                # Show transcription
                with st.expander("📝 What you said", expanded=False):
                    st.info(f"**Transcribed text:**\n{voice_text}")
                    st.caption("💡 The transcription is shown for reference. The AI will generate a perfect professional email from your speech!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Text input with word count
draft = st.text_area(
    f"📝 Type or speak your message:",
    value=voice_text or st.session_state.current_email,
    height=150,
    placeholder=f"Type your rough notes in {input_lang}...",
    help="Use templates above for quick start!"
)

# Word count
if draft:
    word_count = len(draft.split())
    char_count = len(draft)
    st.caption(f"📊 {word_count} words | {char_count} characters")

# Options
col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox("🎭 Tone", ["Formal", "Friendly", "Urgent", "Casual"])
with col2:
    length = st.selectbox("📏 Length", ["Concise", "Detailed", "Very Brief"])

# Generate button
st.markdown("---")
if st.button("✨ Generate Professional Email", use_container_width=True):
    if not draft or draft.strip() == "":
        st.warning("⚠️ Please enter text or record voice first!")
    else:
        with st.spinner("🤖 Creating your email..."):
            try:
                # Add signature if exists
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

Notes: {draft}"""

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
                else:
                    result = f"Subject: Professional Email\n\nDear Recipient,\n\n{draft}{signature_text}"

                # Save to history
                timestamp = datetime.datetime.now().strftime("%d/%m %H:%M")
                st.session_state.history.insert(0, {'email': result, 'timestamp': timestamp})
                st.session_state.last_generated = result
                if len(st.session_state.history) > 10:
                    st.session_state.history = st.session_state.history[:10]

                # Display result
                st.markdown("### ✅ Your Professional Email")
                st.markdown(f'<div style="background:#fff; padding:20px; border-radius:12px; border:2px solid #66bb6a;"><div style="color:#1b5e20; font-size:15px; line-height:1.6; white-space: pre-wrap;">{result}</div></div>', unsafe_allow_html=True)

                # Quick actions
                st.markdown("### 🔄 Quick Actions")
                st.caption("Click to modify the email above")
                action_col1, action_col2, action_col3 = st.columns(3)

                # Store the result in session state for quick actions
                st.session_state.last_generated = result

                with action_col1:
                    if st.button("✂️ Make Shorter", use_container_width=True, key="action_shorter"):
                        # Create a new prompt to shorten
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
                    if st.button("📏 Make Longer", use_container_width=True, key="action_longer"):
                        # Create a new prompt to expand
                        longer_prompt = f"Make this email more detailed and elaborate while maintaining professionalism:\n\n{result}"

                        with st.spinner("📏 Making it longer..."):
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
                                    st.markdown("#### 📏 Longer Version:")
                                    st.markdown(f'<div style="background:#d1ecf1; padding:15px; border-radius:10px; border:2px solid #17a2b8;"><div style="color:#333; font-size:15px; line-height:1.6; white-space: pre-wrap;">{longer_result}</div></div>', unsafe_allow_html=True)
                                    st.code(longer_result, language=None)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                with action_col3:
                    if st.button("😊 Friendlier", use_container_width=True, key="action_friendly"):
                        # Create a new prompt to make friendlier
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

                # Copy section
                st.markdown("### 📋 Copy Email")
                st.code(result, language=None)
                st.info("👆 Tap and hold to copy")

                # Share buttons
                st.markdown("### 📤 Share")
                share_col1, share_col2 = st.columns(2)

                with share_col1:
                    whatsapp_text = urllib.parse.quote(result)
                    st.markdown(f'<a href="https://wa.me/?text={whatsapp_text}" target="_blank" style="text-decoration:none; display:block;"><div style="background:#25D366; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📱 WhatsApp</div></a>', unsafe_allow_html=True)

                with share_col2:
                    email_subject = urllib.parse.quote("Email from ProMailer AI")
                    email_body = urllib.parse.quote(result)
                    st.markdown(f'<a href="mailto:?subject={email_subject}&body={email_body}" style="text-decoration:none; display:block;"><div style="background:#EA4335; color:white; padding:14px; border-radius:10px; text-align:center; font-weight:bold; font-size:15px;">📧 Email</div></a>', unsafe_allow_html=True)
                
                st.info("💡 **Tip:** Email button works best on mobile. If it doesn't open on desktop, use the copy section above to paste into your email client.")

                st.balloons()

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
ai_names = {"gemini": "🤖 Google Gemini AI", "groq": "🚀 Groq AI", "huggingface": "🤗 Hugging Face"}
if 'ai_provider' in locals():
    st.markdown(f'<div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); padding: 10px; border-radius: 8px; text-align: center; border: 2px solid #66bb6a; margin-bottom: 10px;"><div style="font-weight: bold; color: #1b5e20; font-size: 13px;">Powered by: {ai_names.get(ai_provider, ai_provider)}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #666; padding: 15px; font-size: 13px;'>ProMailer AI Enhanced - Built with 💚 by Bhushan</div>", unsafe_allow_html=True)
