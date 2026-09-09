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
# HTML HELPER
# ============================================================

def html(content):
    st.html(content)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):
    return re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email.strip()
    )


# ============================================================
# GOOGLE SHEET SUBMISSION
# ============================================================

def submit_to_google(payload):

    try:

        response = requests.post(
            GOOGLE_SCRIPT_URL,
            data=json.dumps(payload),
            headers={
                "Content-Type": "text/plain;charset=utf-8"
            },
            timeout=20,
            allow_redirects=True,
        )

        return response.status_code == 200

    except Exception:

        return False


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = True

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 0

if "chat_data" not in st.session_state:
    st.session_state.chat_data = {}

if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Welcome to JYORA AI.\n"
                "Let's understand your business requirement."
            ),
        }
    ]


# ============================================================
# GLOBAL CSS
# ============================================================

html(
    """
<style>

/* ============================================================
   GOOGLE FONT
============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);


/* ============================================================
   GLOBAL
============================================================ */

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: #FFFFFF;
    color: #0F172A;
}

.block-container {
    padding-top: 1.3rem !important;
    padding-bottom: 5rem !important;
    max-width: 1380px !important;
}


/* ============================================================
   HEADER
============================================================ */

.top-header {

    width: 100%;

    padding: 8px 0 17px 0;

    border-bottom: 1px solid #E5E7EB;

    margin-bottom: 12px;
}

.header-inner {

    display: flex;

    align-items: center;

    justify-content: space-between;
}

.brand {

    display: flex;

    align-items: center;

    gap: 11px;
}

.brand-symbol {

    width: 43px;

    height: 43px;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        );

    display: flex;

    align-items: center;

    justify-content: center;

    color: white;

    font-size: 21px;

    font-weight: 900;

    box-shadow:
        0 8px 22px rgba(37,99,235,0.20);
}

.brand-name {

    font-size: 30px;

    line-height: 1;

    font-weight: 850;

    letter-spacing: -1.5px;
}

.jyora-text {
    color: #0F172A;
}

.ai-text {
    color: #2563EB;
}

.brand-description {

    font-size: 10px;

    color: #64748B;

    margin-top: 5px;

    letter-spacing: 0.4px;
}


/* ============================================================
   NAVIGATION
============================================================ */

div.stButton > button {

    border-radius: 8px !important;

    border: 1px solid #E2E8F0 !important;

    background: #FFFFFF !important;

    color: #334155 !important;

    font-weight: 600 !important;

    min-height: 36px !important;

    transition: all 0.2s ease !important;
}

div.stButton > button:hover {

    border-color: #2563EB !important;

    color: #2563EB !important;

    box-shadow:
        0 4px 14px rgba(37,99,235,0.10) !important;
}


/* ============================================================
   HERO
============================================================ */

.hero-section {

    position: relative;

    overflow: hidden;

    border-radius: 26px;

    padding: 82px 45px 80px 45px;

    margin-top: 15px;

    margin-bottom: 55px;

    background:

        radial-gradient(
            circle at 85% 20%,
            rgba(59,130,246,0.22),
            transparent 30%
        ),

        radial-gradient(
            circle at 10% 90%,
            rgba(37,99,235,0.16),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #F8FAFC 0%,
            #EFF6FF 48%,
            #FFFFFF 100%
        );

    border: 1px solid #DBEAFE;
}

.hero-content {

    max-width: 900px;

    margin: auto;

    text-align: center;
}

.hero-badge {

    display: inline-block;

    padding: 8px 15px;

    border-radius: 30px;

    background: #FFFFFF;

    border: 1px solid #BFDBFE;

    color: #2563EB;

    font-size: 11px;

    font-weight: 750;

    letter-spacing: 0.5px;

    margin-bottom: 22px;
}

.hero-title {

    font-size: 58px;

    line-height: 1.04;

    font-weight: 900;

    letter-spacing: -3.2px;

    color: #0F172A;

    margin: 0 auto;
}

.hero-title span {
    color: #2563EB;
}

.hero-description {

    max-width: 760px;

    margin: 25px auto 30px auto;

    color: #475569;

    font-size: 16px;

    line-height: 1.75;
}

.hero-mini {

    color: #64748B;

    font-size: 11px;

    margin-top: 20px;
}


/* ============================================================
   SECTIONS
============================================================ */

.section {

    padding: 25px 0 55px 0;
}

.section-center {
    text-align: center;
}

.section-label {

    color: #2563EB;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.4px;

    text-transform: uppercase;

    margin-bottom: 10px;
}

.section-title {

    font-size: 37px;

    font-weight: 850;

    letter-spacing: -1.8px;

    color: #0F172A;

    margin-bottom: 10px;
}

.section-description {

    color: #64748B;

    font-size: 14px;

    line-height: 1.7;

    max-width: 720px;

    margin: auto;
}


/* ============================================================
   FEATURE CARDS
============================================================ */

.feature-card {

    height: 100%;

    min-height: 235px;

    padding: 28px;

    border-radius: 18px;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 8px 30px rgba(15,23,42,0.035);

    transition: all 0.25s ease;
}

.feature-card:hover {

    transform: translateY(-5px);

    border-color: #BFDBFE;

    box-shadow:
        0 18px 45px rgba(15,23,42,0.08);
}

.feature-icon {

    width: 48px;

    height: 48px;

    border-radius: 13px;

    background: #EFF6FF;

    border: 1px solid #DBEAFE;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 22px;

    margin-bottom: 18px;
}

.feature-title {

    color: #0F172A;

    font-size: 17px;

    font-weight: 750;

    margin-bottom: 9px;
}

.feature-text {

    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   DARK SECTION
============================================================ */

.dark-section {

    background:

        radial-gradient(
            circle at 85% 20%,
            rgba(37,99,235,0.22),
            transparent 28%
        ),

        #0B1220;

    border-radius: 25px;

    padding: 55px 40px;

    color: white;

    margin: 35px 0 65px 0;
}

.dark-label {

    color: #60A5FA;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.5px;

    text-transform: uppercase;
}

.dark-title {

    font-size: 38px;

    font-weight: 850;

    letter-spacing: -1.8px;

    margin: 10px 0;
}

.dark-text {

    color: #CBD5E1;

    font-size: 14px;

    line-height: 1.7;

    max-width: 700px;
}

.dark-card {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius: 16px;

    padding: 22px;

    height: 100%;
}

.dark-card-title {

    color: white;

    font-weight: 700;

    font-size: 15px;

    margin-bottom: 7px;
}

.dark-card-text {

    color: #94A3B8;

    font-size: 12px;

    line-height: 1.6;
}


/* ============================================================
   METRICS
============================================================ */

.metric {

    text-align: center;

    padding: 22px;

    border-right: 1px solid #E2E8F0;
}

.metric:last-child {
    border-right: none;
}

.metric-value {

    font-size: 34px;

    font-weight: 850;

    color: #2563EB;
}

.metric-label {

    font-size: 11px;

    color: #64748B;

    margin-top: 5px;
}


/* ============================================================
   PROCESS
============================================================ */

.process-card {

    padding: 25px;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    background: #FFFFFF;

    height: 100%;
}

.process-number {

    font-size: 12px;

    font-weight: 800;

    color: #2563EB;

    margin-bottom: 12px;
}

.process-title {

    font-size: 16px;

    font-weight: 750;

    color: #0F172A;
}

.process-text {

    font-size: 12px;

    color: #64748B;

    line-height: 1.65;

    margin-top: 7px;
}


/* ============================================================
   TECHNOLOGY
============================================================ */

.tech-pill {

    display: inline-block;

    padding: 10px 16px;

    border-radius: 30px;

    border: 1px solid #E2E8F0;

    background: white;

    color: #334155;

    font-size: 12px;

    font-weight: 650;

    margin: 5px;
}


/* ============================================================
   PROJECTS
============================================================ */

.project-card {

    border: 1px solid #E2E8F0;

    background: #FFFFFF;

    border-radius: 18px;

    padding: 25px;

    min-height: 210px;

    box-shadow:
        0 6px 25px rgba(15,23,42,0.035);
}

.project-tag {

    display: inline-block;

    color: #2563EB;

    background: #EFF6FF;

    border: 1px solid #DBEAFE;

    border-radius: 20px;

    padding: 5px 9px;

    font-size: 9px;

    font-weight: 800;

    text-transform: uppercase;
}

.project-title {

    color: #0F172A;

    font-size: 17px;

    font-weight: 750;

    margin: 13px 0 8px 0;
}

.project-text {

    color: #64748B;

    font-size: 12px;

    line-height: 1.65;
}


/* ============================================================
   CTA
============================================================ */

.cta-section {

    position: relative;

    overflow: hidden;

    background:

        radial-gradient(
            circle at 85% 20%,
            rgba(96,165,250,0.25),
            transparent 28%
        ),

        linear-gradient(
            135deg,
            #0F172A,
            #172554
        );

    border-radius: 24px;

    padding: 60px 35px;

    margin: 45px 0;

    text-align: center;

    color: white;
}

.cta-title {

    font-size: 36px;

    font-weight: 850;

    letter-spacing: -1.5px;
}

.cta-text {

    max-width: 650px;

    margin: 13px auto 25px auto;

    color: #CBD5E1;

    font-size: 14px;

    line-height: 1.7;
}


/* ============================================================
   FORM
============================================================ */

.form-container {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 20px;

    padding: 30px;

    box-shadow:
        0 10px 35px rgba(15,23,42,0.05);
}


/* ============================================================
   CHATBOT CONTAINER
============================================================ */

.st-key-floating_chatbot {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 310px !important;

    max-width: calc(100vw - 40px) !important;

    z-index: 999999 !important;

    background: #FFFFFF !important;

    border: 1px solid #D9E2EC !important;

    border-radius: 16px !important;

    box-shadow:
        0 15px 45px rgba(15,23,42,0.20),
        0 5px 15px rgba(15,23,42,0.08) !important;

    overflow: visible !important;

    padding: 0 !important;

    margin: 0 !important;
}


/* ============================================================
   CHAT HEADER
============================================================ */

.jyora-chat-header {

    width: 100% !important;

    min-height: 60px !important;

    box-sizing: border-box !important;

    padding: 12px 48px 11px 14px !important;

    background:
        linear-gradient(
            135deg,
            #0F172A 0%,
            #2563EB 100%
        ) !important;

    border-radius: 15px 15px 0 0 !important;

    display: block !important;

    position: relative !important;

    overflow: visible !important;
}


/* ============================================================
   CHAT TITLE
============================================================ */

.jyora-chat-title {

    display: block !important;

    width: 100% !important;

    color: #FFFFFF !important;

    font-family: "Inter", sans-serif !important;

    font-size: 13px !important;

    font-weight: 800 !important;

    line-height: 18px !important;

    margin: 0 !important;

    padding: 0 !important;

    text-align: left !important;

    visibility: visible !important;

    opacity: 1 !important;

    white-space: nowrap !important;
}


/* ============================================================
   CHAT SUBTITLE
============================================================ */

.jyora-chat-subtitle {

    display: block !important;

    width: 100% !important;

    color: #DBEAFE !important;

    font-family: "Inter", sans-serif !important;

    font-size: 9px !important;

    font-weight: 500 !important;

    line-height: 13px !important;

    margin: 2px 0 0 0 !important;

    padding: 0 !important;

    text-align: left !important;

    visibility: visible !important;

    opacity: 1 !important;

    white-space: nowrap !important;
}


/* ============================================================
   CLOSE BUTTON
============================================================ */

.st-key-chat_close_btn {

    position: absolute !important;

    top: 10px !important;

    right: 8px !important;

    width: 27px !important;

    height: 27px !important;

    z-index: 1000000 !important;

    padding: 0 !important;

    margin: 0 !important;

    background: transparent !important;
}

.st-key-chat_close_btn > div {

    width: 27px !important;

    height: 27px !important;

}

.st-key-chat_close_btn button {

    width: 25px !important;

    height: 25px !important;

    min-height: 25px !important;

    max-height: 25px !important;

    padding: 0 !important;

    margin: 0 !important;

    border-radius: 50% !important;

    background:
        rgba(255,255,255,0.16) !important;

    color: #FFFFFF !important;

    border:
        1px solid rgba(255,255,255,0.28) !important;

    font-size: 12px !important;

    font-weight: 700 !important;

    line-height: 1 !important;

    box-shadow: none !important;
}

.st-key-chat_close_btn button:hover {

    background:
        rgba(255,255,255,0.30) !important;

    color: #FFFFFF !important;

    border-color:
        rgba(255,255,255,0.50) !important;
}


/* ============================================================
   CHAT BODY
============================================================ */

.chat-body {

    padding: 8px 9px 5px 9px !important;

    max-height: 220px !important;

    overflow-y: auto !important;

    background: #FFFFFF !important;
}

.chat-message {

    padding: 7px 9px !important;

    border-radius: 9px !important;

    margin: 5px 0 !important;

    font-size: 10px !important;

    line-height: 1.45 !important;

    white-space: pre-wrap !important;
}

.chat-assistant {

    background: #EFF6FF !important;

    color: #1E3A8A !important;

    border:
        1px solid #DBEAFE !important;
}

.chat-user {

    background: #0F172A !important;

    color: white !important;

    margin-left: 18px !important;
}


/* ============================================================
   CHAT INPUT
============================================================ */

.st-key-floating_chatbot input {

    font-size: 10px !important;
}

.st-key-floating_chatbot textarea {

    font-size: 10px !important;
}

.st-key-floating_chatbot button {

    min-height: 28px !important;

    padding: 4px 7px !important;

    font-size: 9px !important;

    border-radius: 7px !important;
}


/* ============================================================
   CHAT SERVICE BUTTONS
============================================================ */

.st-key-floating_chatbot
div[data-testid="stButton"]
button {

    white-space: normal !important;

    text-align: left !important;

    padding-left: 10px !important;

    min-height: 28px !important;

    font-size: 9px !important;
}


/* ============================================================
   REOPEN CHAT
============================================================ */

.st-key-open_chat_container {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    z-index: 999999 !important;

    width: 56px !important;

    height: 56px !important;

    padding: 0 !important;

    margin: 0 !important;
}

.st-key-open_chat_container button {

    width: 56px !important;

    height: 56px !important;

    min-height: 56px !important;

    padding: 0 !important;

    border-radius: 50% !important;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        ) !important;

    color: white !important;

    border: none !important;

    box-shadow:
        0 10px 30px rgba(15,23,42,0.25) !important;

    font-size: 21px !important;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    border-top: 1px solid #E2E8F0;

    margin-top: 55px;

    padding: 30px 0 10px 0;

    text-align: center;

    color: #64748B;

    font-size: 11px;
}

.footer-brand {

    color: #0F172A;

    font-size: 18px;

    font-weight: 800;

    margin-bottom: 7px;
}

.footer-ai {
    color: #2563EB;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 700px) {

    .block-container {

        padding-left: 1rem !important;

        padding-right: 1rem !important;
    }

    .hero-section {

        padding: 55px 20px;

        border-radius: 20px;
    }

    .hero-title {

        font-size: 39px;

        letter-spacing: -2px;
    }

    .hero-description {

        font-size: 14px;
    }

    .section-title {

        font-size: 29px;
    }

    .brand-name {

        font-size: 25px;
    }

    .brand-description {

        font-size: 8px;
    }

    .metric {

        border-right: none;

        border-bottom:
            1px solid #E2E8F0;
    }

    .dark-section {

        padding: 35px 20px;
    }

    .dark-title {

        font-size: 29px;
    }

    .cta-section {

        padding: 45px 20px;
    }

    .cta-title {

        font-size: 29px;
    }

    .st-key-floating_chatbot {

        left: 10px !important;

        bottom: 10px !important;

        width: 280px !important;

        max-width: calc(100vw - 20px) !important;
    }

    .st-key-open_chat_container {

        left: 10px !important;

        bottom: 10px !important;
    }

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

            <div class="brand-symbol">
                J
            </div>

            <div>

                <div class="brand-name">

                    <span class="jyora-text">
                        JYORA
                    </span>

                    <span class="ai-text">
                        AI
                    </span>

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
    ("Start a Project", "Request Project"),
    ("About", "About"),
    ("Contact", "Contact"),
]


for col, (label, page) in zip(
    nav_cols,
    navigation
):

    with col:

        if st.button(
            label,
            use_container_width=True,
            key=f"nav_{page}",
        ):

            st.session_state.page = page

            st.rerun()


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            ✦ AI • DATA • BUSINESS INTELLIGENCE
        </div>

        <div class="hero-title">
            Intelligence That
            <span>Moves Business Forward</span>
        </div>

        <div class="hero-description">

            JYORA AI helps businesses transform complex data
            into intelligent decisions through Artificial Intelligence,
            Business Intelligence, Predictive Analytics and Automation.

        </div>

        <div class="hero-mini">
            Predict • Analyze • Automate • Optimize
        </div>

    </div>

</div>
"""
    )


    left, center, right = st.columns([1, 2, 1])

    with center:

        b1, b2 = st.columns(2)

        with b1:

            if st.button(
                "🚀 Start a Project",
                use_container_width=True,
                key="hero_start",
            ):

                st.session_state.page = "Request Project"

                st.rerun()

        with b2:

            if st.button(
                "Explore Solutions",
                use_container_width=True,
                key="hero_solutions",
            ):

                st.session_state.page = "Services"

                st.rerun()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # METRICS
    # ========================================================

    metric_cols = st.columns(4)

    metrics = [

        ("11+", "Years Analytics Experience"),

        ("50+", "Analytics Solutions"),

        ("7+", "Team Leadership"),

        ("24/7", "Data-Driven Insights"),
    ]


    for col, (value, label) in zip(
        metric_cols,
        metrics
    ):

        with col:

            html(
                f"""
<div class="metric">

    <div class="metric-value">
        {value}
    </div>

    <div class="metric-label">
        {label}
    </div>

</div>
"""
            )


    # ========================================================
    # WHAT WE DO
    # ========================================================

    html(
        """
<div class="section section-center">

    <div class="section-label">
        WHAT WE DO
    </div>

    <div class="section-title">
        Technology Built Around Your Business
    </div>

    <div class="section-description">

        From raw data to intelligent decisions,
        JYORA AI combines analytics, artificial intelligence
        and automation to solve real business problems.

    </div>

</div>
"""
    )


    services = [

        (
            "🤖",
            "Artificial Intelligence",
            "Predictive models, machine learning, forecasting and intelligent decision systems."
        ),

        (
            "📊",
            "Business Intelligence",
            "Power BI dashboards, KPI systems, executive reporting and data visualization."
        ),

        (
            "🔮",
            "Predictive Analytics",
            "Forecast demand, identify risks, predict delays and discover future trends."
        ),

        (
            "⚙️",
            "Intelligent Automation",
            "Automate repetitive reporting, operational processes, MIS and data workflows."
        ),

        (
            "🗄️",
            "Data Engineering",
            "SQL, ETL, APIs, data transformation and reliable analytics-ready datasets."
        ),

        (
            "🚚",
            "Logistics Intelligence",
            "Shipment, SLA, TAT, hub, delivery and operational performance analytics."
        ),
    ]


    service_cols = st.columns(3)


    for i, (
        icon,
        title,
        text
    ) in enumerate(services):

        with service_cols[i % 3]:

            html(
                f"""
<div class="feature-card">

    <div class="feature-icon">
        {icon}
    </div>

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {text}
    </div>

</div>
"""
            )

        if (i + 1) % 3 == 0:

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


    # ========================================================
    # DARK AI SECTION
    # ========================================================

    html(
        """
<div class="dark-section">

    <div class="dark-label">
        INTELLIGENT TECHNOLOGY
    </div>

    <div class="dark-title">
        From Data to Decisions
    </div>

    <div class="dark-text">

        Modern businesses generate enormous amounts of data.
        JYORA AI turns that data into useful intelligence,
        helping teams understand what happened, why it happened
        and what should happen next.

    </div>

</div>
"""
    )


    dark_cols = st.columns(3)

    dark_features = [

        (
            "01",
            "Understand",
            "Connect your business data and uncover the metrics that matter."
        ),

        (
            "02",
            "Predict",
            "Use machine learning and advanced analytics to anticipate outcomes."
        ),

        (
            "03",
            "Automate",
            "Convert insights into automated business workflows and decisions."
        ),
    ]


    for col, (
        num,
        title,
        text
    ) in zip(
        dark_cols,
        dark_features
    ):

        with col:

            html(
                f"""
<div class="dark-card">

    <div class="dark-label">
        {num}
    </div>

    <div class="dark-card-title">
        {title}
    </div>

    <div class="dark-card-text">
        {text}
    </div>

</div>
"""
            )


    # ========================================================
    # PROCESS
    # ========================================================

    html(
        """
<div class="section section-center">

    <div class="section-label">
        HOW IT WORKS
    </div>

    <div class="section-title">
        A Smarter Way to Solve Business Problems
    </div>

    <div class="section-description">

        A practical process designed to move from
        business problem to measurable solution.

    </div>

</div>
"""
    )


    process = [

        (
            "01",
            "Understand",
            "We understand your business process, goals and challenges."
        ),

        (
            "02",
            "Connect",
            "We connect databases, files, APIs and existing systems."
        ),

        (
            "03",
            "Analyze",
            "We transform data into meaningful KPIs and intelligence."
        ),

        (
            "04",
            "Predict",
            "AI and machine learning identify future opportunities and risks."
        ),

        (
            "05",
            "Automate",
            "We automate repetitive reporting and operational workflows."
        ),

        (
            "06",
            "Optimize",
            "Continuous insights help improve business performance."
        ),
    ]


    process_cols = st.columns(3)


    for i, (
        number,
        title,
        text
    ) in enumerate(process):

        with process_cols[i % 3]:

            html(
                f"""
<div class="process-card">

    <div class="process-number">
        STEP {number}
    </div>

    <div class="process-title">
        {title}
    </div>

    <div class="process-text">
        {text}
    </div>

</div>
"""
            )

        if (i + 1) % 3 == 0:

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


    # ========================================================
    # TECHNOLOGY
    # ========================================================

    html(
        """
<div class="section section-center">

    <div class="section-label">
        TECHNOLOGY
    </div>

    <div class="section-title">
        Built With Modern Data & AI Technologies
    </div>

</div>
"""
    )


    technologies = [

        "Python",
        "SQL",
        "Power BI",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "XGBoost",
        "Random Forest",
        "Prophet",
        "TensorFlow",
        "Keras",
        "PySpark",
        "REST APIs",
        "ETL",
        "Streamlit",
    ]


    html(
        '<div style="text-align:center;">'
        + "".join(
            f'<span class="tech-pill">{tech}</span>'
            for tech in technologies
        )
        + "</div>"
    )


    # ========================================================
    # CTA
    # ========================================================

    html(
        """
<div class="cta-section">

    <div class="cta-title">
        Ready to Make Your Data Intelligent?
    </div>

    <div class="cta-text">

        Tell us about your business problem and
        we'll help identify the right analytics,
        AI or automation solution.

    </div>

</div>
"""
    )


    if st.button(
        "🚀 Start Your Project",
        use_container_width=True,
        key="home_cta",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# SERVICES PAGE
# ============================================================

def services_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            JYORA AI SOLUTIONS
        </div>

        <div class="hero-title">
            Technology That
            <span>Works For You</span>
        </div>

        <div class="hero-description">

            Practical AI, analytics, BI and automation
            solutions designed around real business requirements.

        </div>

    </div>

</div>
"""
    )


    services = [

        (
            "🤖",
            "AI & Machine Learning",
            "Build prediction, classification, forecasting and intelligent decision models."
        ),

        (
            "📊",
            "Power BI & BI",
            "Create interactive dashboards, executive KPI systems and automated reporting."
        ),

        (
            "🔮",
            "Predictive Analytics",
            "Forecast demand, shipment delays, sales, customer behavior and operational risks."
        ),

        (
            "⚙️",
            "Automation & MIS",
            "Reduce manual work through automated reporting and business workflows."
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Build optimized queries, transformation pipelines and analytics datasets."
        ),

        (
            "🔗",
            "API & Integration",
            "Connect databases, APIs, JSON feeds, Excel and multiple business systems."
        ),
    ]


    cols = st.columns(3)


    for i, (
        icon,
        title,
        text
    ) in enumerate(services):

        with cols[i % 3]:

            html(
                f"""
<div class="feature-card">

    <div class="feature-icon">
        {icon}
    </div>

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {text}
    </div>

</div>
"""
            )

        if (i + 1) % 3 == 0:

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


    html(
        """
<div class="cta-section">

    <div class="cta-title">
        Have a Business Problem?
    </div>

    <div class="cta-text">
        Let's turn it into a data-driven solution.
    </div>

</div>
"""
    )


    if st.button(
        "🚀 Discuss Your Requirement",
        use_container_width=True,
        key="services_cta",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# PROJECTS PAGE
# ============================================================

def projects_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            USE CASES
        </div>

        <div class="hero-title">
            Real Problems.
            <span>Intelligent Solutions.</span>
        </div>

        <div class="hero-description">

            Examples of analytics, AI and automation
            solutions that can transform operational
            and business data.

        </div>

    </div>

</div>
"""
    )


    projects = [

        (
            "LOGISTICS",
            "Shipment Delay Prediction",
            "Use machine learning to identify shipments at risk of delay and improve proactive operational decisions."
        ),

        (
            "BUSINESS INTELLIGENCE",
            "Courier Hub Performance",
            "Monitor hub performance, SLA, TAT, shipment volume and delivery KPIs through interactive BI dashboards."
        ),

        (
            "FORECASTING",
            "Demand Forecasting",
            "Predict future demand using historical business data and time-series forecasting models."
        ),

        (
            "CUSTOMER ANALYTICS",
            "Customer Churn Prediction",
            "Identify customers with higher churn probability and enable proactive retention strategies."
        ),

        (
            "AUTOMATION",
            "Automated MIS Reporting",
            "Replace repetitive manual reporting with automated data extraction, transformation and distribution."
        ),

        (
            "DATA ENGINEERING",
            "Analytics Data Pipeline",
            "Combine SQL databases, APIs, Excel and operational systems into a reliable reporting dataset."
        ),
    ]


    cols = st.columns(2)


    for i, (
        tag,
        title,
        text
    ) in enumerate(projects):

        with cols[i % 2]:

            html(
                f"""
<div class="project-card">

    <div class="project-tag">
        {tag}
    </div>

    <div class="project-title">
        {title}
    </div>

    <div class="project-text">
        {text}
    </div>

</div>
"""
            )

        if (i + 1) % 2 == 0:

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )


    html(
        """
<div class="cta-section">

    <div class="cta-title">
        Your Business Could Be Next
    </div>

    <div class="cta-text">

        Share your current process, data source
        and business challenge.

    </div>

</div>
"""
    )


    if st.button(
        "🚀 Start a Project",
        use_container_width=True,
        key="projects_cta",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# REQUEST PROJECT
# ============================================================

def request_project_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            START A PROJECT
        </div>

        <div class="hero-title">
            Let's Build Something
            <span>Intelligent</span>
        </div>

        <div class="hero-description">

            Tell us about your business requirement and
            we'll help identify the right AI, analytics,
            BI or automation solution.

        </div>

    </div>

</div>
"""
    )


    html(
        """
<div class="form-container">

    <div class="section-label">
        PROJECT INFORMATION
    </div>

</div>
"""
    )


    col1, col2 = st.columns(2)


    with col1:

        company = st.text_input(
            "Company Name",
            placeholder="Your company name",
            key="company_form",
        )

        contact = st.text_input(
            "Contact Person *",
            placeholder="Your name",
            key="contact_form",
        )

        email = st.text_input(
            "Business Email *",
            placeholder="name@company.com",
            key="email_form",
        )

        phone = st.text_input(
            "Phone / WhatsApp",
            placeholder="+91 XXXXX XXXXX",
            key="phone_form",
        )


    with col2:

        service = st.selectbox(
            "Required Solution",
            [
                "AI / Machine Learning",
                "Power BI Dashboard",
                "Logistics Analytics",
                "Predictive Analytics",
                "Automation / MIS",
                "SQL / Data Engineering",
                "API / Data Integration",
                "Not Sure",
            ],
            key="service_form",
        )


        data_source = st.selectbox(
            "Current Data Source",
            [
                "MySQL / SQL Database",
                "Excel / CSV",
                "API / JSON",
                "Power BI",
                "Multiple Sources",
                "Not Sure",
            ],
            key="data_source_form",
        )


        timeline = st.selectbox(
            "Expected Timeline",
            [
                "Within 1 Week",
                "1–2 Weeks",
                "2–4 Weeks",
                "1–2 Months",
                "Flexible",
            ],
            key="timeline_form",
        )


    requirement = st.text_area(
        "Requirement *",
        placeholder=(
            "Describe your business problem, "
            "current process, data available and expected solution..."
        ),
        height=160,
        key="requirement_form",
    )


    if st.button(
        "🚀 Submit Project Request",
        use_container_width=True,
        key="submit_project_request",
    ):

        if not contact.strip():

            st.error(
                "Please enter your contact name."
            )

        elif not email.strip():

            st.error(
                "Please enter your business email."
            )

        elif not valid_email(email):

            st.error(
                "Please enter a valid email address."
            )

        elif not requirement.strip():

            st.error(
                "Please describe your requirement."
            )

        else:

            payload = {

                "Date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                "Company": company.strip(),

                "Contact": contact.strip(),

                "Email": email.strip(),

                "Phone": phone.strip(),

                "Service": service,

                "Data_Source": data_source,

                "Timeline": timeline,

                "Requirement": requirement.strip(),

                "Source": "JYORA AI Website",
            }


            if submit_to_google(payload):

                st.success(
                    "✅ Thank you! Your project request has been submitted successfully."
                )

            else:

                st.error(
                    "Unable to submit your request. "
                    "Please try again later."
                )


# ============================================================
# ABOUT
# ============================================================

def about_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            ABOUT JYORA AI
        </div>

        <div class="hero-title">
            Making Business Data
            <span>More Intelligent</span>
        </div>

        <div class="hero-description">

            JYORA AI focuses on practical Artificial Intelligence,
            Business Intelligence, Data Analytics and Automation
            solutions that help businesses make faster and better decisions.

        </div>

    </div>

</div>
"""
    )


    cols = st.columns(3)


    about_items = [

        (
            "🎯",
            "Our Mission",
            "Turn complex business data into clear, actionable intelligence."
        ),

        (
            "💡",
            "Our Approach",
            "Combine business understanding with modern data and AI technologies."
        ),

        (
            "🚀",
            "Our Vision",
            "Help businesses become more intelligent, automated and data-driven."
        ),
    ]


    for col, (
        icon,
        title,
        text
    ) in zip(
        cols,
        about_items
    ):

        with col:

            html(
                f"""
<div class="feature-card">

    <div class="feature-icon">
        {icon}
    </div>

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {text}
    </div>

</div>
"""
            )


# ============================================================
# CONTACT
# ============================================================

def contact_page():

    html(
        """
<div class="hero-section">

    <div class="hero-content">

        <div class="hero-badge">
            CONTACT JYORA AI
        </div>

        <div class="hero-title">
            Let's Talk About
            <span>Your Data</span>
        </div>

        <div class="hero-description">

            Have a dashboard requirement, AI idea,
            automation challenge or data problem?

            Let's discuss it.

        </div>

    </div>

</div>
"""
    )


    cols = st.columns(3)


    contact_items = [

        (
            "📧",
            "Email",
            "support@logiintelli.com"
        ),

        (
            "📱",
            "WhatsApp",
            "+91 8825674102"
        ),

        (
            "🕘",
            "Business Hours",
            "Monday – Friday | 9 AM – 6 PM IST"
        ),
    ]


    for col, (
        icon,
        title,
        text
    ) in zip(
        cols,
        contact_items
    ):

        with col:

            html(
                f"""
<div class="feature-card">

    <div class="feature-icon">
        {icon}
    </div>

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {text}
    </div>

</div>
"""
            )


    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )


    if st.button(
        "🚀 Start a Project",
        use_container_width=True,
        key="contact_project",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# PAGE ROUTER
# ============================================================

if st.session_state.page == "Home":

    home_page()

elif st.session_state.page == "Services":

    services_page()

elif st.session_state.page == "Projects":

    projects_page()

elif st.session_state.page == "Request Project":

    request_project_page()

elif st.session_state.page == "About":

    about_page()

elif st.session_state.page == "Contact":

    contact_page()


# ============================================================
# JYORA AI CHATBOT
# ============================================================

if st.session_state.chat_open:

    with st.container(
        key="floating_chatbot"
    ):

        # ====================================================
        # CHAT HEADER
        # ====================================================
        # IMPORTANT:
        # Do NOT put this inside st.columns().
        # ====================================================

        st.markdown(
            """
<div class="jyora-chat-header">

    <div class="jyora-chat-title">
        🤖 JYORA AI Assistant
    </div>

    <div class="jyora-chat-subtitle">
        AI & Project Consultation
    </div>

</div>
""",
            unsafe_allow_html=True,
        )


        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        with st.container(
            key="chat_close_btn"
        ):

            if st.button(
                "✕",
                key="btn_close_chat",
                help="Close JYORA AI Assistant",
            ):

                st.session_state.chat_open = False

                st.session_state.chat_step = 0

                st.session_state.chat_data = {}

                st.session_state.chat_messages = [

                    {
                        "role": "assistant",

                        "text": (
                            "👋 Welcome to JYORA AI.\n"
                            "Let's understand your business requirement."
                        ),
                    }

                ]

                st.rerun()


        # ====================================================
        # CHAT HISTORY
        # ====================================================

        st.markdown(
            '<div class="chat-body">',
            unsafe_allow_html=True,
        )


        for msg in st.session_state.chat_messages:

            role_class = (

                "chat-assistant"

                if msg["role"] == "assistant"

                else "chat-user"
            )


            safe_text = (
                msg["text"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )


            safe_text = safe_text.replace(
                "\n",
                "<br>"
            )


            st.markdown(
                f"""
<div class="chat-message {role_class}">
    {safe_text}
</div>
""",
                unsafe_allow_html=True,
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


        # ====================================================
        # STEP 0 — NAME
        # ====================================================

        if st.session_state.chat_step == 0:

            with st.form(
                key="chat_step_0",
                clear_on_submit=True,
            ):

                user_name = st.text_input(
                    "Your Name",
                    placeholder="Type your name...",
                    key="input_chat_name",
                )


                if st.form_submit_button(
                    "Next ➔",
                    use_container_width=True,
                ):

                    if user_name.strip():

                        name = user_name.strip()


                        st.session_state.chat_data[
                            "Contact"
                        ] = name


                        st.session_state.chat_messages.append(
                            {
                                "role": "user",
                                "text": name,
                            }
                        )


                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "text": (
                                    f"Nice to meet you, {name}!\n"
                                    "What solution are you looking for?"
                                ),
                            }
                        )


                        st.session_state.chat_step = 1

                        st.rerun()

                    else:

                        st.error(
                            "Please enter your name."
                        )


        # ====================================================
        # STEP 1 — SERVICE
        # ====================================================

        elif st.session_state.chat_step == 1:

            service_options = [

                "🤖 AI / Machine Learning",

                "📊 Power BI Dashboard",

                "🚚 Logistics Analytics",

                "🔮 Predictive Analytics",

                "⚙️ Automation / MIS",

                "🗄️ SQL / Data Engineering",

                "💡 Not Sure",
            ]


            for index, option in enumerate(
                service_options
            ):

                if st.button(
                    option,
                    key=f"chat_service_{index}",
                    use_container_width=True,
                ):

                    clean_option = option


                    if " " in option:

                        clean_option = option.split(
                            " ",
                            1
                        )[1]


                    st.session_state.chat_data[
                        "Service"
                    ] = clean_option


                    st.session_state.chat_messages.append(
                        {
                            "role": "user",
                            "text": option,
                        }
                    )


                    st.session_state.chat_messages.append(
                        {
                            "role": "assistant",
                            "text": (
                                "Great. What is your business email?"
                            ),
                        }
                    )


                    st.session_state.chat_step = 2

                    st.rerun()


        # ====================================================
        # STEP 2 — EMAIL
        # ====================================================

        elif st.session_state.chat_step == 2:

            with st.form(
                key="chat_step_2",
                clear_on_submit=True,
            ):

                user_email = st.text_input(
                    "Business Email",
                    placeholder="name@company.com",
                    key="input_chat_email",
                )


                if st.form_submit_button(
                    "Next ➔",
                    use_container_width=True,
                ):

                    if valid_email(user_email):

                        email = user_email.strip()


                        st.session_state.chat_data[
                            "Email"
                        ] = email


                        st.session_state.chat_messages.append(
                            {
                                "role": "user",
                                "text": email,
                            }
                        )


                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "text": (
                                    "Thanks!\n"
                                    "What is your Phone / WhatsApp number?"
                                ),
                            }
                        )


                        st.session_state.chat_step = 3

                        st.rerun()

                    else:

                        st.error(
                            "Please enter a valid email."
                        )


        # ====================================================
        # STEP 3 — PHONE
        # ====================================================

        elif st.session_state.chat_step == 3:

            with st.form(
                key="chat_step_3",
                clear_on_submit=True,
            ):

                user_phone = st.text_input(
                    "Phone / WhatsApp",
                    placeholder="+91 XXXXX XXXXX",
                    key="input_chat_phone",
                )


                if st.form_submit_button(
                    "Next ➔",
                    use_container_width=True,
                ):

                    if user_phone.strip():

                        phone = user_phone.strip()


                        st.session_state.chat_data[
                            "Phone"
                        ] = phone


                        st.session_state.chat_messages.append(
                            {
                                "role": "user",
                                "text": phone,
                            }
                        )


                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "text": (
                                    "Almost done!\n"
                                    "Tell us about your business requirement."
                                ),
                            }
                        )


                        st.session_state.chat_step = 4

                        st.rerun()

                    else:

                        st.error(
                            "Please enter your phone number."
                        )


        # ====================================================
        # STEP 4 — REQUIREMENT
        # ====================================================

        elif st.session_state.chat_step == 4:

            with st.form(
                key="chat_step_4",
                clear_on_submit=True,
            ):

                user_req = st.text_area(
                    "Requirement",
                    placeholder=(
                        "Example: I need a Power BI dashboard "
                        "for shipment tracking..."
                    ),
                    key="input_chat_req",
                    height=90,
                )


                if st.form_submit_button(
                    "Submit Request 🚀",
                    use_container_width=True,
                ):

                    if user_req.strip():

                        requirement = user_req.strip()


                        st.session_state.chat_data[
                            "Requirement"
                        ] = requirement


                        st.session_state.chat_messages.append(
                            {
                                "role": "user",
                                "text": requirement,
                            }
                        )


                        payload = {

                            "Date": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                            "Company": "",

                            "Contact": (
                                st.session_state.chat_data.get(
                                    "Contact",
                                    "",
                                )
                            ),

                            "Email": (
                                st.session_state.chat_data.get(
                                    "Email",
                                    "",
                                )
                            ),

                            "Phone": (
                                st.session_state.chat_data.get(
                                    "Phone",
                                    "",
                                )
                            ),

                            "Service": (
                                st.session_state.chat_data.get(
                                    "Service",
                                    "",
                                )
                            ),

                            "Data_Source": "Chatbot Input",

                            "Timeline": "Flexible",

                            "Requirement": requirement,

                            "Source": "JYORA AI Assistant",
                        }


                        submit_to_google(payload)


                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "text": (
                                    "✅ Thank you!\n"
                                    "Your request has been received.\n\n"
                                    "The JYORA AI team will "
                                    "contact you shortly."
                                ),
                            }
                        )


                        st.session_state.chat_step = 5

                        st.rerun()

                    else:

                        st.error(
                            "Please describe your requirement."
                        )


        # ====================================================
        # STEP 5 — COMPLETE
        # ====================================================

        elif st.session_state.chat_step == 5:

            st.markdown(
                """
<div style="
    text-align:center;
    padding:10px;
    color:#64748B;
    font-size:10px;
">
    Thank you for contacting JYORA AI.
</div>
""",
                unsafe_allow_html=True,
            )


# ============================================================
# REOPEN CHAT
# ============================================================

else:

    with st.container(
        key="open_chat_container"
    ):

        if st.button(
            "💬",
            key="btn_reopen_chat",
            help="Open JYORA AI Assistant",
        ):

            st.session_state.chat_open = True

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

html(
    """
<div class="footer">

    <div class="footer-brand">

        JYORA
        <span class="footer-ai">
            AI
        </span>

    </div>

    <div>
        AI • Data Analytics • Business Intelligence • Automation
    </div>

    <div style="margin-top:8px;">
        Turning Business Data Into Intelligent Decisions
    </div>

    <div style="margin-top:12px;">
        © 2026 JYORA AI. All rights reserved.
    </div>

</div>
"""
)
