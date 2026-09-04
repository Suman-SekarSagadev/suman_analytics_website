from datetime import datetime
import json
import pandas as pd
import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Suman Analytics | AI, Data & Logistics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CUSTOM CSS (AI/ML Background Image + Dark Visual Theme)
# ============================================================

st.markdown(
    """
<style>
/* HIDE DEFAULT SIDEBAR ENTIRELY */
[data-testid="stSidebar"] {
    display: none !important;
}

/* FIX TOP HEADER BAR BACKGROUND & BUTTON VISIBILITY */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

[data-testid="stHeader"] * {
    color: #F9FAFB !important;
}

/* HIGH-TECH AI/ML DATA ANALYTICS BACKGROUND */
.stApp {
    background-color: #030712;
    background-image: 
        /* Radial glow accents for contrast */
        radial-gradient(circle at 15% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(124, 58, 237, 0.15) 0%, transparent 40%),
        /* Dark overlay gradient to keep text crisp */
        linear-gradient(180deg, rgba(3, 7, 18, 0.82) 0%, rgba(3, 7, 18, 0.92) 100%),
        /* AI Neural Mesh & Data Visualization Image */
        url("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #F3F4F6 !important;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* HEADER WITH GLOW EFFECTS */
.main-title {
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 0px;
    background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.sub-title {
    font-size: 16px;
    color: #9CA3AF !important;
    margin-top: 4px;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
}

/* TOP NAVIGATION STYLING */
div[data-testid="stHorizontalBlock"] {
    background: rgba(17, 24, 39, 0.65);
    padding: 8px 12px;
    border-radius: 12px;
    border: 1px solid rgba(56, 189, 248, 0.2);
    backdrop-filter: blur(12px);
    margin-bottom: 25px;
}

div[data-testid="stHorizontalBlock"] button {
    background-color: transparent !important;
    color: #9CA3AF !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stHorizontalBlock"] button:hover {
    color: #38BDF8 !important;
    background: rgba(56, 189, 248, 0.15) !important;
}

/* HERO CONTAINER WITH GLASSMORPHISM & NEON BORDER */
.hero {
    padding: 40px 35px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.7) 100%);
    border: 1px solid rgba(56, 189, 248, 0.3);
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(16px);
    color: #FFFFFF !important;
    margin-top: 10px;
    margin-bottom: 35px;
}

.hero h1, .hero h2 {
    color: #FFFFFF !important;
    font-weight: 800;
}

.hero p {
    color: #D1D5DB !important;
    font-size: 17px;
    line-height: 1.7;
}

/* SECTIONS */
.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #F9FAFB !important;
    margin-top: 35px;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #9CA3AF !important;
    font-size: 15px;
    margin-bottom: 25px;
}

/* GLASS CARDS & METRICS */
.card, .project-card, .metric-card {
    background: rgba(15, 23, 42, 0.75);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    margin-bottom: 20px;
}

.card:hover, .project-card:hover, .metric-card:hover {
    border-color: rgba(56, 189, 248, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(56, 189, 248, 0.2);
}

.card h3, .project-card h3 {
    color: #38BDF8 !important;
    margin-bottom: 10px;
}

.card p, .card li, .project-card p, .project-card b {
    color: #D1D5DB !important;
    line-height: 1.6;
}

.metric-card {
    text-align: center;
    padding: 20px;
}

.metric-value {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(90deg, #38BDF8, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-label {
    color: #9CA3AF !important;
    font-size: 14px;
    margin-top: 4px;
}

/* WORKFLOW */
.workflow {
    background: rgba(15, 23, 42, 0.75);
    border-radius: 18px;
    padding: 30px 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    margin-top: 20px;
    margin-bottom: 30px;
    overflow-x: auto;
}

.workflow-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 1100px;
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
    font-weight: 700;
    color: #F9FAFB !important;
}

.workflow-desc {
    font-size: 12px;
    color: #9CA3AF !important;
    margin-top: 4px;
}

.workflow-arrow {
    font-size: 22px;
    color: #38BDF8 !important;
}

/* FORM OVERRIDES */
div[data-testid="stForm"] {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div style="text-align:center;">
    <div class="main-title">🚚 SUMAN ANALYTICS</div>
    <div class="sub-title">Logistics Analytics • AI & Predictive Intelligence • BI Automation</div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# TOP NAVIGATION BAR (Horizontal Pill-Buttons)
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

nav_cols = st.columns(6)
pages = ["Home", "Services", "Projects", "Request Project", "About", "Contact"]

for idx, page_name in enumerate(pages):
    with nav_cols[idx]:
        is_selected = st.session_state.page == page_name
        btn_label = f"• {page_name} •" if is_selected else page_name
        if st.button(btn_label, key=f"nav_{page_name}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

page = st.session_state.page

# ============================================================
# HOME
# ============================================================

if page == "Home":
    st.markdown(
        """
<div class="hero">
<h1>Logistics Analytics & Artificial Intelligence</h1>
<p>I build practical data analytics, machine learning, business intelligence, and process automation solutions tailored specifically for courier, logistics, and supply chain enterprises.</p>
<p>From ERP/API data pipeline extraction to predictive machine learning models, SQL data engineering, and real-time Power BI dashboards — I turn raw operational logs into high-impact strategic decisions.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">10+</div><div class="metric-label">Years Experience</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">50+</div><div class="metric-label">Analytics & AI Pipelines</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">24/7</div><div class="metric-label">Automated Systems</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">BI + AI</div><div class="metric-label">Tech Architecture</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">What I Build</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Solutions engineered specifically around logistics operations and predictive analytics.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    services = [
        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending, RTO, hub, and state performance.",
        ),
        (
            "🚚",
            "TAT & Ageing",
            "Shipment ageing, transit time, delivery SLA performance, and bottleneck detection.",
        ),
        (
            "⚙️",
            "MIS Automation",
            "Automate daily operational reporting from ERPs, REST APIs, SQL databases, and Excel.",
        ),
        (
            "🏢",
            "Hub Analytics",
            "Measure hub throughput capacity, productivity, service levels, and staffing efficiency.",
        ),
        (
            "🔗",
            "API & ERP Integration",
            "Connect legacy ERPs and modern REST APIs using Python, SQL, and business intelligence suites.",
        ),
        (
            "🤖",
            "Predictive AI & ML",
            "Machine Learning for shipment delay predictions, RTO risk scoring, and demand forecasting.",
        ),
    ]

    for i, service in enumerate(services):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(
                f"""
<div class="card">
<div style="font-size:35px; margin-bottom: 8px;">{service[0]}</div>
<h3>{service[1]}</h3>
<p>{service[2]}</p>
</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Logistics Data Flow</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">End-to-end shipment telemetry from booking to AI-monitored delivery.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="workflow">
<div class="workflow-container">
<div class="workflow-step"><div class="workflow-icon">📦</div><div class="workflow-name">Booking</div><div class="workflow-desc">Shipment Created</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">🚛</div><div class="workflow-name">Pickup</div><div class="workflow-desc">Shipment Picked</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">🏢</div><div class="workflow-name">Inbound</div><div class="workflow-desc">Hub Received</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">🔄</div><div class="workflow-name">Processing</div><div class="workflow-desc">Hub Processing</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">🚚</div><div class="workflow-name">Transit</div><div class="workflow-desc">Shipment Moving</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">📍</div><div class="workflow-name">Out for Delivery</div><div class="workflow-desc">Last Mile</div></div>
<div class="workflow-arrow">→</div>
<div class="workflow-step"><div class="workflow-icon">✅</div><div class="workflow-name">Delivery</div><div class="workflow-desc">Shipment Delivered</div></div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="hero">
<h2>Have a Logistics Data or AI Problem?</h2>
<p>Share your requirement to design custom analytics, machine learning algorithms, or automated data pipelines for your network.</p>
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# SERVICES
# ============================================================

elif page == "Services":
    st.markdown(
        '<div class="section-title">Logistics & AI Solutions</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Project-based analytics and machine learning solutions engineered around your operation.</div>',
        unsafe_allow_html=True,
    )

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
                "Booking vs. delivery velocity",
                "Pending ageing control",
                "RTO minimization metrics",
                "First-attempt delivery rate",
                "Hub SLA rankings",
            ],
        ),
        (
            "🔄",
            "Inbound / Outbound Network",
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
                "Cron-scheduled jobs",
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
                "Anomaly & exception detection",
                "Custom ML algorithms",
            ],
        ),
    ]

    for i in range(0, len(service_details), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(service_details):
                icon, title, items = service_details[i + j]
                with cols[j]:
                    item_html = "".join([f"<li>{item}</li>" for item in items])
                    st.markdown(
                        f"""
<div class="card">
<div style="font-size:35px; margin-bottom: 8px;">{icon}</div>
<h3>{title}</h3>
<ul>{item_html}</ul>
</div>
""",
                        unsafe_allow_html=True,
                    )

# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":
    st.markdown(
        '<div class="section-title">Logistics & AI Projects</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Sample project ideas demonstrating core capabilities in logistics analytics and machine learning.</div>',
        unsafe_allow_html=True,
    )

    projects = [
        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending, RTO, ageing, and hub performance.",
            "Power BI • SQL • DAX",
            "Operations Analytics",
        ),
        (
            "02",
            "Shipment TAT & Ageing",
            "Identify delayed shipments, ageing buckets, route-level delays, and SLA performance limits.",
            "SQL • Python • Power BI",
            "TAT Analytics",
        ),
        (
            "03",
            "Hub Performance Analytics",
            "Compare hubs based on booking, delivery, pending, RTO, weight, and operational SLAs.",
            "SQL • Power BI • DAX",
            "Hub Analytics",
        ),
        (
            "04",
            "Inbound / Outbound Analytics",
            "Analyze shipment movement from origin state and hub to destination hub across transit corridors.",
            "SQL • Python • Power BI",
            "Network Analytics",
        ),
        (
            "05",
            "Shipment Delay Prediction AI",
            "Machine learning model using XGBoost to identify shipments with high probabilities of delay before SLA breaches.",
            "Python • XGBoost • ML",
            "Predictive AI",
        ),
        (
            "06",
            "Automated Daily MIS Engine",
            "ERP/API automated data extraction, transformation, validation, and scheduled report distribution.",
            "Python • SQL • API",
            "Automation",
        ),
    ]

    for i in range(0, len(projects), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(projects):
                number, title, description, tech, category = projects[i + j]
                with cols[j]:
                    st.markdown(
                        f"""
<div class="project-card">
<div style="font-size:13px; color:#38BDF8; font-weight: 700;">PROJECT {number}</div>
<h3>{title}</h3>
<p>{description}</p>
<b>Technology:</b> <p>{tech}</p>
<b>Category:</b> <p>{category}</p>
</div>
""",
                        unsafe_allow_html=True,
                    )

# ============================================================
# REQUEST PROJECT
# ============================================================

elif page == "Request Project":
    st.markdown(
        '<div class="section-title">Request a Project</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="section-subtitle">
    Share your logistics analytics, machine learning, or automation project specifications.
    </div>
    """,
        unsafe_allow_html=True,
    )

    GOOGLE_SHEET_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwRG4BzU91339mhwtD3QIGBkJWphnJkJ3R01LURdLV6Ge8znKM4arEKttRR800MdGBI/exec"

    with st.form("project_request_form"):
        col1, col2 = st.columns(2)

        with col1:
            company_name = st.text_input("Company Name")
            contact_name = st.text_input("Contact Person*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")

        with col2:
            service = st.selectbox(
                "Required Solution",
                [
                    "Power BI Dashboard",
                    "SQL Analytics",
                    "Predictive AI / Machine Learning",
                    "TAT & Ageing Analytics",
                    "Hub Performance",
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
            "Describe Your Requirement*",
            height=150,
            placeholder=(
                "Example: We need an automated daily courier performance "
                "dashboard and an AI model for predicting shipment delay risk."
            ),
        )

        submitted = st.form_submit_button("Submit Project Request")

        if submitted:
            if not contact_name or not email or not requirement:
                st.warning(
                    "Please provide Contact Person, Email, and Requirement details."
                )
            else:
                payload = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Company": company_name,
                    "Contact": contact_name,
                    "Email": email,
                    "Phone": phone,
                    "Service": service,
                    "Data_Source": data_source,
                    "Timeline": timeline,
                    "Requirement": requirement,
                }

                try:
                    response = requests.post(
                        GOOGLE_SHEET_WEB_APP_URL,
                        data=json.dumps(payload),
                        headers={"Content-Type": "text/plain;charset=utf-8"},
                        timeout=10,
                    )

                    if response.status_code == 200:
                        st.success(
                            "Thank you! Your project request has been logged successfully into our system."
                        )
                    else:
                        st.error(
                            f"Submission error ({response.status_code}). Please try again."
                        )

                except Exception as e:
                    st.error(f"Failed to transmit request: {e}")

# ============================================================
# ABOUT
# ============================================================

elif page == "About":
    st.markdown(
        '<div class="section-title">About Suman Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="card">
<p><b>Suman Analytics</b> delivers enterprise-grade analytics, machine learning, and automation solutions engineered for the logistics, courier, and supply chain industries.</p>
<p>By processing complex operational streams into interactive dashboards, predictive AI models, and automated data pipelines, businesses unlock end-to-end visibility, decrease manual reporting work, and optimize delivery SLA performance.</p>
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":
    st.markdown(
        '<div class="section-title">Contact Information</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
<div class="card">
<h3>Email</h3>
<p><a href="mailto:sumansekar1205@gmail.com" style="color: #38BDF8;">sumansekar1205@gmail.com</a></p>
<h3>Phone / WhatsApp</h3>
<p><a href="https://wa.me/918825674102" target="_blank" style="color: #38BDF8;">📱 +91 8825674102 (Chat on WhatsApp)</a></p>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
<div class="card">
<h3>LinkedIn</h3>
<p><a href="https://linkedin.com/in/sumansekar12/" target="_blank" style="color: #38BDF8;">linkedin.com/in/sumansekar12/</a></p>
<h3>GitHub</h3>
<p><a href="https://github.com/Suman-SekarSagadev" target="_blank" style="color: #38BDF8;">github.com/Suman-SekarSagadev</a></p>
</div>
""",
            unsafe_allow_html=True,
        )
