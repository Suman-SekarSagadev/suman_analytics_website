```python
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
# HELPERS
# ============================================================

def html(content):
    st.html(content)


def valid_email(email):
    return re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email.strip()
    )


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
# CHAT RESET
# ============================================================

def reset_chat_state():

    st.session_state.chat_step = 0

    st.session_state.chat_data = {}

    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "text": (
                "👋 Welcome to JYORA AI.<br>"
                "Let's understand your business requirement."
            ),
        }
    ]


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "chat_messages" not in st.session_state:
    reset_chat_state()


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
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: #FFFFFF;
    color: #0F172A;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 1380px !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.top-header {
    width: 100%;
    padding: 10px 0 20px 0;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 20px;
}

.header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-symbol {
    width: 46px;
    height: 46px;
    min-width: 46px;

    border-radius: 12px;

    background: linear-gradient(
        135deg,
        #0F172A,
        #2563EB
    );

    display: flex;
    align-items: center;
    justify-content: center;

    color: #FFFFFF !important;

    font-size: 22px;
    font-weight: 900;

    box-shadow:
        0 8px 22px rgba(37,99,235,0.20);
}

.brand-name {
    font-size: 32px !important;
    line-height: 1.2 !important;

    font-weight: 900 !important;

    letter-spacing: -1px;

    display: block !important;
    visibility: visible !important;

    opacity: 1 !important;
}

.jyora-text {
    color: #0F172A !important;
}

.ai-text {
    color: #2563EB !important;
}

.brand-description {
    font-size: 11px;

    color: #64748B !important;

    margin-top: 3px;

    letter-spacing: 0.5px;

    font-weight: 600;
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

    min-height: 38px !important;

    transition: all 0.2s ease !important;
}

div.stButton > button:hover {

    border-color: #2563EB !important;

    color: #2563EB !important;

    box-shadow:
        0 4px 14px rgba(37,99,235,0.10) !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-section {

    position: relative;

    border-radius: 24px;

    padding: 70px 40px;

    margin-bottom: 40px;

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(59,130,246,0.15),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #F8FAFC 0%,
            #EFF6FF 100%
        );

    border: 1px solid #DBEAFE;

    text-align: center;
}

.hero-badge {

    display: inline-block;

    padding: 6px 14px;

    border-radius: 30px;

    background: #FFFFFF;

    border: 1px solid #BFDBFE;

    color: #2563EB;

    font-size: 11px;

    font-weight: 750;

    margin-bottom: 18px;
}

.hero-title {

    font-size: 52px;

    line-height: 1.1;

    font-weight: 900;

    letter-spacing: -2px;

    color: #0F172A;
}

.hero-title span {
    color: #2563EB;
}

.hero-description {

    max-width: 720px;

    margin: 20px auto;

    color: #475569;

    font-size: 16px;

    line-height: 1.6;
}


/* ============================================================
   FEATURE CARDS
   ============================================================ */

.feature-card {

    padding: 24px;

    border-radius: 16px;

    background: #FFFFFF;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.03);

    height: 100%;
}

.feature-title {

    color: #0F172A;

    font-size: 16px;

    font-weight: 750;

    margin-bottom: 8px;
}

.feature-text {

    color: #64748B;

    font-size: 13px;

    line-height: 1.6;
}


/* ============================================================
   JYORA FLOATING CHATBOT
   ============================================================ */

/*
   IMPORTANT:
   Use a wrapper with fixed position.
   The Streamlit buttons remain functional while
   the visual container stays at bottom-left.
*/

.jyora-chat-wrapper {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    width: 310px !important;

    z-index: 2147483647 !important;

    pointer-events: none !important;
}


/* ============================================================
   CHAT OPEN BOX
   ============================================================ */

.jyora-chat-box {

    width: 310px !important;

    background: #FFFFFF !important;

    border: 1px solid #DCE3ED !important;

    border-radius: 16px !important;

    overflow: hidden !important;

    box-shadow:
        0 18px 45px rgba(15,23,42,0.22) !important;

    pointer-events: auto !important;
}


/* ============================================================
   CHAT HEADER
   ============================================================ */

.jyora-chat-header {

    background:
        linear-gradient(
            135deg,
            #0F172A 0%,
            #1D4ED8 100%
        ) !important;

    color: #FFFFFF !important;

    padding: 14px 16px !important;

    min-height: 58px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: space-between !important;
}

.jyora-chat-header-left {

    display: flex !important;

    align-items: center !important;

    gap: 10px !important;
}

.jyora-chat-avatar {

    width: 34px !important;

    height: 34px !important;

    min-width: 34px !important;

    border-radius: 10px !important;

    background: rgba(255,255,255,0.15) !important;

    border: 1px solid rgba(255,255,255,0.25) !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    font-size: 17px !important;
}


/*
   THIS IS THE IMPORTANT HEADING FIX
*/

.jyora-chat-title {

    color: #FFFFFF !important;

    font-size: 14px !important;

    line-height: 18px !important;

    font-weight: 800 !important;

    display: block !important;

    visibility: visible !important;

    opacity: 1 !important;

    white-space: nowrap !important;
}

.jyora-chat-subtitle {

    color: rgba(255,255,255,0.75) !important;

    font-size: 10px !important;

    line-height: 14px !important;

    font-weight: 500 !important;

    margin-top: 1px !important;
}


/* ============================================================
   CHAT BODY
   ============================================================ */

.jyora-chat-body {

    padding: 12px !important;

    max-height: 220px !important;

    overflow-y: auto !important;

    background: #FFFFFF !important;
}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

.jyora-message {

    padding: 8px 10px !important;

    border-radius: 9px !important;

    font-size: 11px !important;

    line-height: 1.45 !important;

    margin-bottom: 8px !important;

    word-wrap: break-word !important;
}

.jyora-message-assistant {

    background: #EFF6FF !important;

    color: #1E3A8A !important;

    border: 1px solid #DBEAFE !important;

    margin-right: 12px !important;
}

.jyora-message-user {

    background: #0F172A !important;

    color: #FFFFFF !important;

    margin-left: 25px !important;

    text-align: right !important;
}


/* ============================================================
   CHAT STREAMLIT CONTROLS
   ============================================================ */

.jyora-chat-controls {

    padding: 0 12px 12px 12px !important;

    background: #FFFFFF !important;
}


/*
   Make chatbot input small
*/

.jyora-chat-controls input {

    font-size: 11px !important;

    min-height: 34px !important;
}


/*
   Chat buttons
*/

.jyora-chat-controls button {

    min-height: 32px !important;

    font-size: 11px !important;

    border-radius: 7px !important;
}


/* ============================================================
   FLOATING CHAT BUTTON
   ============================================================ */

.jyora-chat-launcher {

    position: fixed !important;

    left: 20px !important;

    bottom: 20px !important;

    z-index: 2147483647 !important;

    pointer-events: auto !important;
}

.jyora-chat-launcher button {

    border-radius: 50px !important;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #2563EB
        ) !important;

    color: #FFFFFF !important;

    border: none !important;

    padding: 0 18px !important;

    min-height: 42px !important;

    font-size: 12px !important;

    font-weight: 700 !important;

    box-shadow:
        0 10px 25px rgba(37,99,235,0.25) !important;
}

.jyora-chat-launcher button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 14px 30px rgba(37,99,235,0.30) !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    border-top: 1px solid #E2E8F0;

    margin-top: 60px;

    padding: 25px 0;

    text-align: center;

    color: #64748B;

    font-size: 12px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    .hero-title {
        font-size: 36px;
    }

    .hero-section {
        padding: 45px 20px;
    }

    .jyora-chat-wrapper,
    .jyora-chat-box {

        width: 285px !important;
    }

    .jyora-chat-wrapper {

        left: 10px !important;

        bottom: 10px !important;
    }

    .jyora-chat-launcher {

        left: 10px !important;

        bottom: 10px !important;
    }

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

            <div class="brand-symbol">
                J
            </div>

            <div>

                <div class="brand-name">

                    <span class="jyora-text">
                        JYORA
                    </span>

                    <span class="ai-text">
                        AI
                    </span>

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
    ("Use Cases", "Projects"),
    ("Solutions", "Services"),
    ("Start Project", "Request Project"),
    ("About", "About"),
    ("Contact", "Contact"),
]

for col, (label, page) in zip(nav_cols, navigation):

    with col:

        if st.button(
            label,
            use_container_width=True,
            key=f"nav_{page}"
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

    <div class="hero-badge">
        ✦ AI • DATA • BUSINESS INTELLIGENCE
    </div>

    <div class="hero-title">
        Intelligence That
        <span>
            Moves Business Forward
        </span>
    </div>

    <div class="hero-description">

        JYORA AI helps businesses transform
        complex data into intelligent decisions
        through AI, Predictive Analytics and Automation.

    </div>

</div>
"""
    )

    services = [

        (
            "🤖 Artificial Intelligence",
            "Predictive models, machine learning, and decision engines."
        ),

        (
            "📊 Business Intelligence",
            "Interactive Power BI dashboards, KPI systems, and visualization."
        ),

        (
            "🔮 Predictive Analytics",
            "Forecast demand, mitigate risks, and spot trends."
        ),

        (
            "⚙️ Intelligent Automation",
            "Automate workflows, reporting pipelines, and repetitive data tasks."
        ),

    ]

    cols = st.columns(2)

    for idx, (title, desc) in enumerate(services):

        with cols[idx % 2]:

            html(
                f"""
<div class="feature-card" style="margin-bottom:15px;">

    <div class="feature-title">
        {title}
    </div>

    <div class="feature-text">
        {desc}
    </div>

</div>
"""
            )


# ============================================================
# SERVICES
# ============================================================

def services_page():

    st.title("Solutions & Services")

    st.write(
        "Custom enterprise-grade AI, BI, and ETL pipeline solutions."
    )


# ============================================================
# PROJECTS
# ============================================================

def projects_page():

    st.title("Case Studies & Projects")

    st.write(
        "Explore how our predictive models drive growth "
        "across logistics and retail."
    )


# ============================================================
# REQUEST PROJECT
# ============================================================

def request_project_page():

    st.title("Start a Project")

    with st.form("req_form"):

        name = st.text_input("Name")

        email = st.text_input("Email")

        overview = st.text_area(
            "Project Overview"
        )

        submitted = st.form_submit_button(
            "Submit"
        )

        if submitted:

            if not name.strip():

                st.error("Please enter your name.")

            elif not valid_email(email):

                st.error("Please enter a valid email.")

            else:

                payload = {

                    "type": "project_request",

                    "name": name.strip(),

                    "email": email.strip(),

                    "project_overview": overview.strip(),

                    "timestamp": datetime.now().isoformat(),

                }

                success = submit_to_google(payload)

                if success:

                    st.success(
                        "Project request submitted successfully."
                    )

                else:

                    st.warning(
                        "Request submitted, but confirmation could not be verified."
                    )


# ============================================================
# ABOUT
# ============================================================

def about_page():

    st.title("About JYORA AI")

    st.write(
        "Over a decade of expertise delivering actionable insights."
    )


# ============================================================
# CONTACT
# ============================================================

def contact_page():

    st.title("Contact Us")

    st.write(
        "Get in touch with our engineering team."
    )


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

current_page_func = pages.get(
    st.session_state.page,
    home_page
)

current_page_func()


# ============================================================
# FLOATING CHATBOT
# ============================================================

def render_floating_chatbot():

    # --------------------------------------------------------
    # CLOSED STATE
    # --------------------------------------------------------

    if not st.session_state.chat_open:

        st.markdown(
            '<div class="jyora-chat-launcher">',
            unsafe_allow_html=True
        )

        if st.button(
            "💬 Chat with JYORA AI",
            key="btn_open_chat"
        ):

            st.session_state.chat_open = True

            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        return


    # --------------------------------------------------------
    # OPEN STATE
    # --------------------------------------------------------

    st.markdown(
        '<div class="jyora-chat-wrapper">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="jyora-chat-box">',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CHAT HEADER
    # --------------------------------------------------------

    html(
        """
<div class="jyora-chat-header">

    <div class="jyora-chat-header-left">

        <div class="jyora-chat-avatar">
            🤖
        </div>

        <div>

            <div class="jyora-chat-title">
                JYORA AI Assistant
            </div>

            <div class="jyora-chat-subtitle">
                ● Online • AI & Project Consultation
            </div>

        </div>

    </div>

</div>
"""
    )


    # --------------------------------------------------------
    # CLOSE BUTTON
    # --------------------------------------------------------

    if st.button(
        "✕ Close & New Chat",
        key="btn_close_chat",
        use_container_width=True
    ):

        st.session_state.chat_open = False

        reset_chat_state()

        st.rerun()


    # --------------------------------------------------------
    # CHAT MESSAGES
    # --------------------------------------------------------

    chat_html = '<div class="jyora-chat-body">'

    for msg in st.session_state.chat_messages:

        if msg["role"] == "assistant":

            cls = "jyora-message-assistant"

        else:

            cls = "jyora-message-user"

        chat_html += (
            f'<div class="jyora-message {cls}">'
            f'{msg["text"]}'
            f'</div>'
        )

    chat_html += "</div>"

    html(chat_html)


    # --------------------------------------------------------
    # CHAT CONTROLS
    # --------------------------------------------------------

    st.markdown(
        '<div class="jyora-chat-controls">',
        unsafe_allow_html=True
    )

    step = st.session_state.chat_step


    # --------------------------------------------------------
    # STEP 0 — NAME
    # --------------------------------------------------------

    if step == 0:

        name = st.text_input(
            "Name",
            key="chat_name",
            placeholder="Your name..."
        )

        if st.button(
            "Next →",
            key="chat_btn_s0",
            use_container_width=True
        ):

            if name.strip():

                st.session_state.chat_data["name"] = (
                    name.strip()
                )

                st.session_state.chat_messages.append(
                    {
                        "role": "user",
                        "text": name.strip()
                    }
                )

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "text": "What service do you need?"
                    }
                )

                st.session_state.chat_step = 1

                st.rerun()

            else:

                st.warning(
                    "Please enter your name."
                )


    # --------------------------------------------------------
    # STEP 1 — SERVICE
    # --------------------------------------------------------

    elif step == 1:

        options = [

            "AI Solutions",

            "BI & Dashboards",

            "Predictive Analytics",

            "Automation",

        ]

        for opt in options:

            if st.button(
                opt,
                key=f"chat_opt_{opt}",
                use_container_width=True
            ):

                st.session_state.chat_data[
                    "service"
                ] = opt

                st.session_state.chat_messages.append(
                    {
                        "role": "user",
                        "text": opt
                    }
                )

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "text": "Please enter your email."
                    }
                )

                st.session_state.chat_step = 2

                st.rerun()


    # --------------------------------------------------------
    # STEP 2 — EMAIL
    # --------------------------------------------------------

    elif step == 2:

        email = st.text_input(
            "Email",
            key="chat_email",
            placeholder="email@domain.com"
        )

        if st.button(
            "Submit Request",
            key="chat_btn_s2",
            use_container_width=True
        ):

            if valid_email(email):

                clean_email = email.strip()

                st.session_state.chat_data[
                    "email"
                ] = clean_email

                st.session_state.chat_messages.append(
                    {
                        "role": "user",
                        "text": clean_email
                    }
                )


                payload = {

                    "type": "chat_lead",

                    "name": st.session_state.chat_data.get(
                        "name"
                    ),

                    "service": st.session_state.chat_data.get(
                        "service"
                    ),

                    "email": clean_email,

                    "timestamp": datetime.now().isoformat(),

                }


                submit_to_google(payload)


                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "text": (
                            "✅ Thanks! "
                            "We'll reach out soon."
                        )
                    }
                )

                st.session_state.chat_step = 3

                st.rerun()

            else:

                st.error(
                    "Please enter a valid email."
                )


    # --------------------------------------------------------
    # STEP 3 — COMPLETED
    # --------------------------------------------------------

    elif step == 3:

        if st.button(
            "Start New Session",
            key="chat_btn_reset",
            use_container_width=True
        ):

            reset_chat_state()

            st.rerun()


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# RENDER CHATBOT
# ============================================================

render_floating_chatbot()


# ============================================================
# FOOTER
# ============================================================

html(
    """
<div class="footer">

    <div>
        <b>JYORA AI</b>
        — Data Intelligence & Automation Platform
    </div>

    <div>
        © 2026 JYORA AI. All rights reserved.
    </div>

</div>
"""
)
```
