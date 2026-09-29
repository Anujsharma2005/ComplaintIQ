import html
import random
import streamlit as st

from nlp.analyzer import analyze_complaint

# ============================================================
# COMPLAINTIQ — CUSTOMER COMPLAINT INTELLIGENCE
# Complete standalone Streamlit UI
# ============================================================

st.set_page_config(
    page_title="ComplaintIQ — Customer Complaint Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# GLOBAL CSS
# ------------------------------------------------------------

st.markdown(
    r"""
<style>
/* =========================
   CORE
   ========================= */

:root {
    --bg: #6F6FFF;
    --panel: rgba(10, 15, 31, 0.72);
    --panel-strong: rgba(12, 18, 38, 0.90);
    --line: rgba(125, 151, 255, 0.16);
    --line-bright: rgba(108, 143, 255, 0.34);
    --text: #f5f7ff;
    --muted: #8c96b2;
    --blue: #5c7cff;
    --cyan: #005385;
    --purple: #9a6cff;
    --green: #45e6a0;
    --red: #ff5f70;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

[data-testid="stAppViewContainer"] {
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =========================
   REAL MOTION BACKGROUND
   ========================= */

.motion-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(circle at 50% 40%, rgba(31, 52, 122, 0.12), transparent 42%),
        #03050d;
}

/* Moving aurora blobs */
.motion-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(55px);
    opacity: 0.48;
    will-change: transform;
}

.orb-1 {
    width: 520px;
    height: 520px;
    left: -120px;
    top: -130px;
    background: radial-gradient(circle, rgba(68, 91, 255, .48), transparent 68%);
    animation: drift1 18s ease-in-out infinite alternate;
}

.orb-2 {
    width: 470px;
    height: 470px;
    right: -100px;
    top: 8%;
    background: radial-gradient(circle, rgba(0, 203, 255, .34), transparent 67%);
    animation: drift2 22s ease-in-out infinite alternate;
}

.orb-3 {
    width: 560px;
    height: 560px;
    left: 30%;
    bottom: -310px;
    background: radial-gradient(circle, rgba(139, 76, 255, .34), transparent 68%);
    animation: drift3 25s ease-in-out infinite alternate;
}

.orb-4 {
    width: 300px;
    height: 300px;
    left: 48%;
    top: 20%;
    background: radial-gradient(circle, rgba(0, 236, 255, .16), transparent 70%);
    animation: drift4 15s ease-in-out infinite alternate;
}

/* Large slowly rotating light */
.light-ring {
    position: absolute;
    width: 720px;
    height: 720px;
    left: 50%;
    top: 38%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    border: 1px solid rgba(91, 123, 255, .08);
    box-shadow:
        0 0 90px rgba(61, 104, 255, .06),
        inset 0 0 90px rgba(61, 104, 255, .04);
    animation: ringMove 30s linear infinite;
}

.light-ring::before,
.light-ring::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    inset: 70px;
    border: 1px solid rgba(50, 214, 255, .05);
}

.light-ring::after {
    inset: 145px;
    border-color: rgba(160, 102, 255, .05);
}

/* Moving grid */
.motion-grid {
    position: absolute;
    inset: -100px;
    opacity: .42;
    background-image:
        linear-gradient(rgba(100, 124, 255, .055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(100, 124, 255, .055) 1px, transparent 1px);
    background-size: 64px 64px;
    transform: perspective(900px) rotateX(57deg) scale(1.55);
    transform-origin: center bottom;
    animation: gridTravel 12s linear infinite;
    mask-image: linear-gradient(to top, rgba(0,0,0,.85), transparent 82%);
}

/* Diagonal moving energy */
.energy-line {
    position: absolute;
    width: 80vw;
    height: 1px;
    left: -20vw;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(78, 126, 255, 0),
        rgba(72, 182, 255, .45),
        rgba(145, 92, 255, .30),
        transparent
    );
    filter: blur(1px);
    opacity: .55;
}

.energy-1 {
    top: 27%;
    transform: rotate(-12deg);
    animation: energy1 15s linear infinite;
}

.energy-2 {
    top: 67%;
    transform: rotate(9deg);
    animation: energy2 15s linear infinite;
}

/* Scanning beam */
.scan {
    position: absolute;
    left: 0;
    right: 0;
    height: 150px;
    top: -170px;
    background: linear-gradient(
        to bottom,
        transparent,
        rgba(60, 143, 255, 0.02),
        rgba(64, 194, 255, 0.10),
        rgba(89, 113, 255, 0.03),
        transparent
    );
    filter: blur(8px);
    animation: scanDown 20s linear infinite;
}

/* Floating particles */
.particle {
    position: absolute;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background: rgba(126, 177, 255, .72);
    box-shadow: 0 0 10px rgba(91, 147, 255, .8);
    animation: particleFloat var(--duration) ease-in-out infinite;
    animation-delay: var(--delay);
}

.particle.small {
    width: 2px;
    height: 2px;
    opacity: .55;
}

.particle.cyan {
    background: rgba(61, 224, 255, .8);
    box-shadow: 0 0 12px rgba(61, 224, 255, .85);
}

.particle.purple {
    background: rgba(169, 117, 255, .75);
    box-shadow: 0 0 12px rgba(169, 117, 255, .75);
}

/* Ensure actual Streamlit content sits above animation */
[data-testid="stAppViewContainer"] > .main,
[data-testid="stAppViewContainer"] [data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 2;
}

/* =========================
   SIDEBAR
   ========================= */

[data-testid="stSidebar"] {
    background: rgba(4, 7, 17, .90) !important;
    border-right: 1px solid rgba(112, 137, 255, .13);
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}

.brand {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 3px;
}

.brand-mark {
    color: #6e8cff;
    font-size: 20px;
    text-shadow: 0 0 16px rgba(91, 124, 255, .75);
}

.brand-name {
    font-size: 21px;
    font-weight: 850;
    letter-spacing: -0.7px;
    color: #f7f8ff;
}

.brand-sub {
    color: #68738f;
    font-size: 10px;
    margin: 7px 0 38px;
}

.side-label {
    color: #64708d;
    font-size: 9px;
    letter-spacing: 1.7px;
    font-weight: 800;
    margin: 22px 0 10px;
}

.stack-card {
    border: 1px solid rgba(110, 137, 255, .13);
    background: rgba(10, 15, 30, .72);
    border-radius: 11px;
    padding: 10px 12px;
    margin-bottom: 7px;
    color: #d7dcef;
    font-size: 11px;
}

.stack-card span {
    color: #68738f;
}

/* =========================
   HERO
   ========================= */

.hero {
    position: relative;
    overflow: hidden;
    min-height: 430px;
    border-radius: 26px;
    border: 1px solid rgba(102, 132, 255, .23);
    background:
        linear-gradient(135deg, rgba(14, 22, 54, .88), rgba(4, 8, 20, .72)),
        radial-gradient(circle at 85% 10%, rgba(0, 209, 255, .12), transparent 32%);
    box-shadow:
        0 35px 90px rgba(0,0,0,.32),
        inset 0 1px 0 rgba(255,255,255,.035);
    padding: 64px 62px;
}

.hero::before {
    content: "";
    position: absolute;
    width: 420px;
    height: 420px;
    right: -150px;
    top: -180px;
    border: 1px solid rgba(93, 125, 255, .20);
    border-radius: 50%;
    animation: heroRing 16s linear infinite;
}

.hero::after {
    content: "";
    position: absolute;
    width: 520px;
    height: 520px;
    right: -200px;
    top: -230px;
    border: 1px solid rgba(51, 210, 255, .08);
    border-radius: 50%;
    animation: heroRing 23s linear infinite reverse;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(71, 103, 255, .09);
    border: 1px solid rgba(94, 125, 255, .23);
    color: #9caeff;
    font-size: 9px;
    letter-spacing: 1.4px;
    font-weight: 850;
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4af0a5;
    box-shadow: 0 0 12px #4af0a5;
    animation: pulseDot 1.8s infinite;
}

.hero-title {
    position: relative;
    z-index: 2;
    font-size: clamp(45px, 5.4vw, 76px);
    line-height: .98;
    letter-spacing: -4.2px;
    font-weight: 900;
    margin: 27px 0 19px;
    max-width: 900px;
}

.hero-title .gradient {
    background: linear-gradient(90deg, #b9c7ff 0%, #70a6ff 42%, #3be1ff 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero-copy {
    max-width: 790px;
    color: #8792b0;
    line-height: 1.75;
    font-size: 14px;
}

.status-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 26px;
}

.status {
    padding: 8px 11px;
    border-radius: 9px;
    border: 1px solid rgba(115, 139, 255, .15);
    background: rgba(15, 21, 43, .72);
    color: #8e9aba;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: .7px;
}

.status.live {
    color: #5ff0ae;
    border-color: rgba(69, 230, 160, .23);
}

/* =========================
   SECTION HEADERS
   ========================= */

.section-title {
    color: #f2f4ff;
    font-size: 20px;
    font-weight: 850;
    letter-spacing: -.7px;
    margin-top: 35px;
    margin-bottom: 5px;
}

.section-sub {
    color: #6f7a96;
    font-size: 11px;
    margin-bottom: 18px;
}


/* =========================
   COMPLAINT WORKSPACE
   ========================= */

.complaint-workspace {
    position: relative;
    padding: 22px;
    border: 1px solid rgba(108, 135, 255, .16);
    border-radius: 22px;
    background:
        linear-gradient(145deg, rgba(12, 18, 38, .74), rgba(5, 9, 20, .67));
    box-shadow:
        0 20px 55px rgba(0,0,0,.18),
        inset 0 1px 0 rgba(255,255,255,.025);
    overflow: hidden;
}

.complaint-workspace::before {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -120px;
    top: -150px;
    border-radius: 50%;
    border: 1px solid rgba(75, 137, 255, .12);
    box-shadow: 0 0 70px rgba(54, 113, 255, .08);
    animation: workspacePulse 8s ease-in-out infinite alternate;
}

.workspace-kicker {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 15px;
}

.workspace-title {
    color: #e9edff;
    font-size: 13px;
    font-weight: 850;
    letter-spacing: .2px;
}

.workspace-status {
    color: #5fe9ab;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.sample-label {
    color: #6f7b98;
    font-size: 9px;
    text-transform: uppercase;
    font-weight: 850;
    letter-spacing: 1.35px;
    margin: 4px 0 10px;
}

.sample-card {
    min-height: 138px;
    border: 1px solid rgba(105, 132, 255, .14);
    border-radius: 14px;
    background: rgba(7, 12, 27, .76);
    padding: 14px;
    transition: .25s ease;
}

.sample-card:hover {
    border-color: rgba(89, 132, 255, .34);
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(24, 62, 153, .10);
}

.sample-type {
    color: #8092ff;
    font-size: 9px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sample-copy {
    color: #929bb2;
    font-size: 10px;
    line-height: 1.55;
    margin-top: 8px;
    min-height: 48px;
}

.sample-action {
    margin-top: 10px;
}

.sample-action div.stButton > button {
    min-height: 34px !important;
    height: 34px !important;
    padding: 0 10px !important;
    border-radius: 9px !important;
    font-size: 10px !important;
}

.complaint-workspace [data-testid="stTextArea"] {
    margin-top: 2px;
}

.complaint-workspace [data-testid="stTextArea"] textarea {
    min-height: 190px !important;
    background:
        linear-gradient(160deg, rgba(12, 18, 36, .96), rgba(7, 11, 24, .94)) !important;
    border-color: rgba(109, 137, 255, .23) !important;
}

.workspace-actions {
    margin-top: 13px;
}

.workspace-actions div.stButton > button {
    height: 52px !important;
    min-height: 52px !important;
    border-radius: 12px !important;
}

.workspace-actions .analyze-wrap div.stButton > button {
    background: linear-gradient(100deg, #4e6cff 0%, #4a82ff 45%, #35d2ff 100%);
}

.workspace-actions .clear-btn div.stButton > button {
    background: rgba(14, 20, 39, .84);
    border: 1px solid rgba(108, 132, 255, .17);
    color: #aeb7cf;
}

.workspace-actions .clear-btn div.stButton > button:hover {
    background: rgba(24, 32, 57, .95);
    border-color: rgba(108, 139, 255, .34);
    color: #f3f6ff;
}

@keyframes workspacePulse {
    from { transform: scale(.92) rotate(0deg); opacity: .45; }
    to { transform: scale(1.08) rotate(18deg); opacity: .9; }
}

/* =========================
   EXAMPLE BUTTONS
   ========================= */

div.stButton > button {
    width: 100%;
    min-height: 43px;
    border-radius: 11px;
    border: 1px solid rgba(114, 137, 255, .16);
    background: rgba(13, 19, 39, .78);
    color: #c9d0e7;
    font-weight: 700;
    transition: all .25s ease;
}

div.stButton > button:hover {
    border-color: rgba(87, 127, 255, .50);
    color: #ffffff;
    background: rgba(31, 44, 83, .82);
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(45, 90, 255, .12);
}

/* Primary analyze button */
.analyze-wrap div.stButton > button {
    min-height: 56px;
    background: linear-gradient(100deg, #526fff, #3f98ff, #39d8ff);
    border: 0;
    color: white;
    font-size: 14px;
    font-weight: 850;
    box-shadow:
        0 12px 35px rgba(55, 105, 255, .25),
        inset 0 1px 0 rgba(255,255,255,.22);
}

.analyze-wrap div.stButton > button:hover {
    transform: translateY(-2px) scale(1.005);
    box-shadow:
        0 18px 48px rgba(55, 105, 255, .34),
        0 0 35px rgba(48, 202, 255, .12);
}

/* =========================
   INPUT
   ========================= */

[data-testid="stTextArea"] textarea {
    min-height: 210px !important;
    border-radius: 17px !important;
    border: 1px solid rgba(110, 136, 255, .20) !important;
    background: rgba(8, 12, 26, .82) !important;
    color: #eef2ff !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
    padding: 18px !important;
    box-shadow: inset 0 0 40px rgba(32, 57, 130, .06);
}

[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(76, 128, 255, .65) !important;
    box-shadow:
        0 0 0 1px rgba(76, 128, 255, .25),
        0 0 40px rgba(53, 101, 255, .10) !important;
}

[data-testid="stTextArea"] label {
    color: #c8cee0 !important;
    font-size: 12px !important;
    font-weight: 750 !important;
}

/* =========================
   METRIC CARDS
   ========================= */

.metric-card {
    min-height: 145px;
    border: 1px solid rgba(112, 137, 255, .15);
    border-radius: 17px;
    background:
        linear-gradient(145deg, rgba(15, 22, 45, .82), rgba(7, 11, 24, .78));
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: .3s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(103, 135, 255, .34);
    box-shadow: 0 18px 45px rgba(0,0,0,.22);
}

.metric-card::after {
    content: "";
    position: absolute;
    width: 130px;
    height: 130px;
    right: -70px;
    bottom: -70px;
    border-radius: 50%;
    background: rgba(71, 111, 255, .13);
    filter: blur(15px);
}

.metric-label {
    color: #697591;
    text-transform: uppercase;
    font-size: 9px;
    letter-spacing: 1.2px;
    font-weight: 850;
}

.metric-value {
    color: #f5f7ff;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -1px;
    margin-top: 16px;
}

.metric-detail {
    color: #818ca7;
    font-size: 10px;
    margin-top: 5px;
}

/* =========================
   RESULT PANELS
   ========================= */

.result-card {
    border: 1px solid rgba(112, 137, 255, .15);
    border-radius: 19px;
    background: rgba(8, 13, 29, .76);
    padding: 23px;
    min-height: 230px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.018);
}

.result-title {
    color: #e9edff;
    font-size: 13px;
    font-weight: 850;
    margin-bottom: 18px;
}

.big-result {
    font-size: 35px;
    font-weight: 900;
    letter-spacing: -1.2px;
    margin-bottom: 7px;
}

.result-muted {
    color: #737e99;
    font-size: 11px;
}

.bar {
    height: 7px;
    border-radius: 999px;
    overflow: hidden;
    background: rgba(255,255,255,.055);
    margin-top: 17px;
}

.bar-fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, #536eff, #42d9ff);
}

.tag {
    display: inline-block;
    padding: 7px 9px;
    border-radius: 8px;
    background: rgba(79, 111, 255, .09);
    border: 1px solid rgba(90, 124, 255, .17);
    color: #9cacd9;
    font-size: 10px;
    margin: 0 6px 7px 0;
}

/* =========================
   ACTION PANEL
   ========================= */

.action-panel {
    border: 1px solid rgba(61, 223, 159, .18);
    border-radius: 19px;
    padding: 23px;
    background:
        linear-gradient(120deg, rgba(25, 89, 68, .13), rgba(7, 15, 27, .76));
    position: relative;
    overflow: hidden;
}

.action-panel::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(#45e6a0, #35b9ff);
}

.action-kicker {
    color: #58e9aa;
    font-size: 9px;
    font-weight: 850;
    letter-spacing: 1.4px;
    text-transform: uppercase;
}

.action-title {
    color: #effff8;
    font-size: 19px;
    font-weight: 850;
    margin-top: 9px;
}

.action-copy {
    color: #8ba99d;
    line-height: 1.65;
    font-size: 12px;
    margin-top: 7px;
}

/* =========================
   PIPELINE
   ========================= */

.pipeline {
    display: flex;
    align-items: center;
    gap: 8px;
    overflow-x: auto;
    padding: 12px 0 16px;
}

.pipe-node {
    min-width: 132px;
    padding: 15px 14px;
    border: 1px solid rgba(106, 132, 255, .15);
    border-radius: 13px;
    background: rgba(9, 14, 30, .75);
    text-align: center;
}

.pipe-node strong {
    display: block;
    color: #e7ebff;
    font-size: 11px;
}

.pipe-node span {
    display: block;
    color: #66728f;
    font-size: 9px;
    margin-top: 5px;
}

.pipe-arrow {
    color: #506dff;
    font-size: 18px;
}

/* =========================
   FOOTER
   ========================= */

.footer {
    text-align: center;
    color: #505a73;
    font-size: 10px;
    padding: 55px 0 25px;
    letter-spacing: .5px;
}

/* =========================
   ANIMATIONS
   ========================= */

@keyframes drift1 {
    0%   { transform: translate(0, 0) scale(1); }
    35%  { transform: translate(260px, 130px) scale(1.16); }
    70%  { transform: translate(120px, 340px) scale(.88); }
    100% { transform: translate(430px, 220px) scale(1.08); }
}

@keyframes drift2 {
    0%   { transform: translate(0, 0) scale(1); }
    30%  { transform: translate(-230px, 100px) scale(1.13); }
    65%  { transform: translate(-330px, 330px) scale(.86); }
    100% { transform: translate(-80px, 450px) scale(1.12); }
}

@keyframes drift3 {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(-250px, -180px) scale(1.2); }
    100% { transform: translate(300px, -80px) scale(.9); }
}

@keyframes drift4 {
    0%   { transform: translate(-80px, -30px) scale(.8); }
    50%  { transform: translate(190px, 140px) scale(1.35); }
    100% { transform: translate(-150px, 250px) scale(.9); }
}

@keyframes ringMove {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to   { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes gridTravel {
    from { background-position: 0 0, 0 0; }
    to   { background-position: 0 64px, 64px 0; }
}

@keyframes energy1 {
    from { transform: translateX(-30vw) rotate(-12deg); }
    to   { transform: translateX(140vw) rotate(-12deg); }
}

@keyframes energy2 {
    from { transform: translateX(-40vw) rotate(9deg); }
    to   { transform: translateX(150vw) rotate(9deg); }
}

@keyframes scanDown {
    0%   { transform: translateY(-15vh); opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: .8; }
    100% { transform: translateY(115vh); opacity: 0; }
}

@keyframes particleFloat {
    0%   { transform: translate3d(0, 0, 0); opacity: .15; }
    25%  { opacity: .75; }
    50%  { transform: translate3d(35px, -75px, 0); opacity: .35; }
    75%  { opacity: .85; }
    100% { transform: translate3d(-25px, -145px, 0); opacity: .08; }
}

@keyframes pulseDot {
    0%,100% { transform: scale(.75); opacity: .65; }
    50% { transform: scale(1.25); opacity: 1; }
}

@keyframes heroRing {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# ANIMATED BACKGROUND HTML
# ------------------------------------------------------------

random.seed(42)

particles = []
for i in range(42):
    left = random.randint(2, 98)
    top = random.randint(4, 96)
    duration = random.randint(7, 18)
    delay = random.randint(-18, 0)
    cls = "particle"
    if i % 4 == 0:
        cls += " cyan"
    elif i % 7 == 0:
        cls += " purple"
    elif i % 3 == 0:
        cls += " small"
    particles.append(
        f'<span class="{cls}" style="left:{left}%;top:{top}%;--duration:{duration}s;--delay:{delay}s"></span>'
    )

st.markdown(
    '<div class="motion-bg">'
    '<div class="motion-orb orb-1"></div>'
    '<div class="motion-orb orb-2"></div>'
    '<div class="motion-orb orb-3"></div>'
    '<div class="motion-orb orb-4"></div>'
    '<div class="light-ring"></div>'
    '<div class="motion-grid"></div>'
    '<div class="energy-line energy-1"></div>'
    '<div class="energy-line energy-2"></div>'
    '<div class="scan"></div>'
    + "".join(particles)
    + "</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">◇</span><span class="brand-name">ComplaintIQ</span></div>'
        '<div class="brand-sub">Customer Complaint Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-label">ANALYSIS MODULES</div>', unsafe_allow_html=True)

    sentiment_on = st.checkbox("Sentiment Analysis", value=True)
    classification_on = st.checkbox("Complaint Classification", value=True)
    keywords_on = st.checkbox("Keyword Extraction", value=True)
    urgency_on = st.checkbox("Urgency Detection", value=True)
    intelligence_on = st.checkbox("AI Intelligence Layer", value=True)

    st.markdown('<div class="side-label">SYSTEM STACK</div>', unsafe_allow_html=True)

    stack = [
        ("Python", "Core application"),
        ("NLTK", "Text processing"),
        ("VADER", "Sentiment scoring"),
        ("Scikit-learn", "Classification"),
        ("Gemini", "AI intelligence layer"),
    ]

    for name, desc in stack:
        st.markdown(
            f'<div class="stack-card"><b>{name}</b> <span>· {desc}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="side-label">PROCESSING PIPELINE</div>', unsafe_allow_html=True)

    for item in ["Input", "NLP Processing", "Classification", "Sentiment", "Urgency", "Action Intelligence"]:
        st.markdown(
            f'<div style="font-size:11px;color:#9aa4bf;margin:9px 0;">'
            f'<span style="color:#5f7cff;margin-right:8px;">●</span>{item}</div>',
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------

st.markdown(
    '<section class="hero">'
    '<div class="eyebrow"><span class="live-dot"></span> AI-POWERED COMPLAINT ANALYTICS</div>'
    '<div class="hero-title">Understand every<br><span class="gradient">customer complaint.</span></div>'
    '<div class="hero-copy">ComplaintIQ transforms unstructured customer complaints into structured intelligence using natural language processing, sentiment analysis, machine learning classification and urgency detection.</div>'
    '<div class="status-row">'
    '<span class="status live">● NLP ENGINE ONLINE</span>'
    '<span class="status">VADER SENTIMENT</span>'
    '<span class="status">ML CLASSIFICATION</span>'
    '<span class="status">AI READY</span>'
    '</div>'
    '</section>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# INPUT
# ------------------------------------------------------------

st.markdown('<div class="section-title">Analyze a complaint</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Load a sample or paste a real customer complaint into the live analysis console.</div>',
    unsafe_allow_html=True,
)

# A pool of realistic sample complaints. Four are selected once per session.
sample_pool = [
    (
        "Delivery delay",
        "My order was supposed to arrive three days ago, but the tracking has not moved and nobody from support has replied."
    ),
    (
        "Unexpected charge",
        "I was charged an extra amount on my card that I do not recognize. Please explain the transaction and reverse it."
    ),
    (
        "Support experience",
        "I have contacted customer support four times and keep receiving automated replies without any actual solution."
    ),
    (
        "Damaged product",
        "The package arrived with the box badly damaged and the product inside is broken. I need a replacement."
    ),
    (
        "Refund pending",
        "I returned the product last week and was told my refund was processed, but the money is still missing from my account."
    ),
    (
        "Wrong item",
        "I ordered a black wireless headset but received a completely different model. Please arrange the correct item."
    ),
    (
        "Login problem",
        "I cannot log into my account after the password reset. The verification code works, but the site keeps rejecting the login."
    ),
    (
        "Service outage",
        "The service has been unavailable since this morning and I have already lost several hours of work because of it."
    ),
]

if "sample_set" not in st.session_state:
    st.session_state.sample_set = random.sample(sample_pool, 4)

if "complaint_text" not in st.session_state:
    st.session_state.complaint_text = ""

st.markdown(
    '<div class="complaint-workspace">'
    '<div class="workspace-kicker">'
    '<div class="workspace-title">Complaint analysis console</div>'
    '<div class="workspace-status">● SYSTEM READY</div>'
    '</div>'
    '<div class="sample-label">Try a sample complaint</div>'
    '</div>',
    unsafe_allow_html=True,
)

sample_cols = st.columns(4)

for idx, (col, (sample_type, sample_copy)) in enumerate(zip(sample_cols, st.session_state.sample_set)):
    with col:
        st.markdown(
            '<div class="sample-card">'
            f'<div class="sample-type">{html.escape(sample_type)}</div>'
            f'<div class="sample-copy">{html.escape(sample_copy)}</div>'
            '<div class="sample-action">',
            unsafe_allow_html=True,
        )
        if st.button("Load sample →", key=f"load_sample_{idx}", use_container_width=True):
            st.session_state.complaint_text = sample_copy
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)

complaint_text = st.text_area(
    "Customer complaint",
    value=st.session_state.complaint_text,
    height=200,
    placeholder="Paste the customer's complaint here…",
    help="ComplaintIQ will extract sentiment, category, urgency, keywords and recommended action.",
)

st.session_state.complaint_text = complaint_text

st.markdown('<div class="workspace-actions">', unsafe_allow_html=True)

action_cols = st.columns([5.2, 1.2], gap="small")

with action_cols[0]:
    st.markdown('<div class="analyze-wrap">', unsafe_allow_html=True)
    analyze_clicked = st.button("◈  ANALYZE COMPLAINT", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with action_cols[1]:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    clear_clicked = st.button("Clear", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------

if analyze_clicked:
    if not complaint_text.strip():
        st.warning("Please enter a customer complaint first.")
        st.stop()

    with st.spinner("Running complaint intelligence..."):
        result = analyze_complaint(complaint_text)

    sentiment = result.get("sentiment", {}) or {}
    classification = result.get("classification", {}) or {}
    urgency = result.get("urgency", {}) or {}
    keywords = result.get("keywords", []) or []

    sentiment_label = str(sentiment.get("label", "Unknown"))
    compound = float(sentiment.get("compound", 0) or 0)
    positive = float(sentiment.get("positive", 0) or 0)
    neutral = float(sentiment.get("neutral", 0) or 0)
    negative = float(sentiment.get("negative", 0) or 0)

    category = str(classification.get("category", "Unknown"))
    confidence = float(classification.get("confidence", 0) or 0)

    urgency_level = str(urgency.get("level", "Normal"))
    indicators = urgency.get("indicators", []) or []

    # Normalize confidence if analyzer returns 0–1
    confidence_pct = confidence * 100 if confidence <= 1 else confidence
    confidence_pct = max(0, min(100, confidence_pct))

    # --------------------------------------------------------
    # KPI STRIP
    # --------------------------------------------------------

    st.markdown('<div class="section-title">Complaint intelligence</div>', unsafe_allow_html=True)

    metric_cols = st.columns(4)

    metric_data = [
        ("SENTIMENT", sentiment_label, f"Compound score {compound:.2f}"),
        ("CATEGORY", category, f"{confidence_pct:.0f}% confidence"),
        ("URGENCY", urgency_level, f"{len(indicators)} signal(s) detected"),
        ("TOKENS", str(result.get("token_count", len(result.get("tokens", []) or []))), "Processed text units"),
    ]

    for col, (label, value, detail) in zip(metric_cols, metric_data):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">{html.escape(label)}</div>'
                f'<div class="metric-value">{html.escape(value)}</div>'
                f'<div class="metric-detail">{html.escape(detail)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.write("")

    # --------------------------------------------------------
    # SENTIMENT + CLASSIFICATION
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:
        sentiment_class = sentiment_label.lower()

        if sentiment_class == "positive":
            sentiment_display = "Positive"
            sentiment_symbol = "↑"
        elif sentiment_class == "negative":
            sentiment_display = "Negative"
            sentiment_symbol = "↓"
        else:
            sentiment_display = sentiment_label
            sentiment_symbol = "•"

        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-title">SENTIMENT ANALYSIS</div>'
            f'<div class="big-result">{sentiment_symbol} {html.escape(sentiment_display)}</div>'
            f'<div class="result-muted">VADER compound score: {compound:.3f}</div>'
            f'<div class="bar"><div class="bar-fill" style="width:{max(4, min(100, abs(compound)*100))}%"></div></div>'
            f'<div style="display:flex;justify-content:space-between;margin-top:14px;color:#697591;font-size:10px;">'
            f'<span>Positive {positive:.0%}</span>'
            f'<span>Neutral {neutral:.0%}</span>'
            f'<span>Negative {negative:.0%}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-title">COMPLAINT CLASSIFICATION</div>'
            f'<div class="big-result">{html.escape(category)}</div>'
            f'<div class="result-muted">Model confidence: {confidence_pct:.1f}%</div>'
            f'<div class="bar"><div class="bar-fill" style="width:{confidence_pct:.0f}%"></div></div>'
            f'<div style="margin-top:16px;color:#78839e;font-size:10px;">Classification scores</div>',
            unsafe_allow_html=True,
        )

        scores = classification.get("scores", {}) or {}

        if scores:
            score_items = sorted(
                scores.items(),
                key=lambda x: float(x[1] or 0),
                reverse=True,
            )[:4]

            for score_name, score_value in score_items:
                try:
                    pct = float(score_value) * 100 if float(score_value) <= 1 else float(score_value)
                except Exception:
                    pct = 0

                pct = max(0, min(100, pct))

                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;color:#8993ad;font-size:10px;margin-top:9px;">'
                    f'<span>{html.escape(str(score_name))}</span>'
                    f'<span>{pct:.1f}%</span>'
                    f'</div>'
                    f'<div class="bar" style="height:4px;margin-top:4px;">'
                    f'<div class="bar-fill" style="width:{pct:.0f}%"></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # KEYWORDS + URGENCY
    # --------------------------------------------------------

    st.write("")
    left, right = st.columns(2)

    with left:
        tags_html = ""

        if keywords:
            for word in keywords[:15]:
                tags_html += f'<span class="tag">{html.escape(str(word))}</span>'
        else:
            tags_html = '<span class="result-muted">No keywords extracted.</span>'

        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-title">KEY SIGNALS & KEYWORDS</div>'
            f'<div>{tags_html}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with right:
        urgency_color = "#ff6b7a" if urgency_level.lower() in {"high", "critical", "urgent"} else "#55e7a4"

        indicator_html = ""

        if indicators:
            for item in indicators[:8]:
                indicator_html += (
                    f'<div style="color:#a0aac1;font-size:11px;margin-top:9px;">'
                    f'<span style="color:{urgency_color};margin-right:7px;">●</span>'
                    f'{html.escape(str(item))}'
                    f'</div>'
                )
        else:
            indicator_html = '<div class="result-muted">No explicit urgency indicators detected.</div>'

        st.markdown(
            f'<div class="result-card">'
            f'<div class="result-title">URGENCY DETECTION</div>'
            f'<div class="big-result" style="color:{urgency_color};">{html.escape(urgency_level)}</div>'
            f'<div class="result-muted">Signals detected from complaint language</div>'
            f'{indicator_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # ACTION INTELLIGENCE
    # --------------------------------------------------------

    urgency_lower = urgency_level.lower()
    sentiment_lower = sentiment_label.lower()
    category_lower = category.lower()

    if urgency_lower in {"critical", "urgent", "high"}:
        action_title = "Escalate this complaint immediately"
        action_copy = (
            "The complaint contains strong urgency signals. Route it to a priority support queue, "
            "assign an owner and provide a clear response timeline to the customer."
        )
    elif sentiment_lower == "negative":
        action_title = "Prioritize recovery and resolution"
        action_copy = (
            "The customer is expressing dissatisfaction. Focus on acknowledging the issue, "
            "providing a concrete next step and reducing the effort required from the customer."
        )
    elif "billing" in category_lower or "payment" in category_lower:
        action_title = "Verify the transaction and close the loop"
        action_copy = (
            "Check the payment or billing record, confirm the exact discrepancy and communicate "
            "the expected resolution or refund timeline."
        )
    else:
        action_title = "Assign an owner and resolve the root issue"
        action_copy = (
            "Use the detected category and sentiment to route the complaint to the appropriate "
            "team, then respond with a specific resolution rather than a generic acknowledgement."
        )

    st.write("")
    st.markdown(
        f'<div class="action-panel">'
        f'<div class="action-kicker">ACTION INTELLIGENCE</div>'
        f'<div class="action-title">{html.escape(action_title)}</div>'
        f'<div class="action-copy">{html.escape(action_copy)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # AI INTELLIGENCE LAYER
    # --------------------------------------------------------

    if intelligence_on:
        st.markdown('<div class="section-title">AI intelligence layer</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-sub">A structured interpretation of the signals extracted from this complaint.</div>',
            unsafe_allow_html=True,
        )

        insight_points = []

        if sentiment_lower == "negative":
            insight_points.append("Customer emotion is negative, so the response should acknowledge the problem before moving to resolution.")
        elif sentiment_lower == "positive":
            insight_points.append("The complaint contains comparatively positive language despite the reported issue.")
        else:
            insight_points.append("The emotional signal is relatively neutral, suggesting the response can stay concise and solution-focused.")

        if urgency_lower in {"critical", "urgent", "high"}:
            insight_points.append("Urgency indicators suggest the complaint should be prioritized instead of entering a standard queue.")
        else:
            insight_points.append("No strong critical urgency pattern was detected, so normal service prioritization may be appropriate.")

        insight_points.append(
            f"The classifier maps the complaint to '{category}', providing a starting point for routing it to the relevant team."
        )

        insight_html = "".join(
            f'<div style="display:flex;gap:12px;margin:13px 0;color:#9ba5bd;font-size:12px;line-height:1.55;">'
            f'<span style="color:#5e86ff;font-size:9px;padding-top:5px;">◆</span>'
            f'<span>{html.escape(point)}</span>'
            f'</div>'
            for point in insight_points
        )

        st.markdown(
            f'<div class="result-card" style="min-height:0;">'
            f'<div class="result-title">COMPLAINTIQ INTERPRETATION</div>'
            f'{insight_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.markdown('<div class="section-title">Processing pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">How the complaint moves through the intelligence system.</div>',
        unsafe_allow_html=True,
    )

    pipeline = [
        ("01", "Input", "Raw complaint"),
        ("02", "NLP", "Clean + tokenize"),
        ("03", "Sentiment", "VADER scoring"),
        ("04", "ML", "Issue category"),
        ("05", "Urgency", "Priority signals"),
        ("06", "Action", "Recommended next step"),
    ]

    pipe_html = '<div class="pipeline">'

    for i, (_, title, desc) in enumerate(pipeline):
        pipe_html += (
            f'<div class="pipe-node">'
            f'<strong>{html.escape(title)}</strong>'
            f'<span>{html.escape(desc)}</span>'
            f'</div>'
        )
        if i < len(pipeline) - 1:
            pipe_html += '<div class="pipe-arrow">→</div>'

    pipe_html += "</div>"

    st.markdown(pipe_html, unsafe_allow_html=True)

    # --------------------------------------------------------
    # RAW NLP DATA
    # --------------------------------------------------------

    with st.expander("View NLP processing details"):
        original = result.get("original_text", complaint_text)
        cleaned = result.get("cleaned_text", "")
        tokens = result.get("tokens", [])

        st.write("**Original complaint**")
        st.code(str(original))

        st.write("**Cleaned text**")
        st.code(str(cleaned))

        st.write("**Tokens**")
        st.write(tokens)

else:
    # --------------------------------------------------------
    # EMPTY STATE / LANDING PREVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div style="margin-top:28px;border:1px solid rgba(108,133,255,.13);'
        'border-radius:18px;padding:22px;background:rgba(8,13,28,.58);">'
        '<div style="color:#727e9b;font-size:11px;">SYSTEM STATUS</div>'
        '<div style="color:#dfe5fb;font-size:16px;font-weight:800;margin-top:7px;">Ready for complaint analysis</div>'
        '<div style="color:#68738f;font-size:11px;margin-top:6px;">'
        'Enter a complaint above and run the intelligence pipeline to generate structured insights.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.markdown(
    '<div class="footer">COMPLAINTIQ · CUSTOMER COMPLAINT INTELLIGENCE · NLP + ML + AI</div>',
    unsafe_allow_html=True,
)
