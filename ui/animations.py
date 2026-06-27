import streamlit as st
import time


# ==========================================
# PAGE LOADER
# ==========================================

def page_loader():

    with st.spinner("🚀 Loading ProjectForge AI..."):
        time.sleep(1)


# ==========================================
# PROJECT ANALYSIS LOADER
# ==========================================

def project_analysis_loader():

    progress_bar = st.progress(0)

    status = st.empty()

    steps = [
        "🧠 Understanding Project Idea...",
        "📋 Gathering Requirements...",
        "🏗 Designing Architecture...",
        "⚙ Selecting Technology Stack...",
        "🗄 Planning Database...",
        "🔗 Designing APIs...",
        "📈 Estimating Complexity...",
        "📄 Generating Project Blueprint..."
    ]

    for i, step in enumerate(steps):

        status.markdown(f"### {step}")

        progress_bar.progress((i + 1) / len(steps))

        time.sleep(0.5)

    status.success("✅ Blueprint Generated Successfully!")

    time.sleep(0.8)

    progress_bar.empty()

    status.empty()


# ==========================================
# SUCCESS ANIMATION
# ==========================================

def success_message(message):

    st.success(message)

    time.sleep(1)


# ==========================================
# ERROR MESSAGE
# ==========================================

def error_message(message):

    st.error(message)


# ==========================================
# WARNING MESSAGE
# ==========================================

def warning_message(message):

    st.warning(message)


# ==========================================
# INFO MESSAGE
# ==========================================

def info_message(message):

    st.info(message)


# ==========================================
# METRIC COUNTER
# ==========================================

def animated_metric(title, value):

    placeholder = st.empty()

    for i in range(value + 1):

        placeholder.metric(title, i)

        time.sleep(0.03)


# ==========================================
# TYPEWRITER EFFECT
# ==========================================

def typewriter(text):

    placeholder = st.empty()

    output = ""

    for char in text:

        output += char

        placeholder.markdown(output)

        time.sleep(0.01)


# ==========================================
# GLASS CARD LOADER
# ==========================================

def card_loader():

    with st.container():

        st.markdown(
            """
            <div class="glass-card glow">
                <h3>⚡ ProjectForge AI is working...</h3>
                <p>Please wait while we generate your software blueprint.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(2)