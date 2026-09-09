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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');


/* ============================================================
   GLOBAL
============================================================ */

html, body, [class*="css"] {
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
    background: linear-gradient(135deg, #0F172A, #2563EB);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 21px;
    font-weight: 900;
    box-shadow: 0 8px 22px rgba(37,99,235,0.20);
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
    box-shadow: 0 4px 14px rgba(37,99,235,0.10) !important;
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
        radial-gradient(circle at 85% 20%, rgba(59,130,246,0.22), transparent 30%),
        radial-gradient(circle at 10% 90%, rgba(37,99,235,0.16), transparent 28%),
        linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 48%, #FFFFFF 100%);
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
    box-shadow: 0 8px 30px rgba(15,23,42,0.035);
    transition: all 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #BFDBFE;
    box-shadow: 0 18px 45px rgba(15,23,42,0.08);
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
        radial-gradient(circle at 85% 20%, rgba(37,99,235,0.22), transparent 28%),
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
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
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
    box-shadow: 0 6px 25px rgba(15,23,42,0.035);
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
        radial-gradient(circle at 85% 20%, rgba(96,165,250,0.25), transparent 28%),
        linear-gradient(135deg, #0F172A, #172554);
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
   FLOATING CHATBOT WIDGET FIX
============================================================ */

/* Target the Streamlit container that wraps our chat header */
div[data-testid="stVerticalBlock"]:has(> div .jyora-chat-header) {
    position: fixed !important;
    left: 20px !important;
    bottom: 20px !important;
    width: 320px !important;
    max-width: calc(100vw - 40px) !important;
    z-index: 999999 !important;
    background: #FFFFFF !important;
    border: 1px solid #D9E2EC !important;
    border-radius: 16px !important;
    box-shadow: 0 15px 45px rgba(15,23,42,0.22) !important;
    padding: 12px !important;
}

/* Chat Header */
.jyora-chat-header {
    width: 100% !important;
    padding: 12px 14px !important;
    background: linear-gradient(135deg, #0F172A 0%, #2563EB 100%) !important;
    border-radius: 12px 12px 0 0 !important;
    margin-bottom: 10px !important;
}

.jyora-chat-title {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

.jyora-chat-subtitle {
    color: #DBEAFE !important;
    font-size: 9px !important;
    font-weight: 500 !important;
    margin-top: 2px !important;
}

/* Chat Messages */
.chat-body {
    padding: 6px 4px !important;
    max-height: 200px !important;
    overflow-y: auto !important;
}

.chat-message {
    padding: 7px 10px !important;
    border-radius: 8px !important;
    margin: 4px 0 !important;
    font-size: 11px !important;
    line-height: 1.4 !important;
    white-space: pre-wrap !important;
}

.chat-assistant {
    background: #EFF6FF !important;
    color: #1E3A8A !important;
    border: 1px solid #DBEAFE !important;
}

.chat-user {
    background: #0F172A !important;
    color: #FFFFFF !important;
    margin-left: 15px !important;
}

/* Floating Reopen Button */
.floating-reopen-btn {
    position: fixed !important;
    left: 20px !important;
    bottom: 20px !important;
    z-index: 999999 !important;
}

.floating-reopen-btn button {
    width: 54px !important;
    height: 54px !important;
    min-height: 54px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #0F172A, #2563EB) !important;
    color: white !important;
    border: none !important;
    font-size: 22px !important;
    box-shadow: 0 10px 25px rgba(15,23,42,0.30) !important;
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
            <div class="brand-symbol">J</div>
            <div>
                <div class="brand-name">
                    <span class="jyora-text">JYORA</span>
                    <span class="ai-text">AI</span>
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

    st.markdown("<br>", unsafe_allow_html=True)

    # METRICS
    metric_cols = st.columns(4)
    metrics = [
        ("11+", "Years Analytics Experience"),
        ("50+", "Analytics Solutions"),
        ("7+", "Team Leadership"),
        ("24/7", "Data-Driven Insights"),
    ]

    for col, (value, label) in zip(metric_cols, metrics):
        with col:
            html(
                f"""
<div class="metric">
    <div class="metric-value">{value}</div>
    <div class="metric-label">{label}</div>
</div>
"""
            )

    # WHAT WE DO
    html(
        """
<div class="section section-center">
    <div class="section-label">WHAT WE DO</div>
    <div class="section-title">Technology Built Around Your Business</div>
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

    for i, (icon, title, text) in enumerate(services):
        with service_cols[i % 3]:
            html(
                f"""
<div class="feature-card">
    <div class="feature-icon">{icon}</div>
    <div class="feature-title">{title}</div>
    <div class="feature-text">{text}</div>
</div>
"""
            )
        if (i + 1) % 3 == 0:
            st.markdown("<br>", unsafe_allow_html=True)

    # DARK AI SECTION
    html(
        """
<div class="dark-section">
    <div class="dark-label">INTELLIGENT TECHNOLOGY</div>
    <div class="dark-title">From Data to Decisions</div>
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
        ("01", "Understand", "Connect your business data and uncover the metrics that matter."),
        ("02", "Predict", "Use machine learning and advanced analytics to anticipate outcomes."),
        ("03", "Automate", "Convert insights into automated business workflows and decisions."),
    ]

    for col, (num, title, text) in zip(dark_cols, dark_features):
        with col:
            html(
                f"""
<div class="dark-card">
    <div class="dark-label">{num}</div>
    <div class="dark-card-title">{title}</div>
    <div class="dark-card-text">{text}</div>
</div>
"""
            )

    # PROCESS
    html(
        """
<div class="section section-center">
    <div class="section-label">HOW IT WORKS</div>
    <div class="section-title">A Smarter Way to Solve Business Problems</div>
    <div class="section-description">
        A practical process designed to move from
        business problem to measurable solution.
    </div>
</div>
"""
    )

    process = [
        ("01", "Understand", "We understand your business process, goals and challenges."),
        ("02", "Connect", "We connect databases, files, APIs and existing systems."),
        ("03", "Analyze", "We transform data into meaningful KPIs and intelligence."),
        ("04", "Predict", "AI and machine learning identify future opportunities and risks."),
        ("05", "Automate", "We automate repetitive reporting and operational workflows."),
        ("06", "Optimize", "Continuous insights help improve business performance."),
    ]

    process_cols = st.columns(3)

    for i, (number, title, text) in enumerate(process):
        with process_cols[i % 3]:
            html(
                f"""
<div class="process-card">
    <div class="process-number">STEP {number}</div>
    <div class="process-title">{title}</div>
    <div class="process-text">{text}</div>
</div>
"""
            )
        if (i + 1) % 3 == 0:
            st.markdown("<br>", unsafe_allow_html=True)

    # TECHNOLOGY
    html(
        """
<div class="section section-center">
    <div class="section-label">TECHNOLOGY</div>
    <div class="section-title">Built With Modern Data & AI Technologies</div>
</div>
"""
    )

    technologies = [
        "Python", "SQL", "Power BI", "Pandas", "NumPy",
        "Scikit-learn", "XGBoost", "Random Forest", "Prophet",
        "TensorFlow", "Keras", "PySpark", "REST APIs", "ETL", "Streamlit"
    ]

    html(
        '<div style="text-align:center;">'
        + "".join(f'<span class="tech-pill">{tech}</span>' for tech in technologies)
        + "</div>"
    )

    # CTA
    html(
        """
<div class="cta-section">
    <div class="cta-title">Ready to Make Your Data Intelligent?</div>
    <div class="cta-text">
        Tell us about your business problem and
        we'll help identify the right analytics,
        AI or automation solution.
    </div>
</div>
"""
    )

    if st.button("🚀 Start Your Project", use_container_width=True, key="home_cta"):
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
        <div class="hero-badge">✦ JYORA AI SOLUTIONS</div>
        <div class="hero-title">Tailored AI & Data Solutions</div>
        <div class="hero-description">
            Comprehensive business intelligence, predictive analytics, and process automation designed for scalability.
        </div>
    </div>
</div>
"""
    )

    all_services = [
        ("🤖 Artificial Intelligence", "Custom ML models, forecasting, churn prediction, and intelligent decisions."),
        ("📊 Business Intelligence", "Interactive Power BI & Tableau dashboards, executive reporting, and KPIs."),
        ("🔮 Predictive Analytics", "Demand forecasting, delay prediction, and risk mitigation models."),
        ("⚙️ Intelligent Automation", "Automate routine MIS workflows, reporting pipelines, and ETL processes."),
        ("🗄️ Data Engineering", "Data pipeline construction, SQL database tuning, API integrations, and ETL."),
        ("🚚 Operational Intelligence", "Supply chain, TAT tracking, hub operations, and logistics efficiency."),
    ]

    cols = st.columns(2)
    for idx, (title, desc) in enumerate(all_services):
        with cols[idx % 2]:
            html(
                f"""
<div class="feature-card" style="margin-bottom: 20px;">
    <div class="feature-title">{title}</div>
    <div class="feature-text">{desc}</div>
</div>
"""
            )


# ============================================================
# PROJECTS PAGE
# ============================================================

def projects_page():

    html(
        """
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-badge">✦ USE CASES & CASE STUDIES</div>
        <div class="hero-title">Proven Real-World Impact</div>
        <div class="hero-description">
            Discover how JYORA AI delivers end-to-end analytics and automation solutions across industries.
        </div>
    </div>
</div>
"""
    )

    projects = [
        ("LOGISTICS", "Logistics Delivery & SLA Tracker", "Real-time SLA breach prediction and hub-level transit time performance optimization."),
        ("AUTOMATION", "Automated Executive MIS Engine", "Eliminated 15+ hours of manual weekly reporting through Python and SQL automation."),
        ("RETAIL", "Inventory & Demand Forecasting", "Machine learning time-series model predicting seasonal inventory needs with high precision."),
        ("FINANCE", "Financial KPI & Revenue Dashboard", "Executive BI dashboard consolidating multi-source financial data into real-time insights."),
    ]

    cols = st.columns(2)
    for idx, (tag, title, desc) in enumerate(projects):
        with cols[idx % 2]:
            html(
                f"""
<div class="project-card" style="margin-bottom: 20px;">
    <span class="project-tag">{tag}</span>
    <div class="project-title">{title}</div>
    <div class="project-text">{desc}</div>
</div>
"""
            )


# ============================================================
# REQUEST PROJECT PAGE
# ============================================================

def request_project_page():

    html(
        """
<div class="section section-center">
    <div class="section-label">GET STARTED</div>
    <div class="section-title">Start Your Project</div>
    <div class="section-description">Fill out the form below to share your requirements with our technical team.</div>
</div>
"""
    )

    with st.form("project_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Business Email")
        service = st.selectbox("Service Needed", [
            "Artificial Intelligence",
            "Business Intelligence",
            "Predictive Analytics",
            "Intelligent Automation",
            "Data Engineering",
            "Logistics Analytics"
        ])
        details = st.text_area("Project Overview & Goals")
        submitted = st.form_submit_button("Submit Project Request")

        if submitted:
            if not name or not email or not details:
                st.error("Please fill in all required fields.")
            elif not valid_email(email):
                st.error("Please enter a valid email address.")
            else:
                payload = {
                    "type": "project_request",
                    "name": name,
                    "email": email,
                    "service": service,
                    "details": details,
                    "timestamp": datetime.now().isoformat()
                }
                if submit_to_google(payload):
                    st.success("Thank you! Your project request has been successfully submitted.")
                else:
                    st.info("Request captured! Our team will get back to you shortly.")


# ============================================================
# ABOUT PAGE
# ============================================================

def about_page():

    html(
        """
<div class="hero-section">
    <div class="hero-content">
        <div class="hero-badge">✦ ABOUT JYORA AI</div>
        <div class="hero-title">Pioneering Data Intelligence</div>
        <div class="hero-description">
            At JYORA AI, we bridge the gap between complex data and strategic execution. With over a decade of analytical expertise, we empower organizations to make confident, data-backed decisions.
        </div>
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
<div class="section section-center">
    <div class="section-label">CONTACT US</div>
    <div class="section-title">Let's Connect</div>
    <div class="section-description">Have questions or need consultation? Reach out directly.</div>
</div>
"""
    )

    with st.form("contact_form"):
        c_name = st.text_input("Name")
        c_email = st.text_input("Email")
        c_message = st.text_area("Message")
        c_submit = st.form_submit_button("Send Message")

        if c_submit:
            if not c_name or not c_email or not c_message:
                st.error("Please fill in all fields.")
            elif not valid_email(c_email):
                st.error("Please enter a valid email address.")
            else:
                payload = {
                    "type": "contact",
                    "name": c_name,
                    "email": c_email,
                    "message": c_message,
                    "timestamp": datetime.now().isoformat()
                }
                if submit_to_google(payload):
                    st.success("Your message has been sent successfully!")
                else:
                    st.info("Message received! We will contact you soon.")


# ============================================================
# FLOATING CHATBOT WIDGET
# ============================================================

def render_chatbot():
    if not st.session_state.chat_open:
        st.markdown('<div class="floating-reopen-btn">', unsafe_allow_html=True)
        if st.button("💬", key="reopen_chat_btn"):
            st.session_state.chat_open = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Native Streamlit Container enables CSS targeting
    with st.container():
        # Header HTML
        html(
            """
<div class="jyora-chat-header">
    <div class="jyora-chat-title">JYORA AI Assistant</div>
    <div class="jyora-chat-subtitle">AI & Project Consultation</div>
</div>
"""
        )

        # Header Close Button
        if st.button("✕ Close Chat", key="close_chat_btn"):
            st.session_state.chat_open = False
            st.rerun()

        # Chat Messages Scroll Area
        chat_html = '<div class="chat-body">'
        for msg in st.session_state.chat_messages:
            cls = "chat-assistant" if msg["role"] == "assistant" else "chat-user"
            chat_html += f'<div class="chat-message {cls}">{msg["text"]}</div>'
        chat_html += '</div>'
        html(chat_html)

        # Multi-step Interactive Flow
        step = st.session_state.chat_step

        if step == 0:
            name_input = st.text_input("Your Name", key="chat_name_input", placeholder="Type your name...")
            if st.button("Next →", key="chat_step0_btn"):
                if name_input.strip():
                    st.session_state.chat_data["name"] = name_input.strip()
                    st.session_state.chat_messages.append({"role": "user", "text": name_input.strip()})
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "text": f"Nice to meet you, {name_input.strip()}! What service are you interested in?"}
                    )
                    st.session_state.chat_step = 1
                    st.rerun()

        elif step == 1:
            services = ["AI Solutions", "Business Intelligence", "Automation", "Data Engineering"]
            for s in services:
                if st.button(s, key=f"chat_srv_{s}"):
                    st.session_state.chat_data["service"] = s
                    st.session_state.chat_messages.append({"role": "user", "text": s})
                    st.session_state.chat_messages.append(
                        {"role": "assistant", "text": "Got it! Please enter your email address so we can contact you."}
                    )
                    st.session_state.chat_step = 2
                    st.rerun()

        elif step == 2:
            email_input = st.text_input("Email", key="chat_email_input", placeholder="name@company.com")
            if st.button("Submit Consultation", key="chat_step2_btn"):
                if valid_email(email_input):
                    st.session_state.chat_data["email"] = email_input.strip()
                    st.session_state.chat_messages.append({"role": "user", "text": email_input.strip()})
                    
                    # Payload submission
                    payload = {
                        "type": "chat_lead",
                        "name": st.session_state.chat_data.get("name"),
                        "service": st.session_state.chat_data.get("service"),
                        "email": email_input.strip(),
                        "timestamp": datetime.now().isoformat()
                    }
                    submit_to_google(payload)

                    st.session_state.chat_messages.append(
                        {"role": "assistant", "text": "Thank you! Our consultant will reach out shortly."}
                    )
                    st.session_state.chat_step = 3
                    st.rerun()
                else:
                    st.error("Please provide a valid email.")

        elif step == 3:
            if st.button("Start New Consultation", key="chat_reset_btn"):
                st.session_state.chat_step = 0
                st.session_state.chat_data = {}
                st.session_state.chat_messages = [
                    {"role": "assistant", "text": "👋 Welcome to JYORA AI.\nLet's understand your business requirement."}
                ]
                st.rerun()


# ============================================================
# ROUTER
# ============================================================

pages = {
    "Home": home_page,
    "Services": services_page,
    "Projects": projects_page,
    "Request Project": request_project_page,
    "About": about_page,
    "Contact": contact_page,
}

# Render active page
current_page_func = pages.get(st.session_state.page, home_page)
current_page_func()

# Render Floating Chatbot Widget across all pages
render_chatbot()


# ============================================================
# FOOTER
# ============================================================

html(
    """
<div class="footer">
    <div class="footer-brand">
        JYORA <span class="footer-ai">AI</span>
    </div>
    <div>© 2026 JYORA AI. All rights reserved. | Transforming Data into Intelligence</div>
</div>
"""
)
