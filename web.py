from datetime import datetime
import json
import streamlit as st
import requests


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LogiIntelli | Logistics AI, Data Analytics & Business Intelligence",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HTML HELPER
# ============================================================

def html(content):
    """
    Render HTML directly using Streamlit's native HTML renderer.
    This prevents HTML from appearing as plain text/code.
    """
    st.html(content)


# ============================================================
# CUSTOM CSS
# ============================================================

html("""
<style>

html, body {
    background-color: #F8FAFC;
}

[data-testid="stAppViewContainer"] {
    background-color: #F8FAFC;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ============================================================
   BRAND
============================================================ */

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 900;
    color: #0B2545;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.sub-title {
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    color: #0066CC;
    letter-spacing: .4px;
    margin-bottom: 25px;
}


/* ============================================================
   NAVIGATION
============================================================ */

.nav-button {
    width: 100%;
}


/* ============================================================
   HERO
============================================================ */

.hero {
    padding: 50px 45px;
    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #0B2545 0%,
            #134074 55%,
            #0066CC 100%
        );

    border: 1px solid #0B2545;

    box-shadow:
        0 15px 35px rgba(11, 37, 69, 0.18);

    margin-top: 15px;
    margin-bottom: 35px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 850;
    margin-bottom: 20px;
}

.hero h2 {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 15px;
}

.hero p {
    color: #E2E8F0;
    font-size: 17px;
    line-height: 1.75;
    margin-bottom: 16px;
}

.hero strong {
    color: #FFFFFF;
}


/* ============================================================
   SECTION TITLES
============================================================ */

.section-title {
    font-size: 30px;
    font-weight: 850;
    color: #0B2545;
    margin-top: 40px;
    margin-bottom: 6px;
}

.section-subtitle {
    color: #64748B;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 25px;
}


/* ============================================================
   CARDS
============================================================ */

.card,
.project-card,
.metric-card {

    background: #FFFFFF;

    padding: 25px;

    border-radius: 16px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 5px 15px rgba(15, 23, 42, 0.05);

    margin-bottom: 20px;

    transition:
        transform .25s ease,
        box-shadow .25s ease,
        border-color .25s ease;
}

.card:hover,
.project-card:hover,
.metric-card:hover {

    transform: translateY(-4px);

    border-color: #0066CC;

    box-shadow:
        0 12px 28px rgba(0, 102, 204, 0.12);
}

.card h2,
.card h3,
.project-card h3 {

    color: #0B2545;

    font-weight: 800;

    margin-bottom: 12px;
}

.card p,
.card li,
.project-card p {

    color: #334155;

    line-height: 1.65;
}

.card li {
    margin-bottom: 7px;
}


/* ============================================================
   METRIC CARDS
============================================================ */

.metric-card {

    text-align: center;

    padding: 25px 15px;
}

.metric-value {

    font-size: 34px;

    font-weight: 900;

    color: #0066CC;

    margin-bottom: 5px;
}

.metric-label {

    color: #64748B;

    font-size: 14px;

    font-weight: 650;
}


/* ============================================================
   SERVICE ICON
============================================================ */

.service-icon {

    font-size: 40px;

    margin-bottom: 8px;
}


/* ============================================================
   WORKFLOW
============================================================ */

.workflow {

    background: #FFFFFF;

    border-radius: 18px;

    padding: 30px 20px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 5px 15px rgba(15, 23, 42, 0.04);

    margin-top: 20px;

    margin-bottom: 30px;

    overflow-x: auto;
}

.workflow-container {

    display: flex;

    align-items: center;

    justify-content: space-between;

    min-width: 1050px;
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

    font-weight: 750;

    color: #0B2545;
}

.workflow-desc {

    font-size: 12px;

    color: #64748B;

    margin-top: 4px;
}

.workflow-arrow {

    font-size: 22px;

    color: #0066CC;

    font-weight: 700;
}


/* ============================================================
   FORM
============================================================ */

div[data-testid="stForm"] {

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 18px;

    padding: 28px;

    box-shadow:
        0 8px 25px rgba(15, 23, 42, 0.06);
}

div[data-testid="stWidgetLabel"] label {

    color: #0B2545 !important;

    font-weight: 700 !important;
}

div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea {

    background: #FFFFFF !important;

    color: #0F172A !important;

    border: 1px solid #CBD5E1 !important;

    border-radius: 9px !important;
}

div[data-testid="stForm"] input:focus,
div[data-testid="stForm"] textarea:focus {

    border-color: #0066CC !important;
}


/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {

    border-radius: 9px;

    border: 1px solid #E2E8F0;

    background: #FFFFFF;

    color: #0B2545;

    font-weight: 700;

    min-height: 42px;

    transition: all .2s ease;
}

.stButton > button:hover {

    background: #0B2545;

    color: #FFFFFF;

    border-color: #0B2545;
}


/* ============================================================
   SUBMIT BUTTON
============================================================ */

div[data-testid="stFormSubmitButton"] button {

    background: #0B2545 !important;

    color: #FFFFFF !important;

    border: none !important;

    border-radius: 9px !important;

    font-weight: 750 !important;

    padding: 10px 25px !important;
}

div[data-testid="stFormSubmitButton"] button:hover {

    background: #0066CC !important;
}


/* ============================================================
   CONTACT LINKS
============================================================ */

.contact-link {

    color: #0066CC;

    text-decoration: none;

    font-weight: 650;
}

.contact-link:hover {

    text-decoration: underline;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {

    text-align: center;

    padding: 35px 20px;

    margin-top: 50px;

    color: #64748B;

    font-size: 14px;

    line-height: 1.7;
}

.footer-title {

    color: #0B2545;

    font-size: 19px;

    font-weight: 850;

    margin-bottom: 10px;
}


/* ============================================================
   MOBILE
============================================================ */

@media (max-width: 768px) {

    .main-title {
        font-size: 32px;
    }

    .sub-title {
        font-size: 13px;
    }

    .hero {
        padding: 30px 22px;
    }

    .hero h1 {
        font-size: 26px;
    }

    .hero p {
        font-size: 15px;
    }

    .section-title {
        font-size: 25px;
    }

}

</style>
""")


# ============================================================
# HEADER
# ============================================================

html("""
<div>
    <div class="main-title">
        🚚 LogiIntelli
    </div>

    <div class="sub-title">
        Logistics Analytics • AI & Predictive Intelligence • BI Automation
    </div>
</div>
""")


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# NAVIGATION
# ============================================================

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
            st.rerun()


page = st.session_state.page


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    html("""
    <div class="hero">

        <h1>
            Logistics AI, Data Analytics & Business Intelligence
        </h1>

        <p>
            <strong>LogiIntelli</strong> is a Logistics AI,
            Data Analytics, and Business Intelligence platform focused
            on helping courier, logistics, supply chain, and e-commerce
            businesses transform operational data into actionable intelligence.
        </p>

        <p>
            We build AI-powered logistics analytics, Power BI dashboards,
            SQL data engineering solutions, machine learning models,
            predictive analytics, automated MIS systems, API integrations,
            and real-time operational intelligence platforms.
        </p>

        <p>
            Our expertise includes shipment tracking analytics,
            delivery performance, TAT and ageing analysis,
            hub performance, route analytics,
            shipment delay prediction, demand forecasting,
            ERP automation, and AI-powered supply chain intelligence.
        </p>

    </div>
    """)


    # ========================================================
    # METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("10+", "Years Experience"),
        ("50+", "Analytics & AI Pipelines"),
        ("24/7", "Automated Systems"),
        ("BI + AI", "Technology Architecture"),
    ]

    for col, (value, label) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            html(f"""
            <div class="metric-card">

                <div class="metric-value">
                    {value}
                </div>

                <div class="metric-label">
                    {label}
                </div>

            </div>
            """)


    # ========================================================
    # WHAT WE BUILD
    # ========================================================

    html("""
    <div class="section-title">
        What We Build
    </div>

    <div class="section-subtitle">
        Solutions engineered specifically around logistics operations,
        data analytics, automation, and predictive artificial intelligence.
    </div>
    """)


    services = [

        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending shipments, RTO, hub performance, state performance, and operational KPIs.",
        ),

        (
            "🚚",
            "TAT & Ageing Analytics",
            "Shipment ageing analysis, transit time monitoring, delivery SLA performance, bottleneck detection, and delayed shipment identification.",
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate daily operational reporting from ERPs, REST APIs, SQL databases, Python pipelines, and Excel reporting systems.",
        ),

        (
            "🏢",
            "Hub Performance Analytics",
            "Measure hub throughput, productivity, service levels, pending shipments, delivery performance, and operational efficiency.",
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect legacy ERP systems and modern REST APIs using Python, SQL, automation, and business intelligence platforms.",
        ),

        (
            "🤖",
            "Predictive AI & Machine Learning",
            "Machine learning solutions for shipment delay prediction, RTO risk scoring, demand forecasting, anomaly detection, and operational intelligence.",
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

                    <div class="service-icon">
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


    # ========================================================
    # DATA FLOW
    # ========================================================

    html("""
    <div class="section-title">
        Logistics Data Flow
    </div>

    <div class="section-subtitle">
        End-to-end shipment telemetry and operational intelligence
        from booking to AI-monitored delivery.
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
                <div class="workflow-name">Out for Delivery</div>
                <div class="workflow-desc">Last Mile</div>
            </div>

            <div class="workflow-arrow">→</div>

            <div class="workflow-step">
                <div class="workflow-icon">✅</div>
                <div class="workflow-name">Delivery</div>
                <div class="workflow-desc">Shipment Delivered</div>
            </div>

        </div>

    </div>
    """)


    # ========================================================
    # CTA
    # ========================================================

    html("""
    <div class="hero">

        <h2>
            Have a Logistics Data or AI Problem?
        </h2>

        <p>
            Share your business requirement and explore custom solutions
            for logistics analytics, Power BI dashboards,
            machine learning, SQL data engineering,
            automated MIS reporting, and AI-powered
            operational intelligence.
        </p>

    </div>
    """)


# ============================================================
# SERVICES PAGE
# ============================================================

elif page == "Services":

    html("""
    <div class="section-title">
        Logistics & AI Solutions
    </div>

    <div class="section-subtitle">
        Project-based analytics, business intelligence, automation,
        and machine learning solutions engineered around logistics operations.
    </div>
    """)


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
                "Booking vs delivery velocity",
                "Pending ageing control",
                "RTO minimization metrics",
                "First-attempt delivery rate",
                "Hub SLA rankings",
            ],
        ),

        (
            "🔄",
            "Inbound / Outbound Network Analytics",
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
                "Anomaly detection",
                "Custom machine learning models",
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

                    <div class="service-icon">
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
    <div class="section-title">
        Logistics & AI Projects
    </div>

    <div class="section-subtitle">
        Sample projects demonstrating capabilities in logistics analytics,
        business intelligence, automation, and machine learning.
    </div>
    """)


    projects = [

        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending shipments, RTO, ageing, hub performance, and business KPIs.",
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
            "Compare hubs based on booking, delivery, pending shipments, RTO, shipment weight, productivity, and operational SLAs.",
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
            "Machine learning model using XGBoost to identify shipments with high probabilities of delay before SLA breaches.",
            "Python • XGBoost • Machine Learning",
            "Predictive AI",
        ),

        (
            "06",
            "Automated Daily MIS Engine",
            "ERP and API automated data extraction, transformation, validation, and scheduled report distribution.",
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

                    <div style="
                        color:#0066CC;
                        font-size:13px;
                        font-weight:800;
                        margin-bottom:8px;
                    ">
                        PROJECT {number}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                    <p>
                        <strong>Technology:</strong><br>
                        {tech}
                    </p>

                    <p>
                        <strong>Category:</strong><br>
                        {category}
                    </p>

                </div>
                """)


# ============================================================
# REQUEST PROJECT
# ============================================================

elif page == "Request Project":

    html("""
    <div class="section-title">
        Request a Project
    </div>

    <div class="section-subtitle">
        Share your logistics analytics, business intelligence,
        machine learning, or automation project requirements.
    </div>
    """)


    GOOGLE_SHEET_WEB_APP_URL = st.secrets.get(
        "GOOGLE_SHEET_WEB_APP_URL",
        ""
    )


    if not GOOGLE_SHEET_WEB_APP_URL:

        st.info(
            "Project request system is currently being configured."
        )


    with st.form("project_request_form"):

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
            height=150,
            placeholder=(
                "Example: We need an automated daily courier "
                "performance dashboard and an AI model for "
                "predicting shipment delay risk."
            ),
        )


        submitted = st.form_submit_button(
            "Submit Project Request"
        )


        if submitted:

            if not contact_name.strip():

                st.warning(
                    "Please enter the Contact Person name."
                )

            elif not email.strip():

                st.warning(
                    "Please enter your Email address."
                )

            elif not requirement.strip():

                st.warning(
                    "Please describe your project requirement."
                )

            elif not GOOGLE_SHEET_WEB_APP_URL:

                st.error(
                    "Project request system is not configured yet."
                )

            else:

                payload = {

                    "Date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

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
                        headers={
                            "Content-Type":
                            "text/plain;charset=utf-8"
                        },
                        timeout=15,
                    )


                    if response.status_code == 200:

                        st.success(
                            "🎉 Thank you! Your project request "
                            "has been submitted successfully."
                        )

                    else:

                        st.error(
                            f"Submission failed. "
                            f"Status Code: {response.status_code}"
                        )


                except requests.exceptions.Timeout:

                    st.error(
                        "Request timed out. Please try again."
                    )


                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Unable to submit request: {e}"
                    )


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    html("""
    <div class="section-title">
        About LogiIntelli
    </div>

    <div class="card">

        <h2>
            AI & Data Intelligence for Logistics
        </h2>

        <p>
            <strong>LogiIntelli</strong> is an AI, Data Analytics,
            and Business Intelligence platform focused on
            logistics, courier, supply chain,
            and e-commerce industries.
        </p>

        <p>
            We transform complex operational data into
            actionable business intelligence using SQL,
            Python, Power BI, machine learning,
            APIs, and automated data pipelines.
        </p>

        <p>
            Our expertise includes logistics analytics,
            shipment tracking, delivery performance,
            TAT and ageing analysis, hub performance,
            route analytics, predictive AI,
            shipment delay prediction,
            demand forecasting, and MIS automation.
        </p>

        <p>
            LogiIntelli helps businesses improve operational
            visibility, reduce manual reporting,
            identify bottlenecks, monitor delivery SLAs,
            and make better data-driven decisions using
            modern analytics and artificial intelligence.
        </p>

    </div>
    """)


    html("""
    <div class="card">

        <h3>
            Our Technology Stack
        </h3>

        <p>
            🐍 Python &nbsp; • &nbsp;
            🗄️ SQL & Data Engineering &nbsp; • &nbsp;
            📊 Power BI & DAX &nbsp; • &nbsp;
            🤖 Machine Learning & AI &nbsp; • &nbsp;
            🔗 REST APIs & Automation
        </p>

    </div>
    """)


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    html("""
    <div class="section-title">
        Contact LogiIntelli
    </div>

    <div class="section-subtitle">
        Let's discuss your logistics analytics,
        AI, automation, or business intelligence requirements.
    </div>
    """)


    c1, c2 = st.columns(2)


    with c1:

        html("""
        <div class="card">

            <h3>
                📧 Email
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="mailto:sumansekar1205@gmail.com"
                >
                    sumansekar1205@gmail.com
                </a>
            </p>

            <h3>
                📱 Phone / WhatsApp
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://wa.me/918825674102"
                    target="_blank"
                >
                    +91 8825674102
                </a>
            </p>

        </div>
        """)


    with c2:

        html("""
        <div class="card">

            <h3>
                💼 LinkedIn
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://linkedin.com/in/sumansekar12/"
                    target="_blank"
                >
                    linkedin.com/in/sumansekar12/
                </a>
            </p>

            <h3>
                💻 GitHub
            </h3>

            <p>
                <a
                    class="contact-link"
                    href="https://github.com/Suman-SekarSagadev"
                    target="_blank"
                >
                    github.com/Suman-SekarSagadev
                </a>
            </p>

        </div>
        """)


# ============================================================
# FOOTER
# ============================================================

html("""
<hr style="
    border:0;
    border-top:1px solid #E2E8F0;
    margin-top:50px;
">

<div class="footer">

    <div class="footer-title">
        🚚 LogiIntelli
    </div>

    <div>
        Logistics AI • Data Analytics • Business Intelligence
    </div>

    <br>

    <div>
        Power BI Dashboards • Machine Learning • SQL Data Engineering
        • Shipment Analytics • Supply Chain Intelligence • MIS Automation
    </div>

    <br>

    <div>
        © 2026 LogiIntelli. All Rights Reserved.
    </div>

</div>
""")
