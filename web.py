from datetime import datetime
import json
import re
import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JYORA AI | AI, Data Analytics & Business Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GOOGLE APPS SCRIPT
# ============================================================

GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyate5bFtUmuT6TB1YqYhSGq0ED09kuMSXHdkYfj86avev7GZqnSlpyhlgXOfaorycl"
    "/exec"
)

# ============================================================
# HELPERS & VALIDATION
# ============================================================

def html(content):
    st.html(content)

def valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip())

def submit_to_google(payload):
    try:
        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "text/plain;charset=utf-8"},
            timeout=20,
            allow_redirects=True,
        )
        return response.status_code == 200
    except Exception:
        return False

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def reset_chat_state():
    st.session_state.chat_step = 0
    st.session_state.chat_data = {}
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": "👋 Welcome to JYORA AI.\nLet's understand your business requirement.",
        }
    ]

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    reset_chat_state()

# ============================================================
# GLOBAL STYLES & HEADER FIXES
# ============================================================

html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: #FFFFFF;
    color: #0F172A;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 1380px !important;
}

/* HEADER FIXES */
.top-header {
    width: 100%;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 20px;
    overflow: visible !important;
}

.header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-symbol {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0F172A, #2563EB);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 22px;
    font-weight: 900;
    box-shadow: 0 8px 22px rgba(37,99,235,0.20);
    flex-shrink: 0;
}

.brand-name {
    font-size: 32px !important;
    line-height: 1.2 !important;
    font-weight: 850 !important;
    letter-spacing: -1px;
    display: block !important;
    visibility: visible !important;
}

.jyora-text {
    color: #0F172A !important;
}

.ai-text {
    color: #2563EB !important;
}

.brand-description {
    font-size: 11px;
    color: #64748B;
    margin-top: 2px;
    letter-spacing: 0.5px;
    font-weight: 600;
}

/* NAVIGATION */
div.stButton > button {
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
    background: #FFFFFF !important;
    color: #334155 !important;
    font-weight: 600 !important;
    min-height: 38px !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.10) !important;
}

/* HERO SECTION */
.hero-section {
    position: relative;
    border-radius: 24px;
    padding: 70px 40px;
    margin-bottom: 40px;
    background: radial-gradient(circle at 85% 20%, rgba(59,130,246,0.15), transparent 30%),
                linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
    border: 1px solid #DBEAFE;
    text-align: center;
}

.hero-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 30px;
    background: #FFFFFF;
    border: 1px solid #BFDBFE;
    color: #2563EB;
    font-size: 11px;
    font-weight: 750;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 52px;
    line-height: 1.1;
    font-weight: 900;
    letter-spacing: -2px;
    color: #0F172A;
}

.hero-title span {
    color: #2563EB;
}

.hero-description {
    max-width: 720px;
    margin: 20px auto;
    color: #475569;
    font-size: 16px;
    line-height: 1.6;
}

/* CARDS */
.feature-card {
    padding: 24px;
    border-radius: 16px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    box-shadow: 0 6px 20px rgba(15,23,42,0.03);
    height: 100%;
}

.feature-title {
    color: #0F172A;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 8px;
}

.feature-text {
    color: #64748B;
    font-size: 13px;
    line-height: 1.6;
}

/* CHATBOT FLOATING OVERLAY UI */
.chat-launcher {
    position: fixed;
    bottom: 25px;
    left: 25px;
    z-index: 999999;
}

.chat-box-container {
    position: fixed;
    bottom: 25px;
    left: 25px;
    width: 300px;
    background: #FFFFFF;
    border-radius: 16px;
    box-shadow: 0 12px 35px rgba(15,23,42,0.20);
    border: 1px solid #E2E8F0;
    z-index: 999999;
    overflow: hidden;
}

.chat-box-header {
    background: linear-gradient(135deg, #0F172A, #2563EB);
    color: white;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chat-box-title {
    font-size: 13px;
    font-weight: 800;
}

.chat-box-subtitle {
    font-size: 10px;
    opacity: 0.8;
}

.chat-box-body {
    padding: 12px;
    max-height: 220px;
    overflow-y: auto;
}

.chat-msg {
    padding: 8px 10px;
    border-radius: 8px;
    font-size: 11px;
    line-height: 1.4;
    margin-bottom: 8px;
}

.chat-msg-assistant {
    background: #EFF6FF;
    color: #1E3A8A;
    border: 1px solid #DBEAFE;
}

.chat-msg-user {
    background: #0F172A;
    color: white;
    margin-left: 15px;
}

.footer {
    border-top: 1px solid #E2E8F0;
    margin-top: 60px;
    padding: 25px 0;
    text-align: center;
    color: #64748B;
    font-size: 12px;
}
</style>
"""
)

# ============================================================
# WEBSITE HEADER
# ============================================================

html(
    """
<div class="top-header">
    <div class="header-inner">
        <div class="brand">
            <div class="brand-symbol">J</div>
            <div>
                <div class="brand-name">
                    <span class="jyora-text">JYORA</span>
                    <span class="ai-text">AI</span>
                </div>
                <div class="brand-description">
                    AI • DATA • INTELLIGENCE • AUTOMATION
                </div>
            </div>
        </div>
    </div>
</div>
"""
)

# ============================================================
# NAVIGATION
# ============================================================

nav_cols = st.columns(6)
navigation = [
    ("Home", "Home"),
    ("Solutions", "Services"),
    ("Use Cases", "Projects"),
    ("Start Project", "Request Project"),
    ("About", "About"),
    ("Contact", "Contact"),
]

for col, (label, page) in zip(nav_cols, navigation):
    with col:
        if st.button(label, use_container_width=True, key=f"nav_{page}"):
            st.session_state.page = page
            st.rerun()

# ============================================================
# PAGES
# ============================================================

def home_page():
    html(
        """
    <div class="hero-section">
        <div class="hero-badge">✦ AI • DATA • BUSINESS INTELLIGENCE</div>
        <div class="hero-title">Intelligence That <span>Moves Business Forward</span></div>
        <div class="hero-description">
            JYORA AI helps businesses transform complex data into intelligent decisions through AI, Predictive Analytics and Automation.
        </div>
    </div>
    """
    )

    services = [
        ("🤖 Artificial Intelligence", "Predictive models, machine learning, and decision engines."),
        ("📊 Business Intelligence", "Interactive Power BI dashboards, KPI systems, and visualization."),
        ("🔮 Predictive Analytics", "Forecast demand, mitigate risks, and spot trends."),
        ("⚙️ Intelligent Automation", "Automate workflows, reporting pipelines, and repetitive data tasks."),
    ]

    cols = st.columns(2)
    for idx, (title, desc) in enumerate(services):
        with cols[idx % 2]:
            html(
                f"""
            <div class="feature-card" style="margin-bottom:15px;">
                <div class="feature-title">{title}</div>
                <div class="feature-text">{desc}</div>
            </div>
            """
            )

def services_page():
    st.title("Solutions & Services")
    st.write("Custom enterprise-grade AI, BI, and ETL pipeline solutions.")

def projects_page():
    st.title("Case Studies & Projects")
    st.write("Explore how our predictive models drive growth across logistics and retail.")

def request_project_page():
    st.title("Start a Project")
    with st.form("req_form"):
        st.text_input("Name")
        st.text_input("Email")
        st.text_area("Project Overview")
        if st.form_submit_button("Submit"):
            st.success("Submitted successfully.")

def about_page():
    st.title("About JYORA AI")
    st.write("Over a decade of expertise delivering actionable insights.")

def contact_page():
    st.title("Contact Us")
    st.write("Get in touch with our engineering team.")

# ============================================================
# ROUTER
# ============================================================

pages = {
    "Home": home_page,
    "Services": services_page,
    "Projects": projects_page,
    "Request Project": request_project_page,
    "About": about_page,
    "Contact": contact_page,
}

current_page_func = pages.get(st.session_state.page, home_page)
current_page_func()

# ============================================================
# LEFT SIDE SMALL FLOATING CHATBOT WIDGET
# ============================================================

def render_floating_chatbot():
    # Closed State Launcher
    if not st.session_state.chat_open:
        st.markdown('<div class="chat-launcher">', unsafe_allow_html=True)
        if st.button("💬 Chat", key="btn_open_chat"):
            st.session_state.chat_open = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Open State Small Container
    st.markdown('<div class="chat-box-container">', unsafe_allow_html=True)
    
    html(
        """
    <div class="chat-box-header">
        <div>
            <div class="chat-box-title">JYORA AI Assistant</div>
            <div class="chat-box-subtitle">Online</div>
        </div>
    </div>
    """
    )

    if st.button("✕ Close & New Chat", key="btn_close_chat", use_container_width=True):
        st.session_state.chat_open = False
        reset_chat_state()
        st.rerun()

    # Message View
    chat_html = '<div class="chat-box-body">'
    for msg in st.session_state.chat_messages:
        cls = "chat-msg-assistant" if msg["role"] == "assistant" else "chat-msg-user"
        chat_html += f'<div class="chat-msg {cls}">{msg["text"]}</div>'
    chat_html += '</div>'
    html(chat_html)

    # Multi-step Flow
    step = st.session_state.chat_step

    if step == 0:
        name = st.text_input("Name", key="chat_name", placeholder="Your name...")
        if st.button("Next →", key="chat_btn_s0"):
            if name.strip():
                st.session_state.chat_data["name"] = name.strip()
                st.session_state.chat_messages.append({"role": "user", "text": name.strip()})
                st.session_state.chat_messages.append({"role": "assistant", "text": "What service do you need?"})
                st.session_state.chat_step = 1
                st.rerun()

    elif step == 1:
        opts = ["AI Solutions", "BI & Dashboards", "Automation"]
        for opt in opts:
            if st.button(opt, key=f"chat_opt_{opt}"):
                st.session_state.chat_data["service"] = opt
                st.session_state.chat_messages.append({"role": "user", "text": opt})
                st.session_state.chat_messages.append({"role": "assistant", "text": "Please enter your email."})
                st.session_state.chat_step = 2
                st.rerun()

    elif step == 2:
        email = st.text_input("Email", key="chat_email", placeholder="email@domain.com")
        if st.button("Submit", key="chat_btn_s2"):
            if valid_email(email):
                st.session_state.chat_data["email"] = email.strip()
                st.session_state.chat_messages.append({"role": "user", "text": email.strip()})
                
                payload = {
                    "type": "chat_lead",
                    "name": st.session_state.chat_data.get("name"),
                    "service": st.session_state.chat_data.get("service"),
                    "email": email.strip(),
                    "timestamp": datetime.now().isoformat(),
                }
                submit_to_google(payload)

                st.session_state.chat_messages.append({"role": "assistant", "text": "Thanks! We'll reach out soon."})
                st.session_state.chat_step = 3
                st.rerun()
            else:
                st.error("Invalid Email")

    elif step == 3:
        if st.button("Start New Session", key="chat_btn_reset"):
            reset_chat_state()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

render_floating_chatbot()

# ============================================================
# FOOTER
# ============================================================

html(
    """
<div class="footer">
    <div><b>JYORA AI</b> — Data Intelligence & Automation Platform</div>
    <div>© 2026 JYORA AI. All rights reserved.</div>
</div>
"""
)
