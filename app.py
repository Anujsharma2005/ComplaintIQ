import html
import textwrap
import streamlit as st

from nlp.analyzer import analyze_complaint

# ============================================================
# COMPLAINTIQ — PREMIUM AI COMMAND CENTER
# ============================================================

st.set_page_config(
    page_title="ComplaintIQ — AI Complaint Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM UI / ANIMATED BACKGROUND
# ============================================================

def ui(markup, **kwargs):
    """Render HTML without indentation accidentally becoming Markdown code."""
    return st.markdown(textwrap.dedent(markup).strip(), **kwargs)


ui(
    """
<style>
/* ---------- GLOBAL ---------- */

:root {
    --bg: #050816;
    --bg-2: #080d1d;
    --panel: rgba(13, 19, 39, 0.72);
    --panel-strong: rgba(16, 23, 47, 0.90);
    --border: rgba(148, 163, 184, 0.14);
    --text: #f5f7ff;
    --muted: #8d98b2;
    --blue: #5b7cff;
    --cyan: #39d9ff;
    --violet: #9b6cff;
    --green: #43e6a2;
    --red: #ff5c7a;
    --amber: #ffc857;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(91, 124, 255, 0.12), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(57, 217, 255, 0.08), transparent 25%),
        radial-gradient(circle at 60% 90%, rgba(155, 108, 255, 0.10), transparent 28%),
        linear-gradient(135deg, #050816 0%, #070b18 48%, #040612 100%);
    color: var(--text);
    min-height: 100vh;
}

/* Animated atmospheric layers */
.stApp::before {
    content: "";
    position: fixed;
    inset: -25%;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at 20% 30%, rgba(91,124,255,.14), transparent 20%),
        radial-gradient(circle at 75% 20%, rgba(57,217,255,.10), transparent 18%),
        radial-gradient(circle at 55% 80%, rgba(155,108,255,.12), transparent 22%);
    filter: blur(16px);
    animation: atmosphere 20s ease-in-out infinite alternate;
}

.stApp::after {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: .28;
    background-image:
        linear-gradient(rgba(91,124,255,.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(91,124,255,.045) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: linear-gradient(to bottom, black, transparent 90%);
    animation: gridmove 28s linear infinite;
}

@keyframes atmosphere {
    0% { transform: translate3d(-2%, -1%, 0) scale(1); }
    50% { transform: translate3d(2%, 1%, 0) scale(1.05); }
    100% { transform: translate3d(-1%, 3%, 0) scale(1.02); }
}

@keyframes gridmove {
    from { transform: translateY(0); }
    to { transform: translateY(42px); }
}

@keyframes pulse {
    0%, 100% { opacity: .55; transform: scale(.92); }
    50% { opacity: 1; transform: scale(1.08); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

@keyframes shimmer {
    0% { background-position: -250% 0; }
    100% { background-position: 250% 0; }
}

@keyframes scan {
    0% { transform: translateY(-100%); opacity: 0; }
    15% { opacity: .8; }
    85% { opacity: .35; }
    100% { transform: translateY(100vh); opacity: 0; }
}

/* Keep Streamlit content above atmospheric layers */
header, .stApp > div, [data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.main .block-container {
    max-width: 1500px;
    padding: 2.2rem 3rem 4rem 3rem;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(8,12,28,.98), rgba(5,8,20,.98));
    border-right: 1px solid rgba(91,124,255,.13);
    box-shadow: 15px 0 50px rgba(0,0,0,.20);
}

section[data-testid="stSidebar"] > div {
    padding: 0.65rem 1.15rem 1rem 1.15rem;
}

/* Use the full sidebar height without leaving a dead zone at the top. */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    min-height: calc(100vh - 12px);
    box-sizing: border-box;
}

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 4px;
}

.brand-mark {
    width: 36px;
    height: 36px;
    border-radius: 11px;
    display: grid;
    place-items: center;
    color: white;
    font-size: 18px;
    font-weight: 800;
    background:
        linear-gradient(135deg, #5b7cff, #8f62ff 55%, #39d9ff);
    box-shadow:
        0 0 25px rgba(91,124,255,.34),
        inset 0 1px 0 rgba(255,255,255,.35);
    animation: float 4s ease-in-out infinite;
}

.brand {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 23px;
    font-weight: 700;
    letter-spacing: -0.7px;
    color: #f7f9ff;
}

.sidebar-subtitle {
    color: #75809c;
    font-size: 11px;
    margin: 3px 0 26px 47px;
    letter-spacing: .3px;
}

.sidebar-section {
    color: #687491;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.7px;
    margin: 27px 0 10px 3px;
}

section[data-testid="stSidebar"] .stCheckbox {
    margin-bottom: -4px;
}

section[data-testid="stSidebar"] .stCheckbox label {
    color: #aeb8cf !important;
    font-size: 12px !important;
}

section[data-testid="stSidebar"] .stCheckbox label:hover {
    color: white !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(148,163,184,.10);
    margin: 25px 0;
}

section[data-testid="stSidebar"] .stCaption {
    color: #687491 !important;
    font-size: 11px !important;
}

.system-card {
    border: 1px solid rgba(91,124,255,.12);
    background: rgba(12,18,38,.55);
    border-radius: 14px;
    padding: 12px;
    margin-top: 8px;
}

.system-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #8792ae;
    font-size: 10px;
    padding: 5px 0;
}

.system-row strong {
    color: #d9e0f2;
    font-weight: 600;
}

/* ---------- HERO ---------- */

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,.13);
    border-radius: 26px;
    padding: 31px 34px 29px 34px;
    margin-bottom: 22px;
    background:
        linear-gradient(135deg, rgba(18,27,57,.88), rgba(8,13,30,.72)),
        radial-gradient(circle at 88% 25%, rgba(57,217,255,.12), transparent 25%);
    box-shadow:
        0 30px 80px rgba(0,0,0,.28),
        inset 0 1px 0 rgba(255,255,255,.06);
    backdrop-filter: blur(8px);
}

.hero::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -80px;
    top: -120px;
    border-radius: 50%;
    background: rgba(91,124,255,.16);
    filter: blur(20px);
    animation: pulse 5s ease-in-out infinite;
}

.hero::after {
    content: "";
    position: absolute;
    height: 1px;
    left: 0;
    right: 0;
    top: 0;
    background: linear-gradient(90deg, transparent, rgba(91,124,255,.75), rgba(57,217,255,.7), transparent);
    animation: shimmer 5s linear infinite;
    background-size: 250% 100%;
}

.hero-grid {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    gap: 25px;
}

.eyebrow {
    color: #7d8bad;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 11px;
}

.hero-title {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: clamp(34px, 4vw, 56px);
    line-height: .98;
    font-weight: 700;
    letter-spacing: -2.5px;
    margin: 0;
    color: #f8faff;
}

.hero-title span {
    background: linear-gradient(100deg, #ffffff 10%, #89a1ff 45%, #4de1ff 80%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-copy {
    max-width: 720px;
    color: #8d98b2;
    font-size: 14px;
    line-height: 1.65;
    margin-top: 14px;
}

.hero-status {
    min-width: 175px;
    padding: 14px 17px;
    border-radius: 17px;
    border: 1px solid rgba(67,230,162,.16);
    background: rgba(67,230,162,.055);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.03);
}

.status-top {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #e5fff4;
    font-size: 12px;
    font-weight: 700;
}

.status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #43e6a2;
    box-shadow: 0 0 14px #43e6a2;
    animation: pulse 1.7s ease-in-out infinite;
}

.status-sub {
    color: #71829d;
    font-size: 10px;
    margin-top: 6px;
}

/* ---------- SECTION HEADERS ---------- */

.section-head {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 20px;
    margin: 26px 0 13px;
}

.section-title {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #f5f7ff;
    font-size: 18px;
    font-weight: 650;
    letter-spacing: -.5px;
}

.section-subtitle {
    color: #6f7b96;
    font-size: 11px;
    margin-top: 4px;
}

.live-badge {
    color: #8190b1;
    border: 1px solid rgba(148,163,184,.13);
    background: rgba(15,22,45,.55);
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ---------- INPUT AREA ---------- */

.input-shell {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(91,124,255,.18);
    border-radius: 22px;
    padding: 21px 22px 18px;
    background:
        linear-gradient(145deg, rgba(17,25,53,.86), rgba(8,13,29,.78));
    box-shadow:
        0 20px 60px rgba(0,0,0,.20),
        inset 0 1px 0 rgba(255,255,255,.045);
    backdrop-filter: blur(7px);
}

.input-shell::before {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -90px;
    bottom: -90px;
    background: rgba(91,124,255,.13);
    filter: blur(18px);
    border-radius: 50%;
}

.input-label {
    color: #e8ecf8;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 4px;
}

.input-hint {
    color: #697590;
    font-size: 11px;
    margin-bottom: 12px;
}

/* Streamlit text area */
div[data-testid="stTextArea"] textarea {
    min-height: 145px !important;
    border-radius: 15px !important;
    border: 1px solid rgba(148,163,184,.14) !important;
    background: rgba(4,8,19,.62) !important;
    color: #eef2ff !important;
    caret-color: #64dfff !important;
    font-size: 13px !important;
    line-height: 1.7 !important;
    padding: 15px !important;
    box-shadow: inset 0 0 30px rgba(0,0,0,.13) !important;
    transition: .25s ease !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(91,124,255,.65) !important;
    box-shadow:
        0 0 0 1px rgba(91,124,255,.28),
        0 0 35px rgba(91,124,255,.10),
        inset 0 0 30px rgba(0,0,0,.15) !important;
}

div[data-testid="stTextArea"] label {
    display: none !important;
}

/* ---------- BUTTONS ---------- */

div.stButton > button {
    height: 45px;
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,.12);
    background: rgba(18,27,55,.86);
    color: #cbd5ee;
    font-size: 12px;
    font-weight: 650;
    letter-spacing: .1px;
    transition: all .22s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.035);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    border-color: rgba(91,124,255,.45);
    background: rgba(27,39,79,.95);
    color: white;
    box-shadow: 0 12px 30px rgba(0,0,0,.22), 0 0 25px rgba(91,124,255,.08);
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #4e68e9, #745cf1 55%, #4388ff);
    border: 1px solid rgba(255,255,255,.13);
    color: white;
    box-shadow:
        0 10px 28px rgba(91,124,255,.22),
        inset 0 1px 0 rgba(255,255,255,.22);
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(100deg, #6179ff, #886ffb 55%, #55a0ff);
    box-shadow:
        0 15px 36px rgba(91,124,255,.30),
        0 0 30px rgba(91,124,255,.12);
}

/* ---------- METRIC CARDS ---------- */

.metric-card {
    position: relative;
    overflow: hidden;
    min-height: 125px;
    border-radius: 18px;
    border: 1px solid rgba(148,163,184,.12);
    padding: 18px 19px;
    background:
        linear-gradient(145deg, rgba(18,26,53,.88), rgba(8,13,29,.78));
    box-shadow:
        0 15px 40px rgba(0,0,0,.18),
        inset 0 1px 0 rgba(255,255,255,.035);
    transition: .25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(91,124,255,.27);
    box-shadow:
        0 22px 48px rgba(0,0,0,.25),
        0 0 30px rgba(91,124,255,.06);
}

.metric-card::after {
    content: "";
    position: absolute;
    width: 100px;
    height: 100px;
    right: -45px;
    bottom: -55px;
    border-radius: 50%;
    background: rgba(91,124,255,.10);
    filter: blur(12px);
}

.metric-label {
    color: #71809d;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.4px;
}

.metric-value {
    color: #f4f7ff;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 24px;
    line-height: 1.1;
    font-weight: 700;
    margin-top: 14px;
    letter-spacing: -.8px;
}

.metric-accent {
    width: 27px;
    height: 3px;
    border-radius: 20px;
    background: linear-gradient(90deg, #5b7cff, #39d9ff);
    margin-top: 12px;
    box-shadow: 0 0 12px rgba(57,217,255,.3);
}

/* ---------- RESULT CARDS ---------- */

.result-card {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,.12);
    border-radius: 18px;
    padding: 20px;
    margin-top: 16px;
    background:
        linear-gradient(145deg, rgba(15,23,47,.88), rgba(8,13,29,.76));
    box-shadow:
        0 15px 45px rgba(0,0,0,.17),
        inset 0 1px 0 rgba(255,255,255,.035);
}

.result-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 38%;
    height: 1px;
    background: linear-gradient(90deg, #5b7cff, transparent);
}

.result-title {
    color: #edf1fc;
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 14px;
    font-weight: 650;
    letter-spacing: -.2px;
    margin-bottom: 13px;
}

.result-label {
    color: #75819d;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    font-weight: 700;
}

.result-value {
    color: #f4f7ff;
    font-size: 15px;
    font-weight: 650;
    margin-top: 4px;
}

.detail-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(148,163,184,.07);
    color: #8e9ab4;
    font-size: 11px;
}

.detail-row:last-child {
    border-bottom: 0;
}

.detail-row strong {
    color: #dbe2f2;
}

/* ---------- TAGS ---------- */

.tag {
    display: inline-block;
    padding: 7px 10px;
    margin: 3px 5px 3px 0;
    border-radius: 999px;
    border: 1px solid rgba(91,124,255,.17);
    background: rgba(91,124,255,.075);
    color: #aebeff;
    font-size: 10px;
    font-weight: 600;
    transition: .2s ease;
}

.tag:hover {
    border-color: rgba(57,217,255,.38);
    color: #d8f9ff;
    transform: translateY(-1px);
}

/* ---------- PIPELINE ---------- */

.pipeline {
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 17px 0 4px;
    flex-wrap: wrap;
}

.pipe-node {
    border: 1px solid rgba(91,124,255,.15);
    background: rgba(91,124,255,.055);
    border-radius: 9px;
    padding: 7px 9px;
    color: #8f9cba;
    font-size: 9px;
    font-weight: 600;
}

.pipe-arrow {
    color: #53617f;
    font-size: 10px;
}

/* ---------- PROGRESS ---------- */

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #5b7cff, #39d9ff) !important;
}

div[data-testid="stProgress"] {
    margin: 8px 0;
}

/* ---------- STREAMLIT TEXT ---------- */

.stMarkdown, .stCaption, .stText {
    color: #8d98b2;
}

[data-testid="stExpander"] {
    border: 1px solid rgba(148,163,184,.10) !important;
    border-radius: 15px !important;
    background: rgba(10,15,31,.55) !important;
}

[data-testid="stExpander"] summary {
    color: #9ca8c2 !important;
    font-size: 11px !important;
}

/* ---------- INFO / ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid rgba(91,124,255,.18);
    background: rgba(91,124,255,.07);
}


/* ---------- AI INTELLIGENCE CARD ---------- */
.ai-intel {
    border: 1px solid rgba(91,124,255,.13);
    background: linear-gradient(135deg, rgba(91,124,255,.07), rgba(57,217,255,.035));
    border-radius: 14px;
    padding: 17px;
}
.ai-intel-title {
    color: #dce4ff;
    font-size: 12px;
    font-weight: 650;
    margin-bottom: 6px;
}
.ai-intel-copy {
    color: #77849f;
    font-size: 11px;
    line-height: 1.65;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #56617a;
    font-size: 9px;
    letter-spacing: .8px;
    margin-top: 45px;
    padding: 20px 0 5px;
    border-top: 1px solid rgba(148,163,184,.08);
}

/* ---------- MOBILE ---------- */

@media (max-width: 900px) {
    .main .block-container {
        padding: 1.2rem 1rem 3rem;
    }

    .hero {
        padding: 24px;
        border-radius: 20px;
    }

    .hero-grid {
        grid-template-columns: 1fr;
    }

    .hero-status {
        width: fit-content;
    }

    .hero-title {
        font-size: 38px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================

if "complaint" not in st.session_state:
    st.session_state.complaint = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    ui(
        """
        <div class="brand-wrap">
            <div class="brand-mark">◈</div>
            <div class="brand">ComplaintIQ</div>
        </div>
        <div class="sidebar-subtitle">CUSTOMER COMPLAINT INTELLIGENCE</div>
        """,
        unsafe_allow_html=True,
    )

    ui('<div class="sidebar-section">Analysis Modules</div>', unsafe_allow_html=True)

    sentiment_enabled = st.checkbox("Sentiment Analysis", value=True)
    category_enabled = st.checkbox("Complaint Classification", value=True)
    keywords_enabled = st.checkbox("Keyword Extraction", value=True)
    urgency_enabled = st.checkbox("Urgency Detection", value=True)
    llm_enabled = st.checkbox("LLM Analysis", value=True)

    st.divider()

    ui('<div class="sidebar-section">System Stack</div>', unsafe_allow_html=True)

    ui(
        """
        <div class="system-card">
            <div class="system-row"><span>NLP Engine</span><strong>Python</strong></div>
            <div class="system-row"><span>Classification</span><strong>TF-IDF</strong></div>
            <div class="system-row"><span>Sentiment</span><strong>VADER</strong></div>
            <div class="system-row"><span>LLM</span><strong>Gemini API</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ui(
        '<div style="height:14px"></div><div class="sidebar-section">Pipeline</div>',
        unsafe_allow_html=True,
    )

    ui(
        """
        <div class="pipeline" style="display:block;">
            <div class="pipe-node">01 · INPUT</div>
            <div style="height:8px"></div>
            <div class="pipe-node">02 · NLP PROCESSING</div>
            <div style="height:8px"></div>
            <div class="pipe-node">03 · CLASSIFICATION</div>
            <div style="height:8px"></div>
            <div class="pipe-node">04 · ACTION INTELLIGENCE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ui(
        """
        <div style="margin-top:92px;padding-bottom:16px;color:#4f5a73;font-size:9px;line-height:1.7;letter-spacing:.4px;">
            COMPLAINTIQ<br>
            ACADEMIC NLP PROJECT
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

ui(
    """
    <div class="hero">
        <div class="hero-grid">
            <div>
                <div class="eyebrow">AI-POWERED CUSTOMER INTELLIGENCE · 01</div>
                <div class="hero-title">
                    Turn complaints into<br>
                    <span>clear actions.</span>
                </div>
                <div class="hero-copy">
                    ComplaintIQ transforms raw customer complaints into structured
                    sentiment, category, urgency and keyword intelligence using
                    a multi-stage NLP pipeline.
                </div>
            </div><div class="hero-status">
                <div class="status-top">
                    <span class="status-dot"></span>
                    SYSTEM READY
                </div>
                <div class="status-sub">NLP pipeline operational</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# INPUT
# ============================================================

ui(
    """
    <div class="section-head">
        <div>
            <div class="section-title">Complaint intelligence console</div>
            <div class="section-subtitle">Paste a customer message and let the NLP pipeline break it down.</div>
        </div>
        <div class="live-badge">● Live analysis</div>
    </div>

    <div class="input-shell">
        <div class="input-label">Customer complaint</div>
        <div class="input-hint">Use a real complaint or load the built-in sample to test the system.</div>
    """,
    unsafe_allow_html=True,
)

complaint = st.text_area(
    "Customer complaint",
    value=st.session_state.complaint,
    placeholder=(
        "Example: I have been waiting for three days for my order. "
        "The delivery team has not responded to my calls."
    ),
    height=145,
    label_visibility="collapsed",
)

button1, button2, button3 = st.columns([1.35, 1.0, 0.65])

with button1:
    analyze_button = st.button(
        "✦  Analyze complaint",
        use_container_width=True,
        type="primary",
    )

with button2:
    sample_button = st.button(
        "↗  Load sample",
        use_container_width=True,
    )

with button3:
    clear_button = st.button(
        "×  Clear",
        use_container_width=True,
    )

ui("</div>", unsafe_allow_html=True)


# ============================================================
# BUTTON ACTIONS
# ============================================================

if sample_button:
    st.session_state.complaint = (
        "I ordered my package five days ago and it still has not been delivered. "
        "I have contacted customer support multiple times but nobody has responded. "
        "This is extremely frustrating and I need the package immediately."
    )
    st.rerun()

if clear_button:
    st.session_state.complaint = ""
    st.session_state.analysis = None
    st.rerun()


# ============================================================
# ANALYZE
# ============================================================

if analyze_button:
    if not complaint.strip():
        st.warning("Please enter a customer complaint first.")
    else:
        st.session_state.complaint = complaint

        with st.spinner("Running NLP analysis..."):
            try:
                result = analyze_complaint(complaint)
                st.session_state.analysis = result
            except Exception as error:
                st.error(f"Analysis failed: {error}")


# ============================================================
# RESULTS
# ============================================================

if st.session_state.analysis:
    result = st.session_state.analysis

    sentiment_data = result["sentiment"]
    classification_data = result["classification"]
    urgency_data = result["urgency"]
    keywords = result["keywords"]

    ui(
        """
        <div class="section-head" style="margin-top:32px;">
            <div>
                <div class="section-title">Analysis overview</div>
                <div class="section-subtitle">
                    Results generated from the ComplaintIQ NLP pipeline.
                </div>
            </div>
            <div class="live-badge">Analysis complete</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    sentiment_label = (
        sentiment_data["label"] if sentiment_enabled else "Disabled"
    )

    category_label = (
        classification_data["category"] if category_enabled else "Disabled"
    )

    urgency_label = (
        urgency_data["level"] if urgency_enabled else "Disabled"
    )

    metrics = [
        ("Sentiment", sentiment_label),
        ("Category", category_label),
        ("Urgency", urgency_label),
        ("NLP Tokens", result["token_count"]),
    ]

    for col, (label, value) in zip(
        [col1, col2, col3, col4],
        metrics,
    ):
        with col:
            ui(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{html.escape(str(label))}</div>
                    <div class="metric-value">{html.escape(str(value))}</div>
                    <div class="metric-accent"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------
    # DETAIL COLUMNS
    # --------------------------------------------------------

    left, right = st.columns(2, gap="large")

    # SENTIMENT
    with left:
        ui(
            '<div class="result-card"><div class="result-title">◉ Sentiment analysis</div>',
            unsafe_allow_html=True,
        )

        if sentiment_enabled:
            compound = float(sentiment_data["compound"])
            progress_value = min(max((compound + 1) / 2, 0), 1)

            ui(
                f"""
                <div class="detail-row">
                    <span>Overall sentiment</span>
                    <strong>{html.escape(str(sentiment_data["label"]))}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(progress_value)

            ui(
                f"""
                <div class="detail-row">
                    <span>Compound score</span>
                    <strong>{compound:.3f}</strong>
                </div>
                <div class="detail-row">
                    <span>Positive</span>
                    <strong>{float(sentiment_data["positive"]):.2f}</strong>
                </div>
                <div class="detail-row">
                    <span>Neutral</span>
                    <strong>{float(sentiment_data["neutral"]):.2f}</strong>
                </div>
                <div class="detail-row">
                    <span>Negative</span>
                    <strong>{float(sentiment_data["negative"]):.2f}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Sentiment analysis is disabled.")

        ui("</div>", unsafe_allow_html=True)

    # CLASSIFICATION
    with right:
        ui(
            '<div class="result-card"><div class="result-title">⌁ Complaint classification</div>',
            unsafe_allow_html=True,
        )

        if category_enabled:
            ui(
                f"""
                <div class="detail-row">
                    <span>Detected category</span>
                    <strong>{html.escape(str(classification_data["category"]))}</strong>
                </div>
                <div class="detail-row">
                    <span>Confidence</span>
                    <strong>{float(classification_data["confidence"]):.3f}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )

            ui(
                '<div style="margin-top:16px;margin-bottom:6px;" class="result-label">Category similarity</div>',
                unsafe_allow_html=True,
            )

            for category, score in sorted(
                classification_data["scores"].items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                safe_category = html.escape(str(category))
                score_value = float(score)

                ui(
                    f"""
                    <div class="detail-row">
                        <span>{safe_category}</span>
                        <strong>{score_value:.3f}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(min(score_value, 1.0))
        else:
            st.info("Complaint classification is disabled.")

        ui("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    ui(
        '<div class="result-card"><div class="result-title"># Extracted keywords</div>',
        unsafe_allow_html=True,
    )

    if keywords_enabled and keywords:
        tags = "".join(
            f'<span class="tag">{html.escape(str(keyword))}</span>'
            for keyword in keywords
        )
        ui(tags, unsafe_allow_html=True)

    elif keywords_enabled:
        st.info("No significant keywords detected.")

    else:
        st.info("Keyword extraction is disabled.")

    ui("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # URGENCY
    # --------------------------------------------------------

    ui(
        '<div class="result-card"><div class="result-title">⚡ Urgency assessment</div>',
        unsafe_allow_html=True,
    )

    if urgency_enabled:
        indicators = urgency_data.get("indicators", [])

        ui(
            f"""
            <div class="detail-row">
                <span>Urgency level</span>
                <strong>{html.escape(str(urgency_data["level"]))}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if indicators:
            safe_indicators = ", ".join(
                html.escape(str(item)) for item in indicators
            )

            ui(
                f"""
                <div class="detail-row">
                    <span>Detected indicators</span>
                    <strong>{safe_indicators}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            ui(
                """
                <div style="color:#74809a;font-size:11px;margin-top:10px;">
                    No explicit urgency indicators detected.
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Urgency detection is disabled.")

    ui("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # NLP PREPROCESSING
    # --------------------------------------------------------

    with st.expander("⌘  View NLP preprocessing details"):
        ui("**Original text**")
        st.write(result["original_text"])

        ui("**Cleaned text**")
        st.code(result["cleaned_text"])

        ui("**Tokens after preprocessing**")
        st.write(result["tokens"])

    # --------------------------------------------------------
    # LLM INTELLIGENCE
    # --------------------------------------------------------

    if llm_enabled:
        ui(
            '<div class="result-card"><div class="result-title">✦ AI response intelligence</div><div class="ai-intel"><div class="ai-intel-title">Gemini intelligence layer ready</div><div class="ai-intel-copy">The NLP pipeline has prepared the complaint context. The Gemini LLM can use these results to generate a complaint summary, recommended resolution, escalation decision and professional customer response.</div><div class="pipeline"><div class="pipe-node">NLP</div><div class="pipe-arrow">→</div><div class="pipe-node">CONTEXT</div><div class="pipe-arrow">→</div><div class="pipe-node">GEMINI</div><div class="pipe-arrow">→</div><div class="pipe-node">ACTION</div></div></div></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

ui(
    """
    <div class="footer">
        COMPLAINTIQ &nbsp;·&nbsp;
        NATURAL LANGUAGE PROCESSING &nbsp;·&nbsp;
        TF-IDF &nbsp;·&nbsp;
        MACHINE LEARNING &nbsp;·&nbsp;
        LARGE LANGUAGE MODELS
    </div>
    """,
    unsafe_allow_html=True,
)
