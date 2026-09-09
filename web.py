import json
import re
from datetime import datetime

import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LogiIntelli | Logistics Analytics, AI & BI",
    page_icon="🚚",
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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli.<br><br>"
                "I'm your AI & Project Consultation Assistant.<br><br>"
                "How can I help you today?"
            ),
        }
    ]


# ============================================================
# HTML HELPER
# ============================================================

def render_html(content):
    st.markdown(content, unsafe_allow_html=True)


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
<style>

/* ============================================================
   BASIC PAGE
============================================================ */

html,
body,
.stApp {
    font-family: Arial, Helvetica, sans-serif !important;
}

.stApp {
    background: #f8fafc !important;
}

.block-container {
    max-width: 1380px !important;
    padding-top: 1rem !important;
    padding-bottom: 70px !important;
}


/* ============================================================
   HIDE STREAMLIT DEFAULT UI
============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}


/* ============================================================
   HEADER
============================================================ */

.logi-header {
    padding: 12px 0 18px 0;
    margin-bottom: 18px;
    border-bottom: 1px solid #e2e8f0;
}

.logi-brand {
    color: #0f172a;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1.5px;
}

.logi-brand-blue {
    color: #2563eb;
}

.logi-subtitle {
    margin-top: 7px;
    color: #64748b;
    font-size: 11px;
    font-weight: 500;
}


/* ============================================================
   NAVIGATION
============================================================ */

div[data-testid="stButton"] > button {
    min-height: 40px !important;
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    background: #ffffff !important;
    color: #334155 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #2563eb !important;
    background: #eff6ff !important;
    color: #2563eb !important;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    margin-bottom: 35px;
    padding: 70px 20px 65px 20px;
    text-align: center;
    border-radius: 25px;
    background:
        radial-gradient(
            circle at top center,
            #dbeafe 0%,
            #f8fafc 50%,
            #f8fafc 100%
        );
}

.hero-badge {
    display: inline-block;
    margin-bottom: 20px;
    padding: 8px 16px;
    border: 1px solid #bfdbfe;
    border-radius: 30px;
    background: #eff6ff;
    color: #2563eb;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.7px;
}

.hero-title {
    max-width: 950px;
    margin: auto;
    color: #0f172a;
    font-size: 54px;
    line-height: 1.08;
    font-weight: 900;
    letter-spacing: -2.5px;
}

.hero-blue {
    color: #2563eb;
}

.hero-description {
    max-width: 760px;
    margin: 22px auto 0 auto;
    color: #64748b;
    font-size: 16px;
    line-height: 1.7;
}


/* ============================================================
   SECTIONS
============================================================ */

.section-title {
    margin-top: 35px;
    margin-bottom: 8px;
    color: #0f172a;
    font-size: 30px;
    font-weight: 850;
}

.section-description {
    margin-bottom: 25px;
    color: #64748b;
    font-size: 14px;
    line-height: 1.6;
}


/* ============================================================
   CARDS
============================================================ */

.info-card {
    min-height: 175px;
    margin-bottom: 18px;
    padding: 25px;
    box-sizing: border-box;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.04);
}

.info-card:hover {
    border-color: #bfdbfe;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
}

.card-icon {
    margin-bottom: 13px;
    font-size: 30px;
}

.card-title {
    margin-bottom: 8px;
    color: #0f172a;
    font-size: 17px;
    font-weight: 800;
}

.card-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.7;
}


/* ============================================================
   METRICS
============================================================ */

.metric-card {
    padding: 23px 10px;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.035);
}

.metric-value {
    color: #2563eb;
    font-size: 31px;
    font-weight: 900;
}

.metric-label {
    margin-top: 5px;
    color: #64748b;
    font-size: 11px;
}


/* ============================================================
   PROJECT
============================================================ */

.project-card {
    min-height: 205px;
    margin-bottom: 18px;
    padding: 25px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.04);
}

.project-icon {
    margin-bottom: 8px;
    font-size: 28px;
}

.project-category {
    margin-bottom: 8px;
    color: #2563eb;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.project-title {
    margin-bottom: 8px;
    color: #0f172a;
    font-size: 18px;
    font-weight: 800;
}

.project-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.7;
}


/* ============================================================
   TECHNOLOGY
============================================================ */

.tech-card {
    padding: 15px 8px;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    color: #0f172a;
    font-size: 13px;
    font-weight: 700;
}


/* ============================================================
   CONTACT
============================================================ */

.contact-card {
    min-height: 165px;
    padding: 28px;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.04);
}

.contact-icon {
    margin-bottom: 12px;
    font-size: 30px;
}

.contact-title {
    margin-bottom: 7px;
    color: #0f172a;
    font-size: 16px;
    font-weight: 800;
}

.contact-value {
    color: #64748b;
    font-size: 13px;
    line-height: 1.6;
}


/* ============================================================
   CTA
============================================================ */

.cta {
    margin-top: 45px;
    margin-bottom: 30px;
    padding: 50px 25px;
    text-align: center;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a, #1e40af);
    color: white;
}

.cta-title {
    margin-bottom: 10px;
    font-size: 31px;
    font-weight: 900;
}

.cta-description {
    max-width: 650px;
    margin: auto;
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.7;
}


/* ============================================================
   FOOTER
============================================================ */

.site-footer {
    margin-top: 60px;
    padding: 25px 0;
    border-top: 1px solid #e2e8f0;
    text-align: center;
    color: #64748b;
    font-size: 11px;
}


/* ============================================================
   CHATBOT
============================================================ */

/*
    IMPORTANT:

    The chatbot is positioned with fixed CSS.

    It is NOT a Streamlit container.

    Therefore it does not consume page space and does not
    collapse the Home page.
*/


.logi-chat-area {
    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    z-index: 999999 !important;

    width: 330px !important;

    max-width: calc(100vw - 40px) !important;

    pointer-events: none !important;
}


/* ============================================================
   CHAT WINDOW
============================================================ */

.logi-chat-box {
    width: 330px;
    max-width: 100%;

    overflow: hidden;

    margin-bottom: 10px;

    background: #ffffff;

    border: 1px solid #dbe3ec;

    border-radius: 18px;

    box-shadow:
        0 18px 55px rgba(15, 23, 42, 0.25);

    pointer-events: auto;
}


/* ============================================================
   CHAT HEADER
============================================================ */

.logi-chat-header {
    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 14px 15px;

    background:
        linear-gradient(
            135deg,
            #0f172a,
            #2563eb
        );

    color: white;
}

.logi-chat-header-left {
    display: flex;

    align-items: center;

    gap: 10px;
}

.logi-chat-avatar {
    display: flex;

    align-items: center;

    justify-content: center;

    width: 35px;

    height: 35px;

    border-radius: 50%;

    background: rgba(255,255,255,0.16);

    font-size: 18px;
}

.logi-chat-name {
    font-size: 13px;

    font-weight: 800;
}

.logi-chat-status {
    margin-top: 2px;

    color: #bfdbfe;

    font-size: 9px;
}

.logi-chat-close-button {
    width: 30px !important;

    height: 30px !important;

    min-height: 30px !important;

    padding: 0 !important;

    border: 0 !important;

    border-radius: 50% !important;

    background: rgba(255,255,255,0.15) !important;

    color: white !important;

    font-size: 14px !important;
}

.logi-chat-close-button:hover {
    background: rgba(255,255,255,0.30) !important;

    color: white !important;
}


/* ============================================================
   CHAT BODY
============================================================ */

.logi-chat-body {
    max-height: 285px;

    overflow-y: auto;

    padding: 13px;

    background: #f8fafc;
}


/* ============================================================
   MESSAGES
============================================================ */

.logi-chat-message {
    max-width: 90%;

    margin-bottom: 9px;

    padding: 9px 11px;

    border-radius: 11px;

    font-size: 10px;

    line-height: 1.55;
}

.logi-chat-bot-message {
    margin-right: 20px;

    color: #1e3a8a;

    background: #eff6ff;

    border: 1px solid #dbeafe;
}

.logi-chat-user-message {
    margin-left: 20px;

    color: white;

    background: #0f172a;
}


/* ============================================================
   QUICK OPTIONS
============================================================ */

.logi-chat-options-title {
    padding: 10px 12px 5px 12px;

    color: #64748b;

    background: #ffffff;

    font-size: 9px;

    font-weight: 700;
}

.logi-chat-option-button {
    width: 100% !important;

    min-height: 34px !important;

    margin-bottom: 5px !important;

    padding: 6px 8px !important;

    border-radius: 8px !important;

    background: #ffffff !important;

    border: 1px solid #dbe3ec !important;

    color: #334155 !important;

    font-size: 10px !important;

    font-weight: 600 !important;
}

.logi-chat-option-button:hover {
    background: #eff6ff !important;

    border-color: #2563eb !important;

    color: #2563eb !important;
}


/* ============================================================
   CHAT INPUT
============================================================ */

.logi-chat-input-label {
    padding: 5px 12px;

    color: #64748b;

    background: #ffffff;

    font-size: 9px;
}


/* ============================================================
   CHAT LAUNCHER
============================================================ */

.logi-chat-launcher-area {
    display: flex;

    align-items: center;

    gap: 10px;

    pointer-events: auto;
}

.logi-chat-launcher-text {
    padding: 7px 10px;

    border-radius: 10px;

    background: #0f172a;

    color: white;

    font-size: 10px;

    font-weight: 600;

    box-shadow:
        0 5px 15px rgba(15,23,42,0.15);
}

.logi-chat-open-button {
    width: 60px !important;

    height: 60px !important;

    min-height: 60px !important;

    padding: 0 !important;

    border: 0 !important;

    border-radius: 50% !important;

    background:
        linear-gradient(
            135deg,
            #0f172a,
            #2563eb
        ) !important;

    color: white !important;

    font-size: 24px !important;

    box-shadow:
        0 12px 30px rgba(15,23,42,0.28) !important;
}

.logi-chat-open-button:hover {
    background:
        linear-gradient(
            135deg,
            #1e293b,
            #1d4ed8
        ) !important;

    color: white !important;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 600px) {

    .hero {
        padding: 45px 15px;
    }

    .hero-title {
        font-size: 38px;
        letter-spacing: -1.5px;
    }

    .logi-chat-area {
        left: 10px !important;

        bottom: 10px !important;

        width: 300px !important;

        max-width: calc(100vw - 20px) !important;
    }

    .logi-chat-box {
        width: 300px;
    }

    .logi-chat-launcher-text {
        display: none;
    }
}

</style>
"""
)


# ============================================================
# HEADER
# ============================================================

render_html(
    """
<div class="logi-header">

    <div class="logi-brand">
        🚚 Logi<span class="logi-brand-blue">Intelli</span>
    </div>

    <div class="logi-subtitle">
        Logistics Analytics • AI & Predictive Intelligence • BI Automation
    </div>

</div>
"""
)


# ============================================================
# NAVIGATION
# ============================================================

nav_items = [
    ("🏠 Home", "Home"),
    ("🛠️ Services", "Services"),
    ("📊 Projects", "Projects"),
    ("📝 Request Project", "Request Project"),
    ("👤 About", "About"),
    ("📞 Contact", "Contact"),
]

nav_cols = st.columns(6)

for index, (label, page_name) in enumerate(nav_items):

    with nav_cols[index]:

        if st.button(
            label,
            key=f"navigation_{index}",
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()


# ============================================================
# CHATBOT FUNCTIONS
# ============================================================

def add_chat_message(role, text):

    st.session_state.chat_messages.append(
        {
            "role": role,
            "text": text,
        }
    )


def chatbot_reply(option):

    replies = {

        "Power BI Dashboard":
            (
                "📊 <b>Power BI</b> is a great choice.<br><br>"
                "We can help with dashboards, KPI reporting, "
                "DAX, Power Query, data modelling and automated "
                "business reporting."
            ),

        "Logistics Analytics":
            (
                "🚚 We can help with <b>Logistics Analytics</b> "
                "including shipment tracking, SLA, TAT, hub "
                "performance, delivery analytics and exception reporting."
            ),

        "AI / Machine Learning":
            (
                "🤖 We can build <b>AI & Machine Learning</b> "
                "solutions such as demand forecasting, shipment "
                "delay prediction, churn prediction and predictive analytics."
            ),

        "Automation / MIS":
            (
                "⚙️ We can automate <b>MIS and reporting</b> "
                "using Python, SQL, Excel, APIs and scheduled workflows."
            ),

        "SQL / Data Engineering":
            (
                "🗄️ We can help with <b>SQL & Data Engineering</b>, "
                "ETL, database optimization, data transformation "
                "and reporting datasets."
            ),

        "Project Consultation":
            (
                "💡 No problem. Tell us about your business problem, "
                "current data source and expected outcome. "
                "We can help identify the right solution."
            ),
    }

    return replies.get(
        option,
        (
            "Thanks for your message! 😊 "
            "Please describe your requirement and "
            "we will help you identify the right solution."
        ),
    )


def select_chat_option(option):

    add_chat_message(
        "user",
        option,
    )

    add_chat_message(
        "assistant",
        chatbot_reply(option),
    )


# ============================================================
# CHATBOT UI
# ============================================================

def show_chatbot():

    render_html(
        '<div class="logi-chat-area">'
    )


    # ========================================================
    # OPEN CHAT
    # ========================================================

    if not st.session_state.chat_open:

        render_html(
            """
<div class="logi-chat-launcher-area">

    <div class="logi-chat-launcher-text">
        Need help? Chat with us
    </div>

</div>
"""
        )

        if st.button(
            "💬",
            key="open_logi_chat",
            help="Open LogiIntelli AI Assistant",
        ):

            st.session_state.chat_open = True

            st.rerun()


    # ========================================================
    # CHAT OPEN
    # ========================================================

    else:

        render_html(
            """
<div class="logi-chat-box">

    <div class="logi-chat-header">

        <div class="logi-chat-header-left">

            <div class="logi-chat-avatar">
                🤖
            </div>

            <div>

                <div class="logi-chat-name">
                    LogiIntelli AI Assistant
                </div>

                <div class="logi-chat-status">
                    ● Online • AI & Project Consultation
                </div>

            </div>

        </div>

    </div>

    <div class="logi-chat-body">
"""
        )


        # ----------------------------------------------------
        # MESSAGES
        # ----------------------------------------------------

        for message in st.session_state.chat_messages:

            role = message["role"]

            if role == "assistant":

                render_html(
                    f"""
<div class="logi-chat-message logi-chat-bot-message">
    {message["text"]}
</div>
"""
                )

            else:

                render_html(
                    f"""
<div class="logi-chat-message logi-chat-user-message">
    {message["text"]}
</div>
"""
                )


        render_html(
            """
    </div>

</div>
"""
        )


        # ----------------------------------------------------
        # OPTIONS
        # ----------------------------------------------------

        render_html(
            """
<div style="
    width:330px;
    max-width:100%;
    padding:8px 10px 3px 10px;
    background:#ffffff;
    border-left:1px solid #dbe3ec;
    border-right:1px solid #dbe3ec;
">

    <div class="logi-chat-options-title">
        QUICK OPTIONS
    </div>

</div>
"""
        )


        option_cols = st.columns(2)


        options = [
            ("📊 Power BI", "Power BI Dashboard"),
            ("🚚 Logistics", "Logistics Analytics"),
            ("🤖 AI / ML", "AI / Machine Learning"),
            ("⚙️ Automation", "Automation / MIS"),
            ("🗄️ SQL", "SQL / Data Engineering"),
            ("💡 Consultation", "Project Consultation"),
        ]


        for index, (
            button_text,
            option_value
        ) in enumerate(options):

            with option_cols[index % 2]:

                if st.button(
                    button_text,
                    key=f"chat_option_{index}",
                    use_container_width=True,
                ):

                    select_chat_option(
                        option_value
                    )

                    st.rerun()


        # ----------------------------------------------------
        # CONTACT BUTTONS
        # ----------------------------------------------------

        render_html(
            """
<div style="
    width:330px;
    max-width:100%;
    padding:4px 10px;
    background:#ffffff;
    border-left:1px solid #dbe3ec;
    border-right:1px solid #dbe3ec;
">

    <div style="
        padding:5px 2px;
        color:#64748b;
        font-size:9px;
    ">
        Need a detailed discussion?
    </div>

</div>
"""
        )


        contact_cols = st.columns(2)


        with contact_cols[0]:

            if st.button(
                "📝 Request Project",
                key="chat_request_project",
                use_container_width=True,
            ):

                st.session_state.page = "Request Project"

                st.session_state.chat_open = False

                st.rerun()


        with contact_cols[1]:

            if st.button(
                "✉️ Email",
                key="chat_email",
                use_container_width=True,
            ):

                add_chat_message(
                    "user",
                    "I want to contact LogiIntelli.",
                )

                add_chat_message(
                    "assistant",
                    (
                        "📧 You can contact us at "
                        "<b>support@logiintelli.com</b>."
                    ),
                )

                st.rerun()


        # ----------------------------------------------------
        # CLOSE BUTTON
        # ----------------------------------------------------

        if st.button(
            "✕  Close Chat",
            key="close_logi_chat",
            use_container_width=True,
        ):

            st.session_state.chat_open = False

            st.rerun()


    render_html(
        "</div>"
    )


# ============================================================
# HOME
# ============================================================

def show_home():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        🚚 LOGISTICS • DATA • AI • BUSINESS INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn Your Business Data Into
        <span class="hero-blue">
            Intelligent Decisions
        </span>
    </div>

    <div class="hero-description">
        LogiIntelli helps businesses transform operational data
        into powerful dashboards, predictive models,
        automation solutions and actionable business intelligence.
    </div>

</div>
"""
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

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

            render_html(
                f"""
<div class="metric-card">

    <div class="metric-value">
        {value}
    </div>

    <div class="metric-label">
        {label}
    </div>

</div>
"""
            )


    # --------------------------------------------------------
    # SERVICES
    # --------------------------------------------------------

    render_html(
        """
<div class="section-title">
    What We Do
</div>

<div class="section-description">
    End-to-end analytics and technology solutions designed
    for operational efficiency and business growth.
</div>
"""
    )


    services = [

        (
            "📊",
            "Power BI & Business Intelligence",
            "Interactive dashboards, KPI monitoring, DAX, Power Query and executive reporting.",
        ),

        (
            "🚚",
            "Logistics Analytics",
            "Shipment analytics, hub performance, SLA, TAT, delivery and operational intelligence.",
        ),

        (
            "🤖",
            "AI & Machine Learning",
            "Forecasting, prediction, classification, churn models and intelligent decision systems.",
        ),

        (
            "⚙️",
            "Automation & MIS",
            "Automate repetitive reports, Excel workflows, Python processes and operational MIS.",
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL, ETL, data transformation and reporting datasets.",
        ),

        (
            "🔗",
            "API & Data Integration",
            "Connect APIs, databases, JSON feeds and multiple data sources.",
        ),
    ]


    service_cols = st.columns(3)


    for index, (
        icon,
        title,
        description
    ) in enumerate(services):

        with service_cols[index % 3]:

            render_html(
                f"""
<div class="info-card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-description">
        {description}
    </div>

</div>
"""
            )


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    render_html(
        """
<div class="section-title">
    How We Work
</div>

<div class="section-description">
    A simple process from business requirement to deployment.
</div>
"""
    )


    workflow = [

        (
            "01",
            "Understand",
            "Understand the business problem and objectives.",
        ),

        (
            "02",
            "Analyze",
            "Study data sources and identify opportunities.",
        ),

        (
            "03",
            "Build",
            "Develop dashboards, models and automation.",
        ),

        (
            "04",
            "Deliver",
            "Deploy the solution and provide actionable insights.",
        ),
    ]


    workflow_cols = st.columns(4)


    for col, (
        number,
        title,
        description
    ) in zip(
        workflow_cols,
        workflow
    ):

        with col:

            render_html(
                f"""
<div class="info-card">

    <div style="
        color:#2563eb;
        font-size:12px;
        font-weight:900;
        margin-bottom:10px;
    ">
        {number}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-description">
        {description}
    </div>

</div>
"""
            )


    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    render_html(
        """
<div class="section-title">
    Technology Stack
</div>

<div class="section-description">
    Modern tools for analytics, AI and data engineering.
</div>
"""
    )


    technologies = [
        "SQL",
        "Python",
        "Power BI",
        "Tableau",
        "PySpark",
        "Machine Learning",
    ]


    technology_cols = st.columns(6)


    for col, technology in zip(
        technology_cols,
        technologies
    ):

        with col:

            render_html(
                f"""
<div class="tech-card">
    {technology}
</div>
"""
            )


    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

    render_html(
        """
<div class="cta">

    <div class="cta-title">
        Have a Business Problem?
    </div>

    <div class="cta-description">
        Let's convert your data into dashboards,
        automation and intelligent business solutions.
    </div>

</div>
"""
    )


    if st.button(
        "🚀 Start Your Project",
        key="home_project_button",
        use_container_width=True,
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# SERVICES
# ============================================================

def show_services():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        OUR SERVICES
    </div>

    <div class="hero-title">
        Analytics & Technology
        <span class="hero-blue">
            Solutions
        </span>
    </div>

    <div class="hero-description">
        Practical analytics, AI, BI and automation solutions
        built around your business requirements.
    </div>

</div>
"""
    )


    services = [

        (
            "📊",
            "Power BI & Business Intelligence",
            "Executive dashboards<br>"
            "Operational dashboards<br>"
            "KPI tracking<br>"
            "DAX<br>"
            "Power Query<br>"
            "Automated reporting",
        ),

        (
            "🚚",
            "Logistics Analytics",
            "Shipment tracking<br>"
            "Hub performance<br>"
            "SLA analytics<br>"
            "TAT analysis<br>"
            "Delivery performance<br>"
            "Exception analytics",
        ),

        (
            "🤖",
            "AI & Machine Learning",
            "Demand forecasting<br>"
            "Delay prediction<br>"
            "Customer churn<br>"
            "Sales forecasting<br>"
            "Classification<br>"
            "Predictive analytics",
        ),

        (
            "⚙️",
            "Automation & MIS",
            "Automated MIS<br>"
            "Excel automation<br>"
            "Python automation<br>"
            "Scheduled reporting<br>"
            "Data refresh<br>"
            "Operational workflows",
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL<br>"
            "Data modelling<br>"
            "ETL pipelines<br>"
            "Data transformation<br>"
            "Database optimization<br>"
            "Reporting datasets",
        ),

        (
            "🔗",
            "API & Data Integration",
            "REST API integration<br>"
            "JSON processing<br>"
            "Database integration<br>"
            "Multi-source analytics<br>"
            "Automated ingestion<br>"
            "Data pipelines",
        ),
    ]


    cols = st.columns(2)


    for index, (
        icon,
        title,
        description
    ) in enumerate(services):

        with cols[index % 2]:

            render_html(
                f"""
<div class="info-card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-description">
        {description}
    </div>

</div>
"""
            )


# ============================================================
# PROJECTS
# ============================================================

def show_projects():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        PROJECTS & SOLUTIONS
    </div>

    <div class="hero-title">
        Real Business Problems.
        <span class="hero-blue">
            Data-Driven Solutions.
        </span>
    </div>

    <div class="hero-description">
        Analytics, AI and automation solutions designed
        for real-world operational businesses.
    </div>

</div>
"""
    )


    projects = [

        (
            "🚚",
            "Courier Hub Performance & SLA Optimization",
            "Logistics Analytics",
            "Power BI dashboards to monitor hub performance, shipment volume, SLA, TAT and delivery efficiency.",
        ),

        (
            "📦",
            "Shipment Tracking & Delay Prediction",
            "AI / Machine Learning",
            "XGBoost-based shipment delay prediction combined with an interactive Streamlit tracking portal.",
        ),

        (
            "📈",
            "Demand Forecasting",
            "Machine Learning",
            "Forecast future demand using historical business data and forecasting techniques.",
        ),

        (
            "👥",
            "Customer Churn Prediction",
            "Machine Learning",
            "Identify customers with higher churn probability using classification models.",
        ),

        (
            "📊",
            "CPG / FMCG Demand & Seller Analytics",
            "Business Intelligence",
            "Analyze product demand, seller performance, sales trends and business KPIs.",
        ),

        (
            "⚙️",
            "Automated MIS & Reporting",
            "Automation",
            "Automate manual reporting workflows using Python, SQL and scheduled pipelines.",
        ),
    ]


    cols = st.columns(2)


    for index, (
        icon,
        title,
        category,
        description
    ) in enumerate(projects):

        with cols[index % 2]:

            render_html(
                f"""
<div class="project-card">

    <div class="project-icon">
        {icon}
    </div>

    <div class="project-category">
        {category}
    </div>

    <div class="project-title">
        {title}
    </div>

    <div class="project-description">
        {description}
    </div>

</div>
"""
            )


# ============================================================
# REQUEST PROJECT
# ============================================================

def show_request_project():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        START A PROJECT
    </div>

    <div class="hero-title">
        Tell Us About Your
        <span class="hero-blue">
            Requirement
        </span>
    </div>

    <div class="hero-description">
        Share your business requirement and we will
        get back to you with the right analytics solution.
    </div>

</div>
"""
    )


    company = st.text_input(
        "Company Name",
        placeholder="Your company name",
        key="project_company",
    )


    col1, col2 = st.columns(2)


    with col1:

        contact = st.text_input(
            "Contact Person *",
            placeholder="Your name",
            key="project_contact",
        )

        email = st.text_input(
            "Business Email *",
            placeholder="name@company.com",
            key="project_email",
        )

        phone = st.text_input(
            "Phone / WhatsApp",
            placeholder="+91 XXXXX XXXXX",
            key="project_phone",
        )


    with col2:

        service = st.selectbox(
            "Required Solution",
            [
                "Power BI Dashboard",
                "Logistics Analytics",
                "AI / Machine Learning",
                "Automation / MIS",
                "SQL / Data Engineering",
                "API / Data Integration",
                "Not Sure",
            ],
            key="project_service",
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
            key="project_data_source",
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
            key="project_timeline",
        )


    requirement = st.text_area(
        "Requirement *",
        placeholder=(
            "Describe your business problem, "
            "current process and expected solution..."
        ),
        height=170,
        key="project_requirement",
    )


    if st.button(
        "🚀 Submit Project Request",
        key="submit_project_request",
        use_container_width=True,
    ):

        if not contact.strip():

            st.error(
                "Please enter your contact name."
            )

        elif not email.strip():

            st.error(
                "Please enter your business email."
            )

        elif not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email.strip(),
        ):

            st.error(
                "Please enter a valid email address."
            )

        elif not requirement.strip():

            st.error(
                "Please describe your requirement."
            )

        else:

            payload = {
                "Date":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                "Company":
                    company.strip(),

                "Contact":
                    contact.strip(),

                "Email":
                    email.strip(),

                "Phone":
                    phone.strip(),

                "Service":
                    service,

                "Data_Source":
                    data_source,

                "Timeline":
                    timeline,

                "Requirement":
                    requirement.strip(),

                "Source":
                    "LogiIntelli Website",
            }


            try:

                response = requests.post(
                    GOOGLE_SCRIPT_URL,
                    data=json.dumps(payload),
                    headers={
                        "Content-Type":
                        "text/plain;charset=utf-8"
                    },
                    timeout=20,
                )


                if response.status_code == 200:

                    st.success(
                        "✅ Your project request has "
                        "been submitted successfully."
                    )

                    st.balloons()

                else:

                    st.error(
                        "Unable to submit your request. "
                        "Please try again."
                    )


            except Exception as error:

                st.error(
                    "Connection error. Please try again later."
                )


# ============================================================
# ABOUT
# ============================================================

def show_about():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        ABOUT LOGIINTELLI
    </div>

    <div class="hero-title">
        Data. Intelligence.
        <span class="hero-blue">
            Business Growth.
        </span>
    </div>

    <div class="hero-description">
        LogiIntelli focuses on transforming raw business data
        into meaningful insights, predictive intelligence
        and automated decision-making solutions.
    </div>

</div>
"""
    )


    cols = st.columns(2)


    with cols[0]:

        render_html(
            """
<div class="info-card">

    <div class="card-icon">
        🎯
    </div>

    <div class="card-title">
        Our Mission
    </div>

    <div class="card-description">
        Make advanced analytics accessible and useful
        for real-world businesses.
    </div>

</div>
"""
        )


    with cols[1]:

        render_html(
            """
<div class="info-card">

    <div class="card-icon">
        💡
    </div>

    <div class="card-title">
        Our Approach
    </div>

    <div class="card-description">
        Combine business understanding with analytical
        engineering to build targeted operational solutions.
    </div>

</div>
"""
        )


    render_html(
        """
<div class="section-title">
    Why Analytics Matters
</div>

<div class="section-description">
    Businesses generate large amounts of operational data.
    The right analytics approach turns that data into
    measurable business decisions.
</div>
"""
    )


    points = [

        (
            "📊",
            "Visibility",
            "Get a clear view of business performance through dashboards and KPIs.",
        ),

        (
            "🔮",
            "Prediction",
            "Use historical data and machine learning to anticipate future outcomes.",
        ),

        (
            "⚡",
            "Automation",
            "Reduce manual work by automating repetitive reporting and data processes.",
        ),
    ]


    cols = st.columns(3)


    for col, (
        icon,
        title,
        description
    ) in zip(
        cols,
        points
    ):

        with col:

            render_html(
                f"""
<div class="info-card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-description">
        {description}
    </div>

</div>
"""
            )


# ============================================================
# CONTACT
# ============================================================

def show_contact():

    render_html(
        """
<div class="hero">

    <div class="hero-badge">
        CONTACT US
    </div>

    <div class="hero-title">
        Let's Discuss Your
        <span class="hero-blue">
            Data Needs
        </span>
    </div>

    <div class="hero-description">
        Reach out directly or submit a project request
        to discuss your analytics requirements.
    </div>

</div>
"""
    )


    cols = st.columns(3)


    with cols[0]:

        render_html(
            """
<div class="contact-card">

    <div class="contact-icon">
        📧
    </div>

    <div class="contact-title">
        Email
    </div>

    <div class="contact-value">
        support@logiintelli.com
    </div>

</div>
"""
        )


    with cols[1]:

        render_html(
            """
<div class="contact-card">

    <div class="contact-icon">
        📱
    </div>

    <div class="contact-title">
        WhatsApp
    </div>

    <div class="contact-value">
        +91 8825674102
    </div>

</div>
"""
        )


    with cols[2]:

        render_html(
            """
<div class="contact-card">

    <div class="contact-icon">
        🕒
    </div>

    <div class="contact-title">
        Working Hours
    </div>

    <div class="contact-value">
        Monday – Friday<br>
        9:00 AM – 6:00 PM IST
    </div>

</div>
"""
        )


    if st.button(
        "🚀 Request a Project",
        key="contact_request_project",
        use_container_width=True,
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# PAGE ROUTER
# ============================================================

if st.session_state.page == "Home":

    show_home()

elif st.session_state.page == "Services":

    show_services()

elif st.session_state.page == "Projects":

    show_projects()

elif st.session_state.page == "Request Project":

    show_request_project()

elif st.session_state.page == "About":

    show_about()

elif st.session_state.page == "Contact":

    show_contact()


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div class="site-footer">

    © 2026 LogiIntelli

    <br>

    Logistics Analytics • AI • Business Intelligence • Automation

</div>
"""
)


# ============================================================
# CHATBOT
# ============================================================

show_chatbot()
