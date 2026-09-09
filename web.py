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
                "I can help identify the right Analytics, "
                "AI, BI or Automation solution for your business."
            ),
        }
    ],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GLOBAL CSS
# ============================================================

html(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ------------------------------------------------------------
   PAGE
------------------------------------------------------------ */

.stApp {
    background:
        linear-gradient(
            180deg,
            #F8FAFC 0%,
            #FFFFFF 45%,
            #F8FAFC 100%
        );
}

/* ------------------------------------------------------------
   REMOVE STREAMLIT DEFAULT SPACE
------------------------------------------------------------ */

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 1400px !important;
}

/* ------------------------------------------------------------
   HEADER
------------------------------------------------------------ */

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0 20px 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 25px;
}

.brand-wrapper {
    display: flex;
    flex-direction: column;
}

.brand-title {
    font-size: 38px;
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
    font-size: 11px;
    color: #64748B;
    margin-top: 5px;
    letter-spacing: 0.2px;
}

/* ------------------------------------------------------------
   NAVIGATION
------------------------------------------------------------ */

div.stButton > button {
    border-radius: 9px !important;
    border: 1px solid #E2E8F0 !important;
    background: white !important;
    color: #334155 !important;
    font-weight: 600 !important;
    min-height: 38px !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.10) !important;
}

/* ------------------------------------------------------------
   HERO
------------------------------------------------------------ */

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

/* ------------------------------------------------------------
   SECTION
------------------------------------------------------------ */

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

/* ------------------------------------------------------------
   CARDS
------------------------------------------------------------ */

.card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    height: 100%;
    box-shadow: 0 5px 20px rgba(15,23,42,0.04);
    transition: all 0.25s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(15,23,42,0.08);
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

/* ------------------------------------------------------------
   METRICS
------------------------------------------------------------ */

.metric-box {
    background: white;
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

/* ------------------------------------------------------------
   PROJECT
------------------------------------------------------------ */

.project-card {
    background: white;
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

/* ------------------------------------------------------------
   CTA
------------------------------------------------------------ */

.cta {
    background: linear-gradient(
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

/* ------------------------------------------------------------
   FORM
------------------------------------------------------------ */

.form-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}

/* ------------------------------------------------------------
   FOOTER
------------------------------------------------------------ */

.footer {
    border-top: 1px solid #E2E8F0;
    margin-top: 60px;
    padding: 25px 0;
    text-align: center;
    color: #64748B;
    font-size: 12px;
}

/* ============================================================
   SMALL FLOATING CHATBOT - BOTTOM LEFT
============================================================ */

.st-key-floating_chatbot {
    position: fixed !important;

    left: 20px !important;
    bottom: 20px !important;

    width: 270px !important;
    max-width: calc(100vw - 40px) !important;

    z-index: 999999 !important;

    background: white !important;

    border: 1px solid #D9E2EC !important;
    border-radius: 14px !important;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.16),
        0 2px 8px rgba(15, 23, 42, 0.08) !important;

    overflow: hidden !important;
}

/* ------------------------------------------------------------
   CHAT HEADER
------------------------------------------------------------ */

.chat-header {
    background: linear-gradient(
        135deg,
        #0F172A,
        #2563EB
    );

    color: white;

    padding: 11px 13px;

    border-radius: 14px 14px 0 0;
}

.chat-header-title {
    font-size: 13px;
    font-weight: 700;
    line-height: 1.2;
}

.chat-header-subtitle {
    font-size: 9px;
    color: #CBD5E1;
    margin-top: 3px;
}

/* ------------------------------------------------------------
   CHAT BODY
------------------------------------------------------------ */

.chat-body {
    padding: 8px 9px 7px 9px;
    max-height: 360px;
    overflow-y: auto;
}

.chat-message {
    padding: 7px 9px;
    border-radius: 9px;
    margin: 5px 0;

    font-size: 10px;
    line-height: 1.4;
}

.chat-assistant {
    background: #EFF6FF;
    color: #1E3A8A;
    border: 1px solid #DBEAFE;
}

.chat-user {
    background: #0F172A;
    color: white;
    margin-left: 20px;
}

/* ------------------------------------------------------------
   CHAT BUTTONS
------------------------------------------------------------ */

.st-key-floating_chatbot button {
    min-height: 30px !important;

    padding:
        4px 8px !important;

    font-size: 10px !important;

    border-radius: 7px !important;
}

/* ------------------------------------------------------------
   CHAT INPUT
------------------------------------------------------------ */

.st-key-floating_chatbot input,
.st-key-floating_chatbot textarea {
    font-size: 10px !important;
    min-height: 30px !important;
}

/* ------------------------------------------------------------
   CHAT CLOSE BUTTON
------------------------------------------------------------ */

.chat-close {
    font-size: 10px;
    color: #CBD5E1;
}

/* ------------------------------------------------------------
   MOBILE
------------------------------------------------------------ */

@media (max-width: 600px) {

    .hero-title {
        font-size: 38px;
    }

    .hero-text {
        font-size: 14px;
    }

    .brand-title {
        font-size: 30px;
    }

    .st-key-floating_chatbot {
        left: 10px !important;
        bottom: 10px !important;
        width: 250px !important;
        max-width: calc(100vw - 20px) !important;
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
        if st.button(label, use_container_width=True):
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

    # Metrics
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
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """
            )

    st.markdown("<br>", unsafe_allow_html=True)

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

    # Services
    service_cols = st.columns(3)

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
            "Automate repetitive reports, data pipelines, Excel workflows and operational MIS."
        ),
        (
            "🗄️",
            "SQL & Data Engineering",
            "Advanced SQL, data transformation, ETL pipelines and scalable reporting datasets."
        ),
        (
            "🔗",
            "API & Data Integration",
            "Connect APIs, databases, JSON feeds and multiple data sources into one analytics ecosystem."
        ),
    ]

    for i, service in enumerate(services):

        with service_cols[i % 3]:

            icon, title, text = service

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

    # Workflow
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

    workflow_cols = st.columns(4)

    workflow = [
        ("01", "Understand", "Understand your business problem and objectives."),
        ("02", "Analyze", "Study your data sources and identify opportunities."),
        ("03", "Build", "Develop dashboards, models, automation or data solutions."),
        ("04", "Deliver", "Deploy the solution and provide actionable insights."),
    ]

    for col, item in zip(workflow_cols, workflow):

        with col:

            number, title, text = item

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

    # Technology
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

    tech_cols = st.columns(6)

    technologies = [
        "SQL",
        "Python",
        "Power BI",
        "Tableau",
        "PySpark",
        "Machine Learning",
    ]

    for col, tech in zip(tech_cols, technologies):

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

    # CTA
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

    for i, service in enumerate(service_details):

        icon, title, points = service

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
            "Power BI dashboards to monitor hub performance, shipment volume, SLA, TAT and delivery efficiency."
        ),
        (
            "📦",
            "Shipment Tracking & Delay Prediction",
            "AI / Machine Learning",
            "XGBoost-based shipment delay prediction combined with an interactive Streamlit tracking portal."
        ),
        (
            "📈",
            "Demand Forecasting",
            "Machine Learning",
            "Forecast future demand using historical business data and time-series forecasting techniques."
        ),
        (
            "👥",
            "Customer Churn Prediction",
            "Machine Learning",
            "Identify customers with higher churn probability using machine learning classification models."
        ),
        (
            "📊",
            "CPG / FMCG Demand & Seller Analytics",
            "Business Intelligence",
            "Analyze product demand, seller performance, sales trends and business KPIs."
        ),
        (
            "⚙️",
            "Automated MIS & Reporting",
            "Automation",
            "Automate manual reporting workflows using Python, SQL and scheduled data pipelines."
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

    with st.container():

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

        submitted = st.form_submit_button(
            "🚀 Submit Project Request",
            use_container_width=True,
        ) if False else False

        html("</div>")

    if st.button(
        "🚀 Submit Project Request",
        use_container_width=True,
        key="submit_project_request",
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
                "Source": "Website Request Project",
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

                    st.session_state.submitted = True

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

    cols = st.columns(3)

    about_cards = [
        (
            "🎯",
            "Our Mission",
            "Make advanced analytics accessible and useful for real-world businesses."
        ),
        (
            "💡",
            "Our Approach",
            "Combine business understanding, analytics and technology to solve practical problems."
        ),
        (
            "🚀",
            "Our Vision",
            "Build intelligent data solutions that help businesses operate smarter and faster."
        ),
    ]

    for col, item in zip(cols, about_cards):

        with col:

            icon, title, text = item

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
                CONTACT
            </div>

            <div class="hero-title">
                Let's Build Something
                <span>Intelligent</span>
            </div>

            <div class="hero-text">
                Have a dashboard, automation, AI or analytics requirement?
                Let's discuss your business problem.
            </div>

        </div>
        """
    )

    cols = st.columns(3)

    contact_details = [
        (
            "📧",
            "Email",
            "support@logiintelli.com"
        ),
        (
            "📱",
            "WhatsApp",
            "+91 8825674102"
        ),
        (
            "🕘",
            "Working Hours",
            "Monday – Friday<br>9:00 AM – 6:00 PM IST"
        ),
    ]

    for col, item in zip(cols, contact_details):

        with col:

            icon, title, text = item

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

    st.markdown("<br>", unsafe_allow_html=True)

    html(
        """
        <div class="cta">

            <div class="cta-title">
                Ready to Get Started?
            </div>

            <div class="cta-text">
                Submit your requirement and let's discuss
                how LogiIntelli can help.
            </div>

        </div>
        """
    )

    if st.button(
        "📝 Request a Project",
        use_container_width=True,
        key="contact_request_project",
    ):

        st.session_state.page = "Request Project"
        st.rerun()


# ============================================================
# CHATBOT FUNCTIONS
# ============================================================

CHAT_QUESTIONS = [
    {
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
        "question": "What is your main business problem?",
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


def add_chat_message(role, text):

    st.session_state.chat_messages.append(
        {
            "role": role,
            "text": text,
        }
    )


def select_chat_option(option):

    step = st.session_state.chat_step

    if step < len(CHAT_QUESTIONS):

        add_chat_message("user", option)

        if step == 0:
            st.session_state.chat_data["Service"] = option

        elif step == 1:
            st.session_state.chat_data["Data_Source"] = option

        elif step == 2:
            st.session_state.chat_data["Problem"] = option

        elif step == 3:
            st.session_state.chat_data["Timeline"] = option

        st.session_state.chat_step += 1

        if st.session_state.chat_step < len(CHAT_QUESTIONS):

            add_chat_message(
                "assistant",
                CHAT_QUESTIONS[
                    st.session_state.chat_step
                ]["question"],
            )

        else:

            add_chat_message(
                "assistant",
                (
                    "Great 👍 I have the basic requirement. "
                    "Please share your contact details so "
                    "our team can get back to you."
                ),
            )

        st.rerun()


def reset_chat():

    st.session_state.chat_step = 0

    st.session_state.chat_data = {}

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

    st.session_state.chat_open = True

    st.rerun()


# ============================================================
# FLOATING CHATBOT
# ============================================================

if st.session_state.chat_open:

    with st.container(key="floating_chatbot"):

        # Header
        html(
            """
            <div class="chat-header">

                <div class="chat-header-title">
                    🤖 LogiIntelli Assistant
                </div>

                <div class="chat-header-subtitle">
                    Project & Analytics Consultation
                </div>

            </div>
            """
        )

        # Chat messages
        html('<div class="chat-body">')

        for message in st.session_state.chat_messages:

            role = message["role"]
            text = message["text"]

            if role == "assistant":

                html(
                    f"""
                    <div class="chat-message chat-assistant">
                        {text}
                    </div>
                    """
                )

            else:

                html(
                    f"""
                    <div class="chat-message chat-user">
                        {text}
                    </div>
                    """
                )

        html("</div>")

        # Question options
        if st.session_state.chat_step < len(CHAT_QUESTIONS):

            current_question = CHAT_QUESTIONS[
                st.session_state.chat_step
            ]

            for index, option in enumerate(
                current_question["options"]
            ):

                if st.button(
                    option,
                    key=f"chat_option_{st.session_state.chat_step}_{index}",
                    use_container_width=True,
                ):

                    select_chat_option(option)

        # Contact form after questions
        else:

            chat_name = st.text_input(
                "Name",
                placeholder="Your name",
                key="chat_name",
            )

            chat_email = st.text_input(
                "Business Email",
                placeholder="name@company.com",
                key="chat_email",
            )

            chat_phone = st.text_input(
                "Phone / WhatsApp",
                placeholder="+91 XXXXX XXXXX",
                key="chat_phone",
            )

            chat_company = st.text_input(
                "Company",
                placeholder="Company name",
                key="chat_company",
            )

            chat_requirement = st.text_area(
                "Additional Requirement",
                placeholder="Tell us anything else...",
                height=65,
                key="chat_requirement",
            )

            chat_col1, chat_col2 = st.columns(2)

            with chat_col1:

                if st.button(
                    "🚀 Submit",
                    use_container_width=True,
                    key="chat_submit",
                ):

                    if not chat_name.strip():

                        st.error("Enter your name.")

                    elif not chat_email.strip():

                        st.error("Enter your email.")

                    elif not re.match(
                        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                        chat_email.strip(),
                    ):

                        st.error("Enter a valid email.")

                    else:

                        payload = {
                            "Date": datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            "Company": chat_company.strip(),
                            "Contact": chat_name.strip(),
                            "Email": chat_email.strip(),
                            "Phone": chat_phone.strip(),
                            "Service": st.session_state.chat_data.get(
                                "Service",
                                "",
                            ),
                            "Data_Source": st.session_state.chat_data.get(
                                "Data_Source",
                                "",
                            ),
                            "Timeline": st.session_state.chat_data.get(
                                "Timeline",
                                "",
                            ),
                            "Problem": st.session_state.chat_data.get(
                                "Problem",
                                "",
                            ),
                            "Requirement": chat_requirement.strip(),
                            "Source": "Website Chatbot",
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

                                add_chat_message(
                                    "assistant",
                                    (
                                        "✅ Thank you! Your project "
                                        "requirement has been received. "
                                        "Our team will contact you soon."
                                    ),
                                )

                                st.session_state.chat_step = (
                                    len(CHAT_QUESTIONS) + 1
                                )

                                st.rerun()

                            else:

                                st.error(
                                    "Unable to submit. Please try again."
                                )

                        except Exception:

                            st.error(
                                "Connection error. Please try again."
                            )

            with chat_col2:

                if st.button(
                    "🔄 Restart",
                    use_container_width=True,
                    key="chat_restart",
                ):

                    reset_chat()

        st.markdown(
            "<div style='height:3px'></div>",
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE ROUTING
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

        © 2026 <b>LogiIntelli</b>.
        Logistics Analytics • AI • Business Intelligence • Automation

        <br><br>

        📧 support@logiintelli.com
        &nbsp; | &nbsp;
        📱 +91 8825674102
        &nbsp; | &nbsp;
        🇮🇳 India

    </div>
    """
)
