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
# IMPORTANT:
# Use markdown instead of st.html for predictable rendering.
# ============================================================

def render_html(content):
    st.markdown(content, unsafe_allow_html=True)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def valid_email(email):

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return bool(
        re.match(
            pattern,
            email.strip()
        )
    )


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

        "Date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Company":
            data.get("company", ""),

        "Contact":
            data.get("name", ""),

        "Email":
            data.get("email", ""),

        "Phone":
            data.get("phone", ""),

        "Industry":
            data.get("industry", ""),

        "Service":
            data.get("service", ""),

        "Data_Source":
            data.get("data_source", ""),

        "Shipment_Volume":
            data.get("volume", ""),

        "Timeline":
            data.get("timeline", ""),

        "Requirement":
            data.get("requirement", "")
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


    # ========================================================
    # STEP 0 - NAME
    # ========================================================

    if step == 0:

        data["name"] = message

        st.session_state.chat_step = 1

        return (
            f"Nice to meet you, **{message}**! 👋\n\n"
            "What is your **company name**?"
        )


    # ========================================================
    # STEP 1 - COMPANY
    # ========================================================

    if step == 1:

        data["company"] = message

        st.session_state.chat_step = 2

        return (
            "Great! 👍\n\n"
            "Which industry does your company operate in?\n\n"
            "Courier / Logistics / E-commerce / "
            "Manufacturing / Retail / Supply Chain / Other"
        )


    # ========================================================
    # STEP 2 - INDUSTRY
    # ========================================================

    if step == 2:

        data["industry"] = message

        st.session_state.chat_step = 3

        return (
            "Thanks! What solution are you looking for?\n\n"
            "📊 Power BI Dashboard\n\n"
            "🗄️ SQL Analytics\n\n"
            "🤖 Predictive AI / Machine Learning\n\n"
            "⚙️ MIS Automation\n\n"
            "🔗 API / ERP Integration\n\n"
            "⏱️ TAT & Ageing Analytics\n\n"
            "🏢 Hub Performance Analytics\n\n"
            "📍 Route Analytics\n\n"
            "Other"
        )


    # ========================================================
    # STEP 3 - SERVICE
    # ========================================================

    if step == 3:

        data["service"] = message

        st.session_state.chat_step = 4

        return (
            "Understood. 👍\n\n"
            "Please describe your **business problem "
            "or project requirement**.\n\n"
            "Example:\n\n"
            "We need a dashboard to monitor delayed "
            "shipments, hub performance and pending ageing."
        )


    # ========================================================
    # STEP 4 - REQUIREMENT
    # ========================================================

    if step == 4:

        data["requirement"] = message

        st.session_state.chat_step = 5

        return (
            "Perfect! What is your current **data source**?\n\n"
            "Excel / CSV / MySQL / SQL Server / "
            "PostgreSQL / ERP / REST API / "
            "Multiple Sources / Other"
        )


    # ========================================================
    # STEP 5 - DATA SOURCE
    # ========================================================

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


    # ========================================================
    # STEP 6 - VOLUME
    # ========================================================

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


    # ========================================================
    # STEP 7 - TIMELINE
    # ========================================================

    if step == 7:

        data["timeline"] = message

        st.session_state.chat_step = 8

        return (
            "Almost done! 😊\n\n"
            "Please provide your **business email address**."
        )


    # ========================================================
    # STEP 8 - EMAIL
    # ========================================================

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
            "You can type **Skip** if you don't want to provide it."
        )


    # ========================================================
    # STEP 9 - PHONE
    # ========================================================

    if step == 9:

        if message.lower() == "skip":

            data["phone"] = ""

        else:

            data["phone"] = message

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

            "Would you like me to **submit this project request**?\n\n"

            "Please type **Yes** or **No**."
        )


    # ========================================================
    # STEP 10 - CONFIRMATION
    # ========================================================

    if step == 10:

        answer = message.lower()

        yes_words = [
            "yes",
            "y",
            "submit",
            "sure",
            "confirm",
            "ok",
            "okay",
            "go ahead"
        ]

        no_words = [
            "no",
            "n",
            "cancel",
            "not now"
        ]


        if answer in yes_words:

            success = submit_chat_request()

            if success:

                st.session_state.chat_submitted = True

                st.session_state.chat_step = 11

                return (
                    "🎉 **Your project request has been submitted successfully!**\n\n"
                    "Thank you for contacting **LogiIntelli**.\n\n"
                    "We have received your requirement and "
                    "will contact you using the details you provided.\n\n"
                    "🚚 **LogiIntelli**\n\n"
                    "Logistics AI • Data Analytics • BI"
                )

            else:

                return (
                    "❌ I couldn't submit the request right now.\n\n"
                    "Please type **Submit** to try again."
                )


        if answer in no_words:

            st.session_state.chat_step = 11

            return (
                "No problem! 👍\n\n"
                "Your request has not been submitted.\n\n"
                "You can start a new conversation whenever you're ready."
            )


        return (
            "Please type **Yes** to submit "
            "or **No** to cancel."
        )


    # ========================================================
    # FINISHED
    # ========================================================

    return (
        "Your conversation is complete. 🎉\n\n"
        "Click **Start New Conversation** if you need anything else."
    )


# ============================================================
# GLOBAL CSS
# ============================================================

render_html(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

html,
body,
.stApp {

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}


/* ============================================================
   APP BACKGROUND
   ============================================================ */

.stApp {

    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 102, 204, 0.07),
            transparent 30%
        ),
        linear-gradient(
            180deg,
            #f8fbff 0%,
            #ffffff 50%,
            #f5f8fc 100%
        );

}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {

    padding-top: 1rem !important;

    padding-bottom: 4rem !important;

    max-width: 1400px !important;

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


/* ============================================================
   HEADER
   ============================================================ */

.logo-title {

    font-size: 27px !important;

    font-weight: 800 !important;

    color: #0B2545 !important;

    line-height: 1.2 !important;

}

.logo-subtitle {

    font-size: 12px !important;

    color: #60758A !important;

    margin-top: 3px !important;

}


/* ============================================================
   NAVIGATION
   ============================================================ */

.stButton > button {

    border-radius: 10px !important;

    border: 1px solid #d9e3ee !important;

    background: white !important;

    color: #0B2545 !important;

    font-weight: 600 !important;

    min-height: 40px !important;

}

.stButton > button:hover {

    border-color: #0066CC !important;

    color: #0066CC !important;

}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    display: block !important;

    width: 100% !important;

    box-sizing: border-box !important;

    padding: 65px 45px !important;

    border-radius: 28px !important;

    background:
        linear-gradient(
            135deg,
            #071d35 0%,
            #0b3c6f 45%,
            #0066cc 100%
        ) !important;

    color: white !important;

    margin-top: 20px !important;

    margin-bottom: 35px !important;

    box-shadow:
        0 20px 60px rgba(0, 50, 100, 0.20) !important;

}

.hero-small-title {

    display: block !important;

    color: #7ec8ff !important;

    font-size: 14px !important;

    font-weight: 800 !important;

    letter-spacing: 1px !important;

    margin-bottom: 12px !important;

}

.hero h1 {

    display: block !important;

    color: #ffffff !important;

    font-size: 50px !important;

    font-weight: 800 !important;

    line-height: 1.1 !important;

    margin: 0 0 15px 0 !important;

    padding: 0 !important;

    visibility: visible !important;

    opacity: 1 !important;

}

.hero p {

    display: block !important;

    max-width: 850px !important;

    color: #dbeeff !important;

    font-size: 18px !important;

    line-height: 1.7 !important;

    margin: 0 !important;

}


/* ============================================================
   SECTION TITLE
   IMPORTANT FIX FOR INVISIBLE HEADINGS
   ============================================================ */

.section-title {

    display: block !important;

    width: 100% !important;

    box-sizing: border-box !important;

    color: #0B2545 !important;

    font-size: 30px !important;

    font-weight: 800 !important;

    line-height: 1.3 !important;

    margin-top: 35px !important;

    margin-bottom: 20px !important;

    padding: 0 !important;

    visibility: visible !important;

    opacity: 1 !important;

}

.section-title * {

    color: #0B2545 !important;

    visibility: visible !important;

    opacity: 1 !important;

}


/* ============================================================
   CARDS
   ============================================================ */

.service-card,
.project-card,
.metric-card,
.info-card {

    display: block !important;

    width: 100% !important;

    box-sizing: border-box !important;

    background: rgba(255,255,255,0.96) !important;

    border: 1px solid #e2eaf2 !important;

    border-radius: 18px !important;

    padding: 24px !important;

    box-shadow:
        0 8px 30px rgba(15,42,70,0.06) !important;

    height: 100% !important;

}

.service-card:hover,
.project-card:hover {

    box-shadow:
        0 15px 40px rgba(15,42,70,0.12) !important;

}


/* ============================================================
   CARD TEXT
   ============================================================ */

.service-card h3,
.project-card h3,
.info-card h2,
.info-card h3,
.info-card h4 {

    color: #0B2545 !important;

    visibility: visible !important;

    opacity: 1 !important;

}

.service-card p,
.project-card p,
.info-card p {

    color: #60758A !important;

}


/* ============================================================
   METRICS
   ============================================================ */

.metric-number {

    font-size: 34px !important;

    font-weight: 800 !important;

    color: #0066CC !important;

}

.metric-label {

    color: #60758A !important;

    font-size: 14px !important;

    margin-top: 5px !important;

}


/* ============================================================
   FORMS
   ============================================================ */

.stTextInput label,
.stTextArea label,
.stSelectbox label {

    color: #0B2545 !important;

    font-weight: 600 !important;

}


/* ============================================================
   SUBMIT BUTTON
   ============================================================ */

.stFormSubmitButton button {

    background:
        linear-gradient(
            135deg,
            #0B2545,
            #0066CC
        ) !important;

    color: white !important;

    border: none !important;

    border-radius: 10px !important;

    font-weight: 800 !important;

}


/* ============================================================
   FLOATING CHAT LAUNCHER
   ============================================================ */

.st-key-chat_launcher {

    position: fixed !important;

    right: 25px !important;

    bottom: 25px !important;

    width: 170px !important;

    z-index: 999999 !important;

}


/* ============================================================
   CHAT LAUNCHER BUTTON
   ============================================================ */

.st-key-chat_launcher button {

    background:
        linear-gradient(
            135deg,
            #0B2545,
            #0066CC
        ) !important;

    color: white !important;

    border: none !important;

    border-radius: 50px !important;

    min-height: 52px !important;

    font-size: 14px !important;

    font-weight: 800 !important;

    box-shadow:
        0 10px 35px rgba(0,82,160,0.35) !important;

}


/* ============================================================
   FLOATING CHAT WINDOW
   ============================================================ */

.st-key-chat_panel {

    position: fixed !important;

    right: 25px !important;

    bottom: 90px !important;

    width: 390px !important;

    max-width: calc(100vw - 30px) !important;

    height: 610px !important;

    max-height: calc(100vh - 120px) !important;

    z-index: 999998 !important;

    background: white !important;

    border-radius: 20px !important;

    border: 1px solid #dce5ef !important;

    box-shadow:
        0 20px 70px rgba(0,0,0,0.25) !important;

    overflow-y: auto !important;

    padding: 18px !important;

    box-sizing: border-box !important;

}


/* ============================================================
   CHAT HEADER
   ============================================================ */

.chat-header {

    background:
        linear-gradient(
            135deg,
            #071d35,
            #0066cc
        ) !important;

    color: white !important;

    padding: 16px !important;

    border-radius: 15px !important;

    margin-bottom: 15px !important;

}

.chat-header-title {

    font-size: 17px !important;

    font-weight: 800 !important;

    color: white !important;

}

.chat-header-status {

    font-size: 11px !important;

    margin-top: 4px !important;

    color: #cce8ff !important;

}


/* ============================================================
   CHAT INFORMATION
   ============================================================ */

.chat-info {

    background: #f2f7fc !important;

    border-radius: 12px !important;

    padding: 12px !important;

    color: #536a80 !important;

    font-size: 12px !important;

    line-height: 1.6 !important;

    margin-bottom: 15px !important;

}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {

    background: transparent !important;

}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {

    position: sticky !important;

    bottom: 0 !important;

    background: white !important;

    z-index: 10 !important;

}


/* ============================================================
   CHAT MARKDOWN
   ============================================================ */

.st-key-chat_panel [data-testid="stChatMessage"] p {

    color: #26384a !important;

}

.st-key-chat_panel [data-testid="stChatMessage"] strong {

    color: #0B2545 !important;

}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    display: block !important;

    text-align: center !important;

    color: #718297 !important;

    font-size: 12px !important;

    padding: 35px 10px !important;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    .block-container {

        padding-left: 15px !important;

        padding-right: 15px !important;

    }

    .hero {

        padding: 40px 25px !important;

        border-radius: 20px !important;

    }

    .hero h1 {

        font-size: 36px !important;

    }

    .hero p {

        font-size: 15px !important;

    }

    .section-title {

        font-size: 25px !important;

    }

    .st-key-chat_launcher {

        right: 15px !important;

        bottom: 15px !important;

        width: 155px !important;

    }

    .st-key-chat_panel {

        right: 10px !important;

        bottom: 80px !important;

        width: calc(100vw - 20px) !important;

        height: 70vh !important;

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
<div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:8px 4px 15px 4px;
">

    <div>

        <div class="logo-title">
            🚚 LogiIntelli
        </div>

        <div class="logo-subtitle">
            Logistics Analytics • AI & Predictive Intelligence • BI Automation
        </div>

    </div>

    <div style="
        color:#0066CC;
        font-size:12px;
        font-weight:800;
    ">
        DATA • AI • AUTOMATION
    </div>

</div>
"""
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
    "Contact"
]

nav_cols = st.columns(6)

for i, page_name in enumerate(pages):

    with nav_cols[i]:

        if st.session_state.page == page_name:

            label = f"● {page_name}"

        else:

            label = page_name

        if st.button(
            label,
            key=f"nav_{i}",
            use_container_width=True
        ):

            st.session_state.page = page_name

            st.rerun()


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page


# ============================================================
# HOME
# ============================================================

if page == "Home":

    render_html(
        """
<div class="hero">

    <div class="hero-small-title">
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
"""
    )


    render_html(
        """
<div class="section-title">
    Our Impact
</div>
"""
    )


    c1, c2, c3, c4 = st.columns(4)


    metrics = [

        ("10+", "Years Experience"),

        ("50+", "Analytics & AI Pipelines"),

        ("24/7", "Automated Systems"),

        ("BI + AI", "Technology Architecture")

    ]


    for col, item in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        number, label = item

        with col:

            render_html(
                f"""
<div class="metric-card">

    <div class="metric-number">
        {number}
    </div>

    <div class="metric-label">
        {label}
    </div>

</div>
"""
            )


    render_html(
        """
<div class="section-title">
    What We Build
</div>
"""
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
            "Identify delayed shipments, ageing patterns and bottlenecks."
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate repetitive daily, weekly and monthly reporting."
        ),

        (
            "🏢",
            "Hub Performance",
            "Measure hub productivity, SLA and operational performance."
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect ERP, databases and REST APIs into analytics pipelines."
        ),

        (
            "🤖",
            "Predictive AI",
            "Predict shipment delays and operational risks."
        )

    ]


    cols = st.columns(3)


    for i, service in enumerate(services):

        icon, title, description = service

        with cols[i % 3]:

            render_html(
                f"""
<div class="service-card">

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
        font-size:13px;
        line-height:1.7;
        color:#60758A;
    ">
        {description}
    </div>

</div>
"""
            )


    render_html(
        """
<div class="section-title">
    How We Work
</div>
"""
    )


    workflow = [

        (
            "01",
            "Understand",
            "Understand your business problem and KPIs."
        ),

        (
            "02",
            "Connect",
            "Connect ERP, SQL, Excel, APIs and other data sources."
        ),

        (
            "03",
            "Build",
            "Build dashboards, automation and AI solutions."
        ),

        (
            "04",
            "Improve",
            "Monitor results and continuously improve operations."
        )

    ]


    cols = st.columns(4)


    for col, item in zip(
        cols,
        workflow
    ):

        number, title, description = item

        with col:

            render_html(
                f"""
<div class="info-card">

    <div style="
        color:#0066CC;
        font-weight:800;
        font-size:13px;
    ">
        {number}
    </div>

    <h3 style="
        color:#0B2545;
        margin:8px 0;
    ">
        {title}
    </h3>

    <p style="
        color:#60758A;
        font-size:13px;
        line-height:1.6;
    ">
        {description}
    </p>

</div>
"""
            )


# ============================================================
# SERVICES
# ============================================================

elif page == "Services":

    render_html(
        """
<div class="section-title">
    Our Services
</div>
"""
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
            "Shipment TAT, ageing buckets, SLA performance and pending shipment analytics."
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate daily MIS, scheduled reports and operational reporting."
        ),

        (
            "🏢",
            "Hub Performance Analytics",
            "Analyze hub productivity, volume, service quality and bottlenecks."
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect REST APIs, ERP systems and SQL databases."
        ),

        (
            "🤖",
            "Predictive AI & Machine Learning",
            "Predict shipment delays and identify operational risk patterns."
        )

    ]


    cols = st.columns(3)


    for i, service in enumerate(services):

        icon, title, description = service

        with cols[i % 3]:

            render_html(
                f"""
<div class="service-card">

    <div style="font-size:35px;">
        {icon}
    </div>

    <h3 style="color:#0B2545;">
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
"""
            )


# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    render_html(
        """
<div class="section-title">
    Projects & Solutions
</div>
"""
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
            "Analyze hub productivity, volume and operational performance."
        ),

        (
            "📦",
            "Inbound / Outbound Analytics",
            "State, hub and route-level inbound and outbound analytics."
        ),

        (
            "🤖",
            "Shipment Delay Prediction AI",
            "Machine learning solution to identify shipments with higher delay risk."
        ),

        (
            "⚙️",
            "Automated Daily MIS Engine",
            "Python-based automated reporting pipeline for logistics operations."
        )

    ]


    cols = st.columns(3)


    for i, project in enumerate(projects):

        icon, title, description = project

        with cols[i % 3]:

            render_html(
                f"""
<div class="project-card">

    <div style="
        font-size:34px;
        margin-bottom:10px;
    ">
        {icon}
    </div>

    <h3 style="
        color:#0B2545;
    ">
        {title}
    </h3>

    <p style="
        color:#60758A;
        font-size:13px;
        line-height:1.7;
    ">
        {description}
    </p>

</div>
"""
            )


# ============================================================
# REQUEST PROJECT
# ============================================================

elif page == "Request Project":

    render_html(
        """
<div class="section-title">
    Request a Project
</div>
"""
    )


    st.write(
        "Tell us about your requirement and we will review it."
    )


    with st.form("request_project_form"):

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
                    "Other"
                ]
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
                    "Other"
                ]
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
                    "Other"
                ]
            )


            timeline = st.selectbox(
                "Expected Timeline",
                [
                    "Less than 1 week",
                    "1–2 weeks",
                    "2–4 weeks",
                    "1–2 months",
                    "Not decided"
                ]
            )


        requirement = st.text_area(
            "Project Requirement *",
            height=170,
            placeholder=(
                "Describe your business problem, "
                "dashboard requirement, automation requirement "
                "or AI requirement."
            )
        )


        submit = st.form_submit_button(
            "🚀 Submit Project Request",
            use_container_width=True
        )


        if submit:

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
                    "Please describe your requirement."
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
                        requirement

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

                        allow_redirects=True

                    )


                    if response.status_code == 200:

                        st.success(
                            "🎉 Project request submitted successfully!"
                        )

                    else:

                        st.error(
                            "Unable to submit the request."
                        )


                except Exception as error:

                    st.error(
                        f"Submission error: {error}"
                    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    render_html(
        """
<div class="section-title">
    About LogiIntelli
</div>

<div class="info-card">

    <h2 style="color:#0B2545;">
        Logistics Intelligence Through Data
    </h2>

    <p style="
        color:#60758A;
        font-size:15px;
        line-height:1.8;
    ">
        LogiIntelli focuses on solving real-world logistics,
        supply chain and operational challenges using data,
        business intelligence, automation and artificial intelligence.
    </p>

    <p style="
        color:#60758A;
        font-size:15px;
        line-height:1.8;
    ">
        Our solutions combine SQL, Python, Power BI,
        REST APIs, ERP integration, automation and
        machine learning to transform operational data
        into actionable business intelligence.
    </p>

</div>
"""
    )


    render_html(
        """
<div class="section-title">
    Technology Stack
</div>
"""
    )


    technologies = [

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
        "Automation"

    ]


    cols = st.columns(4)


    for i, technology in enumerate(technologies):

        with cols[i % 4]:

            render_html(
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
"""
            )


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    render_html(
        """
<div class="section-title">
    Let's Work Together
</div>

<p style="
    color:#60758A;
    font-size:15px;
">
    Have a logistics analytics, BI, automation or AI requirement?
</p>
"""
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        render_html(
            """
<div class="info-card">

    <div style="font-size:28px;">
        📧
    </div>

    <h4 style="color:#0B2545;">
        Email
    </h4>

    <p>
        sumansekar1205@gmail.com
    </p>

</div>
"""
        )


    with c2:

        render_html(
            """
<div class="info-card">

    <div style="font-size:28px;">
        📱
    </div>

    <h4 style="color:#0B2545;">
        WhatsApp
    </h4>

    <p>
        +91 8825674102
    </p>

</div>
"""
        )


    with c3:

        render_html(
            """
<div class="info-card">

    <div style="font-size:28px;">
        💼
    </div>

    <h4 style="color:#0B2545;">
        LinkedIn
    </h4>

    <p>
        linkedin.com/in/sumansekar12/
    </p>

</div>
"""
        )


    with c4:

        render_html(
            """
<div class="info-card">

    <div style="font-size:28px;">
        💻
    </div>

    <h4 style="color:#0B2545;">
        GitHub
    </h4>

    <p>
        github.com/Suman-SekarSagadev
    </p>

</div>
"""
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
<div class="footer">

    🚚 <b>LogiIntelli</b>

    <br><br>

    Logistics Analytics • AI • BI • Automation

    <br><br>

    © 2026 LogiIntelli. All rights reserved.

</div>
"""
)


# ============================================================
# FLOATING CHATBOT BUTTON
# ============================================================

with st.container(key="chat_launcher"):

    if st.button(
        "🤖 Chat with us",
        key="floating_chat_button",
        use_container_width=True
    ):

        st.session_state.chat_open = True

        start_chat()

        st.rerun()


# ============================================================
# FLOATING CHAT WINDOW
# ============================================================

if st.session_state.chat_open:

    with st.container(key="chat_panel"):

        render_html(
            """
<div class="chat-header">

    <div style="
        display:flex;
        align-items:center;
        gap:10px;
    ">

        <div style="
            width:40px;
            height:40px;
            background:white;
            border-radius:50%;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:21px;
        ">
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

</div>
"""
        )


        # ====================================================
        # CHAT INFORMATION
        # ====================================================

        render_html(
            """
<div class="chat-info">

    I will ask a few questions about your project
    and collect the information needed by our team.

    <br><br>

    Your request will be submitted to our
    project request Google Sheet after you confirm.

</div>
"""
        )


        # ====================================================
        # MESSAGES
        # ====================================================

        for msg in st.session_state.chat_messages:

            with st.chat_message(
                msg["role"]
            ):

                st.markdown(
                    msg["content"]
                )


        # ====================================================
        # CHAT INPUT
        # ====================================================

        if not st.session_state.chat_submitted:

            user_input = st.chat_input(
                "Type your answer..."
            )


            if user_input:

                st.session_state.chat_messages.append(
                    {
                        "role": "user",
                        "content": user_input
                    }
                )


                response = chatbot_response(
                    user_input
                )


                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )


                st.rerun()


        # ====================================================
        # CHAT CONTROLS
        # ====================================================

        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "🔄 New Chat",
                key="new_chat_button",
                use_container_width=True
            ):

                reset_chat()

                start_chat()

                st.rerun()


        with col2:

            if st.button(
                "✕ Close",
                key="close_chat_button",
                use_container_width=True
            ):

                st.session_state.chat_open = False

                st.rerun()
