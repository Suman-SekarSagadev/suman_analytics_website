```python
from datetime import datetime
import json
import re

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
# GOOGLE APPS SCRIPT URL
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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = True

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli. "
                "I can help identify the right Analytics, "
                "AI, BI or Automation solution for your business."
            ),
        }
    ]


# ============================================================
# RESET CHAT
# ============================================================

def reset_chat():

    st.session_state.chat_open = False

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli. "
                "I can help identify the right Analytics, "
                "AI, BI or Automation solution for your business."
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
   GLOBAL
============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #F8FAFC 0%,
            #FFFFFF 45%,
            #F8FAFC 100%
        );
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 6rem !important;
    max-width: 1400px !important;
}


/* ============================================================
   HEADER
============================================================ */

.top-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 8px 0 18px 0;

    border-bottom: 1px solid #E2E8F0;

    margin-bottom: 18px;
}

.brand-wrapper {
    display: flex;
    flex-direction: column;
}

.brand-title {
    display: block !important;

    font-size: 38px !important;

    font-weight: 900 !important;

    letter-spacing: -1.8px !important;

    line-height: 1.1 !important;

    margin: 0 !important;

    color: #0F172A !important;

    visibility: visible !important;

    opacity: 1 !important;
}

.logi-text {
    color: #0F172A !important;
}

.intelli-text {
    color: #2563EB !important;
}

.brand-subtitle {
    display: block !important;

    font-size: 11px !important;

    color: #64748B !important;

    margin-top: 6px !important;

    letter-spacing: 0.2px !important;

    visibility: visible !important;

    opacity: 1 !important;
}


/* ============================================================
   NAVIGATION
============================================================ */

div.stButton > button {

    border-radius: 9px !important;

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

    box-shadow:
        0 4px 12px
        rgba(37,99,235,0.10) !important;
}


/* ============================================================
   HERO
============================================================ */

.hero {

    padding: 55px 10px 50px 10px;

    text-align: center;
}

.hero-badge {

    display: inline-block;

    background: #EFF6FF;

    color: #2563EB;

    border: 1px solid #DBEAFE;

    padding: 7px 14px;

    border-radius: 30px;

    font-size: 12px;

    font-weight: 700;

    margin-bottom: 20px;
}

.hero-title {

    font-size: 54px;

    line-height: 1.08;

    font-weight: 850;

    letter-spacing: -2.5px;

    color: #0F172A;

    max-width: 950px;

    margin: auto;
}

.hero-title span {

    color: #2563EB;
}

.hero-text {

    max-width: 760px;

    margin: 20px auto;

    color: #64748B;

    font-size: 17px;

    line-height: 1.7;
}


/* ============================================================
   SECTION
============================================================ */

.section-title {

    font-size: 30px;

    font-weight: 800;

    color: #0F172A;

    margin-bottom: 8px;
}

.section-subtitle {

    color: #64748B;

    font-size: 14px;

    margin-bottom: 25px;
}


/* ============================================================
   CARDS
============================================================ */

.card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    padding: 24px;

    height: 100%;

    box-shadow:
        0 5px 20px
        rgba(15,23,42,0.04);

    transition: all 0.25s ease;
}

.card:hover {

    transform: translateY(-3px);

    box-shadow:
        0 12px 30px
        rgba(15,23,42,0.08);

    border-color: #BFDBFE;
}

.card-icon {

    font-size: 28px;

    margin-bottom: 12px;
}

.card-title {

    color: #0F172A;

    font-size: 17px;

    font-weight: 750;

    margin-bottom: 8px;
}

.card-text {

    color: #64748B;

    font-size: 13px;

    line-height: 1.65;
}


/* ============================================================
   METRICS
============================================================ */

.metric-box {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 14px;

    padding: 20px;

    text-align: center;
}

.metric-number {

    font-size: 30px;

    font-weight: 800;

    color: #2563EB;
}

.metric-label {

    font-size: 12px;

    color: #64748B;

    margin-top: 5px;
}


/* ============================================================
   PROJECT
============================================================ */

.project-card {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    padding: 22px;

    margin-bottom: 18px;
}

.project-title {

    font-size: 18px;

    font-weight: 750;

    color: #0F172A;
}

.project-category {

    color: #2563EB;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;

    margin: 7px 0;
}

.project-text {

    color: #64748B;

    font-size: 13px;

    line-height: 1.6;
}


/* ============================================================
   CTA
============================================================ */

.cta {

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E3A8A
        );

    border-radius: 20px;

    padding: 40px;

    text-align: center;

    color: white;

    margin: 45px 0;
}

.cta-title {

    font-size: 30px;

    font-weight: 800;
}

.cta-text {

    color: #CBD5E1;

    font-size: 14px;

    margin: 12px auto 25px auto;

    max-width: 650px;
}


/* ============================================================
   FORM
============================================================ */

.form-card {

    background: white;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 30px;

    box-shadow:
        0 8px 25px
        rgba(15,23,42,0.05);
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    border-top: 1px solid #E2E8F0;

    margin-top: 60px;

    padding: 25px 0;

    text-align: center;

    color: #64748B;

    font-size: 12px;
}


/* ============================================================
   FLOATING CHATBOT
============================================================ */

.st-key-floating_chatbot {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 270px !important;

    max-width:
        calc(100vw - 40px) !important;

    z-index: 999999 !important;

    background: #FFFFFF !important;

    border: 1px solid #CBD5E1 !important;

    border-radius: 14px !important;

    overflow: hidden !important;

    box-shadow:
        0 12px 35px
        rgba(15,23,42,0.20) !important;
}


/* ============================================================
   CHAT HEADER
============================================================ */

.chat-header {

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        ) !important;

    color: #FFFFFF !important;

    padding: 11px 12px !important;

    min-height: 52px !important;

    display: flex !important;

    flex-direction: column !important;

    justify-content: center !important;
}

.chat-header-title {

    color: #FFFFFF !important;

    font-size: 13px !important;

    font-weight: 800 !important;

    line-height: 1.3 !important;

    display: block !important;

    visibility: visible !important;
}

.chat-header-subtitle {

    color: #DBEAFE !important;

    font-size: 9px !important;

    margin-top: 3px !important;

    display: block !important;
}


/* ============================================================
   CLOSE BUTTON
============================================================ */

.st-key-chat_close button {

    width: 28px !important;

    height: 28px !important;

    min-height: 28px !important;

    padding: 0 !important;

    margin-top: 8px !important;

    border-radius: 50% !important;

    border: none !important;

    background:
        rgba(255,255,255,0.18) !important;

    color: #FFFFFF !important;

    font-size: 13px !important;

    font-weight: 800 !important;

    box-shadow: none !important;
}

.st-key-chat_close button:hover {

    background:
        rgba(255,255,255,0.35) !important;

    color: #FFFFFF !important;
}


/* ============================================================
   CHAT BODY
============================================================ */

.chat-body {

    background: #FFFFFF !important;

    padding: 8px !important;

    max-height: 145px !important;

    overflow-y: auto !important;
}


/* ============================================================
   CHAT MESSAGE
============================================================ */

.chat-message {

    padding: 7px 9px !important;

    border-radius: 9px !important;

    margin-bottom: 6px !important;

    font-size: 10px !important;

    line-height: 1.45 !important;

    word-wrap: break-word !important;
}

.chat-assistant {

    background: #EFF6FF !important;

    color: #1E3A8A !important;

    border: 1px solid #DBEAFE !important;

    margin-right: 10px !important;
}

.chat-user {

    background: #0F172A !important;

    color: #FFFFFF !important;

    border: 1px solid #0F172A !important;

    margin-left: 22px !important;
}


/* ============================================================
   CHAT OPTIONS
============================================================ */

.chat-options {

    background: #F8FAFC !important;

    border-top: 1px solid #E2E8F0 !important;

    padding: 7px !important;
}


/* CHAT OPTION BUTTON */

.st-key-floating_chatbot
div.stButton > button {

    min-height: 28px !important;

    height: 28px !important;

    padding: 3px 7px !important;

    margin: 2px 0 !important;

    border-radius: 7px !important;

    font-size: 9px !important;

    font-weight: 600 !important;

    text-align: left !important;

    box-shadow: none !important;
}


/* ============================================================
   CLOSED CHAT BUTTON
============================================================ */

.st-key-open_chat {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    z-index: 999999 !important;
}

.st-key-open_chat button {

    width: 52px !important;

    height: 52px !important;

    min-height: 52px !important;

    padding: 0 !important;

    border-radius: 50% !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        ) !important;

    color: white !important;

    font-size: 21px !important;

    box-shadow:
        0 8px 25px
        rgba(15,23,42,0.25) !important;
}

.st-key-open_chat button:hover {

    color: white !important;

    transform:
        translateY(-2px) !important;
}


/* ============================================================
   REMOVE EXTRA SPACING
============================================================ */

.st-key-floating_chatbot
div[data-testid="stHorizontalBlock"] {

    gap: 0 !important;

    margin: 0 !important;
}

.st-key-floating_chatbot
div[data-testid="stElementContainer"] {

    margin: 0 !important;

    padding: 0 !important;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 600px) {

    .brand-title {

        font-size: 30px !important;
    }

    .brand-subtitle {

        font-size: 9px !important;
    }

    .hero-title {

        font-size: 38px !important;
    }

    .hero-text {

        font-size: 14px !important;
    }

    .st-key-floating_chatbot {

        left: 10px !important;

        bottom: 10px !important;

        width: 250px !important;

        max-width:
            calc(100vw - 20px) !important;
    }

    .chat-body {

        max-height: 130px !important;
    }

    .st-key-open_chat {

        left: 10px !important;

        bottom: 10px !important;
    }
}

</style>
"""
)


# ============================================================
# HEADER
# ============================================================

html(
    """
<div class="top-header">

    <div class="brand-wrapper">

        <div class="brand-title">
            🚚
            <span class="logi-text">Logi</span><span class="intelli-text">Intelli</span>
        </div>

        <div class="brand-subtitle">
            Logistics Analytics • AI & Predictive Intelligence • BI Automation
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
    ("🏠 Home", "Home"),
    ("🛠️ Services", "Services"),
    ("📊 Projects", "Projects"),
    ("📝 Request Project", "Request Project"),
    ("👤 About", "About"),
    ("📞 Contact", "Contact"),
]

for col, (label, page) in zip(nav_cols, navigation):

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
<div class="hero">

    <div class="hero-badge">
        🚚 LOGISTICS • DATA • AI • BUSINESS INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn Your Business Data Into
        <span>Intelligent Decisions</span>
    </div>

    <div class="hero-text">
        LogiIntelli helps businesses transform operational data
        into powerful dashboards, predictive models,
        automation solutions and actionable business intelligence.
    </div>

</div>
"""
    )


    # ========================================================
    # METRICS
    # ========================================================

    cols = st.columns(4)

    metrics = [
        ("11+", "Years Analytics Experience"),
        ("50+", "Analytics Solutions"),
        ("7+", "Team Leadership"),
        ("24/7", "Data-Driven Insights"),
    ]

    for col, (number, label) in zip(cols, metrics):

        with col:

            html(
                f"""
<div class="metric-box">

    <div class="metric-number">
        {number}
    </div>

    <div class="metric-label">
        {label}
    </div>

</div>
"""
            )


    st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # SERVICES
    # ========================================================

    html(
        """
<div class="section-title">
    What We Do
</div>

<div class="section-subtitle">
    End-to-end analytics and technology solutions designed
    for operational and business growth.
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
            "Automate repetitive reports, data pipelines, Excel workflows and operational MIS.",
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL, data transformation, ETL pipelines and scalable reporting datasets.",
        ),

        (
            "🔗",
            "API & Data Integration",
            "Connect APIs, databases, JSON feeds and multiple data sources into one analytics ecosystem.",
        ),
    ]


    service_cols = st.columns(3)

    for i, (icon, title, text) in enumerate(services):

        with service_cols[i % 3]:

            html(
                f"""
<div class="card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-text">
        {text}
    </div>

</div>
"""
            )

        if (i + 1) % 3 == 0:

            st.markdown("<br>", unsafe_allow_html=True)


    # ========================================================
    # WORKFLOW
    # ========================================================

    st.markdown("<br>", unsafe_allow_html=True)

    html(
        """
<div class="section-title">
    How We Work
</div>

<div class="section-subtitle">
    A simple and transparent process from requirement to deployment.
</div>
"""
    )


    workflow = [

        (
            "01",
            "Understand",
            "Understand your business problem and objectives.",
        ),

        (
            "02",
            "Analyze",
            "Study your data sources and identify opportunities.",
        ),

        (
            "03",
            "Build",
            "Develop dashboards, models, automation or data solutions.",
        ),

        (
            "04",
            "Deliver",
            "Deploy the solution and provide actionable insights.",
        ),
    ]


    workflow_cols = st.columns(4)

    for col, (number, title, text) in zip(
        workflow_cols,
        workflow,
    ):

        with col:

            html(
                f"""
<div class="card">

    <div style="
        color:#2563EB;
        font-size:13px;
        font-weight:800;
    ">
        {number}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-text">
        {text}
    </div>

</div>
"""
            )


    # ========================================================
    # TECHNOLOGY
    # ========================================================

    st.markdown("<br><br>", unsafe_allow_html=True)

    html(
        """
<div class="section-title">
    Technology Stack
</div>

<div class="section-subtitle">
    Modern analytics and data technologies.
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


    tech_cols = st.columns(6)

    for col, tech in zip(
        tech_cols,
        technologies,
    ):

        with col:

            html(
                f"""
<div class="metric-box">

    <div style="
        font-weight:700;
        color:#0F172A;
        font-size:13px;
    ">
        {tech}
    </div>

</div>
"""
            )


    # ========================================================
    # CTA
    # ========================================================

    html(
        """
<div class="cta">

    <div class="cta-title">
        Have a Business Problem?
    </div>

    <div class="cta-text">
        Let's convert your data into dashboards,
        automation and intelligent business solutions.
    </div>

</div>
"""
    )


    if st.button(
        "🚀 Start Your Project",
        use_container_width=True,
        key="home_start_project",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# SERVICES PAGE
# ============================================================

def services_page():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        OUR SERVICES
    </div>

    <div class="hero-title">
        Analytics & Technology
        <span>Solutions</span>
    </div>

    <div class="hero-text">
        From business intelligence to machine learning,
        we build solutions around your business requirements.
    </div>

</div>
"""
    )


    service_details = [

        (
            "📊",
            "Power BI & Business Intelligence",
            [
                "Executive dashboards",
                "Operational dashboards",
                "KPI & performance tracking",
                "DAX development",
                "Power Query transformation",
                "Scheduled reporting",
            ],
        ),

        (
            "🚚",
            "Logistics Analytics",
            [
                "Shipment tracking",
                "Hub performance",
                "SLA analytics",
                "TAT analysis",
                "Delivery performance",
                "Exception analytics",
            ],
        ),

        (
            "🤖",
            "AI & Machine Learning",
            [
                "Demand forecasting",
                "Delay prediction",
                "Customer churn prediction",
                "Sales forecasting",
                "Classification models",
                "Predictive analytics",
            ],
        ),

        (
            "⚙️",
            "Automation & MIS",
            [
                "Automated MIS",
                "Excel automation",
                "Python automation",
                "Scheduled reporting",
                "Data refresh automation",
                "Operational workflows",
            ],
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            [
                "Advanced SQL",
                "Data modelling",
                "ETL pipelines",
                "Data transformation",
                "Database optimization",
                "Reporting datasets",
            ],
        ),

        (
            "🔗",
            "API & Data Integration",
            [
                "REST API integration",
                "JSON processing",
                "Database integration",
                "Multi-source analytics",
                "Automated data ingestion",
                "Real-time data pipelines",
            ],
        ),
    ]


    cols = st.columns(2)

    for i, (icon, title, points) in enumerate(
        service_details
    ):

        with cols[i % 2]:

            html(
                f"""
<div class="card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-text">
        {"<br>".join("✓ " + p for p in points)}
    </div>

</div>
"""
            )

        if i % 2 == 1:

            st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PROJECTS PAGE
# ============================================================

def projects_page():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        PROJECTS & SOLUTIONS
    </div>

    <div class="hero-title">
        Real Business Problems.
        <span>Data-Driven Solutions.</span>
    </div>

    <div class="hero-text">
        Example analytics, AI and automation solutions
        designed for operational businesses.
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
            "Forecast future demand using historical business data and time-series forecasting techniques.",
        ),

        (
            "👥",
            "Customer Churn Prediction",
            "Machine Learning",
            "Identify customers with higher churn probability using machine learning classification models.",
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
            "Automate manual reporting workflows using Python, SQL and scheduled data pipelines.",
        ),
    ]


    for icon, title, category, description in projects:

        html(
            f"""
<div class="project-card">

    <div style="font-size:26px;">
        {icon}
    </div>

    <div class="project-category">
        {category}
    </div>

    <div class="project-title">
        {title}
    </div>

    <div class="project-text">
        {description}
    </div>

</div>
"""
        )


# ============================================================
# REQUEST PROJECT PAGE
# ============================================================

def request_project_page():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        START A PROJECT
    </div>

    <div class="hero-title">
        Tell Us About Your
        <span>Requirement</span>
    </div>

    <div class="hero-text">
        Share your business requirement and we will
        get back to you with the right analytics solution.
    </div>

</div>
"""
    )


    html('<div class="form-card">')


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
                "Power BI Dashboard",
                "Logistics Analytics",
                "AI / Machine Learning",
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
            "Please describe your business problem, "
            "current process and expected solution..."
        ),
        height=150,
        key="requirement_form",
    )


    html("</div>")


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
                    "Website Request Project",
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

                    allow_redirects=True,
                )


                if response.status_code == 200:

                    st.success(
                        "✅ Thank you! Your project request "
                        "has been submitted successfully."
                    )

                else:

                    st.error(
                        "Unable to submit your request. "
                        "Please try again."
                    )


            except Exception:

                st.error(
                    "Connection error. "
                    "Please try again later."
                )


# ============================================================
# ABOUT PAGE
# ============================================================

def about_page():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        ABOUT LOGIINTELLI
    </div>

    <div class="hero-title">
        Data. Intelligence.
        <span>Business Growth.</span>
    </div>

    <div class="hero-text">
        LogiIntelli focuses on transforming raw business
        data into meaningful insights, predictive intelligence
        and automated decision-making solutions.
    </div>

</div>
"""
    )


    about_cards = [

        (
            "🎯",
            "Our Mission",
            "Make advanced analytics accessible and useful for real-world businesses.",
        ),

        (
            "💡",
            "Our Approach",
            "Combine business understanding with analytical engineering to build targeted operational solutions.",
        ),
    ]


    cols = st.columns(2)


    for col, (icon, title, text) in zip(
        cols,
        about_cards,
    ):

        with col:

            html(
                f"""
<div class="card">

    <div class="card-icon">
        {icon}
    </div>

    <div class="card-title">
        {title}
    </div>

    <div class="card-text">
        {text}
    </div>

</div>
"""
            )


# ============================================================
# CONTACT PAGE
# ============================================================

def contact_page():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        CONTACT US
    </div>

    <div class="hero-title">
        Let's Discuss Your
        <span>Data Needs</span>
    </div>

    <div class="hero-text">
        Reach out to us directly or request a project quote online.
    </div>

</div>
"""
    )


    cols = st.columns(3)


    with cols[0]:

        html(
            """
<div class="card" style="text-align:center;">

    <div class="card-icon">
        📧
    </div>

    <div class="card-title">
        Email
    </div>

    <div class="card-text">
        support@logiintelli.com
    </div>

</div>
"""
        )


    with cols[1]:

        html(
            """
<div class="card" style="text-align:center;">

    <div class="card-icon">
        📱
    </div>

    <div class="card-title">
        WhatsApp
    </div>

    <div class="card-text">
        +91 8825674102
    </div>

</div>
"""
        )


    with cols[2]:

        html(
            """
<div class="card" style="text-align:center;">

    <div class="card-icon">
        🕒
    </div>

    <div class="card-title">
        Working Hours
    </div>

    <div class="card-text">
        Monday – Friday
        <br>
        9:00 AM – 6:00 PM IST
    </div>

</div>
"""
        )


# ============================================================
# ROUTER
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
# FOOTER
# ============================================================

html(
    """
<div class="footer">

    © LogiIntelli • Logistics Analytics, AI & BI Automation

</div>
"""
)


# ============================================================
# FLOATING CHATBOT
# ============================================================

if st.session_state.chat_open:

    # --------------------------------------------------------
    # CHATBOT CONTAINER
    # --------------------------------------------------------

    st.markdown(
        '<div class="st-key-floating_chatbot">',
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CHAT HEADER
    # --------------------------------------------------------

    header_col1, header_col2 = st.columns(
        [0.84, 0.16]
    )


    with header_col1:

        st.markdown(
            """
            <div class="chat-header">

                <div class="chat-header-title">
                    🤖 LogiIntelli Assistant
                </div>

                <div class="chat-header-subtitle">
                    Project Consultation
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    with header_col2:

        if st.button(
            "✕",
            key="chat_close",
            help="Close chatbot",
        ):

            reset_chat()

            st.rerun()


    # --------------------------------------------------------
    # CHAT BODY
    # --------------------------------------------------------

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


        message_text = msg["text"]


        # Convert bold markdown
        message_text = re.sub(
            r"\*\*(.*?)\*\*",
            r"<strong>\1</strong>",
            message_text,
        )


        st.markdown(
            f"""
            <div class="chat-message {role_class}">
                {message_text}
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CHAT OPTIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="chat-options">',
        unsafe_allow_html=True,
    )


    options = [

        "📊 Power BI Dashboard",

        "🚚 Logistics Analytics",

        "🤖 AI / Machine Learning",

        "⚙️ Automation / MIS",

        "🗄️ SQL / Data Engineering",

        "💡 Not Sure",
    ]


    for option in options:

        if st.button(
            option,
            key=f"chat_option_{option}",
            use_container_width=True,
        ):

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
                        f"Great! Let's discuss your requirements "
                        f"regarding **{option}**. "
                        "Please share your business requirement "
                        "or contact details."
                    ),
                }
            )


            st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CLOSE OUTER CONTAINER
    # --------------------------------------------------------

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# CLOSED CHAT BUTTON
# ============================================================

else:

    st.markdown(
        '<div class="st-key-open_chat">',
        unsafe_allow_html=True,
    )


    if st.button(
        "💬",
        key="open_chat",
        help="Open LogiIntelli Assistant",
    ):

        st.session_state.chat_open = True

        st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )
```
