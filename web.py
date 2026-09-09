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
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli.<br>"
                "I can help with Analytics, AI, BI and Automation."
            ),
        }
    ]


# ============================================================
# CHAT FUNCTIONS
# ============================================================

def open_chat():
    st.session_state.chat_open = True


def close_chat():
    st.session_state.chat_open = False


def add_chat_message(user_text, assistant_text):

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "text": user_text,
        }
    )

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "text": assistant_text,
        }
    )


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
.stApp {
    font-family: "Inter", sans-serif !important;
}

.stApp {
    background: #F8FAFC !important;
}

.block-container {
    max-width: 1380px !important;
    padding-top: 1rem !important;
    padding-bottom: 80px !important;
}


/* ============================================================
   HIDE STREAMLIT DEFAULT
============================================================ */

#MainMenu {
    visibility: hidden !important;
}

footer {
    visibility: hidden !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}


/* ============================================================
   HEADER
============================================================ */

.logi-header {
    width: 100%;
    box-sizing: border-box;

    padding: 12px 0 18px 0;

    margin-bottom: 18px;

    border-bottom: 1px solid #E2E8F0;

    background: transparent;

    position: relative;

    z-index: 10;
}

.logi-brand {
    font-size: 38px;

    line-height: 1.1;

    font-weight: 900;

    letter-spacing: -1.8px;

    color: #0F172A;

    margin: 0;
}

.logi-brand-blue {
    color: #2563EB;
}

.logi-subtitle {
    margin-top: 7px;

    color: #64748B;

    font-size: 11px;

    font-weight: 500;

    letter-spacing: 0.2px;
}


/* ============================================================
   NAVIGATION
============================================================ */

.nav-row {
    margin-bottom: 25px;
}

div[data-testid="stButton"] > button {
    border-radius: 10px !important;

    border: 1px solid #E2E8F0 !important;

    background: #FFFFFF !important;

    color: #334155 !important;

    font-size: 13px !important;

    font-weight: 600 !important;

    min-height: 40px !important;

    transition: all 0.2s ease !important;
}

div[data-testid="stButton"] > button:hover {
    border-color: #2563EB !important;

    color: #2563EB !important;

    background: #EFF6FF !important;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    text-align: center;

    padding: 70px 20px 65px 20px;

    background:
        radial-gradient(
            circle at top center,
            #DBEAFE 0%,
            #F8FAFC 42%,
            #F8FAFC 100%
        );

    border-radius: 25px;

    margin-bottom: 35px;
}

.hero-badge {
    display: inline-block;

    padding: 8px 15px;

    border-radius: 30px;

    background: #EFF6FF;

    border: 1px solid #BFDBFE;

    color: #2563EB;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.7px;

    margin-bottom: 20px;
}

.hero-title {
    max-width: 950px;

    margin: auto;

    color: #0F172A;

    font-size: 56px;

    line-height: 1.05;

    font-weight: 900;

    letter-spacing: -3px;
}

.hero-title-blue {
    color: #2563EB;
}

.hero-description {
    max-width: 760px;

    margin: 22px auto 0 auto;

    color: #64748B;

    font-size: 16px;

    line-height: 1.7;
}


/* ============================================================
   SECTION
============================================================ */

.section-title {
    color: #0F172A;

    font-size: 30px;

    line-height: 1.2;

    font-weight: 850;

    margin-top: 35px;

    margin-bottom: 8px;
}

.section-description {
    color: #64748B;

    font-size: 14px;

    line-height: 1.6;

    margin-bottom: 25px;
}


/* ============================================================
   CARDS
============================================================ */

.info-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 25px;

    min-height: 175px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);

    box-sizing: border-box;

    margin-bottom: 18px;

    transition: 0.2s ease;
}

.info-card:hover {
    transform: translateY(-3px);

    border-color: #BFDBFE;

    box-shadow:
        0 12px 28px rgba(15,23,42,0.08);
}

.card-icon {
    font-size: 30px;

    margin-bottom: 13px;
}

.card-title {
    color: #0F172A;

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 8px;
}

.card-description {
    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   METRICS
============================================================ */

.metric-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    padding: 23px 10px;

    text-align: center;

    box-shadow:
        0 4px 15px rgba(15,23,42,0.035);
}

.metric-value {
    color: #2563EB;

    font-size: 31px;

    font-weight: 900;
}

.metric-label {
    color: #64748B;

    font-size: 11px;

    margin-top: 5px;
}


/* ============================================================
   PROJECT
============================================================ */

.project-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 25px;

    min-height: 205px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);

    margin-bottom: 18px;
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

    letter-spacing: 0.7px;

    margin-bottom: 8px;
}

.project-title {
    color: #0F172A;

    font-size: 18px;

    font-weight: 800;

    margin-bottom: 8px;
}

.project-description {
    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   TECHNOLOGY
============================================================ */

.tech {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 12px;

    padding: 15px 8px;

    text-align: center;

    color: #0F172A;

    font-size: 13px;

    font-weight: 700;
}


/* ============================================================
   CTA
============================================================ */

.cta {
    margin-top: 45px;

    margin-bottom: 40px;

    padding: 50px 25px;

    border-radius: 22px;

    text-align: center;

    color: white;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E40AF
        );
}

.cta-title {
    font-size: 31px;

    font-weight: 900;

    margin-bottom: 10px;
}

.cta-description {
    max-width: 650px;

    margin: auto;

    color: #CBD5E1;

    font-size: 14px;

    line-height: 1.7;
}


/* ============================================================
   FORM
============================================================ */

.form-box {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 20px;

    padding: 30px;

    box-shadow:
        0 7px 25px rgba(15,23,42,0.05);
}


/* ============================================================
   CONTACT
============================================================ */

.contact-card {
    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 28px;

    min-height: 165px;

    text-align: center;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);
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

.contact-value {
    color: #64748B;

    font-size: 13px;

    line-height: 1.6;
}


/* ============================================================
   FOOTER
============================================================ */

.site-footer {
    margin-top: 60px;

    padding: 25px 0;

    border-top: 1px solid #E2E8F0;

    text-align: center;

    color: #64748B;

    font-size: 11px;
}


/* ============================================================
   CHATBOT
============================================================ */

/*
   IMPORTANT:
   The chatbot uses a unique class placed INSIDE its container.
   Only that exact Streamlit vertical block is positioned fixed.
*/

div[data-testid="stVerticalBlock"]:has(
    > div > .floating-chat-marker
) {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 300px !important;

    max-width: calc(100vw - 40px) !important;

    z-index: 2147483647 !important;

    background: #FFFFFF !important;

    border: 1px solid #D8E1EC !important;

    border-radius: 17px !important;

    box-shadow:
        0 18px 45px rgba(15,23,42,0.20) !important;

    overflow: hidden !important;

    padding: 0 !important;

    margin: 0 !important;
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
        );

    padding: 12px 13px;

    color: white;
}

.chat-title {
    font-size: 13px;

    font-weight: 800;
}

.chat-subtitle {
    color: #CBD5E1;

    font-size: 9px;

    margin-top: 3px;
}


/* ============================================================
   CHAT BODY
============================================================ */

.chat-body {
    background: #F8FAFC;

    padding: 10px;

    max-height: 190px;

    overflow-y: auto;
}

.chat-message {
    padding: 8px 9px;

    border-radius: 10px;

    margin-bottom: 7px;

    font-size: 10px;

    line-height: 1.5;
}

.chat-assistant {
    background: #EFF6FF;

    border: 1px solid #DBEAFE;

    color: #1E3A8A;
}

.chat-user {
    background: #0F172A;

    color: #FFFFFF;

    margin-left: 25px;
}


/* ============================================================
   CHAT OPTION AREA
============================================================ */

.chat-options {
    padding: 8px;

    background: #FFFFFF;

    border-top: 1px solid #E2E8F0;
}


/* Make chatbot buttons smaller */

div[data-testid="stVerticalBlock"]:has(
    > div > .floating-chat-marker
) div[data-testid="stButton"] > button {

    min-height: 30px !important;

    height: 30px !important;

    padding: 2px 4px !important;

    font-size: 9px !important;

    border-radius: 8px !important;
}


/* ============================================================
   CHAT CLOSE BUTTON
============================================================ */

.chat-close-button button {

    min-height: 28px !important;

    height: 28px !important;

    width: 28px !important;

    padding: 0 !important;

    border-radius: 50% !important;

    background: rgba(255,255,255,0.15) !important;

    color: white !important;

    border: none !important;

    font-size: 10px !important;
}


/* ============================================================
   CHAT OPEN BUTTON
============================================================ */

div[data-testid="stVerticalBlock"]:has(
    > div > .floating-chat-open-marker
) {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 60px !important;

    height: 60px !important;

    z-index: 2147483647 !important;

    padding: 0 !important;

    margin: 0 !important;
}

div[data-testid="stVerticalBlock"]:has(
    > div > .floating-chat-open-marker
) div[data-testid="stButton"] > button {

    width: 60px !important;

    height: 60px !important;

    min-height: 60px !important;

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

    font-size: 22px !important;

    box-shadow:
        0 12px 28px rgba(15,23,42,0.25) !important;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding-left: 12px !important;

        padding-right: 12px !important;
    }

    .logi-brand {
        font-size: 30px;
    }

    .hero {
        padding: 45px 15px;
    }

    .hero-title {
        font-size: 39px;

        letter-spacing: -1.8px;
    }

    .hero-description {
        font-size: 14px;
    }

    div[data-testid="stVerticalBlock"]:has(
        > div > .floating-chat-marker
    ) {

        left: 10px !important;

        bottom: 10px !important;

        width: 275px !important;

        max-width: calc(100vw - 20px) !important;
    }

    div[data-testid="stVerticalBlock"]:has(
        > div > .floating-chat-open-marker
    ) {

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
<div class="logi-header">

    <div class="logi-brand">
        🚚 <span>Logi</span><span class="logi-brand-blue">Intelli</span>
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

nav_cols = st.columns(6)

nav_items = [
    ("🏠 Home", "Home"),
    ("🛠️ Services", "Services"),
    ("📊 Projects", "Projects"),
    ("📝 Request Project", "Request Project"),
    ("👤 About", "About"),
    ("📞 Contact", "Contact"),
]


for i, (label, page_name) in enumerate(nav_items):

    with nav_cols[i]:

        if st.button(
            label,
            key=f"nav_{i}",
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()


# ============================================================
# HOME
# ============================================================

def show_home():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        🚚 LOGISTICS • DATA • AI • BUSINESS INTELLIGENCE
    </div>

    <div class="hero-title">
        Turn Your Business Data Into
        <span class="hero-title-blue">Intelligent Decisions</span>
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

            html(
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

    html(
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


    for i, (icon, title, description) in enumerate(services):

        with service_cols[i % 3]:

            html(
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

    html(
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


    for col, (number, title, description) in zip(
        workflow_cols,
        workflow
    ):

        with col:

            html(
                f"""
<div class="info-card">

    <div style="
        color:#2563EB;
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

    html(
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


    tech_cols = st.columns(6)


    for col, tech in zip(
        tech_cols,
        technologies
    ):

        with col:

            html(
                f"""
<div class="tech">
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

    html(
        """
<div class="hero">

    <div class="hero-badge">
        OUR SERVICES
    </div>

    <div class="hero-title">
        Analytics & Technology
        <span class="hero-title-blue">Solutions</span>
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
            "Executive dashboards<br>Operational dashboards<br>KPI tracking<br>DAX<br>Power Query<br>Automated reporting",
        ),

        (
            "🚚",
            "Logistics Analytics",
            "Shipment tracking<br>Hub performance<br>SLA analytics<br>TAT analysis<br>Delivery performance<br>Exception analytics",
        ),

        (
            "🤖",
            "AI & Machine Learning",
            "Demand forecasting<br>Delay prediction<br>Customer churn<br>Sales forecasting<br>Classification<br>Predictive analytics",
        ),

        (
            "⚙️",
            "Automation & MIS",
            "Automated MIS<br>Excel automation<br>Python automation<br>Scheduled reporting<br>Data refresh<br>Operational workflows",
        ),

        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL<br>Data modelling<br>ETL pipelines<br>Data transformation<br>Database optimization<br>Reporting datasets",
        ),

        (
            "🔗",
            "API & Data Integration",
            "REST API integration<br>JSON processing<br>Database integration<br>Multi-source analytics<br>Automated ingestion<br>Data pipelines",
        ),
    ]


    cols = st.columns(2)


    for i, (icon, title, description) in enumerate(services):

        with cols[i % 2]:

            html(
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

    html(
        """
<div class="hero">

    <div class="hero-badge">
        PROJECTS & SOLUTIONS
    </div>

    <div class="hero-title">
        Real Business Problems.
        <span class="hero-title-blue">Data-Driven Solutions.</span>
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

    html(
        """
<div class="hero">

    <div class="hero-badge">
        START A PROJECT
    </div>

    <div class="hero-title">
        Tell Us About Your
        <span class="hero-title-blue">Requirement</span>
    </div>

    <div class="hero-description">
        Share your business requirement and we will
        get back to you with the right analytics solution.
    </div>

</div>
"""
    )


    html('<div class="form-box">')


    col1, col2 = st.columns(2)


    with col1:

        company = st.text_input(
            "Company Name",
            placeholder="Your company name",
            key="form_company",
        )

        contact = st.text_input(
            "Contact Person *",
            placeholder="Your name",
            key="form_contact",
        )

        email = st.text_input(
            "Business Email *",
            placeholder="name@company.com",
            key="form_email",
        )

        phone = st.text_input(
            "Phone / WhatsApp",
            placeholder="+91 XXXXX XXXXX",
            key="form_phone",
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
            key="form_service",
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
            key="form_source",
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
            key="form_timeline",
        )


    requirement = st.text_area(
        "Requirement *",
        placeholder=(
            "Describe your business problem, "
            "current process and expected solution..."
        ),
        height=150,
        key="form_requirement",
    )


    html("</div>")


    if st.button(
        "🚀 Submit Project Request",
        key="submit_request",
        use_container_width=True,
    ):

        if not contact.strip():

            st.error("Please enter your contact name.")

        elif not email.strip():

            st.error("Please enter your business email.")

        elif not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            email.strip(),
        ):

            st.error("Please enter a valid email address.")

        elif not requirement.strip():

            st.error("Please describe your requirement.")

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

                "Source": "LogiIntelli Website",
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
                        "✅ Your project request has been "
                        "submitted successfully."
                    )

                    st.balloons()

                else:

                    st.error(
                        "Unable to submit your request. "
                        "Please try again."
                    )

            except Exception as e:

                st.error(
                    "Connection error. Please try again later."
                )


# ============================================================
# ABOUT
# ============================================================

def show_about():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        ABOUT LOGIINTELLI
    </div>

    <div class="hero-title">
        Data. Intelligence.
        <span class="hero-title-blue">Business Growth.</span>
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

        html(
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

        html(
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


    html(
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


    cols = st.columns(3)


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


    for col, (icon, title, description) in zip(
        cols,
        points
    ):

        with col:

            html(
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

    html(
        """
<div class="hero">

    <div class="hero-badge">
        CONTACT US
    </div>

    <div class="hero-title">
        Let's Discuss Your
        <span class="hero-title-blue">Data Needs</span>
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

        html(
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

        html(
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

        html(
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
        key="contact_request",
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

html(
    """
<div class="site-footer">

    © 2026 LogiIntelli

    <br>

    Logistics Analytics • AI • Business Intelligence • Automation

</div>
"""
)


# ============================================================
# GLOBAL FLOATING CHATBOT
# ============================================================

if st.session_state.chat_open:

    # --------------------------------------------------------
    # FIXED CHAT CONTAINER
    # --------------------------------------------------------

    chat_container = st.container()


    with chat_container:

        # Marker used ONLY for CSS identification
        html(
            """
<div class="floating-chat-marker"></div>
"""
        )


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        h1, h2 = st.columns([0.82, 0.18])


        with h1:

            html(
                """
<div class="chat-header">

    <div class="chat-title">
        🤖 LogiIntelli AI
    </div>

    <div class="chat-subtitle">
        Analytics & Project Consultation
    </div>

</div>
"""
            )


        with h2:

            st.markdown(
                '<div class="chat-close-button">',
                unsafe_allow_html=True,
            )


            if st.button(
                "✕",
                key="close_global_chat",
            ):

                close_chat()

                st.rerun()


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )


        # ----------------------------------------------------
        # MESSAGES
        # ----------------------------------------------------

        message_html = """
<div class="chat-body">
"""


        for message in st.session_state.chat_messages:

            if message["role"] == "assistant":

                message_class = "chat-assistant"

            else:

                message_class = "chat-user"


            message_html += f"""
<div class="chat-message {message_class}">
    {message["text"]}
</div>
"""


        message_html += """
</div>
"""


        html(message_html)


        # ----------------------------------------------------
        # OPTIONS
        # ----------------------------------------------------

        html(
            """
<div class="chat-options">
"""
        )


        chat_options = [
            "📊 Power BI",
            "🚚 Logistics",
            "🤖 AI / ML",
            "⚙️ Automation",
            "🗄️ SQL",
            "💡 Not Sure",
        ]


        option_cols = st.columns(2)


        for i, option in enumerate(chat_options):

            with option_cols[i % 2]:

                if st.button(
                    option,
                    key=f"global_chat_option_{i}",
                    use_container_width=True,
                ):

                    if "Power BI" in option:

                        response_text = (
                            "Great! We can help with "
                            "<b>Power BI dashboards</b>, "
                            "DAX, Power Query, KPI reporting "
                            "and business intelligence."
                        )

                    elif "Logistics" in option:

                        response_text = (
                            "We can help with "
                            "<b>Logistics Analytics</b>, "
                            "shipment tracking, SLA, TAT, "
                            "hub performance and delivery analytics."
                        )

                    elif "AI" in option:

                        response_text = (
                            "We can help with "
                            "<b>AI & Machine Learning</b>, "
                            "forecasting, prediction, classification "
                            "and predictive analytics."
                        )

                    elif "Automation" in option:

                        response_text = (
                            "We can help automate "
                            "<b>MIS, Excel, Python and reporting "
                            "workflows</b>."
                        )

                    elif "SQL" in option:

                        response_text = (
                            "We can help with "
                            "<b>SQL, ETL, data transformation, "
                            "database optimization and reporting.</b>"
                        )

                    else:

                        response_text = (
                            "No problem! 😊 Tell us about your "
                            "business problem and we can suggest "
                            "the right Analytics, AI, BI or "
                            "Automation solution."
                        )


                    add_chat_message(
                        option,
                        response_text,
                    )

                    st.rerun()


        html(
            """
</div>
"""
        )


else:

    # ========================================================
    # FLOATING OPEN BUTTON
    # ========================================================

    open_container = st.container()


    with open_container:

        html(
            """
<div class="floating-chat-open-marker"></div>
"""
        )


        if st.button(
            "💬",
            key="open_global_chat",
            help="Open LogiIntelli AI Assistant",
        ):

            open_chat()

            st.rerun()
