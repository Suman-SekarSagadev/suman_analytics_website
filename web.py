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
    "AKfycbyate5bFtUmuT6TB1YqYhSGq0ED09kuMSXHdkYfj86avev7GZqnSlpyhlgXOfaorycl/"
    "exec"
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    st.html(content)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Home",
    "submitted": False,

    # Chatbot
    "chat_open": True,
    "chat_step": 0,
    "chat_data": {},
    "chat_messages": [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli. "
                "I can help you identify the right Analytics, "
                "AI, BI or Automation solution for your business."
            ),
        }
    ],
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

html {
    scroll-behavior: smooth;
}

body {
    background: #F6F8FC;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(37, 99, 235, 0.045),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(14, 165, 233, 0.045),
            transparent 30%
        ),
        #F6F8FC !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

.block-container {
    max-width: 1250px !important;
    padding-top: 0.8rem !important;
    padding-bottom: 4rem !important;
}


/* ============================================================
   STREAMLIT HEADER
   ============================================================ */

[data-testid="stHeader"],
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}


/* ============================================================
   BRAND
   ============================================================ */

.brand-wrapper {
    text-align: center;
    padding: 8px 0 15px 0;
}

.brand-title {
    font-size: 40px;
    font-weight: 850;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin: 0;
}

.logi-text {
    color: #0F172A;
}

.intelli-text {
    color: #2563EB;
}

.brand-subtitle {
    margin-top: 7px;
    font-size: 14px;
    color: #64748B;
    letter-spacing: 0.2px;
}


/* ============================================================
   NAVIGATION
   ============================================================ */

.nav-wrapper {
    background: rgba(255,255,255,0.98);
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 7px;
    margin-bottom: 28px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.05);
}

.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    color: #475569;
    font-size: 14px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #EFF6FF;
    color: #2563EB;
    border-color: #DBEAFE;
}

.stButton > button:focus {
    box-shadow: none !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;
    padding: 65px 55px;
    border-radius: 24px;

    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(59,130,246,0.25),
            transparent 35%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(14,165,233,0.16),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0F172A 0%,
            #172554 55%,
            #1E3A8A 100%
        );

    color: white;

    box-shadow:
        0 18px 45px rgba(15,23,42,0.16);

    margin-bottom: 35px;
}

.hero-content {
    max-width: 820px;
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.18);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: 48px;
    line-height: 1.08;
    margin: 0 0 18px 0;
    font-weight: 800;
    letter-spacing: -1.5px;
}

.hero h1 span {
    color: #60A5FA;
}

.hero p {
    font-size: 17px;
    line-height: 1.75;
    color: #CBD5E1;
    margin: 0;
    max-width: 760px;
}


/* ============================================================
   SECTION
   ============================================================ */

.section-heading {
    margin: 42px 0 22px 0;
}

.section-kicker {
    color: #2563EB;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.section-title {
    font-size: 30px;
    line-height: 1.2;
    color: #0F172A;
    font-weight: 800;
    letter-spacing: -0.8px;
    margin: 0;
}

.section-subtitle {
    color: #64748B;
    font-size: 15px;
    line-height: 1.65;
    margin-top: 8px;
    max-width: 760px;
}


/* ============================================================
   METRICS
   ============================================================ */

.metric-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 23px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.045);
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 9px;
}

.metric-value {
    font-size: 23px;
    font-weight: 800;
    color: #0F172A;
}

.metric-label {
    margin-top: 5px;
    font-size: 13px;
    color: #64748B;
    line-height: 1.45;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 25px;
    min-height: 205px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.045);
    transition: 0.2s ease;
    margin-bottom: 16px;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(15,23,42,0.09);
}

.card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: #EFF6FF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    margin-bottom: 15px;
}

.card h3 {
    color: #0F172A;
    font-size: 18px;
    margin: 0 0 10px 0;
}

.card p {
    color: #64748B;
    font-size: 14px;
    line-height: 1.65;
    margin: 0;
}


/* ============================================================
   SERVICE LIST
   ============================================================ */

.service-list {
    margin-top: 12px;
    padding-left: 0;
    list-style: none;
}

.service-list li {
    color: #475569;
    font-size: 13px;
    padding: 5px 0;
    line-height: 1.5;
}

.service-list li::before {
    content: "✓";
    color: #2563EB;
    font-weight: 800;
    margin-right: 8px;
}


/* ============================================================
   WHY
   ============================================================ */

.why-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    min-height: 165px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.04);
}

.why-card h3 {
    font-size: 17px;
    color: #0F172A;
    margin: 0 0 8px 0;
}

.why-card p {
    font-size: 13px;
    line-height: 1.65;
    color: #64748B;
    margin: 0;
}


/* ============================================================
   WORKFLOW
   ============================================================ */

.workflow {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 25px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.04);
}

.workflow-step {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    color: #334155;
    padding: 10px 13px;
    border-radius: 10px;
    font-size: 12px;
    font-weight: 700;
}

.workflow-arrow {
    color: #94A3B8;
    font-weight: 800;
}


/* ============================================================
   TECHNOLOGY
   ============================================================ */

.tech-strip {
    background: #0F172A;
    border-radius: 18px;
    padding: 25px;
    margin: 28px 0;
}

.tech-title {
    color: white;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 15px;
}

.tech-list {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
}

.tech-item {
    border: 1px solid rgba(255,255,255,0.13);
    background: rgba(255,255,255,0.06);
    color: #E2E8F0;
    border-radius: 999px;
    padding: 7px 12px;
    font-size: 12px;
}


/* ============================================================
   PROJECT
   ============================================================ */

.project-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    padding: 25px;
    min-height: 220px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(15,23,42,0.04);
}

.project-number {
    color: #2563EB;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.project-card h3 {
    color: #0F172A;
    font-size: 18px;
    margin: 0 0 10px 0;
}

.project-card p {
    color: #64748B;
    font-size: 13px;
    line-height: 1.65;
    margin-bottom: 15px;
}

.project-tag {
    display: inline-block;
    padding: 6px 9px;
    border-radius: 7px;
    background: #EFF6FF;
    color: #1D4ED8;
    font-size: 11px;
    font-weight: 700;
    margin: 3px;
}


/* ============================================================
   CTA
   ============================================================ */

.cta {
    background:
        radial-gradient(
            circle at 90% 20%,
            rgba(59,130,246,0.18),
            transparent 35%
        ),
        #172554;

    border-radius: 22px;
    padding: 38px;
    color: white;
    margin: 38px 0;
}

.cta h2 {
    font-size: 28px;
    margin: 0 0 10px 0;
}

.cta p {
    color: #CBD5E1;
    line-height: 1.65;
    margin: 0;
}


/* ============================================================
   CONTACT
   ============================================================ */

.contact-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 23px;
    min-height: 145px;
    margin-bottom: 16px;
}

.contact-card h3 {
    color: #0F172A;
    font-size: 16px;
    margin: 0 0 8px 0;
}

.contact-card p {
    color: #64748B;
    font-size: 13px;
    line-height: 1.6;
    margin: 0;
}

.contact-card a {
    color: #2563EB;
    text-decoration: none;
    font-weight: 600;
}


/* ============================================================
   FORM
   ============================================================ */

div[data-testid="stForm"] {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 5px 20px rgba(15,23,42,0.05);
}

label {
    color: #334155 !important;
    font-weight: 600 !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-color: #CBD5E1 !important;
}


/* ============================================================
   SUCCESS
   ============================================================ */

.success-box {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #065F46;
    border-radius: 14px;
    padding: 18px;
    margin: 15px 0;
    font-weight: 700;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    padding: 30px 0 10px 0;
    margin-top: 45px;
    border-top: 1px solid #E2E8F0;
    color: #94A3B8;
    font-size: 12px;
}

.footer strong {
    color: #475569;
}


/* ============================================================
   ============================================================
   FLOATING CHATBOT
   ============================================================
   ============================================================ */

/*
   IMPORTANT:
   The container itself is fixed to the browser window.
   It is NOT inside the normal website columns.
*/

.st-key-floating_chatbot {

    position: fixed !important;

    right: 24px !important;
    bottom: 24px !important;

    width: 390px !important;
    max-width: calc(100vw - 30px) !important;

    z-index: 999999 !important;

    background: white !important;

    border-radius: 20px !important;

    border: 1px solid #D8E0EA !important;

    box-shadow:
        0 20px 55px rgba(15,23,42,0.22),
        0 5px 15px rgba(15,23,42,0.08) !important;

    overflow: hidden !important;

}


/* Chat header */

.chat-header {

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E3A8A
        );

    color: white;

    padding: 17px 18px;

    border-radius: 18px 18px 0 0;

}

.chat-header-title {
    font-size: 16px;
    font-weight: 800;
}

.chat-header-subtitle {
    font-size: 11px;
    color: #CBD5E1;
    margin-top: 3px;
}


/* Chat messages */

.chat-message {
    padding: 10px 12px;
    border-radius: 12px;
    margin: 6px 0;
    font-size: 12px;
    line-height: 1.5;
}

.chat-assistant {
    background: #EFF6FF;
    color: #1E3A8A;
    border: 1px solid #DBEAFE;
}

.chat-user {
    background: #0F172A;
    color: white;
    margin-left: 30px;
}


/* Chatbot button */

.chat-option button {

    min-height: 36px !important;

    font-size: 12px !important;

    text-align: left !important;

    padding: 6px 10px !important;

    border-radius: 9px !important;

    background: white !important;

    border: 1px solid #DBEAFE !important;

    color: #1E40AF !important;

}

.chat-option button:hover {

    background: #EFF6FF !important;

    border-color: #93C5FD !important;

}


/* Chat form inputs */

.st-key-floating_chatbot input,
.st-key-floating_chatbot textarea {

    font-size: 12px !important;

    border-radius: 9px !important;

}


/* Submit button */

.st-key-floating_chatbot
button[kind="primary"] {

    background: #2563EB !important;

    color: white !important;

    border: none !important;

}


/* Minimized chatbot */

.st-key-floating_chatbot.chat-minimized {

    width: auto !important;

    max-width: none !important;

    background: transparent !important;

    border: none !important;

    box-shadow: none !important;

}


/* Mobile */

@media (max-width: 600px) {

    .st-key-floating_chatbot {

        right: 10px !important;
        bottom: 10px !important;

        width: calc(100vw - 20px) !important;

        max-width: calc(100vw - 20px) !important;

        border-radius: 17px !important;

    }

    .hero {

        padding: 38px 25px;

        border-radius: 18px;

    }

    .hero h1 {

        font-size: 34px;

    }

    .brand-title {

        font-size: 31px;

    }

    .brand-subtitle {

        font-size: 11px;

    }

}


/* Hide empty space generated around fixed chatbot */

.st-key-floating_chatbot > div {

    background: transparent !important;

}


/* ============================================================
   END CHATBOT
   ============================================================ */

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# BRAND
# ============================================================

html(
    """
    <div class="brand-wrapper">

        <div class="brand-title">
            🚚
            <span class="logi-text">Logi</span><span class="intelli-text">Intelli</span>
        </div>

        <div class="brand-subtitle">
            Logistics Analytics • AI & Predictive Intelligence • BI Automation
        </div>

    </div>
    """
)


# ============================================================
# NAVIGATION
# ============================================================

html('<div class="nav-wrapper">')

nav_cols = st.columns(6)

navigation = [
    ("🏠", "Home"),
    ("📊", "Services"),
    ("🚀", "Projects"),
    ("📝", "Request Project"),
    ("👤", "About"),
    ("📞", "Contact"),
]

for i, (icon, name) in enumerate(navigation):

    with nav_cols[i]:

        if st.button(
            f"{icon} {name}",
            key=f"nav_{name}",
            use_container_width=True,
        ):

            st.session_state.page = name
            st.rerun()

html("</div>")


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    html(
        """
        <div class="hero">

            <div class="hero-content">

                <div class="hero-badge">
                    LOGISTICS • DATA • AI • BUSINESS INTELLIGENCE
                </div>

                <h1>
                    Turn Logistics Data Into
                    <span>Business Intelligence</span>
                </h1>

                <p>
                    LogiIntelli helps logistics and operations teams
                    transform complex shipment data into actionable
                    dashboards, predictive analytics, AI solutions
                    and automated reporting systems.
                </p>

            </div>

        </div>
        """
    )


    # ========================================================
    # METRICS
    # ========================================================

    metric_cols = st.columns(4)

    metrics = [
        ("🎯", "10+ Years", "Analytics & Industry Experience"),
        ("📊", "50+ Pipelines", "Analytics & AI Solutions"),
        ("⚡", "24/7", "Automated Data Systems"),
        ("🤖", "AI + BI", "Modern Technology Architecture"),
    ]

    for col, (icon, value, label) in zip(metric_cols, metrics):

        with col:

            html(
                f"""
                <div class="metric-card">

                    <div class="metric-icon">
                        {icon}
                    </div>

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
    # SERVICES
    # ========================================================

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                What We Do
            </div>

            <div class="section-title">
                Data, AI & Logistics Intelligence
            </div>

            <div class="section-subtitle">
                Practical analytics solutions designed around
                real operational problems and measurable
                business outcomes.
            </div>

        </div>
        """
    )

    services = [
        (
            "📊",
            "Business Intelligence",
            "Interactive dashboards and KPI systems for management and operations.",
        ),
        (
            "🚚",
            "Logistics Analytics",
            "Shipment, hub, delivery, SLA, ageing and operational performance analytics.",
        ),
        (
            "🤖",
            "AI & Predictive Analytics",
            "Machine learning models for delay prediction, forecasting and risk analysis.",
        ),
        (
            "⚙️",
            "Data Automation",
            "Automated MIS, ETL pipelines, API integrations and scheduled reporting.",
        ),
        (
            "🗄️",
            "SQL & Data Engineering",
            "High-performance SQL queries, data transformation and analytics-ready datasets.",
        ),
        (
            "📈",
            "Advanced Analytics",
            "Customer, seller, demand, productivity and business performance analytics.",
        ),
    ]

    cols = st.columns(3)

    for i, (icon, title, description) in enumerate(services):

        with cols[i % 3]:

            html(
                f"""
                <div class="card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """
            )


    # ========================================================
    # WORKFLOW
    # ========================================================

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Logistics Intelligence
            </div>

            <div class="section-title">
                From Shipment Event to Decision
            </div>

            <div class="section-subtitle">
                Connect operational events across the complete
                shipment lifecycle.
            </div>

        </div>

        <div class="workflow">

            <div class="workflow-step">Booking</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Pickup</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Inbound</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Processing</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Transit</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Out for Delivery</div>
            <div class="workflow-arrow">→</div>

            <div class="workflow-step">Delivery</div>

        </div>
        """
    )


    # ========================================================
    # TECHNOLOGY
    # ========================================================

    html(
        """
        <div class="tech-strip">

            <div class="tech-title">
                Technology & Analytics Stack
            </div>

            <div class="tech-list">

                <div class="tech-item">Power BI</div>
                <div class="tech-item">SQL</div>
                <div class="tech-item">Python</div>
                <div class="tech-item">Pandas</div>
                <div class="tech-item">NumPy</div>
                <div class="tech-item">XGBoost</div>
                <div class="tech-item">Machine Learning</div>
                <div class="tech-item">REST APIs</div>
                <div class="tech-item">ETL</div>
                <div class="tech-item">DAX</div>
                <div class="tech-item">Excel</div>
                <div class="tech-item">Streamlit</div>

            </div>

        </div>
        """
    )


    # ========================================================
    # WHY LOGIINTELLI
    # ========================================================

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Why LogiIntelli
            </div>

            <div class="section-title">
                Built for Real Business Problems
            </div>

        </div>
        """
    )

    why_items = [
        (
            "🎯",
            "Business Focused",
            "Analytics are designed around operational KPIs and business decisions.",
        ),
        (
            "🚚",
            "Logistics Expertise",
            "Deep understanding of shipment lifecycle, hubs, SLA and delivery operations.",
        ),
        (
            "⚡",
            "Automation First",
            "Reduce repetitive reporting through APIs, ETL and automated data pipelines.",
        ),
        (
            "🤖",
            "AI Ready",
            "Use machine learning where prediction can improve operational decisions.",
        ),
    ]

    cols = st.columns(4)

    for i, (icon, title, description) in enumerate(why_items):

        with cols[i]:

            html(
                f"""
                <div class="why-card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """
            )


    # ========================================================
    # CTA
    # ========================================================

    html(
        """
        <div class="cta">

            <h2>
                Have a Data or Logistics Challenge?
            </h2>

            <p>
                Let's convert your operational data into
                dashboards, automation and intelligent
                decision-support systems.
            </p>

        </div>
        """
    )

    if st.button(
        "📝 Discuss Your Project",
        key="home_project",
        use_container_width=True,
    ):

        st.session_state.page = "Request Project"
        st.rerun()


# ============================================================
# SERVICES
# ============================================================

elif st.session_state.page == "Services":

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Our Services
            </div>

            <div class="section-title">
                Analytics & Technology Solutions
            </div>

            <div class="section-subtitle">
                End-to-end solutions covering business intelligence,
                logistics analytics, AI, automation and data engineering.
            </div>

        </div>
        """
    )

    service_details = [
        (
            "📊",
            "Power BI & Business Intelligence",
            [
                "Management dashboards",
                "Operational KPI dashboards",
                "Real-time / near-real-time reporting",
                "DAX & Power Query",
                "Drill-down analytics",
                "Automated refresh architecture",
            ],
        ),
        (
            "🚚",
            "Courier & Logistics Analytics",
            [
                "Shipment tracking analytics",
                "SLA performance",
                "TAT analytics",
                "Shipment ageing",
                "Hub performance",
                "Delivery productivity",
            ],
        ),
        (
            "🤖",
            "Machine Learning & AI",
            [
                "Shipment delay prediction",
                "Demand forecasting",
                "Customer churn prediction",
                "Risk prediction",
                "Classification models",
                "Predictive analytics",
            ],
        ),
        (
            "⚙️",
            "Data Automation",
            [
                "Daily MIS automation",
                "API integration",
                "Automated Excel reporting",
                "Scheduled data pipelines",
                "Email reporting",
                "Data validation",
            ],
        ),
        (
            "🗄️",
            "SQL & Data Engineering",
            [
                "Advanced SQL",
                "MySQL optimization",
                "Data transformation",
                "ETL pipelines",
                "Data modelling",
                "Analytics-ready datasets",
            ],
        ),
        (
            "📈",
            "Advanced Business Analytics",
            [
                "Customer analytics",
                "Seller analytics",
                "Demand analytics",
                "Productivity analytics",
                "Revenue analytics",
                "Performance analytics",
            ],
        ),
    ]

    cols = st.columns(3)

    for i, (icon, title, items) in enumerate(service_details):

        with cols[i % 3]:

            list_html = "".join(
                f"<li>{item}</li>"
                for item in items
            )

            html(
                f"""
                <div class="card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <ul class="service-list">
                        {list_html}
                    </ul>

                </div>
                """
            )


# ============================================================
# PROJECTS
# ============================================================

elif st.session_state.page == "Projects":

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Selected Projects
            </div>

            <div class="section-title">
                Analytics & AI Solutions
            </div>

            <div class="section-subtitle">
                Examples of practical analytics systems for
                logistics, operations and business intelligence.
            </div>

        </div>
        """
    )

    projects = [
        (
            "01",
            "Courier Operations Dashboard",
            "End-to-end Power BI dashboard covering shipments, deliveries, SLA, productivity and operational KPIs.",
            ["Power BI", "SQL", "DAX", "ETL"],
        ),
        (
            "02",
            "Shipment TAT & Ageing Analytics",
            "Analyse shipment lifecycle, ageing buckets, TAT performance and delayed shipment patterns.",
            ["SQL", "Power BI", "Analytics"],
        ),
        (
            "03",
            "Hub Performance Analytics",
            "Hub-level performance analysis covering inbound, outbound, processing, SLA and productivity.",
            ["Power BI", "SQL", "KPI"],
        ),
        (
            "04",
            "Inbound / Outbound Analytics",
            "Monitor operational flow and identify bottlenecks across courier hubs and service centres.",
            ["SQL", "Power BI", "Operations"],
        ),
        (
            "05",
            "Shipment Delay Prediction AI",
            "XGBoost machine learning model to predict shipment delays and identify high-risk shipments.",
            ["Python", "XGBoost", "ML", "Streamlit"],
        ),
        (
            "06",
            "Automated Daily MIS Engine",
            "Automated data extraction, transformation and reporting system for recurring business MIS.",
            ["Python", "SQL", "API", "Automation"],
        ),
    ]

    cols = st.columns(3)

    for i, (number, title, description, tags) in enumerate(projects):

        with cols[i % 3]:

            tag_html = "".join(
                f'<span class="project-tag">{tag}</span>'
                for tag in tags
            )

            html(
                f"""
                <div class="project-card">

                    <div class="project-number">
                        PROJECT {number}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                    <div>
                        {tag_html}
                    </div>

                </div>
                """
            )


# ============================================================
# REQUEST PROJECT
# ============================================================

elif st.session_state.page == "Request Project":

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Let's Work Together
            </div>

            <div class="section-title">
                Request a Project
            </div>

            <div class="section-subtitle">
                Tell us about your requirement. We will review
                your requirement and get back to you.
            </div>

        </div>
        """
    )

    if st.session_state.submitted:

        html(
            """
            <div class="success-box">
                ✅ Your project request has been submitted successfully.
                Thank you for contacting LogiIntelli.
            </div>
            """
        )

        if st.button(
            "Submit Another Request",
            key="new_request",
        ):

            st.session_state.submitted = False
            st.rerun()

    else:

        with st.form("project_request_form"):

            col1, col2 = st.columns(2)

            with col1:

                company = st.text_input(
                    "Company Name",
                    placeholder="Your company name",
                )

                contact = st.text_input(
                    "Contact Person *",
                    placeholder="Your name",
                )

                email = st.text_input(
                    "Business Email *",
                    placeholder="name@company.com",
                )

                phone = st.text_input(
                    "Phone / WhatsApp",
                    placeholder="+91 XXXXX XXXXX",
                )

            with col2:

                service = st.selectbox(
                    "Required Solution",
                    [
                        "Power BI Dashboard",
                        "Logistics Analytics",
                        "SQL / Data Engineering",
                        "Python Automation",
                        "Machine Learning / AI",
                        "API Integration",
                        "MIS Automation",
                        "Other",
                    ],
                )

                data_source = st.selectbox(
                    "Current Data Source",
                    [
                        "MySQL / SQL Database",
                        "Excel / CSV",
                        "API / JSON",
                        "Power BI",
                        "Multiple Sources",
                        "Other",
                    ],
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
                )

            requirement = st.text_area(
                "Requirement",
                placeholder=(
                    "Please describe your business problem, "
                    "current process and expected solution..."
                ),
                height=180,
            )

            submitted = st.form_submit_button(
                "🚀 Submit Project Request",
                use_container_width=True,
            )

        if submitted:

            errors = []

            if not contact.strip():
                errors.append(
                    "Contact Person is required."
                )

            if not email.strip():
                errors.append(
                    "Business Email is required."
                )

            email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

            if (
                email.strip()
                and not re.match(
                    email_pattern,
                    email.strip(),
                )
            ):

                errors.append(
                    "Please enter a valid email address."
                )

            if not requirement.strip():

                errors.append(
                    "Requirement details are required."
                )

            if errors:

                for error in errors:
                    st.error(error)

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
                    "Source": "Request Project Form",
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

                    if response.status_code in [200, 201]:

                        st.session_state.submitted = True
                        st.rerun()

                    else:

                        st.error(
                            "Unable to submit the request. "
                            "Please try again."
                        )

                except requests.exceptions.RequestException:

                    st.error(
                        "Unable to connect to the submission service."
                    )


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                About LogiIntelli
            </div>

            <div class="section-title">
                Turning Operational Data Into Intelligence
            </div>

            <div class="section-subtitle">
                LogiIntelli focuses on practical data analytics,
                business intelligence, AI and automation solutions
                for logistics and operations.
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

                <h3>
                    Our Mission
                </h3>

                <p>
                    Help businesses make faster and better decisions
                    by converting complex operational data into
                    simple, actionable intelligence.
                </p>

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

                <h3>
                    Our Approach
                </h3>

                <p>
                    Combine domain knowledge, analytics, automation
                    and AI to build solutions that solve real-world
                    business problems.
                </p>

            </div>
            """
        )

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Core Expertise
            </div>

            <div class="section-title">
                Technology Meets Domain Knowledge
            </div>

        </div>
        """
    )

    expertise = [
        (
            "📊",
            "Business Intelligence",
            "Power BI, DAX, Power Query and management reporting.",
        ),
        (
            "🗄️",
            "Data",
            "SQL, MySQL, ETL, APIs and analytics-ready datasets.",
        ),
        (
            "🤖",
            "Artificial Intelligence",
            "Machine learning, forecasting and predictive analytics.",
        ),
        (
            "🚚",
            "Logistics",
            "Shipment, hub, SLA, TAT and delivery analytics.",
        ),
    ]

    cols = st.columns(4)

    for i, (icon, title, description) in enumerate(expertise):

        with cols[i]:

            html(
                f"""
                <div class="why-card">

                    <div class="card-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """
            )


# ============================================================
# CONTACT
# ============================================================

elif st.session_state.page == "Contact":

    html(
        """
        <div class="section-heading">

            <div class="section-kicker">
                Get In Touch
            </div>

            <div class="section-title">
                Contact LogiIntelli
            </div>

            <div class="section-subtitle">
                Have a dashboard, analytics, automation or AI
                requirement? Let's discuss it.
            </div>

        </div>
        """
    )

    cols = st.columns(3)

    with cols[0]:

        html(
            """
            <div class="contact-card">

                <h3>
                    📧 Email
                </h3>

                <p>
                    <a href="mailto:support@logiintelli.com">
                        support@logiintelli.com
                    </a>
                </p>

                <p style="margin-top:6px;">
                    <a href="mailto:sumansekar1205@gmail.com">
                        sumansekar1205@gmail.com
                    </a>
                </p>

            </div>
            """
        )

    with cols[1]:

        html(
            """
            <div class="contact-card">

                <h3>
                    💬 WhatsApp
                </h3>

                <p>
                    <a
                        href="https://wa.me/918825674102"
                        target="_blank"
                    >
                        +91 8825674102
                    </a>
                </p>

                <p style="margin-top:6px;">
                    Available for project discussions.
                </p>

            </div>
            """
        )

    with cols[2]:

        html(
            """
            <div class="contact-card">

                <h3>
                    🕐 Business Hours
                </h3>

                <p>
                    Monday – Friday<br>
                    9:00 AM – 6:00 PM IST
                </p>

                <p style="margin-top:6px;">
                    India
                </p>

            </div>
            """
        )

    html(
        """
        <div class="cta">

            <h2>
                Ready to Transform Your Data?
            </h2>

            <p>
                Start with your business problem and we'll work
                backwards to the right analytics or technology solution.
            </p>

        </div>
        """
    )

    if st.button(
        "📝 Request a Project",
        key="contact_project",
        use_container_width=True,
    ):

        st.session_state.page = "Request Project"
        st.rerun()


# ============================================================
# FOOTER
# ============================================================

html(
    """
    <div class="footer">

        © 2026 <strong>LogiIntelli</strong> ·
        Logistics Analytics · AI · Business Intelligence · Automation

    </div>
    """
)


# ################################################################
# ################################################################
#
#                  FLOATING CHATBOT
#
# ################################################################
# ################################################################


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


def reset_chatbot():

    st.session_state.chat_step = 0

    st.session_state.chat_data = {}

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Hi! Welcome to LogiIntelli. "
                "I can help you identify the right Analytics, "
                "AI, BI or Automation solution for your business."
            ),
        }
    ]

    st.session_state.chat_open = True


def select_chat_option(option):

    step = st.session_state.chat_step

    questions = [
        {
            "key": "Service",
            "question": "What solution are you looking for?",
            "options": [
                "📊 Power BI Dashboard",
                "🚚 Logistics Analytics",
                "🤖 AI / Machine Learning",
                "⚙️ Automation / MIS",
                "🗄️ SQL / Data Engineering",
                "💡 Not Sure",
            ],
        },
        {
            "key": "Data_Source",
            "question": "What type of data do you currently have?",
            "options": [
                "🗄️ MySQL / SQL Database",
                "📗 Excel / CSV",
                "🔗 API / JSON",
                "📊 Power BI",
                "🔀 Multiple Sources",
                "❓ Not Sure",
            ],
        },
        {
            "key": "Problem",
            "question": "What is the main business problem?",
            "options": [
                "📊 Reporting / Dashboard",
                "⏱️ SLA / TAT Problems",
                "🚚 Shipment / Hub Performance",
                "🤖 Prediction / Forecasting",
                "⚡ Manual Process / Automation",
                "💬 Other",
            ],
        },
        {
            "key": "Timeline",
            "question": "When would you like the solution?",
            "options": [
                "🚀 Within 1 Week",
                "📅 1–2 Weeks",
                "📅 2–4 Weeks",
                "🗓️ 1–2 Months",
                "🔄 Flexible",
            ],
        },
    ]

    if step >= len(questions):
        return

    current = questions[step]

    add_chat_message(
        "user",
        option,
    )

    st.session_state.chat_data[
        current["key"]
    ] = option

    st.session_state.chat_step += 1

    if st.session_state.chat_step < len(questions):

        next_question = questions[
            st.session_state.chat_step
        ]["question"]

        add_chat_message(
            "assistant",
            next_question,
        )

    else:

        add_chat_message(
            "assistant",
            (
                "Great! I understand your project requirement. "
                "Please provide your contact details so our team "
                "can contact you."
            ),
        )

    st.rerun()


# ============================================================
# FLOATING CHATBOT CONTAINER
# ============================================================

with st.container(key="floating_chatbot"):

    # ========================================================
    # MINIMIZED VERSION
    # ========================================================

    if not st.session_state.chat_open:

        st.markdown(
            """
            <div style="
                background:#2563EB;
                color:white;
                border-radius:999px;
                padding:4px;
                box-shadow:0 10px 30px rgba(37,99,235,0.35);
            ">
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "💬 Chat with LogiIntelli",
            key="chat_open_button",
            use_container_width=True,
        ):

            st.session_state.chat_open = True
            st.rerun()


    # ========================================================
    # OPEN CHATBOT
    # ========================================================

    else:

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="chat-header">

                <div class="chat-header-title">
                    🤖 LogiIntelli Assistant
                </div>

                <div class="chat-header-subtitle">
                    Project & Analytics Consultation
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # ----------------------------------------------------
        # CLOSE / MINIMIZE
        # ----------------------------------------------------

        if st.button(
            "− Minimize Chat",
            key="chat_minimize",
            use_container_width=True,
        ):

            st.session_state.chat_open = False
            st.rerun()


        # ----------------------------------------------------
        # MESSAGES
        # ----------------------------------------------------

        for message in st.session_state.chat_messages:

            if message["role"] == "assistant":

                st.markdown(
                    f"""
                    <div class="chat-message chat-assistant">
                        🤖 {message["text"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    f"""
                    <div class="chat-message chat-user">
                        {message["text"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


        # ----------------------------------------------------
        # QUESTION FLOW
        # ----------------------------------------------------

        questions = [
            {
                "key": "Service",
                "question": "What solution are you looking for?",
                "options": [
                    "📊 Power BI Dashboard",
                    "🚚 Logistics Analytics",
                    "🤖 AI / Machine Learning",
                    "⚙️ Automation / MIS",
                    "🗄️ SQL / Data Engineering",
                    "💡 Not Sure",
                ],
            },
            {
                "key": "Data_Source",
                "question": "What type of data do you currently have?",
                "options": [
                    "🗄️ MySQL / SQL Database",
                    "📗 Excel / CSV",
                    "🔗 API / JSON",
                    "📊 Power BI",
                    "🔀 Multiple Sources",
                    "❓ Not Sure",
                ],
            },
            {
                "key": "Problem",
                "question": "What is the main business problem?",
                "options": [
                    "📊 Reporting / Dashboard",
                    "⏱️ SLA / TAT Problems",
                    "🚚 Shipment / Hub Performance",
                    "🤖 Prediction / Forecasting",
                    "⚡ Manual Process / Automation",
                    "💬 Other",
                ],
            },
            {
                "key": "Timeline",
                "question": "When would you like the solution?",
                "options": [
                    "🚀 Within 1 Week",
                    "📅 1–2 Weeks",
                    "📅 2–4 Weeks",
                    "🗓️ 1–2 Months",
                    "🔄 Flexible",
                ],
            },
        ]


        # ----------------------------------------------------
        # OPTIONS
        # ----------------------------------------------------

        if st.session_state.chat_step < len(questions):

            current_question = questions[
                st.session_state.chat_step
            ]

            # Question buttons

            for i, option in enumerate(
                current_question["options"]
            ):

                if st.button(
                    option,
                    key=(
                        f"chat_answer_"
                        f"{st.session_state.chat_step}_"
                        f"{i}"
                    ),
                    use_container_width=True,
                ):

                    select_chat_option(option)


        # ----------------------------------------------------
        # CONTACT FORM
        # ----------------------------------------------------

        else:

            st.markdown(
                """
                <div style="
                    font-size:12px;
                    color:#64748B;
                    margin:8px 0;
                ">
                    Please enter your details below.
                </div>
                """,
                unsafe_allow_html=True,
            )

            chat_name = st.text_input(
                "Name *",
                key="floating_chat_name",
                placeholder="Your name",
            )

            chat_email = st.text_input(
                "Business Email *",
                key="floating_chat_email",
                placeholder="name@company.com",
            )

            chat_phone = st.text_input(
                "Phone / WhatsApp",
                key="floating_chat_phone",
                placeholder="+91 XXXXX XXXXX",
            )

            chat_company = st.text_input(
                "Company",
                key="floating_chat_company",
                placeholder="Company name",
            )

            chat_requirement = st.text_area(
                "Additional Requirement",
                key="floating_chat_requirement",
                placeholder=(
                    "Tell us anything else about your project..."
                ),
                height=80,
            )


            # ------------------------------------------------
            # SUBMIT
            # ------------------------------------------------

            if st.button(
                "🚀 Send Project Requirement",
                key="floating_chat_submit",
                type="primary",
                use_container_width=True,
            ):

                errors = []

                if not chat_name.strip():

                    errors.append(
                        "Please enter your name."
                    )

                if not chat_email.strip():

                    errors.append(
                        "Please enter your email."
                    )

                email_pattern = (
                    r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
                )

                if (
                    chat_email.strip()
                    and not re.match(
                        email_pattern,
                        chat_email.strip(),
                    )
                ):

                    errors.append(
                        "Please enter a valid email address."
                    )


                if errors:

                    for error in errors:
                        st.error(error)

                else:

                    payload = {
                        "Date": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Company": chat_company.strip(),
                        "Contact": chat_name.strip(),
                        "Email": chat_email.strip(),
                        "Phone": chat_phone.strip(),

                        "Service":
                            st.session_state.chat_data.get(
                                "Service",
                                "",
                            ),

                        "Data_Source":
                            st.session_state.chat_data.get(
                                "Data_Source",
                                "",
                            ),

                        "Problem":
                            st.session_state.chat_data.get(
                                "Problem",
                                "",
                            ),

                        "Timeline":
                            st.session_state.chat_data.get(
                                "Timeline",
                                "",
                            ),

                        "Requirement":
                            chat_requirement.strip(),

                        "Source":
                            "Website Chatbot",
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


                        if response.status_code in [
                            200,
                            201,
                        ]:

                            add_chat_message(
                                "user",
                                "Contact details submitted.",
                            )

                            add_chat_message(
                                "assistant",
                                (
                                    "✅ Thank you! Your project "
                                    "requirement has been received. "
                                    "Our LogiIntelli team will review "
                                    "it and contact you soon."
                                ),
                            )

                            st.session_state.chat_data[
                                "submitted"
                            ] = True

                            st.rerun()


                        else:

                            st.error(
                                "Unable to submit your requirement. "
                                "Please try again."
                            )


                    except requests.exceptions.RequestException:

                        st.error(
                            "Unable to connect to the submission "
                            "service. Please try again later."
                        )


            # ------------------------------------------------
            # NEW CHAT
            # ------------------------------------------------

            if st.session_state.chat_data.get(
                "submitted",
                False,
            ):

                if st.button(
                    "🔄 Start New Conversation",
                    key="floating_chat_restart",
                    use_container_width=True,
                ):

                    reset_chatbot()
                    st.rerun()


# ============================================================
# END
# ============================================================
