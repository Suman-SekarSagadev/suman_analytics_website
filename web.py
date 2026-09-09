from datetime import datetime
import json
import re
import requests
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JYORA Consulting | Data Analytics, AI & BI",
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
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to JYORA Consulting.<br><br>"
                "How can I help you today?"
            ),
        }
    ]


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(content)


# ============================================================
# GLOBAL CSS
# ============================================================

html(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap'
);


/* ============================================================
   GLOBAL PAGE
============================================================ */

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

    padding-bottom: 70px !important;
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
    visibility: hidden !important;
    height: 0px !important;
}

/* Hide Streamlit developer toolbar / controls */
[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Hide Streamlit deploy/manage controls when exposed in the page DOM */
button[title*="Manage app"],
button[aria-label*="Manage app"],
[title*="Manage app"],
[aria-label*="Manage app"] {
    display: none !important;
    visibility: hidden !important;
}

/* Hide bottom-right Streamlit status/developer area */
.stAppDeployButton,
[data-testid="stAppDeployButton"],
[data-testid="stStatusWidget"],
[data-testid="stToolbarActions"] {
    display: none !important;
    visibility: hidden !important;
}


/* ============================================================
   HEADER
============================================================ */

.logi-header {
    width: 100%;

    padding: 12px 0 18px 0;

    margin-bottom: 18px;

    border-bottom: 1px solid #E2E8F0;
}

.logi-brand {
    font-size: 38px;

    font-weight: 900;

    line-height: 1.1;

    letter-spacing: -1.8px;

    color: #0F172A;
}

.logi-blue {
    color: #2563EB;
}

.logi-subtitle {
    margin-top: 7px;

    color: #64748B;

    font-size: 11px;

    font-weight: 500;
}


/* ============================================================
   NAVIGATION
============================================================ */

div[data-testid="stButton"] > button {
    min-height: 40px !important;

    border-radius: 10px !important;

    border: 1px solid #E2E8F0 !important;

    background: #FFFFFF !important;

    color: #334155 !important;

    font-weight: 600 !important;

    font-size: 13px !important;

    transition: 0.2s ease !important;
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

    margin-bottom: 35px;

    border-radius: 25px;

    background:
        radial-gradient(
            circle at top center,
            #DBEAFE 0%,
            #F8FAFC 45%,
            #F8FAFC 100%
        );
}

.hero-badge {
    display: inline-block;

    padding: 8px 16px;

    margin-bottom: 20px;

    border-radius: 30px;

    background: #EFF6FF;

    border: 1px solid #BFDBFE;

    color: #2563EB;

    font-size: 10px;

    font-weight: 800;

    letter-spacing: 0.7px;
}

.hero-title {
    max-width: 950px;

    margin: auto;

    color: #0F172A;

    font-size: 56px;

    line-height: 1.06;

    font-weight: 900;

    letter-spacing: -3px;
}

.hero-blue {
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
    margin-top: 35px;

    margin-bottom: 8px;

    color: #0F172A;

    font-size: 30px;

    font-weight: 850;
}

.section-description {
    margin-bottom: 25px;

    color: #64748B;

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

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);

    transition: 0.2s ease;
}

.info-card:hover {
    transform: translateY(-3px);

    border-color: #BFDBFE;

    box-shadow:
        0 12px 28px rgba(15,23,42,0.08);
}

.card-icon {
    margin-bottom: 13px;

    font-size: 30px;
}

.card-title {
    margin-bottom: 8px;

    color: #0F172A;

    font-size: 17px;

    font-weight: 800;
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
    padding: 23px 10px;

    text-align: center;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 16px;

    box-shadow:
        0 4px 15px rgba(15,23,42,0.035);
}

.metric-value {
    color: #2563EB;

    font-size: 31px;

    font-weight: 900;
}

.metric-label {
    margin-top: 5px;

    color: #64748B;

    font-size: 11px;
}


/* ============================================================
   PROJECT CARDS
============================================================ */

.project-card {
    min-height: 200px;

    margin-bottom: 18px;

    padding: 25px;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);
}

.project-icon {
    margin-bottom: 8px;

    font-size: 28px;
}

.project-category {
    margin-bottom: 8px;

    color: #2563EB;

    font-size: 10px;

    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 0.7px;
}

.project-title {
    margin-bottom: 8px;

    color: #0F172A;

    font-size: 18px;

    font-weight: 800;
}

.project-description {
    color: #64748B;

    font-size: 13px;

    line-height: 1.7;
}


/* ============================================================
   TECHNOLOGY
============================================================ */

.tech-card {
    padding: 15px 8px;

    text-align: center;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 12px;

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

    text-align: center;

    border-radius: 22px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E40AF
        );
}

.cta-title {
    margin-bottom: 10px;

    font-size: 31px;

    font-weight: 900;
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
    padding: 30px;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 20px;

    box-shadow:
        0 7px 25px rgba(15,23,42,0.05);
}


/* ============================================================
   CONTACT
============================================================ */

.contact-card {
    min-height: 165px;

    padding: 28px;

    text-align: center;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    box-shadow:
        0 5px 20px rgba(15,23,42,0.04);
}

.contact-icon {
    margin-bottom: 12px;

    font-size: 30px;
}

.contact-title {
    margin-bottom: 7px;

    color: #0F172A;

    font-size: 16px;

    font-weight: 800;
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
   FLOATING CHATBOT
============================================================ */

/*
   The chatbot is NOT inside the Streamlit layout.

   It is injected as an independent fixed HTML element.

   Therefore:
   - It does not collapse the page.
   - It does not change page width.
   - It stays on the left side.
   - It stays fixed while scrolling.
*/

.logi-chat-widget {
    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 320px !important;

    max-width: calc(100vw - 40px) !important;

    z-index: 2147483647 !important;

    font-family: "Inter", sans-serif !important;
}


/* ============================================================
   CHAT WINDOW
============================================================ */

.logi-chat-window {
    width: 100%;

    overflow: hidden;

    background: #FFFFFF;

    border: 1px solid #D9E2EC;

    border-radius: 18px;

    box-shadow:
        0 18px 50px rgba(15,23,42,0.25);
}


/* ============================================================
   CHAT HEADER
============================================================ */

.logi-chat-header {
    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 14px 15px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        );
}

.logi-chat-header-left {
    display: flex;

    align-items: center;

    gap: 9px;
}

.logi-chat-avatar {
    display: flex;

    align-items: center;

    justify-content: center;

    width: 34px;

    height: 34px;

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

    color: #BFDBFE;

    font-size: 9px;
}

.logi-chat-close {
    display: flex;

    align-items: center;

    justify-content: center;

    width: 28px;

    height: 28px;

    border: 0;

    border-radius: 50%;

    background: rgba(255,255,255,0.14);

    color: white;

    cursor: pointer;

    font-size: 14px;

    transition: 0.2s;
}

.logi-chat-close:hover {
    background: rgba(255,255,255,0.28);
}


/* ============================================================
   CHAT BODY
============================================================ */

.logi-chat-body {
    height: 250px;

    overflow-y: auto;

    padding: 13px;

    background: #F8FAFC;
}


/* ============================================================
   MESSAGE
============================================================ */

.logi-message {
    max-width: 90%;

    margin-bottom: 9px;

    padding: 9px 11px;

    border-radius: 11px;

    font-size: 10px;

    line-height: 1.55;
}

.logi-message-bot {
    margin-right: 20px;

    color: #1E3A8A;

    background: #EFF6FF;

    border: 1px solid #DBEAFE;
}

.logi-message-user {
    margin-left: 20px;

    color: white;

    background: #0F172A;
}


/* ============================================================
   CHAT OPTIONS
============================================================ */

.logi-chat-options {
    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 7px;

    padding: 10px;

    border-top: 1px solid #E2E8F0;

    background: white;
}

.logi-chat-option {
    padding: 8px 5px;

    border: 1px solid #DCE5EF;

    border-radius: 8px;

    background: #FFFFFF;

    color: #334155;

    cursor: pointer;

    font-family: "Inter", sans-serif;

    font-size: 9px;

    font-weight: 600;

    transition: 0.2s;
}

.logi-chat-option:hover {
    border-color: #2563EB;

    color: #2563EB;

    background: #EFF6FF;
}


/* ============================================================
   CHAT INPUT
============================================================ */

.logi-chat-input-area {
    display: flex;

    gap: 6px;

    padding: 9px;

    border-top: 1px solid #E2E8F0;

    background: #FFFFFF;
}

.logi-chat-input {
    flex: 1;

    min-width: 0;

    padding: 8px 9px;

    border: 1px solid #DCE5EF;

    border-radius: 9px;

    outline: none;

    font-family: "Inter", sans-serif;

    font-size: 10px;
}

.logi-chat-input:focus {
    border-color: #2563EB;
}

.logi-chat-send {
    width: 36px;

    border: none;

    border-radius: 9px;

    background: #2563EB;

    color: white;

    cursor: pointer;

    font-size: 13px;
}


/* ============================================================
   FLOATING CHAT BUTTON
============================================================ */

.logi-chat-launcher {
    display: flex;

    align-items: center;

    justify-content: center;

    width: 60px;

    height: 60px;

    border: none;

    border-radius: 50%;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        );

    color: white;

    cursor: pointer;

    font-size: 23px;

    box-shadow:
        0 12px 30px rgba(15,23,42,0.28);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.logi-chat-launcher:hover {
    transform: scale(1.06);

    box-shadow:
        0 15px 35px rgba(15,23,42,0.35);
}


/* ============================================================
   CHAT NOTIFICATION
============================================================ */

.logi-chat-badge {
    position: absolute;

    top: -2px;

    right: -2px;

    display: flex;

    align-items: center;

    justify-content: center;

    width: 19px;

    height: 19px;

    border-radius: 50%;

    background: #EF4444;

    color: white;

    font-size: 9px;

    font-weight: 800;

    border: 2px solid white;
}


/* ============================================================
   MOBILE CHAT
============================================================ */

@media (max-width: 600px) {

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

    .logi-chat-widget {
        left: 10px !important;

        bottom: 10px !important;

        width: 285px !important;

        max-width: calc(100vw - 20px) !important;
    }

    .logi-chat-launcher {
        width: 56px;

        height: 56px;
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
        JYORA <span class="logi-blue">Consulting</span>
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


for i, (label, page_name) in enumerate(nav_items):

    with nav_cols[i]:

        if st.button(
            label,
            key=f"nav_button_{i}",
            use_container_width=True,
        ):

            st.session_state.page = page_name

            st.rerun()


# ============================================================
# HOME PAGE
# ============================================================

def show_home():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        📊 DATA • AI • BUSINESS INTELLIGENCE • AUTOMATION
    </div>

    <div class="hero-title">
        Turn Your Business Data Into
        <span class="hero-blue">
            Intelligent Decisions
        </span>
    </div>

    <div class="hero-description">
        JYORA Consulting helps businesses transform operational data
        into powerful dashboards, predictive models,
        automation solutions and actionable business intelligence.
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


    for col, (value, label) in zip(cols, metrics):

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


    cols = st.columns(3)


    for i, (icon, title, description) in enumerate(services):

        with cols[i % 3]:

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

        ("01", "Understand", "Understand the business problem and objectives."),

        ("02", "Analyze", "Study data sources and identify opportunities."),

        ("03", "Build", "Develop dashboards, models and automation."),

        ("04", "Deliver", "Deploy the solution and provide actionable insights."),
    ]


    cols = st.columns(4)


    for col, (number, title, description) in zip(
        cols,
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


    cols = st.columns(6)


    for col, technology in zip(
        cols,
        technologies
    ):

        with col:

            html(
                f"""
<div class="tech-card">
    {technology}
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
        key="home_start_project",
        use_container_width=True,
    ):

        st.session_state.page = "Request Project"

        st.rerun()


# ============================================================
# SERVICES PAGE
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
        <span class="hero-blue">Solutions</span>
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
# PROJECTS PAGE
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
# REQUEST PROJECT PAGE
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


    html('<div class="form-box">')


    col1, col2 = st.columns(2)


    with col1:

        company = st.text_input(
            "Company Name",
            placeholder="Your company name",
            key="company_name",
        )

        contact = st.text_input(
            "Contact Person *",
            placeholder="Your name",
            key="contact_person",
        )

        email = st.text_input(
            "Business Email *",
            placeholder="name@company.com",
            key="business_email",
        )

        phone = st.text_input(
            "Phone / WhatsApp",
            placeholder="+91 XXXXX XXXXX",
            key="phone_number",
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
            key="required_service",
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
            key="current_source",
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
            key="expected_timeline",
        )


    requirement = st.text_area(
        "Requirement *",
        placeholder=(
            "Describe your business problem, "
            "current process and expected solution..."
        ),
        height=150,
        key="project_requirement",
    )


    html("</div>")


    if st.button(
        "🚀 Submit Project Request",
        key="submit_project",
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
                    "JYORA Consulting Website",
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


            except Exception:

                st.error(
                    "Connection error. Please try again later."
                )


# ============================================================
# ABOUT PAGE
# ============================================================

def show_about():

    html(
        """
<div class="hero">

    <div class="hero-badge">
        ABOUT JYORA CONSULTING
    </div>

    <div class="hero-title">
        Data. Intelligence.
        <span class="hero-blue">
            Business Growth.
        </span>
    </div>

    <div class="hero-description">
        JYORA Consulting focuses on transforming raw business data
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


    for col, (
        icon,
        title,
        description
    ) in zip(cols, points):

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
# CONTACT PAGE
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
        sumansekar1205@gmail.com
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
        key="contact_project",
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

    © 2026 JYORA Consulting

    <br>

    Logistics Analytics • AI • Business Intelligence • Automation

</div>
"""
)


# ============================================================
# STANDARD FLOATING CHATBOT
#
# This is completely independent from Streamlit widgets.
# ============================================================

chatbot_html = r"""
<div id="logi-chat-widget" class="logi-chat-widget">

    <!-- =====================================================
         OPEN BUTTON
    ====================================================== -->

    <div id="logi-chat-launcher-wrapper">

        <button
            id="logi-chat-launcher"
            class="logi-chat-launcher"
            type="button"
            onclick="logiOpenChat()"
            aria-label="Open JYORA AI Assistant"
        >
            💬

            <span class="logi-chat-badge">
                1
            </span>

        </button>

    </div>


    <!-- =====================================================
         CHAT WINDOW
    ====================================================== -->

    <div
        id="logi-chat-window"
        class="logi-chat-window"
        style="display:none;"
    >

        <!-- HEADER -->

        <div class="logi-chat-header">

            <div class="logi-chat-header-left">

                <div class="logi-chat-avatar">
                    🤖
                </div>

                <div>

                    <div class="logi-chat-name">
                        JYORA AI Assistant
                    </div>

                    <div class="logi-chat-status">
                        ● Online • Analytics Assistant
                    </div>

                </div>

            </div>


            <button
                type="button"
                class="logi-chat-close"
                onclick="logiCloseChat()"
                aria-label="Close chatbot"
            >
                ✕
            </button>

        </div>


        <!-- BODY -->

        <div
            id="logi-chat-body"
            class="logi-chat-body"
        >

            <div class="logi-message logi-message-bot">

                👋 Hi! Welcome to <b>JYORA Consulting</b>.

                <br><br>

                I can help you find the right
                Analytics, AI, BI or Automation solution.

                <br><br>

                What are you looking for?

            </div>

        </div>


        <!-- OPTIONS -->

        <div class="logi-chat-options">

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('Power BI Dashboard')"
            >
                📊 Power BI
            </button>

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('Logistics Analytics')"
            >
                🚚 Logistics
            </button>

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('AI / Machine Learning')"
            >
                🤖 AI / ML
            </button>

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('Automation / MIS')"
            >
                ⚙️ Automation
            </button>

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('SQL / Data Engineering')"
            >
                🗄️ SQL
            </button>

            <button
                type="button"
                class="logi-chat-option"
                onclick="logiSelectOption('Project Consultation')"
            >
                💡 Consultation
            </button>

        </div>


        <!-- INPUT -->

        <div class="logi-chat-input-area">

            <input
                id="logi-chat-input"
                class="logi-chat-input"
                type="text"
                placeholder="Type your requirement..."
                onkeydown="logiHandleEnter(event)"
            />

            <button
                type="button"
                class="logi-chat-send"
                onclick="logiSendMessage()"
                aria-label="Send message"
            >
                ➤
            </button>

        </div>

    </div>

</div>


<script>

(function () {

    /* ========================================================
       CHAT STORAGE
    ======================================================== */

    const STORAGE_KEY = "jyora_consulting_chat_open";



    /* ========================================================
       OPEN CHAT
    ======================================================== */

    window.logiOpenChat = function () {

        const windowElement =
            document.getElementById(
                "logi-chat-window"
            );

        const launcher =
            document.getElementById(
                "logi-chat-launcher-wrapper"
            );

        if (windowElement) {

            windowElement.style.display =
                "block";
        }

        if (launcher) {

            launcher.style.display =
                "none";
        }

        try {

            localStorage.setItem(
                STORAGE_KEY,
                "true"
            );

        } catch (e) {}

    };



    /* ========================================================
       CLOSE CHAT
    ======================================================== */

    window.logiCloseChat = function () {

        const windowElement =
            document.getElementById(
                "logi-chat-window"
            );

        const launcher =
            document.getElementById(
                "logi-chat-launcher-wrapper"
            );

        if (windowElement) {

            windowElement.style.display =
                "none";
        }

        if (launcher) {

            launcher.style.display =
                "block";
        }

        try {

            localStorage.setItem(
                STORAGE_KEY,
                "false"
            );

        } catch (e) {}

    };



    /* ========================================================
       ADD MESSAGE
    ======================================================== */

    function logiAddMessage(
        message,
        type
    ) {

        const body =
            document.getElementById(
                "logi-chat-body"
            );

        if (!body) {
            return;
        }


        const div =
            document.createElement(
                "div"
            );


        div.className =
            "logi-message " +
            (
                type === "user"
                ? "logi-message-user"
                : "logi-message-bot"
            );


        div.innerHTML =
            message;


        body.appendChild(div);


        body.scrollTop =
            body.scrollHeight;
    }



    /* ========================================================
       OPTION SELECTION
    ======================================================== */

    window.logiSelectOption =
        function (option) {

            logiAddMessage(
                option,
                "user"
            );


            let reply = "";


            if (
                option ===
                "Power BI Dashboard"
            ) {

                reply =
                    "📊 Great! We can help with " +
                    "<b>Power BI dashboards</b>, " +
                    "DAX, Power Query, KPI reporting " +
                    "and business intelligence.";

            }


            else if (
                option ===
                "Logistics Analytics"
            ) {

                reply =
                    "🚚 We can help with " +
                    "<b>Logistics Analytics</b>, " +
                    "shipment tracking, SLA, TAT, " +
                    "hub performance and delivery analytics.";

            }


            else if (
                option ===
                "AI / Machine Learning"
            ) {

                reply =
                    "🤖 We can help with " +
                    "<b>AI & Machine Learning</b>, " +
                    "forecasting, prediction, classification " +
                    "and predictive analytics.";

            }


            else if (
                option ===
                "Automation / MIS"
            ) {

                reply =
                    "⚙️ We can help automate " +
                    "<b>MIS, Excel, Python and reporting workflows</b>.";

            }


            else if (
                option ===
                "SQL / Data Engineering"
            ) {

                reply =
                    "🗄️ We can help with " +
                    "<b>SQL, ETL, data transformation, " +
                    "database optimization and reporting datasets</b>.";

            }


            else {

                reply =
                    "💡 Sure! Tell me about your " +
                    "<b>business problem or project requirement</b>. " +
                    "I'll help you identify the right solution.";

            }


            setTimeout(
                function () {

                    logiAddMessage(
                        reply,
                        "bot"
                    );

                },
                350
            );

        };



    /* ========================================================
       SEND TEXT MESSAGE
    ======================================================== */

    window.logiSendMessage =
        function () {

            const input =
                document.getElementById(
                    "logi-chat-input"
                );


            if (!input) {
                return;
            }


            const text =
                input.value.trim();


            if (!text) {
                return;
            }


            logiAddMessage(
                text,
                "user"
            );


            input.value = "";


            setTimeout(
                function () {

                    logiAddMessage(
                        "Thank you! 😊 Please use the <b>Request Project</b> page to submit your detailed requirement, or continue chatting here to discuss your needs.",
                        "bot"
                    );

                },
                400
            );

        };



    /* ========================================================
       ENTER KEY
    ======================================================== */

    window.logiHandleEnter =
        function (event) {

            if (
                event.key ===
                "Enter"
            ) {

                event.preventDefault();

                logiSendMessage();

            }

        };



    /* ========================================================
       INITIAL STATE
    ======================================================== */

    try {

        const saved =
            localStorage.getItem(
                STORAGE_KEY
            );


        if (
            saved ===
            "true"
        ) {

            logiOpenChat();

        }

        else {

            logiCloseChat();

        }

    } catch (e) {

        logiCloseChat();

    }

})();

</script>
"""


# ============================================================
# RENDER CHATBOT
# ============================================================

components.html(chatbot_html, height=1, scrolling=False)
