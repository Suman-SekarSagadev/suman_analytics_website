from datetime import datetime
import json
import pandas as pd
import requests
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Suman Analytics | Logistics Analytics & Automation",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS (Ensures visibility across light & dark themes)
# ============================================================

st.markdown(
    """
<style>
/* MAIN APP BACKGROUND & GLOBAL COLOR FIXES */
.stApp {
    background-color: #f7f9fc;
    color: #111827 !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* HEADER */
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
    color: #111827 !important;
}

.sub-title {
    font-size: 18px;
    color: #4b5563 !important;
    margin-top: 5px;
}

/* HERO */
.hero {
    padding: 45px 35px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1f2937 55%,
        #374151 100%
    );
    color: #ffffff !important;
    margin-top: 20px;
    margin-bottom: 35px;
}

.hero h1, .hero h2, .hero p {
    color: #ffffff !important;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 12px;
}

.hero h2 {
    font-size: 30px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
    line-height: 1.7;
}

/* SECTIONS */
.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #111827 !important;
    margin-top: 35px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #4b5563 !important;
    font-size: 16px;
    margin-bottom: 25px;
}

/* CARDS */
.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    min-height: 190px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

.card h3 {
    color: #111827 !important;
    margin-bottom: 10px;
}

.card p, .card li {
    color: #374151 !important;
    line-height: 1.6;
}

/* PROJECT CARDS */
.project-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    min-height: 280px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

.project-card h3 {
    color: #111827 !important;
}

.project-card p, .project-card b {
    color: #374151 !important;
    line-height: 1.6;
}

/* METRIC CARDS */
.metric-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    text-align: center;
    margin-bottom: 15px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #111827 !important;
}

.metric-label {
    color: #4b5563 !important;
    font-size: 14px;
}

/* WORKFLOW */
.workflow {
    background: #ffffff;
    border-radius: 18px;
    padding: 30px 20px;
    border: 1px solid #e5e7eb;
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
    color: #111827 !important;
}

.workflow-desc {
    font-size: 12px;
    color: #6b7280 !important;
    margin-top: 4px;
}

.workflow-arrow {
    font-size: 25px;
    font-weight: bold;
    color: #9ca3af !important;
    padding: 0 5px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
<div style="text-align:center;">
<h1>🚚</h1>
<h2>SUMAN ANALYTICS</h2>
<p>Logistics Analytics & Automation</p>
</div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Services",
        "Projects",
        "Request Project",
        "About",
        "Contact",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Building data-driven solutions for courier, logistics and supply-chain businesses."
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div style="text-align:center;">
<div class="main-title">SUMAN ANALYTICS</div>
<div class="sub-title">Logistics Analytics • Automation • BI • AI</div>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HOME
# ============================================================

if page == "Home":
    st.markdown(
        """
<div class="hero">
<h1>Logistics Analytics & Automation Solutions</h1>
<p>I build practical data analytics, business intelligence, automation and predictive solutions for logistics and courier businesses.</p>
<p>From ERP/API data extraction to SQL processing, Power BI dashboards, automated MIS and predictive analytics — I convert operational data into business decisions.</p>
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
            '<div class="metric-card"><div class="metric-value">50+</div><div class="metric-label">Analytics Solutions</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">24/7</div><div class="metric-label">Automation</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">BI + AI</div><div class="metric-label">Technology</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">What I Build</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Solutions designed specifically around logistics operations.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    services = [
        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending, RTO, hub and state performance.",
        ),
        (
            "🚚",
            "TAT & Ageing",
            "Shipment ageing, transit time, delivery TAT and operational bottleneck analysis.",
        ),
        (
            "⚙️",
            "MIS Automation",
            "Automate daily MIS from ERP, APIs, SQL databases and Excel sources.",
        ),
        (
            "🏢",
            "Hub Analytics",
            "Measure hub productivity, service levels, ageing, delivery and operational performance.",
        ),
        (
            "🔗",
            "API & ERP Integration",
            "Connect ERP and REST APIs with Python, SQL and BI reporting systems.",
        ),
        (
            "🤖",
            "Predictive Analytics",
            "Shipment delay prediction, risk scoring and operational forecasting.",
        ),
    ]

    for i, service in enumerate(services):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(
                f"""
<div class="card">
<div style="font-size:35px;">{service[0]}</div>
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
        '<div class="section-subtitle">End-to-end shipment movement from booking to delivery.</div>',
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
<h2>Have a Logistics Data Problem?</h2>
<p>Share your requirement and I can help design a practical analytics, automation or reporting solution around your business process.</p>
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# SERVICES
# ============================================================

elif page == "Services":
    st.markdown(
        '<div class="section-title">Logistics Solutions</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Project-based analytics and automation solutions based on your business requirement.</div>',
        unsafe_allow_html=True,
    )

    service_details = [
        (
            "📊",
            "Courier Operations Dashboard",
            [
                "Booking volume",
                "Delivery performance",
                "Pending shipments",
                "RTO analysis",
                "State & hub performance",
                "Daily / weekly / monthly trends",
            ],
        ),
        (
            "⏱️",
            "TAT & Ageing Analytics",
            [
                "Shipment ageing",
                "Transit TAT",
                "Delivery TAT",
                "Ageing buckets",
                "Delayed shipment identification",
                "SLA performance",
            ],
        ),
        (
            "🏢",
            "Hub Performance Analytics",
            [
                "Hub productivity",
                "Booking vs delivery",
                "Pending ageing",
                "RTO percentage",
                "First attempt delivery",
                "Hub ranking",
            ],
        ),
        (
            "🔄",
            "Inbound / Outbound Analytics",
            [
                "State-to-state movement",
                "Hub inbound",
                "Hub outbound",
                "Processing time",
                "Movement ageing",
                "Route performance",
            ],
        ),
        (
            "⚙️",
            "MIS Automation",
            [
                "ERP data extraction",
                "API integration",
                "Python automation",
                "Excel report generation",
                "Scheduled reports",
                "Email automation",
            ],
        ),
        (
            "🤖",
            "Predictive Analytics",
            [
                "Shipment delay prediction",
                "Risk scoring",
                "Demand forecasting",
                "Hub workload prediction",
                "Exception detection",
                "Machine learning models",
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
<div style="font-size:35px;">{icon}</div>
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
        '<div class="section-title">Logistics Projects</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Sample project ideas demonstrating practical logistics analytics capabilities.</div>',
        unsafe_allow_html=True,
    )

    projects = [
        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending, RTO, ageing and hub performance.",
            "Power BI • SQL • DAX",
            "Operations Analytics",
        ),
        (
            "02",
            "Shipment TAT & Ageing",
            "Identify delayed shipments, ageing buckets, route-level delays and SLA performance.",
            "SQL • Python • Power BI",
            "TAT Analytics",
        ),
        (
            "03",
            "Hub Performance Analytics",
            "Compare hubs based on booking, delivery, pending, RTO, weight and service performance.",
            "SQL • Power BI • DAX",
            "Hub Analytics",
        ),
        (
            "04",
            "Inbound / Outbound Analytics",
            "Analyze shipment movement from origin state and hub to destination hub.",
            "SQL • Python • Power BI",
            "Network Analytics",
        ),
        (
            "05",
            "Shipment Delay Prediction",
            "Machine learning model to identify shipments that have a high probability of delayed delivery.",
            "Python • XGBoost • ML",
            "Predictive Analytics",
        ),
        (
            "06",
            "Automated Daily MIS",
            "ERP/API data extraction, transformation, validation and automated report distribution.",
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
<div style="font-size:14px;color:#6b7280;">PROJECT {number}</div>
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
    Tell me about your logistics analytics or automation requirement.
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
                    "TAT & Ageing Analytics",
                    "Hub Performance",
                    "Route Analytics",
                    "Automated MIS",
                    "API / ERP Integration",
                    "Predictive Analytics",
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
                "Example: We need a daily courier performance "
                "dashboard showing booking, delivery, pending, "
                "RTO and hub-wise performance."
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
                    # text/plain header ensures Google Apps Script redirects without HTTP 404/405 errors
                    response = requests.post(
                        GOOGLE_SHEET_WEB_APP_URL,
                        data=json.dumps(payload),
                        headers={"Content-Type": "text/plain;charset=utf-8"},
                        timeout=10,
                    )

                    if response.status_code == 200:
                        st.success(
                            "Thank you! Your project request has been logged successfully into our Google Sheet."
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
<p><b>Suman Analytics</b> provides specialized analytics and automation solutions for the logistics, courier, and supply chain industries.</p>
<p>By transforming raw operational data into interactive dashboards and automated workflows, businesses gain clear operational visibility, reduce manual reporting overhead, and optimize delivery performance.</p>
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
<p><a href="mailto:sumansekar1205@gmail.com">sumansekar1205@gmail.com</a></p>
<h3>Phone / WhatsApp</h3>
<p><a href="https://wa.me/918825674102" target="_blank">📱 +91 8825674102 (Chat on WhatsApp)</a></p>
</div>
""",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
<div class="card">
<h3>LinkedIn</h3>
<p><a href="https://linkedin.com/in/sumansekar12/" target="_blank">linkedin.com/in/sumansekar12/</a></p>
<h3>GitHub</h3>
<p><a href="https://github.com/Suman-SekarSagadev" target="_blank">github.com/Suman-SekarSagadev</a></p>
</div>
""",
            unsafe_allow_html=True,
        )
