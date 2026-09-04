import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Suman Analytics | Logistics Analytics & Automation",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==============================
   MAIN APP
   ============================== */

.stApp {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* ==============================
   HEADER
   ============================== */

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
    color: #111827;
}

.sub-title {
    font-size: 18px;
    color: #6b7280;
    margin-top: 5px;
}

/* ==============================
   HERO
   ============================== */

.hero {
    padding: 45px 35px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #111827 0%,
        #1f2937 55%,
        #374151 100%
    );
    color: white;
    margin-top: 20px;
    margin-bottom: 35px;
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
    color: #d1d5db;
    line-height: 1.7;
}

/* ==============================
   SECTION
   ============================== */

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    margin-top: 35px;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 25px;
}

/* ==============================
   CARDS
   ============================== */

.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    min-height: 190px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

.card h3 {
    color: #111827;
    margin-bottom: 10px;
}

.card p {
    color: #6b7280;
    line-height: 1.6;
}

.card li {
    color: #4b5563;
    margin-bottom: 7px;
}

/* ==============================
   PROJECT CARDS
   ============================== */

.project-card {
    background: white;
    border-radius: 16px;
    padding: 25px;
    border: 1px solid #e5e7eb;
    min-height: 280px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.04);
}

.project-card h3 {
    color: #111827;
}

.project-card p {
    color: #6b7280;
    line-height: 1.6;
}

/* ==============================
   METRIC CARDS
   ============================== */

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    text-align: center;
    margin-bottom: 15px;
}

.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
}

.metric-label {
    color: #6b7280;
    font-size: 14px;
}

/* ==============================
   LOGISTICS DATA FLOW
   ============================== */

.workflow {
    background: white;
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
    color: #111827;
}

.workflow-desc {
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
}

.workflow-arrow {
    font-size: 25px;
    font-weight: bold;
    color: #9ca3af;
    padding: 0 5px;
}

/* ==============================
   FOOTER
   ============================== */

.footer {
    margin-top: 60px;
    padding: 30px;
    background: #111827;
    color: white;
    border-radius: 18px;
    text-align: center;
}

.footer p {
    color: #d1d5db;
}

/* ==============================
   SIDEBAR
   ============================== */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}

</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# SYNTHETIC LOGISTICS DATA
# ============================================================

@st.cache_data
def create_logistics_data():

    np.random.seed(42)

    routes = [
        ("Chennai", "Bangalore"),
        ("Chennai", "Hyderabad"),
        ("Chennai", "Coimbatore"),
        ("Chennai", "Madurai"),
        ("Bangalore", "Chennai"),
        ("Bangalore", "Hyderabad"),
        ("Hyderabad", "Chennai"),
        ("Mumbai", "Pune"),
        ("Pune", "Mumbai"),
        ("Delhi", "Mumbai"),
        ("Kochi", "Chennai"),
        ("Coimbatore", "Chennai")
    ]

    n = 3000

    booking_dates = pd.date_range(
        start="2026-07-01",
        end="2026-08-31",
        periods=n
    )

    route_data = np.random.choice(
        len(routes),
        n
    )

    origin = [
        routes[i][0]
        for i in route_data
    ]

    destination = [
        routes[i][1]
        for i in route_data
    ]

    shipment_status = np.random.choice(
        [
            "Delivered",
            "In Transit",
            "Pending",
            "RTO"
        ],
        n,
        p=[
            0.72,
            0.12,
            0.11,
            0.05
        ]
    )

    weight = np.round(
        np.random.exponential(
            2.5,
            n
        ) + 0.5,
        2
    )

    tat = np.random.randint(
        1,
        8,
        n
    )

    ageing = np.where(
        shipment_status == "Delivered",
        0,
        np.random.randint(
            1,
            12,
            n
        )
    )

    data = pd.DataFrame(
        {
            "AWB": [
                f"AWB{100000 + i}"
                for i in range(n)
            ],
            "Booking_Date": booking_dates,
            "Origin_Hub": origin,
            "Destination_Hub": destination,
            "Status": shipment_status,
            "Weight_KG": weight,
            "TAT_Days": tat,
            "Ageing_Days": ageing
        }
    )

    data["Month"] = (
        data["Booking_Date"]
        .dt.strftime("%b")
    )

    data["Week"] = (
        data["Booking_Date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    return data


df = create_logistics_data()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
<div style="text-align:center;">

<h1>🚚</h1>

<h2>SUMAN ANALYTICS</h2>

<p>
Logistics Analytics & Automation
</p>

</div>
""",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Services",
        "Projects",
        "Live Dashboard",
        "TAT & Ageing",
        "Hub Analytics",
        "Route Analytics",
        "Request Project",
        "About",
        "Contact"
    ]
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

<div class="main-title">
SUMAN ANALYTICS
</div>

<div class="sub-title">
Logistics Analytics • Automation • BI • AI
</div>

</div>
""",
    unsafe_allow_html=True
)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
<div class="hero">

<h1>
Logistics Analytics & Automation Solutions
</h1>

<p>
I build practical data analytics, business intelligence,
automation and predictive solutions for logistics and
courier businesses.
</p>

<p>
From ERP/API data extraction to SQL processing,
Power BI dashboards, automated MIS and predictive analytics —
I convert operational data into business decisions.
</p>

</div>
""",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            """
<div class="metric-card">

<div class="metric-value">
10+
</div>

<div class="metric-label">
Years Experience
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
<div class="metric-card">

<div class="metric-value">
50+
</div>

<div class="metric-label">
Analytics Solutions
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
<div class="metric-card">

<div class="metric-value">
24/7
</div>

<div class="metric-label">
Automation
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            """
<div class="metric-card">

<div class="metric-value">
BI + AI
</div>

<div class="metric-label">
Technology
</div>

</div>
""",
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # WHAT I BUILD
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">What I Build</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Solutions designed specifically around logistics operations.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    services = [

        (
            "📊",
            "Logistics BI",
            "Power BI dashboards for booking, delivery, pending, RTO, hub and state performance."
        ),

        (
            "🚚",
            "TAT & Ageing",
            "Shipment ageing, transit time, delivery TAT and operational bottleneck analysis."
        ),

        (
            "⚙️",
            "MIS Automation",
            "Automate daily MIS from ERP, APIs, SQL databases and Excel sources."
        ),

        (
            "🏢",
            "Hub Analytics",
            "Measure hub productivity, service levels, ageing, delivery and operational performance."
        ),

        (
            "🔗",
            "API & ERP Integration",
            "Connect ERP and REST APIs with Python, SQL and BI reporting systems."
        ),

        (
            "🤖",
            "Predictive Analytics",
            "Shipment delay prediction, risk scoring and operational forecasting."
        )
    ]

    for i, service in enumerate(services):

        target_col = [
            col1,
            col2,
            col3
        ][i % 3]

        with target_col:

            st.markdown(
                f"""
<div class="card">

<div style="font-size:35px;">
{service[0]}
</div>

<h3>
{service[1]}
</h3>

<p>
{service[2]}
</p>

</div>
""",
                unsafe_allow_html=True
            )

    # ========================================================
    # LOGISTICS DATA FLOW
    # ========================================================

    st.markdown(
        '<div class="section-title">Logistics Data Flow</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">End-to-end shipment movement from booking to delivery.</div>',
        unsafe_allow_html=True
    )

    # IMPORTANT:
    # Do NOT indent the HTML inside this string.
    # This prevents Streamlit from displaying it as code.

    st.markdown(
"""<div class="workflow">
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
</div>""",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CTA
    # --------------------------------------------------------

    st.markdown(
        """
<div class="hero">

<h2>
Have a Logistics Data Problem?
</h2>

<p>
Share your requirement and I can help design a practical
analytics, automation or reporting solution around your
business process.
</p>

</div>
""",
        unsafe_allow_html=True
    )

# ============================================================
# SERVICES
# ============================================================

elif page == "Services":

    st.markdown(
        '<div class="section-title">Logistics Solutions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Project-based analytics and automation solutions based on your business requirement.</div>',
        unsafe_allow_html=True
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
                "Daily / weekly / monthly trends"
            ]
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
                "SLA performance"
            ]
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
                "Hub ranking"
            ]
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
                "Route performance"
            ]
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
                "Email automation"
            ]
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
                "Machine learning models"
            ]
        )
    ]

    for i in range(
        0,
        len(service_details),
        3
    ):

        cols = st.columns(3)

        for j in range(3):

            if i + j < len(service_details):

                icon, title, items = service_details[i + j]

                with cols[j]:

                    item_html = "".join(
                        [
                            f"<li>{item}</li>"
                            for item in items
                        ]
                    )

                    st.markdown(
                        f"""
<div class="card">

<div style="font-size:35px;">
{icon}
</div>

<h3>
{title}
</h3>

<ul>
{item_html}
</ul>

</div>
""",
                        unsafe_allow_html=True
                    )

    st.markdown("---")

    st.markdown(
        """
### Typical Technology Stack

**Data Sources**

ERP • MySQL • SQL Server • Excel • CSV • REST APIs

**Processing**

Python • Pandas • SQL • Power Query

**Analytics**

Power BI • Python • Plotly

**Automation**

Python • Windows Scheduler • Airflow • APIs

**Deployment**

Streamlit • FastAPI • Docker
"""
    )

# ============================================================
# PROJECTS
# ============================================================

elif page == "Projects":

    st.markdown(
        '<div class="section-title">Logistics Projects</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Sample project ideas demonstrating practical logistics analytics capabilities.</div>',
        unsafe_allow_html=True
    )

    projects = [

        (
            "01",
            "Courier Operations Dashboard",
            "Complete operational dashboard covering booking, delivery, pending, RTO, ageing and hub performance.",
            "Power BI • SQL • DAX",
            "Operations Analytics"
        ),

        (
            "02",
            "Shipment TAT & Ageing",
            "Identify delayed shipments, ageing buckets, route-level delays and SLA performance.",
            "SQL • Python • Power BI",
            "TAT Analytics"
        ),

        (
            "03",
            "Hub Performance Analytics",
            "Compare hubs based on booking, delivery, pending, RTO, weight and service performance.",
            "SQL • Power BI • DAX",
            "Hub Analytics"
        ),

        (
            "04",
            "Inbound / Outbound Analytics",
            "Analyze shipment movement from origin state and hub to destination hub.",
            "SQL • Python • Power BI",
            "Network Analytics"
        ),

        (
            "05",
            "Shipment Delay Prediction",
            "Machine learning model to identify shipments that have a high probability of delayed delivery.",
            "Python • XGBoost • ML",
            "Predictive Analytics"
        ),

        (
            "06",
            "Automated Daily MIS",
            "ERP/API data extraction, transformation, validation and automated report distribution.",
            "Python • SQL • API",
            "Automation"
        )
    ]

    for i in range(
        0,
        len(projects),
        2
    ):

        cols = st.columns(2)

        for j in range(2):

            if i + j < len(projects):

                number, title, description, tech, category = projects[i + j]

                with cols[j]:

                    st.markdown(
                        f"""
<div class="project-card">

<div style="font-size:14px;color:#6b7280;">
PROJECT {number}
</div>

<h3>
{title}
</h3>

<p>
{description}
</p>

<b>
Technology:
</b>

<p>
{tech}
</p>

<b>
Category:
</b>

<p>
{category}
</p>

</div>
""",
                        unsafe_allow_html=True
                    )

# ============================================================
# LIVE DASHBOARD
# ============================================================

elif page == "Live Dashboard":

    st.markdown(
        '<div class="section-title">Live Logistics Dashboard Demo</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-subtitle">
This dashboard uses synthetic sample data for demonstration.
No company/customer data is used.
</div>
""",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_origin = st.multiselect(
            "Origin Hub",
            sorted(
                df["Origin_Hub"].unique()
            ),
            default=sorted(
                df["Origin_Hub"].unique()
            )
        )

    with col2:

        selected_status = st.multiselect(
            "Shipment Status",
            sorted(
                df["Status"].unique()
            ),
            default=sorted(
                df["Status"].unique()
            )
        )

    with col3:

        selected_destination = st.multiselect(
            "Destination Hub",
            sorted(
                df["Destination_Hub"].unique()
            ),
            default=sorted(
                df["Destination_Hub"].unique()
            )
        )

    filtered_df = df[
        df["Origin_Hub"].isin(
            selected_origin
        )
        &
        df["Status"].isin(
            selected_status
        )
        &
        df["Destination_Hub"].isin(
            selected_destination
        )
    ]

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    total_shipments = len(
        filtered_df
    )

    delivered = len(
        filtered_df[
            filtered_df["Status"] == "Delivered"
        ]
    )

    pending = len(
        filtered_df[
            filtered_df["Status"] == "Pending"
        ]
    )

    rto = len(
        filtered_df[
            filtered_df["Status"] == "RTO"
        ]
    )

    delivery_percentage = (
        delivered
        / total_shipments
        * 100
        if total_shipments > 0
        else 0
    )

    avg_tat = (
        filtered_df["TAT_Days"].mean()
        if total_shipments > 0
        else 0
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(
            "Total Shipments",
            f"{total_shipments:,}"
        )

    with c2:

        st.metric(
            "Delivered",
            f"{delivered:,}"
        )

    with c3:

        st.metric(
            "Delivery %",
            f"{delivery_percentage:.1f}%"
        )

    with c4:

        st.metric(
            "Pending",
            f"{pending:,}"
        )

    with c5:

        st.metric(
            "Avg TAT",
            f"{avg_tat:.1f} Days"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # STATUS + HUB
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        status_data = (
            filtered_df
            .groupby("Status")
            .size()
            .reset_index(
                name="Shipments"
            )
        )

        fig = px.pie(
            status_data,
            names="Status",
            values="Shipments",
            title="Shipment Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        hub_data = (
            filtered_df
            .groupby("Origin_Hub")
            .size()
            .reset_index(
                name="Shipments"
            )
            .sort_values(
                "Shipments",
                ascending=False
            )
        )

        fig = px.bar(
            hub_data,
            x="Origin_Hub",
            y="Shipments",
            title="Shipments by Origin Hub"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # DAILY TREND + ROUTES
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        trend = (
            filtered_df
            .groupby("Booking_Date")
            .size()
            .reset_index(
                name="Shipments"
            )
        )

        fig = px.line(
            trend,
            x="Booking_Date",
            y="Shipments",
            title="Daily Booking Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        route_data = (
            filtered_df
            .groupby(
                [
                    "Origin_Hub",
                    "Destination_Hub"
                ]
            )
            .size()
            .reset_index(
                name="Shipments"
            )
            .sort_values(
                "Shipments",
                ascending=False
            )
            .head(15)
        )

        route_data["Route"] = (
            route_data["Origin_Hub"]
            + " → "
            + route_data["Destination_Hub"]
        )

        fig = px.bar(
            route_data,
            x="Route",
            y="Shipments",
            title="Top Routes"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    st.markdown(
        "### Shipment Data"
    )

    st.dataframe(
        filtered_df.head(100),
        use_container_width=True
    )

# ============================================================
# TAT & AGEING
# ============================================================

elif page == "TAT & Ageing":

    st.markdown(
        '<div class="section-title">TAT & Ageing Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Identify delayed and ageing shipments.</div>',
        unsafe_allow_html=True
    )

    def ageing_bucket(days):

        if days == 0:
            return "Delivered"

        elif days <= 2:
            return "0-2 Days"

        elif days <= 5:
            return "3-5 Days"

        elif days <= 7:
            return "6-7 Days"

        else:
            return "8+ Days"

    ageing_df = df.copy()

    ageing_df["Ageing_Bucket"] = (
        ageing_df["Ageing_Days"]
        .apply(ageing_bucket)
    )

    bucket_data = (
        ageing_df
        .groupby("Ageing_Bucket")
        .size()
        .reset_index(
            name="Shipments"
        )
    )

    order = [
        "Delivered",
        "0-2 Days",
        "3-5 Days",
        "6-7 Days",
        "8+ Days"
    ]

    bucket_data["Ageing_Bucket"] = pd.Categorical(
        bucket_data["Ageing_Bucket"],
        categories=order,
        ordered=True
    )

    bucket_data = bucket_data.sort_values(
        "Ageing_Bucket"
    )

    fig = px.bar(
        bucket_data,
        x="Ageing_Bucket",
        y="Shipments",
        title="Shipment Ageing Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TAT DISTRIBUTION
    # --------------------------------------------------------

    tat_data = (
        df
        .groupby("TAT_Days")
        .size()
        .reset_index(
            name="Shipments"
        )
    )

    fig = px.bar(
        tat_data,
        x="TAT_Days",
        y="Shipments",
        title="TAT Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # DELAYED SHIPMENTS
    # --------------------------------------------------------

    delayed = df[
        (
            df["Status"] != "Delivered"
        )
        &
        (
            df["Ageing_Days"] >= 5
        )
    ]

    st.markdown(
        "### High Ageing Shipments"
    )

    st.dataframe(
        delayed[
            [
                "AWB",
                "Booking_Date",
                "Origin_Hub",
                "Destination_Hub",
                "Status",
                "Ageing_Days",
                "TAT_Days"
            ]
        ]
        .sort_values(
            "Ageing_Days",
            ascending=False
        )
        .head(100),
        use_container_width=True
    )

# ============================================================
# HUB ANALYTICS
# ============================================================

elif page == "Hub Analytics":

    st.markdown(
        '<div class="section-title">Hub Performance Analytics</div>',
        unsafe_allow_html=True
    )

    hub_summary = (
        df
        .groupby("Origin_Hub")
        .agg(
            Total_Shipments=(
                "AWB",
                "count"
            ),
            Delivered=(
                "Status",
                lambda x: (
                    x == "Delivered"
                ).sum()
            ),
            Pending=(
                "Status",
                lambda x: (
                    x == "Pending"
                ).sum()
            ),
            RTO=(
                "Status",
                lambda x: (
                    x == "RTO"
                ).sum()
            ),
            Avg_TAT=(
                "TAT_Days",
                "mean"
            ),
            Avg_Ageing=(
                "Ageing_Days",
                "mean"
            )
        )
        .reset_index()
    )

    hub_summary["Delivery_%"] = (
        hub_summary["Delivered"]
        /
        hub_summary["Total_Shipments"]
        * 100
    )

    hub_summary["RTO_%"] = (
        hub_summary["RTO"]
        /
        hub_summary["Total_Shipments"]
        * 100
    )

    hub_summary = hub_summary.round(2)

    st.dataframe(
        hub_summary.sort_values(
            "Delivery_%",
            ascending=False
        ),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            hub_summary.sort_values(
                "Delivery_%",
                ascending=False
            ),
            x="Origin_Hub",
            y="Delivery_%",
            title="Hub Delivery Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            hub_summary.sort_values(
                "Avg_TAT",
                ascending=False
            ),
            x="Origin_Hub",
            y="Avg_TAT",
            title="Average TAT by Hub"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# ROUTE ANALYTICS
# ============================================================

elif page == "Route Analytics":

    st.markdown(
        '<div class="section-title">Route Performance Analytics</div>',
        unsafe_allow_html=True
    )

    route_summary = (
        df
        .groupby(
            [
                "Origin_Hub",
                "Destination_Hub"
            ]
        )
        .agg(
            Shipments=(
                "AWB",
                "count"
            ),
            Avg_TAT=(
                "TAT_Days",
                "mean"
            ),
            Avg_Ageing=(
                "Ageing_Days",
                "mean"
            ),
            Delivered=(
                "Status",
                lambda x: (
                    x == "Delivered"
                ).sum()
            )
        )
        .reset_index()
    )

    route_summary["Delivery_%"] = (
        route_summary["Delivered"]
        /
        route_summary["Shipments"]
        * 100
    )

    route_summary["Route"] = (
        route_summary["Origin_Hub"]
        + " → "
        + route_summary["Destination_Hub"]
    )

    route_summary = route_summary.round(2)

    st.dataframe(
        route_summary.sort_values(
            "Shipments",
            ascending=False
        ),
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        top_routes = (
            route_summary
            .sort_values(
                "Shipments",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            top_routes,
            x="Route",
            y="Shipments",
            title="Top Routes by Shipment Volume"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        worst_routes = (
            route_summary
            .sort_values(
                "Avg_TAT",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            worst_routes,
            x="Route",
            y="Avg_TAT",
            title="Routes with Highest Average TAT"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ============================================================
# REQUEST PROJECT
# ============================================================

elif page == "Request Project":

    st.markdown(
        '<div class="section-title">Request a Project</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="section-subtitle">
Tell me about your logistics analytics or automation requirement.
</div>
""",
        unsafe_allow_html=True
    )

    with st.form(
        "project_request_form"
    ):

        col1, col2 = st.columns(2)

        with col1:

            company_name = st.text_input(
                "Company Name"
            )

            contact_name = st.text_input(
                "Contact Person"
            )

            email = st.text_input(
                "Email"
            )

            phone = st.text_input(
                "Phone"
            )

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
                    "Other"
                ]
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
                    "Other"
                ]
            )

            timeline = st.selectbox(
                "Expected Timeline",
                [
                    "Less than 1 week",
                    "1-2 weeks",
                    "2-4 weeks",
                    "1-2 months",
                    "Not decided"
                ]
            )

        requirement = st.text_area(
            "Describe Your Requirement",
            height=150,
            placeholder=(
                "Example: We need a daily courier performance "
                "dashboard showing booking, delivery, pending, "
                "RTO and hub-wise performance."
            )
        )

        submitted = st.form_submit_button(
            "Submit Project Request"
        )

        if submitted:

            if (
                not contact_name
                or not email
                or not requirement
            ):

                st.warning(
                    "Please provide Contact Person, Email and Requirement."
                )

            else:

                request_data = pd.DataFrame(
                    [
                        {
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
                            "Requirement": requirement
                        }
                    ]
                )

                request_data.to_csv(
                    "project_requests.csv",
                    mode="a",
                    header=False,
                    index=False
                )

                st.success(
                    "Thank you! Your project requirement has been submitted."
                )

                st.info(
                    "For production use, this form can be connected "
                    "to MySQL, Google Sheets, email or a CRM."
                )

# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    st.markdown(
        '<div class="section-title">About Suman Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
### Data Analytics for Logistics Businesses

I specialize in building practical analytics and automation
solutions for logistics, courier and supply-chain operations.

My approach is simple:

**Understand the business process → Connect the data →
Transform the data → Build analytics → Automate the process.**

### Areas of Expertise

- Logistics Operations Analytics
- Courier Performance Analytics
- Power BI Dashboard Development
- SQL Data Analysis
- Python Automation
- REST API Integration
- ERP Data Integration
- TAT & Ageing Analytics
- Hub Performance
- Route Analytics
- Automated MIS
- Predictive Analytics
- Machine Learning

### Technology

**SQL / Database**

MySQL • SQL Server • Teradata • Snowflake

**Analytics**

Power BI • DAX • Power Query • Excel • Python

**Python**

Pandas • NumPy • Requests • Scikit-learn • XGBoost

**Automation**

Python • APIs • Windows Scheduler • Airflow

**Deployment**

Streamlit • FastAPI • Docker

### Business Objective

The objective is not just to create dashboards.

The objective is to help logistics businesses:

- Reduce manual reporting
- Identify operational problems
- Improve delivery performance
- Reduce shipment ageing
- Monitor hub performance
- Improve decision making
- Automate repetitive processes
"""
    )

# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    st.markdown(
        '<div class="section-title">Contact</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Let us discuss your logistics analytics requirement.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
### 📧 Email

**Sumansekar1205@gmail.com**

### 📱 Phone

**+91 8825674102**

### 💼 LinkedIn

[linkedin.com/in/sumansekar12/](https://www.linkedin.com/in/sumansekar12/)

### 💻 GitHub

[github.com/Suman-SekarSagadev](https://github.com/Suman-SekarSagadev)
"""
        )

    with col2:

        st.markdown(
            """
### Services

🚚 Logistics Analytics

📊 Power BI Dashboards

🗄️ SQL Analytics

⚙️ Python Automation

🔗 API / ERP Integration

⏱️ TAT & Ageing

🏢 Hub Analytics

🤖 Predictive Analytics

### Let's Build Something Useful

If your business has data in ERP, Excel, SQL or APIs,
we can convert that data into useful analytics and
automated reporting solutions.
"""
        )

    st.markdown(
        """
<div class="footer">

<h2>
SUMAN ANALYTICS
</h2>

<p>
Logistics Analytics • Business Intelligence • Automation • AI
</p>

<p>
© 2026 Suman Analytics. All Rights Reserved.
</p>

</div>
""",
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER FOR OTHER PAGES
# ============================================================

if page != "Contact":

    st.markdown(
        """
<div class="footer">

<h2>
SUMAN ANALYTICS
</h2>

<p>
Logistics Analytics • BI • Automation • AI
</p>

<p>
📧 Sumansekar1205@gmail.com
&nbsp;&nbsp; | &nbsp;&nbsp;
📱 +91 8825674102
</p>

<p>
© 2026 Suman Analytics
</p>

</div>
""",
        unsafe_allow_html=True
    )