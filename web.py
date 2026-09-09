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
# GOOGLE APPS SCRIPT URL
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
# CSS
# ============================================================

st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

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

.block-container {
    padding-top: 1rem;
    padding-bottom: 4rem;
}

/* ============================================================
   HEADER
   ============================================================ */

.logo-title {
    font-size: 27px;
    font-weight: 800;
    color: #0B2545;
}

.logo-subtitle {
    font-size: 12px;
    color: #60758A;
    margin-top: 3px;
}

/* ============================================================
   NAVIGATION
   ============================================================ */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #d9e3ee;
    background: white;
    color: #0B2545;
    font-weight: 600;
    min-height: 40px;
}

.stButton > button:hover {
    border-color: #0066CC;
    color: #0066CC;
}

/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 65px 45px;
    border-radius: 28px;
    background:
        linear-gradient(
            135deg,
            #071d35 0%,
            #0b3c6f 45%,
            #0066cc 100%
        );
    color: white;
    margin-top: 20px;
    margin-bottom: 35px;
    box-shadow:
        0 20px 60px rgba(0, 50, 100, 0.20);
}

.hero-small-title {
    color: #7ec8ff;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.hero h1 {
    font-size: 50px;
    line-height: 1.1;
    margin: 0 0 15px 0;
}

.hero p {
    max-width: 850px;
    color: #dbeeff;
    font-size: 18px;
    line-height: 1.7;
}

/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #0B2545;
    margin-top: 35px;
    margin-bottom: 20px;
}

/* ============================================================
   CARDS
   ============================================================ */

.service-card,
.project-card,
.info-card,
.metric-card {
    background: rgba(255,255,255,0.96);
    border: 1px solid #e2eaf2;
    border-radius: 18px;
    padding: 24px;
    box-shadow:
        0 8px 30px rgba(15,42,70,0.06);
    height: 100%;
}

.service-card:hover,
.project-card:hover {
    transform: translateY(-4px);
    box-shadow:
        0 15px 40px rgba(15,42,70,0.12);
}

.metric-number {
    font-size: 34px;
    font-weight: 800;
    color: #0066CC;
}

.metric-label {
    color: #60758A;
    font-size: 14px;
    margin-top: 5px;
}

/* ============================================================
   CHAT LAUNCHER
   ============================================================ */

.chat-launcher-space {
    height: 80px;
}

.chat-launcher-box {
    position: fixed;
    right: 22px;
    bottom: 22px;
    z-index: 9999;
}

.chat-launcher-label {
    background:
        linear-gradient(
            135deg,
            #0B2545,
            #0066CC
        );
    color: white;
    padding: 13px 20px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 14px;
    box-shadow:
        0 10px 35px rgba(0,82,160,0.35);
}

/* ============================================================
   CHAT PANEL
   ============================================================ */

.chat-title {
    font-size: 23px;
    font-weight: 800;
    color: #0B2545;
    margin-bottom: 3px;
}

.chat-status {
    color: #1d9b52;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 15px;
}

.chat-info {
    background: #f2f7fc;
    padding: 13px;
    border-radius: 12px;
    color: #52677b;
    font-size: 13px;
    line-height: 1.6;
    margin-bottom: 15px;
}

.chat-summary {
    background: #f7faff;
    border: 1px solid #dbe8f5;
    border-radius: 12px;
    padding: 15px;
    font-size: 13px;
    line-height: 1.6;
}

/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: #718297;
    font-size: 12px;
    padding: 30px 10px;
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .hero {
        padding: 40px 25px;
    }

    .hero h1 {
        font-size: 36px;
    }

    .hero p {
        font-size: 15px;
    }

    .chat-launcher-box {
        right: 14px;
        bottom: 14px;
    }

    .chat-launcher-label {
        padding: 12px 16px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FUNCTIONS
# ============================================================

def valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email.strip()))


def reset_chat():

    st.session_state.chat_messages = []
    st.session_state.chat_step = 0
    st.session_state.chat_data = {}
    st.session_state.chat_submitted = False


def submit_to_google_sheet():

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
            headers={
                "Content-Type": "text/plain;charset=utf-8"
            },
            timeout=20,
            allow_redirects=True
        )

        if response.status_code == 200:
            return True

        return False

    except Exception:
        return False


# ============================================================
# CHATBOT RESPONSE
# ============================================================

def chatbot_response(message):

    message = message.strip()

    step = st.session_state.chat_step

    data = st.session_state.chat_data

    # --------------------------------------------------------
    # NAME
    # --------------------------------------------------------

    if step == 0:

        data["name"] = message

        st.session_state.chat_step = 1

        return (
            f"Nice to meet you, **{message}**! 👋\n\n"
            "What is your **company name**?"
        )

    # --------------------------------------------------------
    # COMPANY
    # --------------------------------------------------------

    if step == 1:

        data["company"] = message

        st.session_state.chat_step = 2

        return (
            "Great! 👍\n\n"
            "Which industry does your company operate in?\n\n"
            "Courier / Logistics / E-commerce / "
            "Manufacturing / Retail / Other"
        )

    # --------------------------------------------------------
    # INDUSTRY
    # --------------------------------------------------------

    if step == 2:

        data["industry"] = message

        st.session_state.chat_step = 3

        return (
            "What solution are you looking for?\n\n"
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

    # --------------------------------------------------------
    # SERVICE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # REQUIREMENT
    # --------------------------------------------------------

    if step == 4:

        data["requirement"] = message

        st.session_state.chat_step = 5

        return (
            "Perfect! What is your current **data source**?\n\n"
            "Excel / CSV / MySQL / SQL Server / "
            "PostgreSQL / ERP / REST API / "
            "Multiple Sources / Other"
        )

    # --------------------------------------------------------
    # DATA SOURCE
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
    # VOLUME
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
    # TIMELINE
    # --------------------------------------------------------

    if step == 7:

        data["timeline"] = message

        st.session_state.chat_step = 8

        return (
            "Almost done! 😊\n\n"
            "Please provide your **business email address**."
        )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    if step == 8:

        if not valid_email(message):

            return (
                "⚠️ Please enter a valid email address.\n\n"
                "Example: **name@company.com**"
            )

        data["email"] = message

        st.session_state.chat_step = 9

        return (
            "Thanks! 📧\n\n"
            "Please provide your **Phone / WhatsApp number**.\n\n"
            "You can type **Skip** if you don't want to provide it."
        )

    # --------------------------------------------------------
    # PHONE
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CONFIRMATION
    # --------------------------------------------------------

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

            success = submit_to_google_sheet()

            if success:

                st.session_state.chat_submitted = True

                st.session_state.chat_step = 11

                return (
                    "🎉 **Your project request has been submitted successfully!**\n\n"
                    "Thank you for contacting **LogiIntelli**.\n\n"
                    "Our team will review your requirement "
                    "and contact you using the details provided.\n\n"
                    "🚚 LogiIntelli\n"
                    "Logistics AI • Data Analytics • BI"
                )

            else:

                return (
                    "❌ I couldn't submit your request right now.\n\n"
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

    # --------------------------------------------------------
    # FINISHED
    # --------------------------------------------------------

    return (
        "Your conversation is complete. 🎉\n\n"
        "Click **Start New Conversation** if you have another requirement."
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
""",
    unsafe_allow_html=True
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
            key=f"navigation_{i}",
            use_container_width=True
        ):

            st.session_state.page = page_name

            st.rerun()


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    st.markdown(
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
""",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Our Impact</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("10+", "Years Experience"),
        ("50+", "Analytics & AI Pipelines"),
        ("24/7", "Automated Systems"),
        ("BI + AI", "Technology Architecture")
    ]

    for col, metric in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        number, label = metric

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
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">What We Build</div>',
        unsafe_allow_html=True
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

            st.markdown(
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
""",
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">How We Work</div>',
        unsafe_allow_html=True
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

    for col, item in zip(cols, workflow):

        number, title, description = item

        with col:

            st.markdown(
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
""",
                unsafe_allow_html=True
            )


# ============================================================
# SERVICES PAGE
# ============================================================

elif page == "Services":

    st.markdown(
        '<div class="section-title">Our Services</div>',
        unsafe_allow_html=True
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

            st.markdown(
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
""",
                unsafe_allow_html=True
            )


# ============================================================
# PROJECTS PAGE
# ============================================================

elif page == "Projects":

    st.markdown(
        '<div class="section-title">Projects & Solutions</div>',
        unsafe_allow_html=True
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

            st.markdown(
                f"""
<div class="project-card">

    <div style="font-size:34px;">
        {icon}
    </div>

    <h3 style="color:#0B2545;">
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
""",
                unsafe_allow_html=True
            )


# ============================================================
# REQUEST PROJECT PAGE
# ============================================================

elif page == "Request Project":

    st.markdown(
        '<div class="section-title">Request a Project</div>',
        unsafe_allow_html=True
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
# ABOUT PAGE
# ============================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">About LogiIntelli</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
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
""",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Technology Stack</div>',
        unsafe_allow_html=True
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
                unsafe_allow_html=True
            )


# ============================================================
# CONTACT PAGE
# ============================================================

elif page == "Contact":

    st.markdown(
        '<div class="section-title">Let\'s Work Together</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Have a logistics analytics, BI, automation or AI requirement?"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
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
""",
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
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
""",
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
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
""",
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
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
""",
            unsafe_allow_html=True
        )


# ============================================================
# FLOATING CHATBOT BUTTON
# ============================================================

st.markdown(
    """
<div class="chat-launcher-box">

    <div class="chat-launcher-label">
        🤖 Chat with us
    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# CHATBOT CONTROL
# ============================================================

st.markdown(
    "<div class='chat-launcher-space'></div>",
    unsafe_allow_html=True
)

chat_button_col = st.columns([8, 1])

with chat_button_col[1]:

    if st.button(
        "🤖",
        key="open_chat",
        help="Open LogiIntelli Project Assistant"
    ):

        st.session_state.chat_open = True

        if not st.session_state.chat_messages:

            st.session_state.chat_messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "👋 Hi! I'm the **LogiIntelli Project Assistant**.\n\n"
                        "I can collect your project requirements "
                        "and submit them directly to our team.\n\n"
                        "Let's get started!\n\n"
                        "**What is your name?**"
                    )
                }
            )

        st.rerun()


# ============================================================
# CHAT WINDOW
# ============================================================

if st.session_state.chat_open:

    st.markdown(
        '<div class="section-title">🤖 LogiIntelli Project Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="chat-status">
    ● Online • Project Support
</div>

<div class="chat-info">
    I will ask a few questions about your project.
    Your answers will be submitted securely to our
    project request Google Sheet after confirmation.
</div>
""",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CHAT MESSAGES
    # --------------------------------------------------------

    for msg in st.session_state.chat_messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    if not st.session_state.chat_submitted:

        user_input = st.chat_input(
            "Type your answer here..."
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

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    reset_col1, reset_col2, reset_col3 = st.columns(
        [1, 2, 1]
    )

    with reset_col2:

        if st.button(
            "🔄 Start New Conversation",
            key="start_new_chat",
            use_container_width=True
        ):

            reset_chat()

            st.session_state.chat_open = True

            st.rerun()

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    if st.button(
        "✕ Close Assistant",
        key="close_chat",
        use_container_width=True
    ):

        st.session_state.chat_open = False

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">

    🚚 <b>LogiIntelli</b>

    <br><br>

    Logistics Analytics • AI • BI • Automation

    <br><br>

    © 2026 LogiIntelli. All rights reserved.

</div>
""",
    unsafe_allow_html=True
)
