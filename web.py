import streamlit as st
import requests
import json
import re
import html
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LogiIntelli | Logistics AI, Data Analytics & BI",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# GOOGLE APPS SCRIPT WEB APP
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
# HELPER FUNCTIONS
# ============================================================

def valid_email(email):
    return bool(
        re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email.strip()
        )
    )


def reset_chat():
    st.session_state.chat_messages = []
    st.session_state.chat_step = 0
    st.session_state.chat_data = {}
    st.session_state.chat_submitted = False


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
        "Requirement": data.get("requirement", ""),
    }

    try:

        response = requests.post(
            GOOGLE_SHEET_WEB_APP_URL,
            data=json.dumps(payload),
            headers={
                "Content-Type": "text/plain;charset=utf-8"
            },
            timeout=20,
            allow_redirects=True,
        )

        if response.status_code == 200:
            return True, "success"

        return False, response.text

    except requests.exceptions.Timeout:
        return False, "timeout"

    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# CHATBOT LOGIC
# ============================================================

def chatbot_response(user_message):

    step = st.session_state.chat_step
    data = st.session_state.chat_data

    message = user_message.strip()

    # --------------------------------------------------------
    # STEP 0 - NAME
    # --------------------------------------------------------

    if step == 0:

        data["name"] = message

        st.session_state.chat_step = 1

        return (
            f"Nice to meet you, **{message}**! 👋\n\n"
            "What is your **company name**?"
        )

    # --------------------------------------------------------
    # STEP 1 - COMPANY
    # --------------------------------------------------------

    if step == 1:

        data["company"] = message

        st.session_state.chat_step = 2

        return (
            "Great! 👍\n\n"
            "Which industry does your company operate in?\n\n"
            "**Courier / Logistics / E-commerce / Manufacturing / Other**"
        )

    # --------------------------------------------------------
    # STEP 2 - INDUSTRY
    # --------------------------------------------------------

    if step == 2:

        data["industry"] = message

        st.session_state.chat_step = 3

        return (
            "Thanks! What solution are you looking for?\n\n"
            "📊 **Power BI Dashboard**\n\n"
            "🗄️ **SQL Analytics**\n\n"
            "🤖 **Predictive AI / Machine Learning**\n\n"
            "⚙️ **MIS Automation**\n\n"
            "🔗 **API / ERP Integration**\n\n"
            "⏱️ **TAT & Ageing Analytics**\n\n"
            "🏢 **Hub Performance Analytics**\n\n"
            "📍 **Route Analytics**\n\n"
            "**Other**"
        )

    # --------------------------------------------------------
    # STEP 3 - SERVICE
    # --------------------------------------------------------

    if step == 3:

        data["service"] = message

        st.session_state.chat_step = 4

        return (
            "Understood. 👍\n\n"
            "Please describe the **business problem or requirement** "
            "you want to solve.\n\n"
            "For example:\n\n"
            "> We need a dashboard to monitor delayed shipments, "
            "hub performance and pending ageing."
        )

    # --------------------------------------------------------
    # STEP 4 - REQUIREMENT
    # --------------------------------------------------------

    if step == 4:

        data["requirement"] = message

        st.session_state.chat_step = 5

        return (
            "Perfect. What is your current **data source**?\n\n"
            "Excel / CSV / MySQL / SQL Server / PostgreSQL / "
            "ERP / REST API / Multiple Sources / Other"
        )

    # --------------------------------------------------------
    # STEP 5 - DATA SOURCE
    # --------------------------------------------------------

    if step == 5:

        data["data_source"] = message

        st.session_state.chat_step = 6

        return (
            "Approximately how much data do you handle?\n\n"
            "For example:\n\n"
            "• 1,000 shipments/day\n"
            "• 10,000 shipments/day\n"
            "• 1 lakh shipments/day\n"
            "• Not sure"
        )

    # --------------------------------------------------------
    # STEP 6 - DATA VOLUME
    # --------------------------------------------------------

    if step == 6:

        data["volume"] = message

        st.session_state.chat_step = 7

        return (
            "What timeline are you expecting?\n\n"
            "⏱️ Less than 1 week\n\n"
            "⏱️ 1–2 weeks\n\n"
            "⏱️ 2–4 weeks\n\n"
            "⏱️ 1–2 months\n\n"
            "⏱️ Not decided"
        )

    # --------------------------------------------------------
    # STEP 7 - TIMELINE
    # --------------------------------------------------------

    if step == 7:

        data["timeline"] = message

        st.session_state.chat_step = 8

        return (
            "Almost done! 😊\n\n"
            "Please provide your **business email address**."
        )

    # --------------------------------------------------------
    # STEP 8 - EMAIL
    # --------------------------------------------------------

    if step == 8:

        if not valid_email(message):

            return (
                "⚠️ That doesn't look like a valid email address.\n\n"
                "Please enter something like:\n\n"
                "**name@company.com**"
            )

        data["email"] = message

        st.session_state.chat_step = 9

        return (
            "Thanks! 📧\n\n"
            "Please provide your **Phone / WhatsApp number**.\n\n"
            "You can also type **Skip** if you don't want to provide it."
        )

    # --------------------------------------------------------
    # STEP 9 - PHONE
    # --------------------------------------------------------

    if step == 9:

        if message.lower() == "skip":
            data["phone"] = ""
        else:
            data["phone"] = message

        st.session_state.chat_step = 10

        phone_display = data.get("phone") or "Not provided"

        return f"""
### 📋 Project Request Summary

**Name:** {data.get("name", "")}

**Company:** {data.get("company", "")}

**Industry:** {data.get("industry", "")}

**Solution:** {data.get("service", "")}

**Requirement:** {data.get("requirement", "")}

**Data Source:** {data.get("data_source", "")}

**Data Volume:** {data.get("volume", "")}

**Timeline:** {data.get("timeline", "")}

**Email:** {data.get("email", "")}

**Phone:** {phone_display}

---

Would you like me to **submit this project request** to LogiIntelli?

Type **Yes** or **No**.
"""

    # --------------------------------------------------------
    # STEP 10 - CONFIRMATION
    # --------------------------------------------------------

    if step == 10:

        lower_message = message.lower()

        positive_words = [
            "yes",
            "y",
            "sure",
            "submit",
            "confirm",
            "ok",
            "okay",
            "go ahead",
        ]

        negative_words = [
            "no",
            "n",
            "cancel",
            "not now",
        ]

        if lower_message in positive_words:

            success, result = submit_chat_request()

            if success:

                st.session_state.chat_submitted = True
                st.session_state.chat_step = 11

                return (
                    "🎉 **Your project request has been submitted successfully!**\n\n"
                    "Thank you for contacting **LogiIntelli**.\n\n"
                    "We have received your requirement and will contact you "
                    "using the details you provided.\n\n"
                    "🚚 **LogiIntelli — Logistics AI • Data Analytics • BI**"
                )

            if result == "timeout":

                return (
                    "⏱️ The submission timed out.\n\n"
                    "Please type **Submit** to try again."
                )

            return (
                "❌ I couldn't submit the request right now.\n\n"
                "Please try again in a moment."
            )

        if lower_message in negative_words:

            st.session_state.chat_step = 11

            return (
                "No problem! 👍\n\n"
                "I haven't submitted anything.\n\n"
                "Whenever you're ready, you can start a new conversation."
            )

        return (
            "Please type **Yes** to submit the project request "
            "or **No** to cancel."
        )

    return (
        "Your request has already been submitted successfully. 🎉"
    )


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

/* Main page */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 102, 204, 0.08),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #f8fbff 0%,
            #ffffff 45%,
            #f5f8fc 100%
        );
}

/* Remove Streamlit top spacing */

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #d8e2ee;
    background: white;
    font-weight: 600;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #0066cc;
    color: #0066cc;
    transform: translateY(-1px);
}

/* Navigation */

.nav-button button {
    min-height: 42px;
}

/* Cards */

.service-card,
.project-card,
.metric-card,
.info-card {

    background: rgba(255,255,255,0.95);

    border: 1px solid #e4ebf3;

    border-radius: 18px;

    padding: 24px;

    box-shadow:
        0 8px 30px rgba(15, 42, 70, 0.06);

    height: 100%;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.service-card:hover,
.project-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 16px 40px rgba(15, 42, 70, 0.12);
}

/* Hero */

.hero {

    padding: 65px 40px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            #071d35 0%,
            #0b3c6f 45%,
            #0066cc 100%
        );

    color: white;

    margin-bottom: 35px;

    box-shadow:
        0 20px 60px rgba(0, 50, 100, 0.20);
}

.hero h1 {

    font-size: 52px;

    margin-bottom: 12px;

    line-height: 1.1;
}

.hero p {

    font-size: 19px;

    max-width: 800px;

    color: #dbeeff;

    line-height: 1.6;
}

/* Section */

.section-title {

    font-size: 30px;

    font-weight: 800;

    color: #0b2545;

    margin-top: 30px;

    margin-bottom: 20px;
}

/* Metrics */

.metric-number {

    font-size: 34px;

    font-weight: 800;

    color: #0066cc;
}

.metric-label {

    font-size: 14px;

    color: #60758a;

    margin-top: 5px;
}

/* Chat launcher */

#logi-chat-launcher {

    position: fixed;

    right: 25px;

    bottom: 25px;

    z-index: 999999;

    border: none;

    cursor: pointer;

    display: flex;

    align-items: center;

    gap: 10px;

    padding: 13px 19px;

    border-radius: 50px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #0b2545,
            #0066cc
        );

    box-shadow:
        0 10px 35px rgba(0, 82, 160, 0.35);

    font-size: 14px;

    font-weight: 700;
}

#logi-chat-launcher:hover {

    transform: translateY(-2px);

    box-shadow:
        0 14px 40px rgba(0, 82, 160, 0.45);
}

.chat-icon {

    width: 34px;

    height: 34px;

    display: flex;

    align-items: center;

    justify-content: center;

    background: white;

    color: #0066cc;

    border-radius: 50%;

    font-size: 18px;
}

/* Chat window */

#logi-chat-window {

    position: fixed;

    right: 25px;

    bottom: 90px;

    width: 380px;

    max-width: calc(100vw - 30px);

    height: 580px;

    max-height: calc(100vh - 120px);

    background: white;

    border-radius: 20px;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.22);

    border: 1px solid #dce5ef;

    overflow: hidden;

    z-index: 999998;

    display: none;

    flex-direction: column;
}

#logi-chat-window.open {

    display: flex;
}

/* Chat header */

.chat-header {

    background:
        linear-gradient(
            135deg,
            #071d35,
            #0066cc
        );

    color: white;

    padding: 17px 18px;

    display: flex;

    align-items: center;

    justify-content: space-between;
}

.chat-header-left {

    display: flex;

    align-items: center;

    gap: 10px;
}

.chat-header-icon {

    width: 40px;

    height: 40px;

    background: white;

    color: #0066cc;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 20px;
}

.chat-header-title {

    font-size: 15px;

    font-weight: 800;
}

.chat-header-status {

    font-size: 11px;

    opacity: 0.85;

    margin-top: 2px;
}

.chat-close {

    background: rgba(255,255,255,0.15);

    border: none;

    color: white;

    width: 32px;

    height: 32px;

    border-radius: 50%;

    cursor: pointer;

    font-size: 18px;
}

/* Chat body */

.chat-body {

    flex: 1;

    overflow-y: auto;

    padding: 15px;

    background: #f5f8fc;
}

/* Message */

.chat-message {

    max-width: 86%;

    padding: 11px 13px;

    margin-bottom: 10px;

    border-radius: 15px;

    font-size: 13px;

    line-height: 1.5;
}

.chat-bot {

    background: white;

    color: #24384d;

    border: 1px solid #e1e8f0;

    border-bottom-left-radius: 5px;

    margin-right: auto;
}

.chat-user {

    background: #0066cc;

    color: white;

    border-bottom-right-radius: 5px;

    margin-left: auto;
}

/* Chat input */

.chat-input-area {

    padding: 12px;

    border-top: 1px solid #e4e9ef;

    background: white;

    display: flex;

    gap: 8px;
}

.chat-input {

    flex: 1;

    border: 1px solid #d7e0ea;

    border-radius: 12px;

    padding: 10px 12px;

    outline: none;

    font-size: 13px;
}

.chat-send {

    width: 42px;

    border: none;

    border-radius: 12px;

    background: #0066cc;

    color: white;

    cursor: pointer;

    font-size: 17px;
}

/* Mobile */

@media (max-width: 600px) {

    #logi-chat-window {

        right: 10px;

        bottom: 80px;

        width: calc(100vw - 20px);

        height: 70vh;
    }

    #logi-chat-launcher {

        right: 15px;

        bottom: 15px;

        padding: 11px 15px;
    }

    .hero {

        padding: 40px 25px;
    }

    .hero h1 {

        font-size: 36px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:12px 4px 18px 4px;
">
    <div>
        <div style="
            font-size:25px;
            font-weight:800;
            color:#0B2545;
        ">
            🚚 LogiIntelli
        </div>

        <div style="
            font-size:12px;
            color:#60758A;
            margin-top:3px;
        ">
            Logistics Analytics • AI & Predictive Intelligence • BI Automation
        </div>
    </div>

    <div style="
        font-size:12px;
        color:#0066CC;
        font-weight:700;
    ">
        DATA • AI • AUTOMATION
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION
# ============================================================

pages = [
    "Home",
    "Services",
    "Projects",
    "Request Project",
    "About",
    "Contact",
]

nav_cols = st.columns(6)

for idx, page_name in enumerate(pages):

    with nav_cols[idx]:

        selected = (
            st.session_state.page == page_name
        )

        label = (
            f"● {page_name}"
            if selected
            else page_name
        )

        if st.button(
            label,
            key=f"nav_{idx}",
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()


page = st.session_state.page


# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
<div class="hero">

    <div style="
        font-size:14px;
        font-weight:700;
        color:#7ec8ff;
        margin-bottom:12px;
    ">
        LOGISTICS DATA & AI INTELLIGENCE
    </div>

    <h1>
        Turn Logistics Data<br>
        Into Business Intelligence.
    </h1>

    <p>
        Build powerful logistics dashboards, automate MIS,
        integrate ERP/API data and use predictive AI to
        improve shipment visibility, operational efficiency
        and decision making.
    </p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Our Impact</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("10+", "Years Experience"),
        ("50+", "Analytics & AI Pipelines"),
        ("24/7", "Automated Systems"),
        ("BI + AI", "Technology Architecture"),
    ]

    for col, (number, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
<div class="metric-card">

    <div class="metric-number">
        {number}
    </div>

    <div class="metric-label">
        {label}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">What We Build</div>',
        unsafe_allow_html=True,
    )

    services = [
        (
            "📊",
            "Logistics BI",
            "Interactive Power BI dashboards for logistics and operations."
        ),
        (
            "⏱️",
            "TAT & Ageing Analytics",
            "Identify delayed shipments, ageing patterns and operational bottlenecks."
        ),
        (
            "⚙️",
            "MIS Automation",
            "Automate repetitive daily, weekly and monthly reporting."
        ),
        (
            "🏢",
            "Hub Performance",
            "Measure hub productivity, volume, SLA and operational performance."
        ),
        (
            "🔗",
            "API & ERP Integration",
            "Connect ERP, databases and REST APIs into analytics pipelines."
        ),
        (
            "🤖",
            "Predictive AI",
            "Use machine learning to predict shipment delays and operational risks."
        ),
    ]

    service_cols = st.columns(3)

    for index, service in enumerate(services):

        icon, title, description = service

        with service_cols[index % 3]:

            st.markdown(
                f"""
<div class="service-card">

    <div style="
        font-size:30px;
        margin-bottom:12px;
    ">
        {icon}
    </div>

    <div style="
        font-size:18px;
        font-weight:800;
        color:#0B2545;
        margin-bottom:8px;
    ">
        {title}
    </div>

    <div style="
        font-size:13px;
        line-height:1.6;
        color:#60758A;
    ">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">How We Work</div>',
        unsafe_allow_html=True,
    )

    workflow_cols = st.columns(4)

    workflow = [
        ("01", "Understand", "Understand your business problem and KPIs."),
        ("02", "Connect", "Connect ERP, SQL, Excel, APIs and other data sources."),
        ("03", "Build", "Build dashboards, automation and AI solutions."),
        ("04", "Improve", "Monitor results and continuously improve operations."),
    ]

    for col, item in zip(
        workflow_cols,
        workflow
    ):

        number, title, description = item

        with col:

            st.markdown(
                f"""
<div class="info-card">

    <div style="
        font-size:13px;
        color:#0066CC;
        font-weight:800;
    ">
        {number}
    </div>

    <div style="
        font-size:18px;
        font-weight:800;
        margin:8px 0;
        color:#0B2545;
    ">
        {title}
    </div>

    <div style="
        font-size:13px;
        line-height:1.6;
        color:#60758A;
    ">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
<div style="
    margin-top:35px;
    padding:35px;
    border-radius:22px;
    background:#0B2545;
    color:white;
    text-align:center;
">

    <div style="
        font-size:27px;
        font-weight:800;
    ">
        Have a Logistics Analytics Challenge?
    </div>

    <div style="
        color:#cce6ff;
        margin:10px 0 20px 0;
    ">
        Tell us your requirement and let's build the solution.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# SERVICES
# ============================================================

elif page == "Services":

    st.markdown(
        '<div class="section-title">Our Services</div>',
        unsafe_allow_html=True,
    )

    services = [
        (
            "📊",
            "Logistics BI",
            "Power BI dashboards, KPI monitoring, operational reporting and executive analytics."
        ),
        (
            "⏱️",
            "TAT & Ageing Analytics",
            "Shipment TAT, ageing buckets, SLA performance, pending shipment and delay analytics."
        ),
        (
            "⚙️",
            "MIS Automation",
            "Automate daily MIS, scheduled reports, email distribution and operational reporting."
        ),
        (
            "🏢",
            "Hub Performance Analytics",
            "Analyze booking, inbound, outbound, delivery and hub-level operational performance."
        ),
        (
            "🔗",
            "API & ERP Integration",
            "Extract data from REST APIs, ERP systems, SQL databases and multiple sources."
        ),
        (
            "🤖",
            "Predictive AI & Machine Learning",
            "Predict shipment delays, identify risk patterns and support proactive operations."
        ),
    ]

    cols = st.columns(3)

    for i, service in enumerate(services):

        icon, title, description = service

        with cols[i % 3]:

            st.markdown(
                f"""
<div class="service-card">

    <div style="font-size:34px;">
        {icon}
    </div>

    <h3 style="
        color:#0B2545;
        margin-bottom:10px;
    ">
        {title}
    </h3>

    <p style="
        color:#60758A;
        font-size:14px;
        line-height:1.7;
    ">
        {description}
    </p>

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    st.markdown(
        '<div class="section-title">Projects & Solutions</div>',
        unsafe_allow_html=True,
    )

    projects = [
        (
            "🚚",
            "Courier Operations Dashboard",
            "End-to-end Power BI dashboard covering booking, delivery, pending and operational KPIs."
        ),
        (
            "⏱️",
            "Shipment TAT & Ageing Analytics",
            "Monitor shipment lifecycle, ageing buckets, TAT and SLA performance."
        ),
        (
            "🏢",
            "Hub Performance Analytics",
            "Analyze hub productivity, volume, service quality and operational bottlenecks."
        ),
        (
            "📦",
            "Inbound / Outbound Analytics",
            "State, hub and route-level inbound and outbound shipment analytics."
        ),
        (
            "🤖",
            "Shipment Delay Prediction AI",
            "Machine learning model to identify shipments with a higher probability of delay."
        ),
        (
            "⚙️",
            "Automated Daily MIS Engine",
            "Python-based automated reporting pipeline for daily logistics operations."
        ),
    ]

    cols = st.columns(3)

    for i, project in enumerate(projects):

        icon, title, description = project

        with cols[i % 3]:

            st.markdown(
                f"""
<div class="project-card">

    <div style="
        font-size:32px;
        margin-bottom:12px;
    ">
        {icon}
    </div>

    <div style="
        font-size:18px;
        font-weight:800;
        color:#0B2545;
        margin-bottom:10px;
    ">
        {title}
    </div>

    <div style="
        color:#60758A;
        font-size:13px;
        line-height:1.7;
    ">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# REQUEST PROJECT
# ============================================================

elif page == "Request Project":

    st.markdown(
        '<div class="section-title">Request a Project</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Tell us about your requirement. "
        "We will review it and get back to you."
    )

    with st.form("project_request_form"):

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input(
                "Company Name"
            )

            contact = st.text_input(
                "Contact Person *"
            )

            email = st.text_input(
                "Business Email *"
            )

            phone = st.text_input(
                "Phone / WhatsApp"
            )

        with col2:

            industry = st.selectbox(
                "Industry",
                [
                    "Courier / Logistics",
                    "E-commerce",
                    "Manufacturing",
                    "Retail",
                    "Supply Chain",
                    "Other",
                ],
            )

            service = st.selectbox(
                "Service Required",
                [
                    "Power BI Dashboard",
                    "SQL Analytics",
                    "TAT & Ageing Analytics",
                    "MIS Automation",
                    "Hub Performance Analytics",
                    "API / ERP Integration",
                    "Predictive AI / Machine Learning",
                    "Route Analytics",
                    "Other",
                ],
            )

            data_source = st.selectbox(
                "Data Source",
                [
                    "Excel / CSV",
                    "MySQL",
                    "SQL Server",
                    "PostgreSQL",
                    "ERP",
                    "REST API",
                    "Multiple Sources",
                    "Other",
                ],
            )

            timeline = st.selectbox(
                "Expected Timeline",
                [
                    "Less than 1 week",
                    "1–2 weeks",
                    "2–4 weeks",
                    "1–2 months",
                    "Not decided",
                ],
            )

        requirement = st.text_area(
            "Project Requirement *",
            height=160,
            placeholder=(
                "Describe your business problem, "
                "dashboard requirement, automation need, "
                "AI requirement, etc."
            ),
        )

        submitted = st.form_submit_button(
            "🚀 Submit Project Request",
            use_container_width=True,
        )

        if submitted:

            if not contact.strip():

                st.error(
                    "Please enter your contact name."
                )

            elif not email.strip():

                st.error(
                    "Please enter your email."
                )

            elif not valid_email(email):

                st.error(
                    "Please enter a valid email address."
                )

            elif not requirement.strip():

                st.error(
                    "Please describe your project requirement."
                )

            else:

                payload = {

                    "Date":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "Company":
                        company,

                    "Contact":
                        contact,

                    "Email":
                        email,

                    "Phone":
                        phone,

                    "Industry":
                        industry,

                    "Service":
                        service,

                    "Data_Source":
                        data_source,

                    "Timeline":
                        timeline,

                    "Requirement":
                        requirement,
                }

                try:

                    response = requests.post(
                        GOOGLE_SHEET_WEB_APP_URL,
                        data=json.dumps(payload),
                        headers={
                            "Content-Type":
                                "text/plain;charset=utf-8"
                        },
                        timeout=20,
                        allow_redirects=True,
                    )

                    if response.status_code == 200:

                        st.success(
                            "🎉 Project request submitted successfully!"
                        )

                        st.info(
                            "Thank you. We will contact you soon."
                        )

                    else:

                        st.error(
                            "Unable to submit the request."
                        )

                except Exception as e:

                    st.error(
                        f"Submission error: {e}"
                    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">About LogiIntelli</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="info-card">

<h2 style="color:#0B2545;">
Logistics Intelligence Through Data
</h2>

<p style="
    color:#60758A;
    line-height:1.8;
    font-size:15px;
">

LogiIntelli focuses on solving real-world logistics,
supply chain and operational challenges using data,
business intelligence, automation and artificial intelligence.

</p>

<p style="
    color:#60758A;
    line-height:1.8;
    font-size:15px;
">

Our solutions combine SQL, Python, Power BI,
REST APIs, ERP integration, automation and machine
learning to transform operational data into actionable
business intelligence.

</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Technology Stack</div>',
        unsafe_allow_html=True,
    )

    tech = [
        "SQL",
        "Python",
        "Pandas",
        "Power BI",
        "DAX",
        "Power Query",
        "Machine Learning",
        "XGBoost",
        "REST APIs",
        "MySQL",
        "Streamlit",
        "Automation",
    ]

    cols = st.columns(4)

    for i, technology in enumerate(tech):

        with cols[i % 4]:

            st.markdown(
                f"""
<div class="info-card"
style="
    margin-bottom:15px;
    text-align:center;
    padding:16px;
">

<b style="color:#0B2545;">
{technology}
</b>

</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    st.markdown(
        '<div class="section-title">Let's Work Together</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Have a logistics analytics, BI, automation or AI requirement?"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            """
<div class="info-card">

<div style="font-size:28px;">📧</div>

<h4 style="color:#0B2545;">
Email
</h4>

<p>
sumansekar1205@gmail.com
</p>

</div>
""",
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            """
<div class="info-card">

<div style="font-size:28px;">📱</div>

<h4 style="color:#0B2545;">
WhatsApp
</h4>

<p>
+91 8825674102
</p>

</div>
""",
            unsafe_allow_html=True,
        )

    with c3:

        st.markdown(
            """
<div class="info-card">

<div style="font-size:28px;">💼</div>

<h4 style="color:#0B2545;">
LinkedIn
</h4>

<p>
linkedin.com/in/sumansekar12/
</p>

</div>
""",
            unsafe_allow_html=True,
        )

    with c4:

        st.markdown(
            """
<div class="info-card">

<div style="font-size:28px;">💻</div>

<h4 style="color:#0B2545;">
GitHub
</h4>

<p>
github.com/Suman-SekarSagadev
</p>

</div>
""",
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<hr>

<div style="
    text-align:center;
    padding:20px;
    color:#708398;
    font-size:12px;
">

🚚 <b>LogiIntelli</b>

<br><br>

Logistics Analytics • AI • BI • Automation

<br><br>

© 2026 LogiIntelli. All rights reserved.

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# FLOATING CHATBOT FRONTEND
# ============================================================

chat_open = st.session_state.chat_open

display_style = "flex" if chat_open else "none"

# Escape messages safely for HTML
chat_html = ""

for msg in st.session_state.chat_messages:

    role = msg["role"]

    content = msg["content"]

    content = html.escape(content)

    # Basic markdown-like formatting
    content = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        content,
    )

    content = content.replace(
        "\n",
        "<br>"
    )

    if role == "assistant":

        chat_html += f"""
<div class="chat-message chat-bot">
    {content}
</div>
"""

    else:

        chat_html += f"""
<div class="chat-message chat-user">
    {content}
</div>
"""


# ============================================================
# CHATBOT WINDOW
# ============================================================

st.markdown(
    f"""
<div
    id="logi-chat-window"
    class="{'open' if chat_open else ''}"
>

    <div class="chat-header">

        <div class="chat-header-left">

            <div class="chat-header-icon">
                🤖
            </div>

            <div>

                <div class="chat-header-title">
                    LogiIntelli Assistant
                </div>

                <div class="chat-header-status">
                    ● Online • Project Support
                </div>

            </div>

        </div>

        <button
            class="chat-close"
            onclick="closeLogiChat()"
        >
            ×
        </button>

    </div>


    <div class="chat-body">

        {chat_html}

    </div>


    <div class="chat-input-area">

        <input
            id="logi-chat-input"
            class="chat-input"
            type="text"
            placeholder="Type your answer..."
            onkeydown="
                if(event.key === 'Enter') {{
                    sendLogiMessage();
                }}
            "
        >

        <button
            class="chat-send"
            onclick="sendLogiMessage()"
        >
            ➤
        </button>

    </div>

</div>


<button
    id="logi-chat-launcher"
    onclick="toggleLogiChat()"
>

    <span class="chat-icon">
        🤖
    </span>

    <span>
        Chat with us
    </span>

</button>


<script>

function toggleLogiChat() {{

    const windowElement =
        document.getElementById("logi-chat-window");

    const launcher =
        document.getElementById("logi-chat-launcher");

    if (
        windowElement.classList.contains("open")
    ) {{

        windowElement.classList.remove("open");

    }} else {{

        windowElement.classList.add("open");

        setTimeout(function() {{

            const input =
                document.getElementById(
                    "logi-chat-input"
                );

            if(input) {{
                input.focus();
            }}

        }}, 100);

    }}

}}


function closeLogiChat() {{

    const windowElement =
        document.getElementById(
            "logi-chat-window"
        );

    windowElement.classList.remove("open");

}}


function sendLogiMessage() {{

    const input =
        document.getElementById(
            "logi-chat-input"
        );

    const message =
        input.value.trim();

    if(!message) {{
        return;
    }}

    /*
       Streamlit native chat input is handled separately.
       This function places the message into the Streamlit
       query parameters so Python can process it.
    */

    const url =
        new URL(
            window.location.href
        );

    url.searchParams.set(
        "chat_message",
        message
    );

    window.history.replaceState(
        {{}},
        "",
        url
    );

    input.value = "";

    window.location.reload();

}}


window.addEventListener(
    "load",
    function() {{

        const windowElement =
            document.getElementById(
                "logi-chat-window"
            );

        if(windowElement) {{

            const body =
                windowElement.querySelector(
                    ".chat-body"
                );

            if(body) {{
                body.scrollTop =
                    body.scrollHeight;
            }}

        }}

    }}
);

</script>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PROCESS CHAT MESSAGE FROM URL
# ============================================================

query_params = st.query_params

chat_message = query_params.get(
    "chat_message",
    ""
)

if chat_message:

    # Clear query parameter first
    st.query_params.clear()

    # Open chat
    st.session_state.chat_open = True

    # First chatbot message
    if not st.session_state.chat_messages:

        initial_message = (
            "👋 Hi! I'm the **LogiIntelli Project Assistant**.\n\n"
            "I can collect your project requirements and "
            "submit them directly to our team.\n\n"
            "Let's get started!\n\n"
            "**What is your name?**"
        )

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": initial_message,
            }
        )

    # Add user message
    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": chat_message,
        }
    )

    # Generate response
    response = chatbot_response(
        chat_message
    )

    # Add bot response
    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    st.rerun()


# ============================================================
# START CHAT
# ============================================================

if (
    st.session_state.chat_open
    and not st.session_state.chat_messages
):

    initial_message = (
        "👋 Hi! I'm the **LogiIntelli Project Assistant**.\n\n"
        "I can collect your project requirements and "
        "submit them directly to our team.\n\n"
        "Let's get started!\n\n"
        "**What is your name?**"
    )

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": initial_message,
        }
    )

    st.rerun()
