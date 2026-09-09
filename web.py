from datetime import datetime
import json
import re

import requests
import streamlit as st


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
# GOOGLE APPS SCRIPT WEB APP URL
# ============================================================

GOOGLE_SHEET_WEB_APP_URL = (
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
# CUSTOM CSS
# ============================================================

html("""
<style>

/* ============================================================
   GLOBAL
============================================================ */

html, body {
    background-color: #F8FAFC;
}

[data-testid="stAppViewContainer"] {
    background-color: #F8FAFC;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   BRAND
============================================================ */

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #0B2545;
    letter-spacing: -1.5px;
    margin-bottom: 4px;
}

.sub-title {
    text-align: center;
    font-size: 16px;
    font-weight: 650;
    color: #0066CC;
    letter-spacing: .5px;
    margin-bottom: 25px;
}


/* ============================================================
   NAVIGATION
============================================================ */

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    background: #FFFFFF;
    color: #0B2545;
    font-weight: 700;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: #0B2545;
    color: #FFFFFF;
    border-color: #0B2545;
    transform: translateY(-1px);
}


/* ============================================================
   HERO
============================================================ */

.hero {

    padding: 52px 48px;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #0B2545 0%,
            #134074 55%,
            #0066CC 100%
        );

    border: 1px solid #0B2545;

    box-shadow:
        0 18px 40px rgba(11, 37, 69, 0.18);

    margin-top: 15px;

    margin-bottom: 35px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 20px;
    line-height: 1.2;
}

.hero h2 {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 850;
    margin-bottom: 15px;
}

.hero p {
    color: #E2E8F0;
    font-size: 17px;
    line-height: 1.75;
    margin-bottom: 15px;
}

.hero strong {
    color: #FFFFFF;
}


/* ============================================================
   SECTION TITLES
============================================================ */

.section-title {
    font-size: 31px;
    font-weight: 900;
    color: #0B2545;
    margin-top: 42px;
    margin-bottom: 7px;
}

.section-subtitle {
    color: #64748B;
    font-size: 15px;
    line-height: 1.65;
    margin-bottom: 25px;
}


/* ============================================================
   CARDS
============================================================ */

.card,
.project-card,
.metric-card {

    background: #FFFFFF;

    padding: 26px;

    border-radius: 17px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 6px 18px rgba(15, 23, 42, 0.05);

    margin-bottom: 20px;

    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease;
}

.card:hover,
.project-card:hover,
.metric-card:hover {

    transform: translateY(-4px);

    border-color: #0066CC;

    box-shadow:
        0 14px 30px rgba(0, 102, 204, 0.12);
}

.card h2,
.card h3,
.project-card h3 {
    color: #0B2545;
    font-weight: 850;
    margin-bottom: 12px;
}

.card p,
.card li,
.project-card p {
    color: #334155;
    line-height: 1.65;
}

.card li {
    margin-bottom: 7px;
}


/* ============================================================
   METRICS
============================================================ */

.metric-card {
    text-align: center;
    padding: 27px 15px;
}

.metric-value {
    font-size: 35px;
    font-weight: 900;
    color: #0066CC;
    margin-bottom: 5px;
}

.metric-label {
    color: #64748B;
    font-size: 14px;
    font-weight: 700;
}


/* ============================================================
   SERVICE ICON
============================================================ */

.service-icon {
    font-size: 40px;
    margin-bottom: 9px;
}


/* ============================================================
   WORKFLOW
============================================================ */

.workflow {

    background: #FFFFFF;

    border-radius: 18px;

    padding: 30px 20px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 6px 18px rgba(15, 23, 42, 0.04);

    margin-top: 20px;

    margin-bottom: 30px;

    overflow-x: auto;
}

.workflow-container {

    display: flex;

    align-items: center;

    justify-content: space-between;

    min-width: 1050px;
}

.workflow-step {
    text-align: center;
    min-width: 115px;
}

.workflow-icon {
    font-size: 38px;
    margin-bottom: 8px;
}

.workflow-name {
    font-size: 15px;
    font-weight: 800;
    color: #0B2545;
}

.workflow-desc {
    font-size: 12px;
    color: #64748B;
    margin-top: 4px;
}

.workflow-arrow {
    font-size: 22px;
    color: #0066CC;
    font-weight: 800;
}


/* ============================================================
   FORM
============================================================ */

div[data-testid="stForm"] {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 19px;

    padding: 30px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.06);
}

div[data-testid="stWidgetLabel"] label {
    color: #0B2545 !important;
    font-weight: 750 !important;
}

div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea {

    background: #FFFFFF !important;

    color: #0F172A !important;

    border: 1px solid #CBD5E1 !important;

    border-radius: 9px !important;
}


/* ============================================================
   FORM SUBMIT
============================================================ */

div[data-testid="stFormSubmitButton"] button {

    background: #0B2545 !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 10px !important;

    font-weight: 800 !important;

    min-height: 45px;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #0066CC !important;
}


/* ============================================================
   CONTACT
============================================================ */

.contact-link {
    color: #0066CC;
    text-decoration: none;
    font-weight: 700;
}

.contact-link:hover {
    text-decoration: underline;
}


/* ============================================================
   BADGE
============================================================ */

.badge {

    display: inline-block;

    padding: 5px 10px;

    border-radius: 20px;

    background: #EFF6FF;

    color: #0066CC;

    font-size: 12px;

    font-weight: 800;

    margin-top: 5px;
}


/* ============================================================
   CHATBOT
============================================================ */

/*
   Streamlit chat_input is fixed at the bottom of the browser.
   This styling gives it the appearance of a floating assistant.
*/

[data-testid="stChatInput"] {

    border-radius: 18px !important;

}

[data-testid="stChatMessage"] {

    border-radius: 14px;

}


/* ============================================================
   CHATBOT HEADER
============================================================ */

.chat-header {

    background:
        linear-gradient(
            135deg,
            #0B2545,
            #0066CC
        );

    color: white;

    padding: 18px 22px;

    border-radius: 18px;

    margin-bottom: 15px;

    box-shadow:
        0 8px 25px rgba(0, 102, 204, 0.18);
}

.chat-header-title {

    font-size: 20px;

    font-weight: 900;
}

.chat-header-sub {

    font-size: 13px;

    color: #E2E8F0;

    margin-top: 4px;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    text-align: center;

    padding: 38px 20px;

    margin-top: 50px;

    color: #64748B;

    font-size: 14px;

    line-height: 1.7;
}

.footer-title {

    color: #0B2545;

    font-size: 20px;

    font-weight: 900;

    margin-bottom: 10px;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .main-title {
        font-size: 32px;
    }

    .sub-title {
        font-size: 13px;
    }

    .hero {
        padding: 30px 22px;
        border-radius: 16px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .hero h2 {
        font-size: 23px;
    }

    .hero p {
        font-size: 15px;
    }

    .section-title {
        font-size: 25px;
    }

    .metric-value {
        font-size: 29px;
    }

}

</style>
""")


# ============================================================
# CHATBOT FUNCTIONS
# ============================================================

def reset_chat():

    st.session_state.chat_messages = []

    st.session_state.chat_step = 0

    st.session_state.chat_data = {}

    st.session_state.chat_submitted = False


def valid_email(email):

    return re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email.strip()
    )


def submit_chat_request():

    data = st.session_state.chat_data

    payload = {

        "Date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Company": data.get(
            "company",
            ""
        ),

        "Contact": data.get(
            "name",
            ""
        ),

        "Email": data.get(
            "email",
            ""
        ),

        "Phone": data.get(
            "phone",
            ""
        ),

        "Industry": data.get(
            "industry",
            ""
        ),

        "Service": data.get(
            "service",
            ""
        ),

        "Data_Source": data.get(
            "data_source",
            ""
        ),

        "Shipment_Volume": data.get(
            "volume",
            ""
        ),

        "Timeline": data.get(
            "timeline",
            ""
        ),

        "Requirement": data.get(
            "requirement",
            ""
        ),
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

            return True, "success"

        return False, response.text


    except requests.exceptions.Timeout:

        return False, "timeout"


    except requests.exceptions.RequestException as e:

        return False, str(e)


def chatbot_response(user_message):

    step = st.session_state.chat_step

    data = st.session_state.chat_data

    message = user_message.strip()


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
            "Great! Which industry does your company operate in?\n\n"
            "**Courier / Logistics / E-commerce / "
            "Manufacturing / Other**"
        )


    # ========================================================
    # STEP 2 - INDUSTRY
    # ========================================================

    if step == 2:

        data["industry"] = message

        st.session_state.chat_step = 3

        return (
            "What solution are you looking for?\n\n"
            "📊 **Power BI Dashboard**\n\n"
            "🗄️ **SQL Analytics**\n\n"
            "🤖 **Predictive AI / Machine Learning**\n\n"
            "⚙️ **MIS Automation**\n\n"
            "🔗 **API / ERP Integration**\n\n"
            "⏱️ **TAT & Ageing Analytics**\n\n"
            "🏢 **Hub Performance Analytics**\n\n"
            "📍 **Route Analytics**\n\n"
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
            "Please describe the **business problem or "
            "requirement** you want to solve.\n\n"
            "For example:\n"
            "> We need a dashboard to monitor delayed shipments, "
            "hub performance and pending ageing."
        )


    # ========================================================
    # STEP 4 - REQUIREMENT
    # ========================================================

    if step == 4:

        data["requirement"] = message

        st.session_state.chat_step = 5

        return (
            "What is your current **data source**?\n\n"
            "Excel / CSV / MySQL / SQL Server / PostgreSQL / "
            "ERP / REST API / Multiple Sources / Other"
        )


    # ========================================================
    # STEP 5 - DATA SOURCE
    # ========================================================

    if step == 5:

        data["data_source"] = message

        st.session_state.chat_step = 6

        return (
            "Approximately how much data do you handle?\n\n"
            "For example:\n"
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
                "That doesn't look like a valid email address. "
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


    # ========================================================
    # STEP 9 - PHONE
    # ========================================================

    if step == 9:

        if message.lower() == "skip":

            data["phone"] = ""

        else:

            data["phone"] = message

        st.session_state.chat_step = 10

        summary = f"""
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

**Phone:** {data.get("phone", "") or "Not provided"}

---

Would you like me to **submit this project request** to LogiIntelli?
"""

        return summary


    # ========================================================
    # STEP 10 - CONFIRMATION
    # ========================================================

    if step == 10:

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


        lower_message = message.lower()


        if lower_message in positive_words:

            success, result = submit_chat_request()


            if success:

                st.session_state.chat_submitted = True

                st.session_state.chat_step = 11

                return (
                    "🎉 **Your project request has been submitted successfully!**\n\n"
                    "Thank you for contacting **LogiIntelli**.\n\n"
                    "We have received your requirement and will "
                    "contact you using the details you provided.\n\n"
                    "🚚 **LogiIntelli — Logistics AI • Data Analytics • BI**"
                )


            if result == "timeout":

                return (
                    "⏱️ The submission timed out.\n\n"
                    "Please try sending **Submit** again."
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
                "Whenever you're ready, you can use "
                "**Request Project** or start the assistant again."
            )


        return (
            "Please type **Yes** to submit the project request "
            "or **No** to cancel."
        )


    # ========================================================
    # AFTER SUBMISSION
    # ========================================================

    return (
        "Your request has already been submitted successfully. 🎉"
    )


# ============================================================
# HEADER
# ============================================================

html("""
<div>

    <div class="main-title">
        🚚 LogiIntelli
    </div>

    <div class="sub-title">
        Logistics Analytics • AI & Predictive Intelligence • BI Automation
    </div>

</div>
""")


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

    html("""
    <div class="hero">

        <h1>
            Logistics AI, Data Analytics & Business Intelligence
        </h1>

        <p>
            <strong>LogiIntelli</strong> is a Logistics AI,
            Data Analytics, and Business Intelligence platform
            focused on helping courier, logistics, supply chain,
            and e-commerce businesses transform operational data
            into actionable intelligence.
        </p>

        <p>
            We build AI-powered logistics analytics,
            Power BI dashboards, SQL data engineering solutions,
            machine learning models, predictive analytics,
            automated MIS systems, API integrations,
            and real-time operational intelligence platforms.
        </p>

        <p>
            Our expertise includes shipment tracking analytics,
            delivery performance, TAT and ageing analysis,
            hub performance, route analytics,
            shipment delay prediction, demand forecasting,
            ERP automation, and AI-powered supply chain intelligence.
        </p>

    </div>
    """)


    # ========================================================
    # METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("10+", "Years Experience"),
        ("50+", "Analytics & AI Pipelines"),
        ("24/7", "Automated Systems"),
        ("BI + AI", "Technology Architecture"),
    ]

    for col, (value, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            html(f"""
            <div class="metric-card">

                <div class="metric-value">
                    {value}
                </div>

                <div class="metric-label">
                    {label}
                </div>

            </div>
            """)


    # ========================================================
    # SERVICES
    # ========================================================

    html("""
    <div class="section-title">
        What We Build
    </div>

    <div class="section-subtitle">
        Solutions engineered specifically around logistics operations,
        data analytics, automation, and predictive artificial intelligence.
    </div>
    """)


    services = [

        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending shipments, RTO, hub performance, state performance, and operational KPIs.",
        ),

        (
            "🚚",
            "TAT & Ageing Analytics",
            "Shipment ageing analysis, transit time monitoring, delivery SLA performance, bottleneck detection, and delayed shipment identification.",
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate daily operational reporting from ERPs, REST APIs, SQL databases, Python pipelines, and Excel reporting systems.",
        ),

        (
            "🏢",
            "Hub Performance Analytics",
            "Measure hub throughput, productivity, service levels, pending shipments, delivery performance, and operational efficiency.",
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect legacy ERP systems and modern REST APIs using Python, SQL, automation, and business intelligence platforms.",
        ),

        (
            "🤖",
            "Predictive AI & Machine Learning",
            "Machine learning solutions for shipment delay prediction, RTO risk scoring, demand forecasting, anomaly detection, and operational intelligence.",
        ),

    ]


    for i in range(0, len(services), 3):

        cols = st.columns(3)

        for j in range(3):

            if i + j >= len(services):
                continue

            icon, title, description = services[i + j]

            with cols[j]:

                html(f"""
                <div class="card">

                    <div class="service-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """)


    # ========================================================
    # WORKFLOW
    # ========================================================

    html("""
    <div class="section-title">
        Logistics Data Flow
    </div>

    <div class="section-subtitle">
        End-to-end shipment telemetry and operational intelligence
        from booking to AI-monitored delivery.
    </div>

    <div class="workflow">

        <div class="workflow-container">

            <div class="workflow-step">
                <div class="workflow-icon">📦</div>
                <div class="workflow-name">Booking</div>
                <div class="workflow-desc">Shipment Created</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">🚛</div>
                <div class="workflow-name">Pickup</div>
                <div class="workflow-desc">Shipment Picked</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">🏢</div>
                <div class="workflow-name">Inbound</div>
                <div class="workflow-desc">Hub Received</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">🔄</div>
                <div class="workflow-name">Processing</div>
                <div class="workflow-desc">Hub Processing</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">🚚</div>
                <div class="workflow-name">Transit</div>
                <div class="workflow-desc">Shipment Moving</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">📍</div>
                <div class="workflow-name">Out for Delivery</div>
                <div class="workflow-desc">Last Mile</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">✅</div>
                <div class="workflow-name">Delivery</div>
                <div class="workflow-desc">Shipment Delivered</div>
            </div>

        </div>

    </div>
    """)


    # ========================================================
    # CTA
    # ========================================================

    html("""
    <div class="hero">

        <h2>
            Have a Logistics Data or AI Problem?
        </h2>

        <p>
            Our Project Assistant can collect your requirements
            and submit them directly to our project management
            system.
        </p>

        <p>
            Look for the chat assistant at the bottom of the page
            and tell us what you want to build.
        </p>

    </div>
    """)


# ============================================================
# SERVICES
# ============================================================

elif page == "Services":

    html("""
    <div class="section-title">
        Logistics & AI Solutions
    </div>

    <div class="section-subtitle">
        Project-based analytics, business intelligence, automation,
        and machine learning solutions engineered around logistics operations.
    </div>
    """)


    service_details = [

        (
            "📊",
            "Courier Operations Dashboard",
            [
                "Booking volume tracking",
                "Delivery performance metrics",
                "Pending shipments tracking",
                "RTO root-cause analysis",
                "State & hub breakdown",
                "Real-time operational trends",
            ],
        ),

        (
            "⏱️",
            "TAT & Ageing Analytics",
            [
                "Shipment ageing alerts",
                "Transit TAT monitoring",
                "Last-mile SLA performance",
                "Ageing bucket breakdowns",
                "Route bottleneck identification",
                "Delay classification",
            ],
        ),

        (
            "🏢",
            "Hub Performance Analytics",
            [
                "Hub productivity scoring",
                "Booking vs delivery velocity",
                "Pending ageing control",
                "RTO minimization metrics",
                "First-attempt delivery rate",
                "Hub SLA rankings",
            ],
        ),

        (
            "🔄",
            "Inbound / Outbound Network Analytics",
            [
                "State-to-state movement",
                "Hub inbound optimization",
                "Hub outbound monitoring",
                "Processing time analysis",
                "Inter-hub transit ageing",
                "Network lane performance",
            ],
        ),

        (
            "⚙️",
            "MIS Automation",
            [
                "ERP automated extraction",
                "REST API pipelines",
                "Python ETL scripting",
                "Excel report generation",
                "Scheduled automation",
                "Email distribution alerts",
            ],
        ),

        (
            "🤖",
            "Predictive AI & Analytics",
            [
                "Shipment delay prediction",
                "RTO probability scoring",
                "Demand & volume forecasting",
                "Hub workload prediction",
                "Anomaly detection",
                "Custom machine learning models",
            ],
        ),

    ]


    for i in range(0, len(service_details), 3):

        cols = st.columns(3)

        for j in range(3):

            if i + j >= len(service_details):
                continue

            icon, title, items = service_details[i + j]

            item_html = "".join(
                f"<li>{item}</li>"
                for item in items
            )

            with cols[j]:

                html(f"""
                <div class="card">

                    <div class="service-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <ul>
                        {item_html}
                    </ul>

                </div>
                """)


# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    html("""
    <div class="section-title">
        Logistics & AI Projects
    </div>

    <div class="section-subtitle">
        Sample projects demonstrating capabilities in logistics analytics,
        business intelligence, automation, and machine learning.
    </div>
    """)


    projects = [

        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending shipments, RTO, ageing, hub performance, and business KPIs.",
            "Power BI • SQL • DAX",
            "Operations Analytics",
        ),

        (
            "02",
            "Shipment TAT & Ageing Analytics",
            "Identify delayed shipments, ageing buckets, route-level delays, transit performance, and SLA bottlenecks.",
            "SQL • Python • Power BI",
            "TAT Analytics",
        ),

        (
            "03",
            "Hub Performance Analytics",
            "Compare hubs based on booking, delivery, pending shipments, RTO, shipment weight, productivity, and operational SLAs.",
            "SQL • Power BI • DAX",
            "Hub Analytics",
        ),

        (
            "04",
            "Inbound / Outbound Analytics",
            "Analyze shipment movement from origin states and hubs to destination hubs across logistics corridors.",
            "SQL • Python • Power BI",
            "Network Analytics",
        ),

        (
            "05",
            "Shipment Delay Prediction AI",
            "Machine learning model using XGBoost to identify shipments with high probabilities of delay before SLA breaches.",
            "Python • XGBoost • Machine Learning",
            "Predictive AI",
        ),

        (
            "06",
            "Automated Daily MIS Engine",
            "ERP and API automated data extraction, transformation, validation, and scheduled report distribution.",
            "Python • SQL • REST API",
            "Automation",
        ),

    ]


    for i in range(0, len(projects), 2):

        cols = st.columns(2)

        for j in range(2):

            if i + j >= len(projects):
                continue

            number, title, description, tech, category = projects[i + j]

            with cols[j]:

                html(f"""
                <div class="project-card">

                    <div style="
                        color:#0066CC;
                        font-size:13px;
                        font-weight:850;
                        margin-bottom:8px;
                    ">
                        PROJECT {number}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                    <p>
                        <strong>Technology:</strong><br>
                        {tech}
                    </p>

                    <span class="badge">
                        {category}
                    </span>

                </div>
                """)


# ============================================================
# REQUEST PROJECT - NORMAL FORM
# ============================================================

elif page == "Request Project":

    html("""
    <div class="section-title">
        Request a Project
    </div>

    <div class="section-subtitle">
        Prefer a traditional form? You can submit your requirement
        here, or use the LogiIntelli Project Assistant.
    </div>
    """)


    with st.form(
        "project_request_form",
        clear_on_submit=False
    ):

        col1, col2 = st.columns(2)


        with col1:

            company_name = st.text_input(
                "Company Name"
            )

            contact_name = st.text_input(
                "Contact Person *"
            )

            email = st.text_input(
                "Business Email *"
            )

            phone = st.text_input(
                "Phone / WhatsApp"
            )


        with col2:

            service = st.selectbox(
                "Required Solution",
                [
                    "Power BI Dashboard",
                    "SQL Analytics",
                    "Predictive AI / Machine Learning",
                    "TAT & Ageing Analytics",
                    "Hub Performance Analytics",
                    "Route Analytics",
                    "Automated MIS",
                    "API / ERP Integration",
                    "Other",
                ],
            )

            data_source = st.selectbox(
                "Current Data Source",
                [
                    "Excel",
                    "CSV",
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
                    "1-2 weeks",
                    "2-4 weeks",
                    "1-2 months",
                    "Not decided",
                ],
            )


        requirement = st.text_area(
            "Describe Your Requirement *",
            height=160,
            placeholder=(
                "Example: We need an automated daily courier "
                "performance dashboard and an AI model for "
                "predicting shipment delay risk."
            ),
        )


        submitted = st.form_submit_button(
            "🚀 Submit Project Request",
            use_container_width=True,
        )


        if submitted:

            if not contact_name.strip():

                st.warning(
                    "Please enter the Contact Person name."
                )

            elif not email.strip():

                st.warning(
                    "Please enter your Business Email."
                )

            elif not valid_email(email):

                st.warning(
                    "Please enter a valid email address."
                )

            elif not requirement.strip():

                st.warning(
                    "Please describe your project requirement."
                )

            else:

                payload = {

                    "Date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    "Company": company_name.strip(),

                    "Contact": contact_name.strip(),

                    "Email": email.strip(),

                    "Phone": phone.strip(),

                    "Service": service,

                    "Data_Source": data_source,

                    "Timeline": timeline,

                    "Requirement": requirement.strip(),
                }


                try:

                    with st.spinner(
                        "Submitting your project request..."
                    ):

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
                            "🎉 Thank you! Your project request "
                            "has been submitted successfully."
                        )

                        st.info(
                            "Our team will review your requirement "
                            "and contact you shortly."
                        )

                    else:

                        st.error(
                            f"Submission failed. "
                            f"Status Code: {response.status_code}"
                        )

                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ The request timed out. "
                        "Please try again."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Unable to submit request: {str(e)}"
                    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    html("""
    <div class="section-title">
        About LogiIntelli
    </div>

    <div class="section-subtitle">
        AI, analytics, automation and business intelligence
        for logistics and supply chain operations.
    </div>

    <div class="card">

        <h2>
            AI & Data Intelligence for Logistics
        </h2>

        <p>
            <strong>LogiIntelli</strong> is an AI, Data Analytics,
            and Business Intelligence platform focused on
            logistics, courier, supply chain,
            and e-commerce industries.
        </p>

        <p>
            We transform complex operational data into
            actionable business intelligence using SQL,
            Python, Power BI, machine learning,
            APIs, and automated data pipelines.
        </p>

        <p>
            Our expertise includes logistics analytics,
            shipment tracking, delivery performance,
            TAT and ageing analysis, hub performance,
            route analytics, predictive AI,
            shipment delay prediction,
            demand forecasting, and MIS automation.
        </p>

        <p>
            LogiIntelli helps businesses improve operational
            visibility, reduce manual reporting,
            identify bottlenecks, monitor delivery SLAs,
            and make better data-driven decisions using
            modern analytics and artificial intelligence.
        </p>

    </div>
    """)


    html("""
    <div class="card">

        <h3>
            Our Technology Stack
        </h3>

        <p>
            🐍 Python
            &nbsp; • &nbsp;
            🗄️ SQL & Data Engineering
            &nbsp; • &nbsp;
            📊 Power BI & DAX
            &nbsp; • &nbsp;
            🤖 Machine Learning & AI
            &nbsp; • &nbsp;
            🔗 REST APIs & Automation
        </p>

    </div>
    """)


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    html("""
    <div class="section-title">
        Contact LogiIntelli
    </div>

    <div class="section-subtitle">
        Let's discuss your logistics analytics,
        AI, automation, or business intelligence requirements.
    </div>
    """)


    c1, c2 = st.columns(2)


    with c1:

        html("""
        <div class="card">

            <h3>
                📧 Email
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="mailto:sumansekar1205@gmail.com"
                >
                    sumansekar1205@gmail.com
                </a>
            </p>

            <h3>
                📱 Phone / WhatsApp
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://wa.me/918825674102"
                    target="_blank"
                >
                    +91 8825674102
                </a>
            </p>

        </div>
        """)


    with c2:

        html("""
        <div class="card">

            <h3>
                💼 LinkedIn
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://linkedin.com/in/sumansekar12/"
                    target="_blank"
                >
                    linkedin.com/in/sumansekar12/
                </a>
            </p>

            <h3>
                💻 GitHub
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://github.com/Suman-SekarSagadev"
                    target="_blank"
                >
                    github.com/Suman-SekarSagadev
                </a>
            </p>

        </div>
        """)


    html("""
    <div class="hero">

        <h2>
            Let's Build Something Intelligent
        </h2>

        <p>
            Whether you need a Power BI dashboard,
            automated MIS system, SQL analytics solution,
            logistics AI model, API integration,
            or predictive analytics platform,
            LogiIntelli can help transform your operational
            data into measurable business value.
        </p>

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

html("""
<hr style="
    border:0;
    border-top:1px solid #E2E8F0;
    margin-top:50px;
">

<div class="footer">

    <div class="footer-title">
        🚚 LogiIntelli
    </div>

    <div>
        Logistics AI • Data Analytics • Business Intelligence
    </div>

    <br>

    <div>
        Power BI Dashboards • Machine Learning • SQL Data Engineering
        • Shipment Analytics • Supply Chain Intelligence • MIS Automation
    </div>

    <br>

    <div>
        © 2026 LogiIntelli. All Rights Reserved.
    </div>

</div>
""")


# ============================================================
# FLOATING CHATBOT
# ============================================================

html("""
<div style="
    position:fixed;
    right:22px;
    bottom:82px;
    z-index:9999;
">

    <div style="
        background:linear-gradient(135deg,#0B2545,#0066CC);
        color:white;
        padding:12px 17px;
        border-radius:20px;
        box-shadow:0 8px 25px rgba(0,0,0,.18);
        font-size:13px;
        font-weight:700;
    ">

        🤖 LogiIntelli Project Assistant

    </div>

</div>
""")


# ============================================================
# CHATBOT AREA
# ============================================================

html("""
<div class="chat-header">

    <div class="chat-header-title">
        🤖 LogiIntelli Project Assistant
    </div>

    <div class="chat-header-sub">
        Tell us about your project and we'll collect the
        requirements for you.
    </div>

</div>
""")


# ============================================================
# START CHAT
# ============================================================

if not st.session_state.chat_messages:

    initial_message = (
        "👋 Hi! I'm the **LogiIntelli Project Assistant**.\n\n"
        "I can collect your project requirements and submit "
        "them directly to our team.\n\n"
        "Let's get started!\n\n"
        "**What is your name?**"
    )

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": initial_message,
        }
    )


# ============================================================
# DISPLAY CHAT
# ============================================================

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Type your answer here..."
)


if user_input:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # --------------------------------------------------------
    # BOT RESPONSE
    # --------------------------------------------------------

    response = chatbot_response(
        user_input
    )


    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )


    st.rerun()


# ============================================================
# RESET CHAT BUTTON
# ============================================================

if st.session_state.chat_messages:

    reset_col1, reset_col2, reset_col3 = st.columns(
        [1, 1, 1]
    )

    with reset_col2:

        if st.button(
            "🔄 Start New Conversation",
            key="reset_chat",
            use_container_width=True,
        ):

            reset_chat()

            st.rerun()
