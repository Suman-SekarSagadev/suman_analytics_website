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
                "👋 Hi! Welcome to LogiIntelli.<br><br>"
                "I can help you with Analytics, AI, BI, "
                "Automation and Data solutions."
            ),
        }
    ]


def reset_chat():
    st.session_state.chat_open = False
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli.<br><br>"
                "I can help you with Analytics, AI, BI, "
                "Automation and Data solutions."
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
   FONT
============================================================ */

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);

html,
body {
    font-family: "Inter", sans-serif !important;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #F8FAFC 0%,
            #FFFFFF 40%,
            #F8FAFC 100%
        );
}


/* ============================================================
   STREAMLIT MAIN CONTAINER
============================================================ */

.block-container {
    max-width: 1380px !important;
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
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

.top-header {
    width: 100%;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;

    padding: 12px 0 20px 0;

    margin-bottom: 18px;

    border-bottom: 1px solid #E2E8F0;

    position: relative !important;
    z-index: 100 !important;

    visibility: visible !important;
    opacity: 1 !important;
}

.brand-wrapper {
    display: flex !important;
    flex-direction: column !important;

    visibility: visible !important;
    opacity: 1 !important;
}

.brand-title {
    display: block !important;

    font-size: 38px !important;
    font-weight: 900 !important;

    line-height: 1.1 !important;

    letter-spacing: -1.8px !important;

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

    margin-top: 7px !important;

    font-size: 11px !important;

    color: #64748B !important;

    letter-spacing: 0.2px !important;

    visibility: visible !important;
    opacity: 1 !important;
}


/* ============================================================
   NAVIGATION BUTTONS
============================================================ */

div.stButton > button {
    border-radius: 10px !important;

    border: 1px solid #E2E8F0 !important;

    background: #FFFFFF !important;

    color: #334155 !important;

    font-weight: 600 !important;

    min-height: 40px !important;

    transition:
        all 0.2s ease !important;
}

div.stButton > button:hover {
    border-color: #2563EB !important;

    color: #2563EB !important;

    background: #F8FAFF !important;

    box-shadow:
        0 5px 15px rgba(37,99,235,0.10) !important;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    position: relative;

    padding: 65px 20px 55px 20px;

    text-align: center;

    overflow: hidden;
}

.hero::before {
    content: "";

    position: absolute;

    width: 420px;
    height: 420px;

    background: #DBEAFE;

    border-radius: 50%;

    filter: blur(100px);

    opacity: 0.35;

    top: -180px;
    left: 50%;

    transform: translateX(-50%);
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;

    padding: 8px 16px;

    border-radius: 30px;

    background: #EFF6FF;

    border: 1px solid #DBEAFE;

    color: #2563EB;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 0.5px;

    margin-bottom: 20px;
}

.hero-title {
    max-width: 950px;

    margin: auto;

    font-size: 55px;

    line-height: 1.06;

    font-weight: 900;

    letter-spacing: -2.8px;

    color: #0F172A;
}

.hero-title span {
    color: #2563EB;
}

.hero-text {
    max-width: 760px;

    margin: 22px auto 0 auto;

    font-size: 17px;

    line-height: 1.7;

    color: #64748B;
}


/* ============================================================
   SECTION
============================================================ */

.section-title {
    font-size: 30px;

    line-height: 1.2;

    font-weight: 850;

    color: #0F172A;

    margin-top: 10px;

    margin-bottom: 8px;
}

.section-subtitle {
    color: #64748B;

    font-size: 14px;

    line-height: 1.6;

    margin-bottom: 25px;
}


/* ============================================================
   CARDS
============================================================ */

.card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 26px;

    min-height: 180px;

    box-shadow:
        0 6px 22px rgba(15,23,42,0.04);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

.card:hover {
    transform: translateY(-5px);

    border-color: #BFDBFE;

    box-shadow:
        0 16px 35px rgba(15,23,42,0.08);
}

.card-icon {
    font-size: 30px;

    margin-bottom: 15px;
}

.card-title {
    color: #0F172A;

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 9px;
}

.card-text {
    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   METRICS
============================================================ */

.metric-box {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    padding: 22px 15px;

    text-align: center;

    box-shadow:
        0 5px 18px rgba(15,23,42,0.035);
}

.metric-number {
    font-size: 32px;

    font-weight: 900;

    color: #2563EB;

    line-height: 1.1;
}

.metric-label {
    font-size: 11px;

    color: #64748B;

    margin-top: 7px;
}


/* ============================================================
   PROJECT CARD
============================================================ */

.project-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 25px;

    margin-bottom: 18px;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.035);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

.project-card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 15px 30px rgba(15,23,42,0.08);
}

.project-icon {
    font-size: 28px;

    margin-bottom: 8px;
}

.project-category {
    color: #2563EB;

    font-size: 10px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.6px;

    margin-bottom: 7px;
}

.project-title {
    font-size: 18px;

    font-weight: 800;

    color: #0F172A;

    margin-bottom: 8px;
}

.project-text {
    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   TECHNOLOGY
============================================================ */

.tech-box {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 12px;

    padding: 15px 10px;

    text-align: center;

    font-size: 13px;

    font-weight: 700;

    color: #0F172A;

    transition: all 0.2s ease;
}

.tech-box:hover {
    border-color: #93C5FD;

    color: #2563EB;

    transform: translateY(-2px);
}


/* ============================================================
   CTA
============================================================ */

.cta {
    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #0F172A 0%,
            #1E3A8A 100%
        );

    border-radius: 22px;

    padding: 48px 30px;

    text-align: center;

    color: white;

    margin: 55px 0;
}

.cta-title {
    font-size: 31px;

    font-weight: 850;

    margin-bottom: 8px;
}

.cta-text {
    color: #CBD5E1;

    font-size: 14px;

    line-height: 1.7;

    max-width: 650px;

    margin: 0 auto 25px auto;
}


/* ============================================================
   FORM
============================================================ */

.form-section {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 20px;

    padding: 30px;

    box-shadow:
        0 8px 28px rgba(15,23,42,0.05);

    margin-bottom: 30px;
}


/* ============================================================
   CONTACT
============================================================ */

.contact-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 28px;

    text-align: center;

    min-height: 175px;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.04);
}

.contact-icon {
    font-size: 30px;

    margin-bottom: 12px;
}

.contact-title {
    color: #0F172A;

    font-size: 16px;

    font-weight: 800;

    margin-bottom: 7px;
}

.contact-text {
    color: #64748B;

    font-size: 13px;

    line-height: 1.6;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    border-top: 1px solid #E2E8F0;

    margin-top: 60px;

    padding: 28px 0;

    text-align: center;

    color: #64748B;

    font-size: 12px;
}


/* ============================================================
   CHATBOT
============================================================ */

.chat-wrapper {
    position: fixed;

    left: 20px;

    bottom: 20px;

    width: 280px;

    max-width: calc(100vw - 40px);

    z-index: 999999;

    background: #FFFFFF;

    border: 1px solid #DCE5EF;

    border-radius: 16px;

    box-shadow:
        0 15px 40px rgba(15,23,42,0.18);

    overflow: hidden;
}

.chat-header {
    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        );

    color: white;

    padding: 13px 14px;
}

.chat-header-title {
    font-size: 13px;

    font-weight: 800;
}

.chat-header-subtitle {
    font-size: 9px;

    color: #CBD5E1;

    margin-top: 3px;
}

.chat-body {
    padding: 10px;

    max-height: 230px;

    overflow-y: auto;

    background: #F8FAFC;
}

.chat-message {
    padding: 8px 10px;

    border-radius: 10px;

    margin: 6px 0;

    font-size: 10px;

    line-height: 1.5;
}

.chat-assistant {
    background: #EFF6FF;

    color: #1E3A8A;

    border: 1px solid #DBEAFE;
}

.chat-user {
    background: #0F172A;

    color: #FFFFFF;

    margin-left: 25px;
}

.chat-options {
    padding: 9px;

    background: #FFFFFF;

    border-top: 1px solid #E2E8F0;
}

.chat-close-button button {
    border: none !important;

    background: rgba(255,255,255,0.15) !important;

    color: white !important;

    min-height: 25px !important;

    height: 25px !important;

    width: 25px !important;

    border-radius: 50% !important;

    padding: 0 !important;
}

.chat-close-button button:hover {
    background: rgba(255,255,255,0.3) !important;
}


/* ============================================================
   CHAT OPEN BUTTON
============================================================ */

.chat-open {
    position: fixed;

    left: 20px;

    bottom: 20px;

    z-index: 999999;
}

.chat-open button {
    width: 54px !important;

    height: 54px !important;

    min-height: 54px !important;

    border-radius: 50% !important;

    border: none !important;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        ) !important;

    color: white !important;

    font-size: 20px !important;

    box-shadow:
        0 10px 25px rgba(15,23,42,0.2) !important;
}


/* ============================================================
   STREAMLIT INPUTS
============================================================ */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
}

label {
    font-weight: 600 !important;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .brand-title {
        font-size: 30px !important;
    }

    .brand-subtitle {
        font-size: 9px !important;
    }

    .hero {
        padding: 45px 10px 40px 10px;
    }

    .hero-title {
        font-size: 39px;
        letter-spacing: -1.8px;
    }

    .hero-text {
        font-size: 14px;
    }

    .section-title {
        font-size: 25px;
    }

    .chat-wrapper {
        left: 10px;

        bottom: 10px;

        width: 260px;

        max-width: calc(100vw - 20px);
    }

    .chat-open {
        left: 10px;

        bottom: 10px;
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
            🚚 <span class="logi-text">Logi</span><span class="intelli-text">Intelli</span>
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

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    html(
        """
<div class="hero">

    <div class="hero-content">

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

</div>
"""
    )


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # SERVICES
    # --------------------------------------------------------

    html(
        """
<div class="section-title">
    What We Do
</div>

<div class="section-subtitle">
    End-to-end analytics and technology solutions designed
    for operational efficiency and business growth.
</div>
"""
    )


    services = [

        (
            "📊",
            "Power BI & Business Intelligence",
            "Interactive dashboards, KPI monitoring, DAX, Power Query and executive reporting."
        ),

        (
            "🚚",
            "Logistics Analytics",
            "Shipment analytics, hub performance, SLA, TAT, delivery and operational intelligence."
        ),

        (
            "🤖",
            "AI & Machine Learning",
            "Forecasting, prediction, classification, churn models and intelligent decision systems."
        ),

        (
            "⚙️",
            "Automation & MIS",
            "Automate repetitive reports, Excel workflows, Python processes and operational MIS."
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL, data transformation, ETL pipelines and reporting datasets."
        ),

        (
            "🔗",
            "API & Data Integration",
            "Connect APIs, databases, JSON feeds and multiple data sources into one analytics ecosystem."
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


    # --------------------------------------------------------
    # WORKFLOW
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    html(
        """
<div class="section-title">
    How We Work
</div>

<div class="section-subtitle">
    A simple and transparent process from business requirement
    to deployment.
</div>
"""
    )


    workflow = [

        (
            "01",
            "Understand",
            "Understand your business problem and objectives."
        ),

        (
            "02",
            "Analyze",
            "Study your data sources and identify opportunities."
        ),

        (
            "03",
            "Build",
            "Develop dashboards, models, automation or data solutions."
        ),

        (
            "04",
            "Deliver",
            "Deploy the solution and provide actionable insights."
        ),
    ]


    workflow_cols = st.columns(4)

    for col, (number, title, text) in zip(
        workflow_cols,
        workflow
    ):

        with col:

            html(
                f"""
<div class="card">

    <div style="
        color:#2563EB;
        font-size:13px;
        font-weight:900;
        margin-bottom:10px;
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


    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    st.markdown("<br><br>", unsafe_allow_html=True)

    html(
        """
<div class="section-title">
    Technology Stack
</div>

<div class="section-subtitle">
    Modern analytics, cloud and data technologies.
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
        technologies
    ):

        with col:

            html(
                f"""
<div class="tech-box">
    {tech}
</div>
"""
            )


    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

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

    <div class="hero-content">

        <div class="hero-badge">
            OUR SERVICES
        </div>

        <div class="hero-title">
            Analytics & Technology
            <span>Solutions</span>
        </div>

        <div class="hero-text">
            From business intelligence to machine learning,
            we build practical solutions around your business requirements.
        </div>

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

    <div class="hero-content">

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


    cols = st.columns(2)

    for i, (
        icon,
        title,
        category,
        description
    ) in enumerate(projects):

        with cols[i % 2]:

            html(
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

    <div class="project-text">
        {description}
    </div>

</div>
"""
            )

        if i % 2 == 1:
            st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# REQUEST PROJECT PAGE
# ============================================================

def request_project_page():

    html(
        """
<div class="hero">

    <div class="hero-content">

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

</div>
"""
    )


    html(
        """
<div class="form-section">
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


    html(
        """
</div>
"""
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

                    st.balloons()

                else:

                    st.error(
                        "Unable to submit your request. "
                        "Please try again."
                    )


            except Exception:

                st.error(
                    "Connection error. Please try again later."
                )


# ============================================================
# ABOUT PAGE
# ============================================================

def about_page():

    html(
        """
<div class="hero">

    <div class="hero-content">

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

</div>
"""
    )


    cols = st.columns(2)


    with cols[0]:

        html(
            """
<div class="card">

    <div class="card-icon">
        🎯
    </div>

    <div class="card-title">
        Our Mission
    </div>

    <div class="card-text">
        Make advanced analytics accessible and useful
        for real-world businesses.
    </div>

</div>
"""
        )


    with cols[1]:

        html(
            """
<div class="card">

    <div class="card-icon">
        💡
    </div>

    <div class="card-title">
        Our Approach
    </div>

    <div class="card-text">
        Combine business understanding with analytical
        engineering to build targeted operational solutions.
    </div>

</div>
"""
        )


    st.markdown("<br><br>", unsafe_allow_html=True)


    html(
        """
<div class="section-title">
    Why Analytics Matters
</div>

<div class="section-subtitle">
    Businesses generate large amounts of operational data.
    The right analytics approach can turn that data into
    measurable business decisions.
</div>
"""
    )


    cols = st.columns(3)


    about_points = [

        (
            "📊",
            "Visibility",
            "Get a clear view of your business performance through dashboards and KPIs."
        ),

        (
            "🔮",
            "Prediction",
            "Use historical data and machine learning to anticipate future outcomes."
        ),

        (
            "⚡",
            "Automation",
            "Reduce manual work by automating repetitive reporting and data processes."
        ),
    ]


    for col, (icon, title, text) in zip(
        cols,
        about_points
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

    <div class="hero-content">

        <div class="hero-badge">
            CONTACT US
        </div>

        <div class="hero-title">
            Let's Discuss Your
            <span>Data Needs</span>
        </div>

        <div class="hero-text">
            Reach out directly or submit a project request
            and let's discuss how analytics can help your business.
        </div>

    </div>

</div>
"""
    )


    cols = st.columns(3)


    with cols[0]:

        html(
            """
<div class="contact-card">

    <div class="contact-icon">
        📧
    </div>

    <div class="contact-title">
        Email
    </div>

    <div class="contact-text">
        support@logiintelli.com
    </div>

</div>
"""
        )


    with cols[1]:

        html(
            """
<div class="contact-card">

    <div class="contact-icon">
        📱
    </div>

    <div class="contact-title">
        WhatsApp
    </div>

    <div class="contact-text">
        +91 8825674102
    </div>

</div>
"""
        )


    with cols[2]:

        html(
            """
<div class="contact-card">

    <div class="contact-icon">
        🕒
    </div>

    <div class="contact-title">
        Working Hours
    </div>

    <div class="contact-text">
        Monday – Friday<br>
        9:00 AM – 6:00 PM IST
    </div>

</div>
"""
        )


    st.markdown("<br><br>", unsafe_allow_html=True)


    if st.button(
        "🚀 Request a Project",
        use_container_width=True,
        key="contact_project",
    ):

        st.session_state.page = "Request Project"

        st.rerun()


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

    © 2026 LogiIntelli

    <br>

    Logistics Analytics • AI • Business Intelligence • Automation

</div>
"""
)


# ============================================================
# FLOATING CHATBOT
# ============================================================

if st.session_state.chat_open:

    html(
        """
<div class="chat-wrapper">

    <div class="chat-header">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <div>

                <div class="chat-header-title">
                    🤖 LogiIntelli AI Assistant
                </div>

                <div class="chat-header-subtitle">
                    Analytics & Project Consultation
                </div>

            </div>

        </div>

    </div>

</div>
"""
    )


    # Chat header close button
    close_col1, close_col2 = st.columns(
        [0.88, 0.12]
    )


    with close_col2:

        if st.button(
            "✕",
            key="chat_close",
            help="Close chatbot",
        ):

            reset_chat()

            st.rerun()


    # Messages
    html(
        """
<div class="chat-body">
"""
    )


    for msg in st.session_state.chat_messages:

        role_class = (
            "chat-assistant"
            if msg["role"] == "assistant"
            else "chat-user"
        )

        html(
            f"""
<div class="chat-message {role_class}">
    {msg["text"]}
</div>
"""
        )


    html(
        """
</div>
"""
    )


    # Options
    html(
        """
<div class="chat-options">
"""
    )


    options = [

        "📊 Power BI Dashboard",

        "🚚 Logistics Analytics",

        "🤖 AI / Machine Learning",

        "⚙️ Automation / MIS",

        "🗄️ SQL / Data Engineering",

        "💡 Not Sure",
    ]


    option_cols = st.columns(2)


    for i, option in enumerate(options):

        with option_cols[i % 2]:

            if st.button(
                option,
                key=f"chat_option_{i}",
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
                            f"Great choice! 👍<br><br>"
                            f"We can discuss your "
                            f"<b>{option}</b> requirement.<br><br>"
                            "Please use the <b>Request Project</b> "
                            "page to share your business requirement."
                        ),
                    }
                )


                st.rerun()


    html(
        """
</div>
"""
    )


else:

    html(
        """
<div class="chat-open">
"""
    )


    if st.button(
        "💬",
        key="open_chat_btn",
        help="Open AI Assistant",
    ):

        st.session_state.chat_open = True

        st.rerun()


    html(
        """
</div>
"""
    )
