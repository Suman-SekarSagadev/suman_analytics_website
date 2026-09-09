import streamlit as st
import requests
import json
import re
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LogiIntelli | Logistics Analytics & AI",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GOOGLE SHEET WEB APP URL
# ============================================================

GOOGLE_SHEET_WEB_APP_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyate5bFtUmuT6TB1YqYhSGq0ED09kuMSXHdkYfj86avev7GZqnSlpyhlgXOfaorycl"
    "/exec"
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 0

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

if "chat_submitted" not in st.session_state:
    st.session_state.chat_submitted = False


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):
    st.html(content)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email.strip()))


# ============================================================
# RESET CHAT
# ============================================================

def reset_chat():
    st.session_state.chat_messages = []
    st.session_state.chat_step = 0
    st.session_state.chat_data = {}
    st.session_state.chat_submitted = False


# ============================================================
# INITIAL CHAT MESSAGE
# ============================================================

def start_chat():
    if not st.session_state.chat_messages:
        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": (
                    "👋 Hi! I'm the **LogiIntelli Project Assistant**.\n\n"
                    "I can collect your project requirements and "
                    "send them directly to our team.\n\n"
                    "Let's get started!\n\n"
                    "**What is your name?**"
                )
            }
        )


# ============================================================
# SUBMIT CHAT REQUEST TO GOOGLE SHEET
# ============================================================

def submit_chat_request():
    data = st.session_state.chat_data
    payload = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Company": data.get("company", ""),
        "Contact": data.get("name", ""),
        "Email": data.get("email", ""),
        "Phone": data.get("phone", ""),
        "Industry": data.get("industry", ""),
        "Service": data.get("service", ""),
        "Data_Source": data.get("data_source", ""),
        "Shipment_Volume": data.get("volume", ""),
        "Timeline": data.get("timeline", ""),
        "Requirement": data.get("requirement", "")
    }

    try:
        response = requests.post(
            GOOGLE_SHEET_WEB_APP_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "text/plain;charset=utf-8"},
            timeout=20,
            allow_redirects=True
        )
        return response.status_code == 200
    except Exception:
        return False


# ============================================================
# CHATBOT LOGIC
# ============================================================

def chatbot_response(user_message):
    message = user_message.strip()
    step = st.session_state.chat_step
    data = st.session_state.chat_data

    if step == 0:
        data["name"] = message
        st.session_state.chat_step = 1
        return f"Nice to meet you, **{message}**! 👋\n\nWhat is your **company name**?"

    if step == 1:
        data["company"] = message
        st.session_state.chat_step = 2
        return (
            "Great! 👍\n\n"
            "Which industry does your company operate in?\n\n"
            "Courier / Logistics / E-commerce / Manufacturing / Retail / Supply Chain / Other"
        )

    if step == 2:
        data["industry"] = message
        st.session_state.chat_step = 3
        return (
            "Thanks! What solution are you looking for?\n\n"
            "📊 Power BI Dashboard\n\n🗄️ SQL Analytics\n\n🤖 Predictive AI / Machine Learning\n\n"
            "⚙️ MIS Automation\n\n🔗 API / ERP Integration\n\n⏱️ TAT & Ageing Analytics\n\n"
            "🏢 Hub Performance Analytics\n\n📍 Route Analytics\n\nOther"
        )

    if step == 3:
        data["service"] = message
        st.session_state.chat_step = 4
        return (
            "Understood. 👍\n\n"
            "Please describe your **business problem or project requirement**.\n\n"
            "Example:\n\nWe need a dashboard to monitor delayed shipments, hub performance and pending ageing."
        )

    if step == 4:
        data["requirement"] = message
        st.session_state.chat_step = 5
        return (
            "Perfect! What is your current **data source**?\n\n"
            "Excel / CSV / MySQL / SQL Server / PostgreSQL / ERP / REST API / Multiple Sources / Other"
        )

    if step == 5:
        data["data_source"] = message
        st.session_state.chat_step = 6
        return (
            "Approximately how much data do you handle?\n\n"
            "For example:\n\n• 1,000 shipments/day\n• 10,000 shipments/day\n• 1 lakh shipments/day\n• Not sure"
        )

    if step == 6:
        data["volume"] = message
        st.session_state.chat_step = 7
        return (
            "What timeline are you expecting?\n\n"
            "⏱️ Less than 1 week\n\n⏱️ 1–2 weeks\n\n⏱️ 2–4 weeks\n\n⏱️ 1–2 months\n\n⏱️ Not decided"
        )

    if step == 7:
        data["timeline"] = message
        st.session_state.chat_step = 8
        return "Almost done! 😊\n\nPlease provide your **business email address**."

    if step == 8:
        if not valid_email(message):
            return "⚠️ That doesn't look like a valid email address.\n\nPlease enter something like:\n\n**name@company.com**"
        data["email"] = message
        st.session_state.chat_step = 9
        return "Thanks! 📧\n\nPlease provide your **Phone / WhatsApp number**.\n\nYou can type **Skip** if you don't want to provide it."

    if step == 9:
        data["phone"] = "" if message.lower() == "skip" else message
        st.session_state.chat_step = 10
        phone = data.get("phone") or "Not provided"
        return (
            "### 📋 Project Request Summary\n\n"
            f"**Name:** {data.get('name', '')}\n\n"
            f"**Company:** {data.get('company', '')}\n\n"
            f"**Industry:** {data.get('industry', '')}\n\n"
            f"**Solution:** {data.get('service', '')}\n\n"
            f"**Requirement:** {data.get('requirement', '')}\n\n"
            f"**Data Source:** {data.get('data_source', '')}\n\n"
            f"**Data Volume:** {data.get('volume', '')}\n\n"
            f"**Timeline:** {data.get('timeline', '')}\n\n"
            f"**Email:** {data.get('email', '')}\n\n"
            f"**Phone:** {phone}\n\n"
            "---\n\n"
            "Would you like me to **submit this project request**?\n\nPlease type **Yes** or **No**."
        )

    if step == 10:
        answer = message.lower()
        yes_words = ["yes", "y", "submit", "sure", "confirm", "ok", "okay", "go ahead"]
        no_words = ["no", "n", "cancel", "not now"]

        if answer in yes_words:
            if submit_chat_request():
                st.session_state.chat_submitted = True
                st.session_state.chat_step = 11
                return (
                    "🎉 **Your project request has been submitted successfully!**\n\n"
                    "Thank you for contacting **LogiIntelli**.\n\n"
                    "We have received your requirement and will contact you using the details provided.\n\n"
                    "🚚 **LogiIntelli**\n\nLogistics AI • Data Analytics • BI"
                )
            return "❌ I couldn't submit the request right now.\n\nPlease type **Submit** to try again."

        if answer in no_words:
            st.session_state.chat_step = 11
            return "No problem! 👍\n\nYour request has not been submitted.\n\nYou can start a new conversation whenever you're ready."

        return "Please type **Yes** to submit or **No** to cancel."

    return "Your conversation is complete. 🎉\n\nClick **New Chat** if you need anything else."


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
<style>
html, body {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 10% 10%, rgba(0, 102, 204, 0.07), transparent 30%),
                linear-gradient(180deg, #f8fbff 0%, #ffffff 50%, #f5f8fc 100%);
    color-scheme: light;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1400px !important;
}

/* HIDE STREAMLIT TOP TOOLBAR & HEADER */
#MainMenu, header, footer, [data-testid="stHeader"] {
    visibility: hidden !important;
    height: 0px !important;
}

.logo-title {
    font-size: 27px;
    font-weight: 800;
    color: #0B2545;
    line-height: 1.2;
}

.logo-subtitle {
    font-size: 12px;
    color: #60758A;
    margin-top: 4px;
}

.stButton > button {
    border-radius: 10px !important;
    border: 1px solid #d9e3ee !important;
    background: #ffffff !important;
    color: #0B2545 !important;
    font-weight: 600 !important;
    min-height: 40px !important;
}

.stButton > button:hover {
    border-color: #0066CC !important;
    color: #0066CC !important;
}

.hero {
    width: 100%;
    box-sizing: border-box;
    padding: 65px 45px;
    border-radius: 28px;
    background: linear-gradient(135deg, #071d35 0%, #0b3c6f 45%, #0066cc 100%);
    color: #ffffff;
    margin-top: 20px;
    margin-bottom: 35px;
    box-shadow: 0 20px 60px rgba(0, 50, 100, 0.20);
}

.hero-small-title {
    color: #7ec8ff;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 50px;
    line-height: 1.1;
    font-weight: 800;
    margin: 0 0 15px 0;
}

.hero p {
    max-width: 850px;
    color: #dbeeff !important;
    font-size: 18px;
    line-height: 1.7;
    margin: 0;
}

.section-title {
    display: block;
    width: 100%;
    color: #0B2545 !important;
    font-size: 30px;
    font-weight: 800;
    line-height: 1.3;
    margin-top: 35px;
    margin-bottom: 20px;
    padding: 0;
}

.service-card, .project-card, .metric-card, .info-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid #e2eaf2;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(15,42,70,0.06);
    height: 100%;
    box-sizing: border-box;
}

.service-card:hover, .project-card:hover {
    box-shadow: 0 15px 40px rgba(15,42,70,0.12);
}

.metric-number {
    font-size: 34px;
    font-weight: 800;
    color: #0066CC !important;
}

.metric-label {
    color: #60758A !important;
    font-size: 14px;
    margin-top: 5px;
}
</style>
"""
)


# ============================================================
# HEADER
# ============================================================

render_html(
    """
<div style="display:flex; justify-content:space-between; align-items:center; padding:8px 4px 15px 4px;">
    <div>
        <div class="logo-title">🚚 LogiIntelli</div>
        <div class="logo-subtitle">Logistics Analytics • AI & Predictive Intelligence • BI Automation</div>
    </div>
    <div style="color:#0066CC; font-size:12px; font-weight:800;">
        DATA • AI • AUTOMATION
    </div>
</div>
"""
)


# ============================================================
# NAVIGATION
# ============================================================

pages = ["Home", "Services", "Projects", "Request Project", "About", "Contact"]
nav_cols = st.columns(6)

for i, page_name in enumerate(pages):
    with nav_cols[i]:
        label = f"● {page_name}" if st.session_state.page == page_name else page_name
        if st.button(label, key=f"nav_{i}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

page = st.session_state.page


# ============================================================
# HOME
# ============================================================

if page == "Home":
    render_html(
        """
<div class="hero">
    <div class="hero-small-title">LOGISTICS DATA & AI INTELLIGENCE</div>
    <h1>Turn Logistics Data<br>Into Business Intelligence.</h1>
    <p>Build powerful logistics dashboards, automate MIS, integrate ERP/API data and use predictive AI to improve shipment visibility, operational efficiency and decision making.</p>
</div>
"""
    )

    render_html('<div class="section-title">Our Impact</div>')
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("10+", "Years Experience"),
        ("50+", "Analytics & AI Pipelines"),
        ("24/7", "Automated Systems"),
        ("BI + AI", "Technology Architecture")
    ]

    for col, (number, label) in zip([c1, c2, c3, c4], metrics):
        with col:
            render_html(
                f"""
<div class="metric-card">
    <div class="metric-number">{number}</div>
    <div class="metric-label">{label}</div>
</div>
"""
            )

    render_html('<div class="section-title">What We Build</div>')
    services = [
        ("📊", "Logistics BI", "Interactive Power BI dashboards for logistics and operations."),
        ("⏱️", "TAT & Ageing Analytics", "Identify delayed shipments, ageing patterns and bottlenecks."),
        ("⚙️", "MIS Automation", "Automate repetitive daily, weekly and monthly reporting."),
        ("🏢", "Hub Performance", "Measure hub productivity, SLA and operational performance."),
        ("🔗", "API & ERP Integration", "Connect ERP, databases and REST APIs into analytics pipelines."),
        ("🤖", "Predictive AI", "Predict shipment delays and operational risks.")
    ]

    cols = st.columns(3)
    for i, (icon, title, description) in enumerate(services):
        with cols[i % 3]:
            render_html(
                f"""
<div class="service-card">
    <div style="font-size:32px; margin-bottom:12px;">{icon}</div>
    <div style="font-size:18px; font-weight:800; color:#0B2545; margin-bottom:10px;">{title}</div>
    <div style="font-size:13px; line-height:1.7; color:#60758A;">{description}</div>
</div>
"""
            )

# ============================================================
# SERVICES
# ============================================================

elif page == "Services":
    render_html('<div class="section-title">Our Services</div>')

    services = [
        ("📊", "Logistics BI", "Power BI dashboards, KPI monitoring, operational reporting and executive analytics."),
        ("⏱️", "TAT & Ageing Analytics", "Shipment TAT, ageing buckets, SLA performance and pending shipment analytics."),
        ("⚙️", "MIS Automation", "Automate daily MIS, scheduled reports and operational reporting."),
        ("🏢", "Hub Performance Analytics", "Analyze hub productivity, volume, service quality and bottlenecks."),
        ("🔗", "API & ERP Integration", "Connect REST APIs, ERP systems and SQL databases."),
        ("🤖", "Predictive AI & Machine Learning", "Predict shipment delays and identify operational risk patterns.")
    ]

    cols = st.columns(3)
    for i, (icon, title, description) in enumerate(services):
        with cols[i % 3]:
            render_html(
                f"""
<div class="service-card">
    <div style="font-size:35px; margin-bottom:10px;">{icon}</div>
    <h3 style="color:#0B2545; margin-bottom:10px;">{title}</h3>
    <p style="color:#60758A; font-size:14px; line-height:1.7;">{description}</p>
</div>
"""
            )
