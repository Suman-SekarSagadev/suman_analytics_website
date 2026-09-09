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
            "text": "👋 Hi! Welcome to LogiIntelli.\nWhat is your name?",
        }
    ]


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
   GLOBAL
============================================================ */

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #F8FAFC 0%,
            #FFFFFF 45%,
            #F8FAFC 100%
        );
}

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 6rem !important;
    max-width: 1400px !important;
}


/* ============================================================
   HEADER
============================================================ */

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 18px 0;
    border-bottom: 1px solid #E2E8F0;
    margin-bottom: 20px;
}

.brand-wrapper {
    display: flex;
    flex-direction: column;
}

.brand-title {
    font-size: 38px;
    font-weight: 850;
    letter-spacing: -1.5px;
    line-height: 1.1;
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


/* ============================================================
   NAVIGATION
============================================================ */

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


/* ============================================================
   HERO
============================================================ */

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


/* ============================================================
   SECTION & CARDS
============================================================ */

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


/* ============================================================
   METRICS
============================================================ */

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


/* ============================================================
   PROJECT
============================================================ */

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


/* ============================================================
   CTA & FORM
============================================================ */

.cta {
    background: linear-gradient(135deg, #0F172A, #1E3A8A);
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

.form-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 8px 25px rgba(15,23,42,0.05);
}


/* ============================================================
   SMALL FLOATING CHATBOT - BOTTOM LEFT
============================================================ */

.st-key-floating_chatbot {
    position: fixed !important;
    left: 20px !important;
    bottom: 20px !important;
    width: 290px !important;
    max-width: calc(100vw - 40px) !important;
    z-index: 999999 !important;
    background: white !important;
    border: 1px solid #D9E2EC !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(15,23,42,0.18), 0 3px 10px rgba(15,23,42,0.08) !important;
    overflow: hidden !important;
}


/* ============================================================
   CHAT HEADER & CLOSE BUTTON FIX
============================================================ */

.chat-header-bar {
    background: linear-gradient(135deg, #0F172A, #2563EB);
    color: white;
    padding: 10px 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-header-title {
    font-size: 13px;
    font-weight: 700;
    line-height: 1.2;
}

.chat-header-subtitle {
    font-size: 9px;
    color: #CBD5E1;
    margin-top: 2px;
}

.st-key-chat_close_btn button {
    min-height: 24px !important;
    height: 24px !important;
    width: 24px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background: rgba(255, 255, 255, 0.25) !important;
    color: white !important;
    border: none !important;
    font-size: 12px !important;
    cursor: pointer !important;
}

.st-key-chat_close_btn button:hover {
    background: rgba(255, 255, 255, 0.45) !important;
}


/* ============================================================
   CHAT BODY & INPUTS
============================================================ */

.chat-body {
    padding: 10px;
    max-height: 240px;
    overflow-y: auto;
}

.chat-message {
    padding: 7px 9px;
    border-radius: 9px;
    margin: 5px 0;
    font-size: 11px;
    line-height: 1.4;
    white-space: pre-wrap;
}

.chat-assistant {
    background: #EFF6FF;
    color: #1E3A8A;
    border: 1px solid #DBEAFE;
}

.chat-user {
    background: #0F172A;
    color: white;
    margin-left: 15px;
}

.st-key-floating_chatbot input,
.st-key-floating_chatbot textarea {
    font-size: 11px !important;
}

.st-key-floating_chatbot button {
    min-height: 28px !important;
    padding: 4px 8px !important;
    font-size: 10px !important;
    border-radius: 7px !important;
}


/* ============================================================
   REOPEN CHAT BUTTON
============================================================ */

.st-key-open_chat_container {
    position: fixed !important;
    left: 20px !important;
    bottom: 20px !important;
    z-index: 999999 !important;
}

.st-key-open_chat_container button {
    width: 54px !important;
    height: 54px !important;
    min-height: 54px !important;
    padding: 0 !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #0F172A, #2563EB) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 8px 25px rgba(15,23,42,0.25) !important;
    font-size: 22px !important;
}

.st-key-open_chat_container button:hover {
    transform: scale(1.05);
}


/* ============================================================
   MOBILE RESPONSIVENESS
============================================================ */

@media (max-width: 600px) {
    .brand-title {
        font-size: 30px;
    }

    .hero-title {
        font-size: 38px;
    }

    .hero-text {
        font-size: 14px;
    }

    .st-key-floating_chatbot {
        left: 10px !important;
        bottom: 10px !important;
        width: 260px !important;
    }

    .st-key-open_chat_container {
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
<div class="top-header">
    <div class="brand-wrapper">
        <div class="brand-title">
            🚚 <span class="logi-text">Logi</span><span class="intelli-text">Intelli</span>
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
<div class="section-title">What We Do</div>
<div class="section-subtitle">
    End-to-end analytics and technology solutions designed
    for operational and business growth.
</div>
"""
    )

    services = [
        ("📊", "Power BI & Business Intelligence", "Interactive dashboards, KPI monitoring, DAX, Power Query and executive reporting."),
        ("🚚", "Logistics Analytics", "Shipment analytics, hub performance, SLA, TAT, delivery and operational intelligence."),
        ("🤖", "AI & Machine Learning", "Forecasting, prediction, classification, churn models and intelligent decision systems."),
        ("⚙️", "Automation & MIS", "Automate repetitive reports, data pipelines, Excel workflows and operational MIS."),
        ("🗄️", "SQL & Data Engineering", "Advanced SQL, data transformation, ETL pipelines and scalable reporting datasets."),
        ("🔗", "API & Data Integration", "Connect APIs, databases, JSON feeds and multiple data sources into one analytics ecosystem."),
    ]

    service_cols = st.columns(3)
    for i, (icon, title, text) in enumerate(services):
        with service_cols[i % 3]:
            html(
                f"""
<div class="card">
    <div class="card-icon">{icon}</div>
    <div class="card-title">{title}</div>
    <div class="card-text">{text}</div>
</div>
"""
            )
        if (i + 1) % 3 == 0:
            st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Your Project", use_container_width=True, key="home_start_project"):
        st.session_state.page = "Request Project"
        st.rerun()


# ============================================================
# SERVICES PAGE
# ============================================================

def services_page():
    html(
        """
<div class="hero">
    <div class="hero-badge">OUR SERVICES</div>
    <div class="hero-title">Analytics & Technology <span>Solutions</span></div>
    <div class="hero-text">From business intelligence to machine learning, we build solutions around your business requirements.</div>
</div>
"""
    )


# ============================================================
# PROJECTS PAGE
# ============================================================

def projects_page():
    html(
        """
<div class="hero">
    <div class="hero-badge">PROJECTS & SOLUTIONS</div>
    <div class="hero-title">Real Business Problems. <span>Data-Driven Solutions.</span></div>
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
    <div class="hero-badge">START A PROJECT</div>
    <div class="hero-title">Tell Us About Your <span>Requirement</span></div>
</div>
"""
    )

    html('<div class="form-card">')
    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company Name", placeholder="Your company name", key="company_form")
        contact = st.text_input("Contact Person *", placeholder="Your name", key="contact_form")
        email = st.text_input("Business Email *", placeholder="name@company.com", key="email_form")
        phone = st.text_input("Phone / WhatsApp", placeholder="+91 XXXXX XXXXX", key="phone_form")

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
        placeholder="Please describe your business problem, current process and expected solution...",
        height=150,
        key="requirement_form",
    )

    html("</div>")

    if st.button("🚀 Submit Project Request", use_container_width=True, key="submit_project_request"):
        if not contact.strip():
            st.error("Please enter your contact name.")
        elif not email.strip():
            st.error("Please enter your business email.")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()):
            st.error("Please enter a valid email address.")
        elif not requirement.strip():
            st.error("Please describe your requirement.")
        else:
            payload = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                    headers={"Content-Type": "text/plain;charset=utf-8"},
                    timeout=20,
                    allow_redirects=True,
                )

                if response.status_code == 200:
                    st.success("✅ Thank you! Your project request has been submitted successfully.")
                else:
                    st.error("Unable to submit your request. Please try again.")

            except Exception:
                st.error("Connection error. Please try again later.")


# ============================================================
# ABOUT & CONTACT PAGE
# ============================================================

def about_page():
    html("<div class='hero'><div class='hero-title'>About Us</div></div>")

def contact_page():
    html("<div class='hero'><div class='hero-title'>Contact Us</div></div>")


# ============================================================
# ROUTER
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
# FLOATING CHATBOT ENGINE (STEP-BY-STEP LEAD CAPTURE)
# ============================================================

if st.session_state.chat_open:
    with st.container(key="floating_chatbot"):
        
        # Header Row with Integrated Visible Close Button
        c_hdr, c_close = st.columns([0.82, 0.18])
        with c_hdr:
            st.markdown(
                """
                <div class="chat-header-bar">
                    <div>
                        <div class="chat-header-title">🤖 LogiIntelli Assistant</div>
                        <div class="chat-header-subtitle">Project & Analytics Consultation</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c_close:
            with st.container(key="chat_close_btn"):
                if st.button("✕", key="btn_close_chat", help="Close Chat"):
                    st.session_state.chat_open = False
                    st.rerun()

        # Chat Message Log
        st.markdown('<div class="chat-body">', unsafe_allow_html=True)
        for msg in st.session_state.chat_messages:
            role_class = "chat-assistant" if msg["role"] == "assistant" else "chat-user"
            st.markdown(
                f'<div class="chat-message {role_class}">{msg["text"]}</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        # Step 0: Ask Name
        if st.session_state.chat_step == 0:
            with st.form(key="chat_step_0", clear_on_submit=True):
                user_name = st.text_input("Your Name", placeholder="Type your name...", key="input_chat_name")
                if st.form_submit_button("Next ➔", use_container_width=True):
                    if user_name.strip():
                        st.session_state.chat_data["Contact"] = user_name.strip()
                        st.session_state.chat_messages.append({"role": "user", "text": user_name.strip()})
                        st.session_state.chat_messages.append(
                            {"role": "assistant", "text": f"Nice to meet you, {user_name.strip()}! What solution are you looking for?"}
                        )
                        st.session_state.chat_step = 1
                        st.rerun()

        # Step 1: Select Service
        elif st.session_state.chat_step == 1:
            services_options = [
                "Power BI Dashboard",
                "Logistics Analytics",
                "AI / Machine Learning",
                "Automation / MIS",
                "SQL / Data Engineering",
                "Not Sure",
            ]
            for s_opt in services_options:
                if st.button(s_opt, key=f"chat_s_{s_opt}", use_container_width=True):
                    st.session_state.chat_data["Service"] = s_opt
                    st.session_state.chat_messages.append({"role": "user", "text": s_opt})
                    st.session_state.chat_messages.append({"role": "assistant", "text": "Got it! What is your business email address?"})
                    st.session_state.chat_step = 2
                    st.rerun()

        # Step 2: Business Email
        elif st.session_state.chat_step == 2:
            with st.form(key="chat_step_2", clear_on_submit=True):
                user_email = st.text_input("Business Email", placeholder="name@company.com", key="input_chat_email")
                if st.form_submit_button("Next ➔", use_container_width=True):
                    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", user_email.strip()):
                        st.session_state.chat_data["Email"] = user_email.strip()
                        st.session_state.chat_messages.append({"role": "user", "text": user_email.strip()})
                        st.session_state.chat_messages.append({"role": "assistant", "text": "Thanks! What is your Phone / WhatsApp number?"})
                        st.session_state.chat_step = 3
                        st.rerun()
                    else:
                        st.error("Please enter a valid email.")

        # Step 3: Phone Number
        elif st.session_state.chat_step == 3:
            with st.form(key="chat_step_3", clear_on_submit=True):
                user_phone = st.text_input("Phone Number", placeholder="+91 XXXXX XXXXX", key="input_chat_phone")
                if st.form_submit_button("Next ➔", use_container_width=True):
                    if user_phone.strip():
                        st.session_state.chat_data["Phone"] = user_phone.strip()
                        st.session_state.chat_messages.append({"role": "user", "text": user_phone.strip()})
                        st.session_state.chat_messages.append(
                            {"role": "assistant", "text": "Great! Please brief us on your requirement or current process."}
                        )
                        st.session_state.chat_step = 4
                        st.rerun()

        # Step 4: Requirement Details & Submit
        elif st.session_state.chat_step == 4:
            with st.form(key="chat_step_4", clear_on_submit=True):
                user_req = st.text_area("Requirement Details", placeholder="Type requirement details here...", key="input_chat_req")
                if st.form_submit_button("Submit Request 🚀", use_container_width=True):
                    if user_req.strip():
                        st.session_state.chat_data["Requirement"] = user_req.strip()
                        st.session_state.chat_messages.append({"role": "user", "text": user_req.strip()})

                        # Submit payload to Google Script
                        payload = {
                            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Company": st.session_state.chat_data.get("Contact", ""),
                            "Contact": st.session_state.chat_data.get("Contact", ""),
                            "Email": st.session_state.chat_data.get("Email", ""),
                            "Phone": st.session_state.chat_data.get("Phone", ""),
                            "Service": st.session_state.chat_data.get("Service", ""),
                            "Data_Source": "Chatbot Input",
                            "Timeline": "Flexible",
                            "Requirement": st.session_state.chat_data.get("Requirement", ""),
                            "Source": "Chatbot Assistant",
                        }

                        try:
                            requests.post(
                                GOOGLE_SCRIPT_URL,
                                data=json.dumps(payload),
                                headers={"Content-Type": "text/plain;charset=utf-8"},
                                timeout=15,
                            )
                        except Exception:
                            pass

                        st.session_state.chat_messages.append(
                            {
                                "role": "assistant",
                                "text": "✅ Thank you! Your request has been recorded. Our team will get back to you shortly.",
                            }
                        )
                        st.session_state.chat_step = 5
                        st.rerun()

else:
    # Re-open Floating Action Button
    with st.container(key="open_chat_container"):
        if st.button("💬", key="btn_reopen_chat", help="Open Chat Assistant"):
            st.session_state.chat_open = True
            st.rerun()
