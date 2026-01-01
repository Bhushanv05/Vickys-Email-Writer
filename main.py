import streamlit as st
import anthropic
from datetime import datetime

# Configure Streamlit
st.set_page_config(
    page_title="Email Writer",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal, professional styling
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
    
    [data-testid="stMainBlockContainer"] {
        background: white;
        max-width: 1200px;
    }
    
    [data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    
    h1, h2, h3 { color: #1a1a1a; font-weight: 600; margin: 0.5rem 0; }
    h1 { font-size: 28px; margin-bottom: 1.5rem; }
    h2 { font-size: 18px; margin-bottom: 1rem; }
    h3 { font-size: 14px; margin-bottom: 0.75rem; color: #555; }
    
    p { color: #333; font-size: 14px; line-height: 1.6; margin: 0.5rem 0; }
    
    .stat-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 12px;
        margin: 10px 0;
        text-align: center;
    }
    
    .stat-card h3 { color: #666; font-size: 12px; margin-bottom: 8px; }
    .stat-card p { font-size: 24px; font-weight: 700; color: #2c3e50; margin: 0; }
    
    .section-divider { 
        border-top: 1px solid #e0e0e0;
        margin: 1.5rem 0;
    }
    
    textarea { 
        border: 1px solid #ddd !important;
        border-radius: 4px;
        font-size: 14px;
    }
    
    .stButton > button {
        background: #2c3e50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: #1a252f;
    }
    
    .success-message {
        background: #f0f8f4;
        border-left: 3px solid #27ae60;
        padding: 12px;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .info-text { color: #666; font-size: 13px; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "email_count" not in st.session_state:
    st.session_state.email_count = 0
if "api_calls" not in st.session_state:
    st.session_state.api_calls = 0
if "generated_emails" not in st.session_state:
    st.session_state.generated_emails = []

# Sidebar: Configuration & Stats
with st.sidebar:
    st.markdown("### Settings")
    
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Enter your Anthropic API key"
    )
    
    tone = st.selectbox(
        "Email Tone",
        ["Professional", "Friendly", "Formal", "Casual"],
        index=0
    )
    
    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "German", "Japanese"],
        index=0
    )
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Consolidated stats
    st.markdown("### Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h3>Generated</h3>
            <p>{st.session_state.email_count}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>API Calls</h3>
            <p>{st.session_state.api_calls}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### About")
    st.markdown(
        '<p class="info-text">Professional email generation powered by Claude AI. Create polished, effective emails in seconds.</p>',
        unsafe_allow_html=True
    )

# Main content area
st.markdown("## Email Writer")
st.markdown('<p class="info-text">Generate professional, personalized emails with AI assistance</p>', unsafe_allow_html=True)

# Input section
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown("### Compose")
    
    recipient = st.text_input(
        "Recipient Name",
        placeholder="e.g., John Smith",
        help="Name of the email recipient"
    )
    
    subject = st.text_input(
        "Email Subject",
        placeholder="e.g., Project Update",
        help="Subject line of the email"
    )
    
    purpose = st.text_area(
        "Email Purpose",
        placeholder="Briefly describe what this email is about...",
        height=100,
        help="What do you want to communicate?"
    )
    
    context = st.text_area(
        "Additional Context (Optional)",
        placeholder="Any other details that might help...",
        height=80,
        help="Background information, previous discussions, etc."
    )

with col2:
    st.markdown("### Options")
    length = st.select_slider(
        "Email Length",
        options=["Short", "Medium", "Long"],
        value="Medium"
    )
    
    include_greeting = st.checkbox("Include greeting", value=True)
    include_closing = st.checkbox("Include closing", value=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    generate_btn = st.button("Generate Email", type="primary")

# Generation logic
if generate_btn:
    if not api_key:
        st.error("Please enter your Anthropic API key in the sidebar")
    elif not purpose:
        st.error("Please describe the email purpose")
    else:
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # Construct prompt
            prompt = f"""Generate a professional email with these specifications:
Recipient: {recipient if recipient else 'Colleague'}
Subject: {subject if subject else 'Message'}
Purpose: {purpose}
Tone: {tone}
Language: {language}
Length: {length}
Include greeting: {include_greeting}
Include closing: {include_closing}
Additional context: {context if context else 'None'}

Please generate only the email body, without any preamble or explanation."""
            
            with st.spinner("Generating email..."):
                message = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
            
            email_content = message.content[0].text
            
            # Update stats
            st.session_state.email_count += 1
            st.session_state.api_calls += 1
            st.session_state.generated_emails.append({
                "timestamp": datetime.now(),
                "recipient": recipient or "Colleague",
                "subject": subject or "Message",
                "content": email_content
            })
            
            # Display result
            st.markdown("""
            <div class="success-message">
                <strong>Email generated successfully</strong>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Generated Email")
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text_area(
                    "Email Content",
                    value=email_content,
                    height=300,
                    disabled=True,
                    label_visibility="collapsed"
                )
            with col2:
                st.button("Copy", key="copy_btn", help="Copy to clipboard")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Regenerate", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("Download", use_container_width=True):
                    st.download_button(
                        "Download",
                        email_content,
                        file_name=f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    )
            with col3:
                if st.button("Clear", use_container_width=True):
                    st.session_state.email_count = 0
                    st.rerun()
        
        except anthropic.APIError as e:
            st.error(f"API Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# History section (minimal)
if st.session_state.generated_emails:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Recent Emails")
    
    for idx, email in enumerate(reversed(st.session_state.generated_emails[-5:])):
        with st.expander(f"{email['subject']} → {email['recipient']}", expanded=False):
            st.text(email['content'])
            st.caption(f"Generated: {email['timestamp'].strftime('%Y-%m-%d %H:%M')}")
