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
# GOOGLE APPS SCRIPT WEB APP
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

if "submitted" not in st.session_state:
    st.session_state.submitted = False


# ============================================================
# CUSTOM CSS
# ============================================================

html("""
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
            rgba(37, 99, 235, 0.04),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(14, 165, 233, 0.04),
            transparent 30%
        ),
        #F6F8FC;
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,0.75);
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}


/* ============================================================
   REMOVE DEFAULT STREAMLIT SPACE
============================================================ */

div[data-testid="stVerticalBlock"] > div {
    gap: 0.5rem;
}


/* ============================================================
   BRAND
============================================================ */

.brand-wrapper {
    text-align: center;
    padding: 15px 0 8px 0;
}

.brand-title {
    font-size: 48px;
    line-height: 1;
    font-weight: 950;
    letter-spacing: -2px;
    color: #0B1F3A;
}

.brand-title span {
    color: #2563EB;
}

.brand-subtitle {
    margin-top: 10px;
    color: #64748B;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.1px;
    text-transform: uppercase;
}


/* ============================================================
   NAVIGATION
============================================================ */

.nav-wrapper {
    background: rgba(255,255,255,0.88);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 7px;
    margin: 15px 0 28px 0;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.stButton > button {
    width: 100%;
    min-height: 43px;
    border-radius: 11px;
    border: 1px solid transparent;
    background: transparent;
    color: #475569;
    font-weight: 750;
    font-size: 14px;
    transition: all .2s ease;
}

.stButton > button:hover {
    background: #EFF6FF;
    color: #2563EB;
    border-color: #DBEAFE;
    transform: translateY(-1px);
}


/* ============================================================
   HERO
============================================================ */

.hero {
    position: relative;
    overflow: hidden;
    padding: 65px 58px;
    border-radius: 28px;

    background:
        radial-gradient(
            circle at 85% 15%,
            rgba(96,165,250,0.30),
            transparent 28%
        ),
        radial-gradient(
            circle at 15% 100%,
            rgba(14,165,233,0.18),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #071A33 0%,
            #0B2A52 48%,
            #0758B5 100%
        );

    border: 1px solid rgba(255,255,255,0.08);
    box-shadow:
        0 25px 60px rgba(7,26,51,0.22);

    margin-bottom: 30px;
}

.hero::after {
    content: "";
    position: absolute;
    width: 300px;
    height: 300px;
    right: -120px;
    bottom: -150px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.10);
}

.hero-eyebrow {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 30px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    color: #BFDBFE;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: .8px;
    text-transform: uppercase;
    margin-bottom: 18px;
}

.hero h1 {
    max-width: 850px;
    color: #FFFFFF;
    font-size: 46px;
    line-height: 1.12;
    font-weight: 950;
    letter-spacing: -1.5px;
    margin: 0 0 20px 0;
}

.hero h1 span {
    color: #60A5FA;
}

.hero p {
    max-width: 900px;
    color: #D9E6F5;
    font-size: 17px;
    line-height: 1.75;
    margin: 0 0 12px 0;
}

.hero strong {
    color: #FFFFFF;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 27px;
}

.hero-tag {
    padding: 8px 13px;
    border-radius: 30px;
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.14);
    color: #E0F2FE;
    font-size: 12px;
    font-weight: 750;
}


/* ============================================================
   SECTION HEADERS
============================================================ */

.section-heading {
    margin-top: 48px;
    margin-bottom: 22px;
}

.section-kicker {
    color: #2563EB;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.section-title {
    color: #0B1F3A;
    font-size: 32px;
    font-weight: 950;
    letter-spacing: -0.8px;
    margin: 0;
}

.section-subtitle {
    max-width: 850px;
    color: #64748B;
    font-size: 15px;
    line-height: 1.7;
    margin-top: 8px;
}


/* ============================================================
   METRICS
============================================================ */

.metric-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 24px 15px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(15,23,42,0.045);
    transition: all .25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #BFDBFE;
    box-shadow: 0 15px 30px rgba(37,99,235,0.10);
}

.metric-icon {
    font-size: 22px;
    margin-bottom: 7px;
}

.metric-value {
    color: #2563EB;
    font-size: 34px;
    font-weight: 950;
    letter-spacing: -1px;
}

.metric-label {
    color: #64748B;
    font-size: 12px;
    font-weight: 800;
    margin-top: 4px;
}


/* ============================================================
   CARDS
============================================================ */

.card {
    height: 100%;
    background: rgba(255,255,255,0.95);
    border: 1px solid #E2E8F0;
    border-radius: 19px;
    padding: 26px;
    margin-bottom: 18px;
    box-shadow: 0 7px 20px rgba(15,23,42,0.045);
    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease;
}

.card:hover {
    transform: translateY(-5px);
    border-color: #BFDBFE;
    box-shadow: 0 17px 35px rgba(37,99,235,0.10);
}

.card h3 {
    color: #0B1F3A;
    font-size: 19px;
    font-weight: 900;
    margin: 8px 0 10px 0;
}

.card p,
.card li {
    color: #475569;
    font-size: 14px;
    line-height: 1.7;
}

.card ul {
    padding-left: 19px;
    margin-bottom: 0;
}

.card li {
    margin-bottom: 7px;
}

.card-icon {
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    font-size: 25px;
}


/* ============================================================
   WHY LOGIINTELLI
============================================================ */

.why-card {
    background: linear-gradient(
        145deg,
        #FFFFFF,
        #F8FBFF
    );
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 18px;
}

.why-number {
    font-size: 13px;
    color: #2563EB;
    font-weight: 900;
    margin-bottom: 10px;
}

.why-title {
    color: #0B1F3A;
    font-size: 18px;
    font-weight: 900;
    margin-bottom: 8px;
}

.why-text {
    color: #64748B;
    font-size: 14px;
    line-height: 1.7;
}


/* ============================================================
   TECHNOLOGY STRIP
============================================================ */

.tech-strip {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    padding: 22px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    box-shadow: 0 7px 20px rgba(15,23,42,0.04);
}

.tech-pill {
    padding: 9px 15px;
    border-radius: 30px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    color: #334155;
    font-size: 12px;
    font-weight: 800;
}


/* ============================================================
   WORKFLOW
============================================================ */

.workflow {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 22px;
    padding: 30px 18px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.04);
    overflow-x: auto;
}

.workflow-container {
    min-width: 1100px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.workflow-step {
    min-width: 120px;
    text-align: center;
}

.workflow-icon {
    width: 55px;
    height: 55px;
    margin: auto auto 9px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    background: #EFF6FF;
    border: 1px solid #DBEAFE;
    font-size: 25px;
}

.workflow-name {
    color: #0B1F3A;
    font-size: 13px;
    font-weight: 900;
}

.workflow-desc {
    color: #94A3B8;
    font-size: 11px;
    margin-top: 4px;
}

.workflow-arrow {
    color: #2563EB;
    font-size: 23px;
    font-weight: 900;
}


/* ============================================================
   PROJECT CARD
============================================================ */

.project-card {
    height: 100%;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 7px 22px rgba(15,23,42,0.045);
    transition: all .25s ease;
}

.project-card:hover {
    transform: translateY(-5px);
    border-color: #93C5FD;
    box-shadow: 0 18px 35px rgba(37,99,235,0.10);
}

.project-number {
    color: #2563EB;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1px;
}

.project-card h3 {
    color: #0B1F3A;
    font-size: 20px;
    font-weight: 900;
    margin: 9px 0 10px 0;
}

.project-card p {
    color: #64748B;
    font-size: 14px;
    line-height: 1.7;
}

.project-tech {
    display: inline-block;
    margin-top: 5px;
    padding: 6px 11px;
    border-radius: 20px;
    background: #F1F5F9;
    color: #334155;
    font-size: 11px;
    font-weight: 800;
}

.project-category {
    display: inline-block;
    margin-top: 10px;
    padding: 6px 11px;
    border-radius: 20px;
    background: #EFF6FF;
    color: #2563EB;
    font-size: 11px;
    font-weight: 850;
}


/* ============================================================
   CTA
============================================================ */

.cta {
    position: relative;
    overflow: hidden;
    margin-top: 45px;
    padding: 45px 40px;
    border-radius: 24px;
    text-align: center;
    background:
        radial-gradient(
            circle at 50% -50%,
            rgba(96,165,250,0.30),
            transparent 50%
        ),
        linear-gradient(
            135deg,
            #0B1F3A,
            #0B4F91
        );
    box-shadow: 0 20px 45px rgba(11,31,58,0.18);
}

.cta h2 {
    color: #FFFFFF;
    font-size: 29px;
    font-weight: 950;
    margin-bottom: 10px;
}

.cta p {
    max-width: 750px;
    margin: auto;
    color: #DCEBFA;
    font-size: 15px;
    line-height: 1.7;
}


/* ============================================================
   CONTACT
============================================================ */

.contact-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

.contact-item {
    padding: 15px 0;
    border-bottom: 1px solid #F1F5F9;
}

.contact-item:last-child {
    border-bottom: none;
}

.contact-label {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.contact-value {
    margin-top: 4px;
    color: #0B1F3A;
    font-size: 15px;
    font-weight: 750;
}

.contact-link {
    color: #2563EB;
    text-decoration: none;
}

.contact-link:hover {
    text-decoration: underline;
}


/* ============================================================
   FORM
============================================================ */

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 21px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(15,23,42,0.06);
}

div[data-testid="stWidgetLabel"] label {
    color: #0B1F3A !important;
    font-weight: 800 !important;
}

div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea,
div[data-testid="stForm"] select {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

div[data-testid="stForm"] input:focus,
div[data-testid="stForm"] textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.10) !important;
}


/* ============================================================
   FORM SUBMIT
============================================================ */

div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(
        135deg,
        #0B1F3A,
        #2563EB
    ) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 850 !important;
    min-height: 48px !important;
    box-shadow: 0 8px 18px rgba(37,99,235,0.20);
    transition: all .2s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(37,99,235,0.28);
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    margin-top: 60px;
    padding: 35px 20px 10px 20px;
    border-top: 1px solid #E2E8F0;
    text-align: center;
}

.footer-brand {
    color: #0B1F3A;
    font-size: 21px;
    font-weight: 950;
}

.footer-text {
    color: #64748B;
    font-size: 13px;
    margin-top: 7px;
}

.footer-copy {
    color: #94A3B8;
    font-size: 11px;
    margin-top: 14px;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .brand-title {
        font-size: 34px;
        letter-spacing: -1px;
    }

    .brand-subtitle {
        font-size: 10px;
        letter-spacing: .6px;
    }

    .hero {
        padding: 35px 23px;
        border-radius: 20px;
    }

    .hero h1 {
        font-size: 31px;
        letter-spacing: -1px;
    }

    .hero p {
        font-size: 14px;
    }

    .section-title {
        font-size: 26px;
    }

    .metric-value {
        font-size: 28px;
    }

    .card,
    .project-card {
        padding: 22px;
    }

    .cta {
        padding: 35px 22px;
        border-radius: 20px;
    }

    .cta h2 {
        font-size: 25px;
    }
}

</style>
""")


# ============================================================
# HEADER
# ============================================================

html("""
<div class="brand-wrapper">
    <div class="brand-title">
        🚚 Logi<span>Intelli</span>
    </div>

    <div class="brand-subtitle">
        Logistics Analytics • AI • Business Intelligence • Automation
    </div>
</div>
""")


# ============================================================
# NAVIGATION
# ============================================================

html('<div class="nav-wrapper">')

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

        selected = st.session_state.page == page_name

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
            st.session_state.submitted = False
            st.rerun()

html("</div>")


page = st.session_state.page


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    html("""
    <div class="hero">

        <div class="hero-eyebrow">
            🚀 Logistics Intelligence Platform
        </div>

        <h1>
            Turn Logistics Data Into
            <span>Business Intelligence.</span>
        </h1>

        <p>
            <strong>LogiIntelli</strong> helps courier, logistics,
            supply-chain, and e-commerce businesses transform
            operational data into actionable insights.
        </p>

        <p>
            From shipment tracking and TAT analytics to Power BI,
            SQL engineering, automation, predictive AI, and
            machine learning — we build solutions around
            real-world logistics operations.
        </p>

        <div class="hero-tags">
            <div class="hero-tag">📊 Power BI</div>
            <div class="hero-tag">🧠 Predictive AI</div>
            <div class="hero-tag">🗄️ SQL Analytics</div>
            <div class="hero-tag">⚙️ MIS Automation</div>
            <div class="hero-tag">🔗 API Integration</div>
            <div class="hero-tag">🚚 Logistics Intelligence</div>
        </div>

    </div>
    """)


    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("🎯", "10+", "Years Experience"),
        ("📊", "50+", "Analytics Pipelines"),
        ("⚡", "24/7", "Automated Systems"),
        ("🧠", "BI + AI", "Technology Stack"),
    ]

    for col, (icon, value, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            html(f"""
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
            """)


    # --------------------------------------------------------
    # WHAT WE BUILD
    # --------------------------------------------------------

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Our Capabilities
        </div>

        <div class="section-title">
            What We Build
        </div>

        <div class="section-subtitle">
            Practical analytics and AI solutions designed around
            logistics operations, business intelligence, and
            enterprise data.
        </div>

    </div>
    """)


    services = [

        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending shipments, RTO, hub performance, SLA monitoring, and executive KPIs."
        ),

        (
            "⏱️",
            "TAT & Ageing",
            "Shipment ageing, transit TAT, SLA monitoring, bottleneck identification, and delayed shipment analysis."
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate daily reports using SQL, Python, APIs, Excel, ERP systems, and scheduled data pipelines."
        ),

        (
            "🏢",
            "Hub Analytics",
            "Analyze hub throughput, productivity, pending ageing, delivery performance, RTO, and operational efficiency."
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect ERP systems, REST APIs, databases, Python pipelines, and BI platforms into a unified reporting flow."
        ),

        (
            "🤖",
            "Predictive AI",
            "Machine learning solutions for shipment delay prediction, RTO risk, forecasting, anomaly detection, and operational intelligence."
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
                """)


    # --------------------------------------------------------
    # WHY LOGIINTELLI
    # --------------------------------------------------------

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Why LogiIntelli
        </div>

        <div class="section-title">
            Built for Real Logistics Operations
        </div>

        <div class="section-subtitle">
            We focus on the operational problems behind the data,
            not just creating attractive dashboards.
        </div>

    </div>
    """)


    why_items = [

        (
            "01",
            "Domain-focused analytics",
            "Solutions designed around courier, CEP, supply-chain, hub, shipment, TAT, ageing, delivery, and RTO operations."
        ),

        (
            "02",
            "From data to decision",
            "We connect raw operational data to KPIs, dashboards, alerts, predictive models, and management decisions."
        ),

        (
            "03",
            "Automation first",
            "Reduce manual Excel work through SQL, Python, APIs, ETL pipelines, scheduled reporting, and automated MIS."
        ),

        (
            "04",
            "Scalable architecture",
            "Solutions can evolve from simple reporting into automated analytics platforms and AI-powered operational systems."
        ),

    ]


    for i in range(0, len(why_items), 2):

        cols = st.columns(2)

        for j in range(2):

            if i + j >= len(why_items):
                continue

            number, title, description = why_items[i + j]

            with cols[j]:

                html(f"""
                <div class="why-card">

                    <div class="why-number">
                        {number}
                    </div>

                    <div class="why-title">
                        {title}
                    </div>

                    <div class="why-text">
                        {description}
                    </div>

                </div>
                """)


    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Technology
        </div>

        <div class="section-title">
            Technology Stack
        </div>

    </div>

    <div class="tech-strip">

        <div class="tech-pill">Power BI</div>
        <div class="tech-pill">SQL</div>
        <div class="tech-pill">Python</div>
        <div class="tech-pill">Pandas</div>
        <div class="tech-pill">NumPy</div>
        <div class="tech-pill">XGBoost</div>
        <div class="tech-pill">Machine Learning</div>
        <div class="tech-pill">REST APIs</div>
        <div class="tech-pill">ETL</div>
        <div class="tech-pill">DAX</div>
        <div class="tech-pill">Excel</div>
        <div class="tech-pill">Streamlit</div>

    </div>
    """)


    # --------------------------------------------------------
    # DATA FLOW
    # --------------------------------------------------------

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Operational Intelligence
        </div>

        <div class="section-title">
            Logistics Data Flow
        </div>

        <div class="section-subtitle">
            Transform shipment events into operational visibility
            and predictive intelligence.
        </div>

    </div>
    """)


    html("""
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
                <div class="workflow-name">Last Mile</div>
                <div class="workflow-desc">Out for Delivery</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">✅</div>
                <div class="workflow-name">Delivery</div>
                <div class="workflow-desc">Completed</div>
            </div>

        </div>

    </div>
    """)


    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

    html("""
    <div class="cta">

        <h2>
            Have a Logistics Data Problem?
        </h2>

        <p>
            Let's turn your operational data into dashboards,
            automation, predictive analytics, and actionable
            business intelligence.
        </p>

    </div>
    """)


# ============================================================
# SERVICES PAGE
# ============================================================

elif page == "Services":

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Services
        </div>

        <div class="section-title">
            Logistics & AI Solutions
        </div>

        <div class="section-subtitle">
            Project-based analytics, business intelligence,
            automation, and machine learning solutions engineered
            around logistics operations.
        </div>

    </div>
    """)


    service_details = [

        (
            "📊",
            "Courier Operations Dashboard",
            [
                "Booking volume tracking",
                "Delivery performance metrics",
                "Pending shipment monitoring",
                "RTO root-cause analysis",
                "State & hub breakdown",
                "Operational trend monitoring",
            ],
        ),

        (
            "⏱️",
            "TAT & Ageing Analytics",
            [
                "Shipment ageing alerts",
                "Transit TAT monitoring",
                "Last-mile SLA performance",
                "Ageing bucket analysis",
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
            "Inbound / Outbound Analytics",
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
                "Automated alerts",
            ],
        ),

        (
            "🤖",
            "Predictive AI",
            [
                "Shipment delay prediction",
                "RTO probability scoring",
                "Demand forecasting",
                "Hub workload prediction",
                "Anomaly detection",
                "Custom ML models",
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

                    <div class="card-icon">
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
# PROJECTS PAGE
# ============================================================

elif page == "Projects":

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Portfolio
        </div>

        <div class="section-title">
            Logistics & AI Projects
        </div>

        <div class="section-subtitle">
            Examples of analytics, automation, business intelligence,
            and machine learning solutions.
        </div>

    </div>
    """)


    projects = [

        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending shipments, RTO, ageing, hub performance, and management KPIs.",
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
            "Compare hubs using booking, delivery, pending shipments, RTO, shipment weight, productivity, and operational SLA metrics.",
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
            "XGBoost-based machine learning solution designed to identify shipments with high probability of delay before SLA breaches.",
            "Python • XGBoost • ML",
            "Predictive AI",
        ),

        (
            "06",
            "Automated Daily MIS Engine",
            "Automated ERP/API extraction, transformation, validation, reporting, and scheduled operational distribution.",
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

                    <div class="project-number">
                        PROJECT {number}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                    <div class="project-tech">
                        {tech}
                    </div>

                    <br>

                    <div class="project-category">
                        {category}
                    </div>

                </div>
                """)


# ============================================================
# REQUEST PROJECT PAGE
# ============================================================

elif page == "Request Project":

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Start a Project
        </div>

        <div class="section-title">
            Request a Project
        </div>

        <div class="section-subtitle">
            Tell us about your logistics analytics, BI,
            automation, or machine learning requirement.
        </div>

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

            contact_name_clean = contact_name.strip()
            email_clean = email.strip()
            requirement_clean = requirement.strip()

            if not contact_name_clean:

                st.warning(
                    "Please enter the Contact Person name."
                )

            elif not email_clean:

                st.warning(
                    "Please enter your Business Email."
                )

            elif not re.match(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                email_clean
            ):

                st.warning(
                    "Please enter a valid email address."
                )

            elif not requirement_clean:

                st.warning(
                    "Please describe your project requirement."
                )

            else:

                payload = {

                    "Date":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "Company":
                        company_name.strip(),

                    "Contact":
                        contact_name_clean,

                    "Email":
                        email_clean,

                    "Phone":
                        phone.strip(),

                    "Service":
                        service,

                    "Data_Source":
                        data_source,

                    "Timeline":
                        timeline,

                    "Requirement":
                        requirement_clean,

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

                        st.session_state.submitted = True

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
                            "Submission failed. "
                            f"Server returned status "
                            f"{response.status_code}."
                        )

                        st.code(
                            response.text[:500]
                        )


                except requests.exceptions.Timeout:

                    st.error(
                        "⏱️ The request timed out. "
                        "Please try again."
                    )


                except requests.exceptions.ConnectionError:

                    st.error(
                        "🌐 Unable to connect to the project "
                        "request server. Please check your "
                        "internet connection and try again."
                    )


                except Exception as e:

                    st.error(
                        f"⚠️ An unexpected error occurred: {str(e)}"
                    )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "About":

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            About
        </div>

        <div class="section-title">
            About LogiIntelli
        </div>

        <div class="section-subtitle">
            Bridging the gap between complex operational data
            and actionable business decisions.
        </div>

    </div>


    <div class="card">

        <div class="card-icon">
            🚚
        </div>

        <h3>
            Our Mission
        </h3>

        <p>
            LogiIntelli focuses on solving practical logistics
            challenges by transforming raw operational tracking
            data into clean, structured, and actionable
            intelligence.
        </p>

        <p>
            We specialize in end-to-end data pipelines,
            custom BI reporting systems, automated MIS,
            operational analytics, and predictive machine
            learning solutions tailored for courier,
            express, parcel, supply-chain, and e-commerce
            environments.
        </p>

    </div>
    """)


    c1, c2 = st.columns(2)


    with c1:

        html("""
        <div class="card">

            <div class="card-icon">
                🧠
            </div>

            <h3>
                Core Expertise
            </h3>

            <ul>

                <li>
                    Power BI & Interactive Dashboard Engineering
                </li>

                <li>
                    SQL Data Warehousing & ETL Pipelines
                </li>

                <li>
                    Predictive Machine Learning
                </li>

                <li>
                    Automated MIS & Enterprise Reporting
                </li>

                <li>
                    REST API Integrations
                </li>

            </ul>

        </div>
        """)


    with c2:

        html("""
        <div class="card">

            <div class="card-icon">
                🌐
            </div>

            <h3>
                Domain Knowledge
            </h3>

            <ul>

                <li>
                    First-Mile, Mid-Mile & Last-Mile Tracking
                </li>

                <li>
                    TAT & Ageing Optimization
                </li>

                <li>
                    Hub Throughput & Load Balancing
                </li>

                <li>
                    RTO Minimization
                </li>

                <li>
                    Carrier Performance & SLA Benchmarking
                </li>

            </ul>

        </div>
        """)


# ============================================================
# CONTACT PAGE
# ============================================================

elif page == "Contact":

    html("""
    <div class="section-heading">

        <div class="section-kicker">
            Contact
        </div>

        <div class="section-title">
            Let's Talk
        </div>

        <div class="section-subtitle">
            Have a logistics data challenge or want to discuss
            a custom analytics solution?
        </div>

    </div>
    """)


    c1, c2 = st.columns(2)


    with c1:

        html("""
        <div class="contact-card">

            <div class="card-icon">
                📩
            </div>

            <h3 style="color:#0B1F3A; margin-top:12px;">
                Contact Information
            </h3>

            <div class="contact-item">

                <div class="contact-label">
                    Email
                </div>

                <div class="contact-value">

                    <a
                        class="contact-link"
                        href="mailto:support@logiintelli.com"
                    >
                        support@logiintelli.com
                    </a>

                    <br>

                    <a
                        class="contact-link"
                        href="mailto:sumansekar1205@gmail.com"
                    >
                        sumansekar1205@gmail.com
                    </a>

                </div>

            </div>


            <div class="contact-item">

                <div class="contact-label">
                    WhatsApp
                </div>

                <div class="contact-value">

                    <a
                        class="contact-link"
                        href="https://wa.me/918825674102"
                        target="_blank"
                    >
                        +91 8825674102
                    </a>

                </div>

            </div>


            <div class="contact-item">

                <div class="contact-label">
                    Business Hours
                </div>

                <div class="contact-value">
                    Monday – Friday<br>
                    9:00 AM – 6:00 PM IST
                </div>

            </div>


            <div class="contact-item">

                <div class="contact-label">
                    Location
                </div>

                <div class="contact-value">
                    India
                </div>

            </div>

        </div>
        """)


    with c2:

        html("""
        <div class="contact-card">

            <div class="card-icon">
                🚀
            </div>

            <h3 style="color:#0B1F3A; margin-top:12px;">
                Start a Project
            </h3>

            <p style="
                color:#64748B;
                font-size:14px;
                line-height:1.7;
                margin-top:12px;
            ">
                Need a Power BI dashboard, SQL analytics,
                automated MIS, API integration, shipment
                prediction model, or logistics intelligence
                platform?
            </p>

            <p style="
                color:#64748B;
                font-size:14px;
                line-height:1.7;
            ">
                Submit your requirement through the
                <strong>Request Project</strong> section
                and provide a few details about your
                business problem.
            </p>

        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

html("""
<div class="footer">

    <div class="footer-brand">
        🚚 LogiIntelli
    </div>

    <div class="footer-text">
        Logistics AI • Data Analytics • Business Intelligence • Automation
    </div>

    <div class="footer-copy">
        © 2026 LogiIntelli. All rights reserved.
    </div>

</div>
""")
