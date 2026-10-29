import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Vertex Precision Engineering — AI Assistant",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>
/* ── Page background: light ── */
.stApp { background-color: #EAF2FB; }
section[data-testid="stSidebar"] { display: none; }

/* ── Body text: dark navy on the light page ── */
body, p, div, span, li, td, th, label { color: #16314F; }
.stMarkdown p, .stMarkdown li { color: #16314F; font-size: 1.1rem !important; line-height: 1.7; }
h2, h3    { color: #0D47A1; }
strong, b { color: #0D47A1; }

/* ── Banner ── */
.vx-banner {
    background: linear-gradient(90deg, #0D47A1, #1565C0, #0D47A1);
    border-radius: 14px;
    padding: 22px 28px 20px 28px;
    margin-bottom: 20px;
    border-left: 6px solid #FFB300;
}
.vx-banner-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #FFFFFF !important;
    margin: 0 0 8px 0;
    line-height: 1.25;
}
.vx-banner p {
    font-size: 1.15rem !important;
    color: #E3F2FD !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* ── Subtitle (caption) ── */
.stCaption, .stCaption p { color: #4A6D94 !important; font-size: 1.05rem !important; }

/* ── "Ask me about" line ── */
.ask-line { font-size: 1.15rem !important; color: #16314F !important; margin-bottom: 14px; }
.ask-line strong { color: #0D47A1 !important; }

/* ── Chat bubbles ── */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
}
[data-testid="stChatMessage"][data-message-author-role="user"] {
    background-color: #DBEAFE !important;
    border: 1px solid #93C5FD !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"][data-message-author-role="user"] p,
[data-testid="stChatMessage"][data-message-author-role="user"] * {
    color: #16314F !important;
}
[data-testid="stChatMessage"][data-message-author-role="assistant"] {
    background-color: #F1F5F9 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 14px 20px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"][data-message-author-role="assistant"] p,
[data-testid="stChatMessage"][data-message-author-role="assistant"] * {
    color: #16314F !important;
}

/* ── Writing (input) box ── */
[data-testid="stChatInput"] textarea {
    font-size: 1.1rem   !important;
    min-height: 72px    !important;
    padding: 18px 24px  !important;
    background-color: #FFFFFF !important;
    color: #16314F       !important;
    border: 2px solid #90CAF9 !important;
    border-radius: 12px  !important;
    width: 100%          !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #7C96B5 !important; }
[data-testid="stChatInput"] button { background-color: #1E88E5 !important; border-radius: 8px !important; }

/* ── Divider ── */
hr { border-color: rgba(13,71,161,0.18) !important; }

/* ── Spinner ── */
.stSpinner > div { color: #1565C0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Left/right panels: problem / solution / sample questions, and how it works + price ──
SAMPLE_QUESTIONS = [
    "What materials do you work with?",
    "Track order VPE-1003",
    "Do you hold ISO 9001 or AS9100 certification?",
]


def _ask_sample(question):
    st.session_state.messages.append({"role": "user", "content": question})


PANEL_CSS = """
<style>
.st-key-vx_left, .st-key-vx_right {
    background: #FFFFFF;
    border: 1px solid #90CAF9;
    border-top: 5px solid #FFB300;
    border-radius: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.18);
    padding: 20px 20px 22px 20px;
}
.st-key-vx_left [data-testid="stMarkdownContainer"],
.st-key-vx_right [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }

.st-key-vx_left p, .st-key-vx_right li, .st-key-vx_right .vx-invest {
    font-size: 19px !important;
    line-height: 1.5 !important;
    color: #1a1a1a !important;
}
.st-key-vx_left p { margin: 0 0 14px 0 !important; }
.st-key-vx_left b, .st-key-vx_right b { color: #0D47A1 !important; font-weight: 800 !important; }
.st-key-vx_left p.vx-try { font-size: 20px !important; margin: 6px 0 0 0 !important; }
.st-key-vx_right .vx-title {
    font-size: 23px !important;
    font-weight: 800 !important;
    line-height: 1.3 !important;
    color: #0D47A1 !important;
    margin-bottom: 14px !important;
}
.st-key-vx_right ol { margin: 0 0 18px 0; padding-left: 1.3em; }
.st-key-vx_right li { margin-bottom: 10px; }
.st-key-vx_right .vx-invest {
    background: #E3F2FD;
    border-left: 5px solid #FFB300;
    border-radius: 8px;
    padding: 12px 14px;
}

.st-key-vx_left .stElementContainer, .st-key-vx_left .stButton { width: 100% !important; }
.st-key-vx_left .stButton > button {
    width: 100% !important;
    height: auto;
    min-height: 0;
    background: #FFFFFF !important;
    color: #0D47A1 !important;
    border: 1.5px solid #1E88E5 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}
.st-key-vx_left .stButton > button * { justify-content: flex-start !important; text-align: left !important; }
.st-key-vx_left .stButton > button p {
    font-size: 18px !important;
    font-weight: 600 !important;
    line-height: 1.4 !important;
    margin: 0 !important;
    color: #0D47A1 !important;
}
.st-key-vx_left .stButton > button:hover {
    background: #0D47A1 !important;
    color: #FFB300 !important;
    border-color: #0D47A1 !important;
}
.st-key-vx_left .stButton > button:hover p,
.st-key-vx_left .stButton > button:focus p,
.st-key-vx_left .stButton > button:active p {
    color: #FFB300 !important;
}

.st-key-vx_chat {
    background: #FFFFFF !important;
    border: 1px solid #90CAF9 !important;
    border-top: 5px solid #FFB300 !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    min-height: 200px;
    box-shadow: 0 2px 12px rgba(13,71,161,0.12);
}
</style>
"""

# ── SVG Mechanical Components ─────────────────────────────────────────────────

GEAR_BIG = """<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="44" y="2"  width="12" height="18" rx="3" fill="#BBDEFB"/>
  <rect x="44" y="80" width="12" height="18" rx="3" fill="#BBDEFB"/>
  <rect x="2"  y="44" width="18" height="12" rx="3" fill="#BBDEFB"/>
  <rect x="80" y="44" width="18" height="12" rx="3" fill="#BBDEFB"/>
  <rect x="14" y="8"  width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(45 20 17)"/>
  <rect x="74" y="8"  width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(-45 80 17)"/>
  <rect x="14" y="74" width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(-45 20 83)"/>
  <rect x="74" y="74" width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(45 80 83)"/>
  <circle cx="50" cy="50" r="30" fill="#1E88E5" stroke="#90CAF9" stroke-width="2"/>
  <circle cx="50" cy="50" r="12" fill="#0D47A1" stroke="#90CAF9" stroke-width="2"/>
  <line x1="50" y1="38" x2="50" y2="62" stroke="#90CAF9" stroke-width="3.5"/>
  <line x1="38" y1="50" x2="62" y2="50" stroke="#90CAF9" stroke-width="3.5"/>
  <line x1="41" y1="41" x2="59" y2="59" stroke="#64B5F6" stroke-width="2"/>
  <line x1="59" y1="41" x2="41" y2="59" stroke="#64B5F6" stroke-width="2"/>
</svg>"""

GEAR_SMALL = """<svg width="72" height="72" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="44" y="2"  width="12" height="18" rx="3" fill="#BBDEFB"/>
  <rect x="44" y="80" width="12" height="18" rx="3" fill="#BBDEFB"/>
  <rect x="2"  y="44" width="18" height="12" rx="3" fill="#BBDEFB"/>
  <rect x="80" y="44" width="18" height="12" rx="3" fill="#BBDEFB"/>
  <rect x="14" y="8"  width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(45 20 17)"/>
  <rect x="74" y="8"  width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(-45 80 17)"/>
  <rect x="14" y="74" width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(-45 20 83)"/>
  <rect x="74" y="74" width="12" height="18" rx="3" fill="#BBDEFB" transform="rotate(45 80 83)"/>
  <circle cx="50" cy="50" r="30" fill="#1565C0" stroke="#64B5F6" stroke-width="2"/>
  <circle cx="50" cy="50" r="11" fill="#0D47A1" stroke="#64B5F6" stroke-width="2"/>
  <line x1="50" y1="39" x2="50" y2="61" stroke="#64B5F6" stroke-width="3"/>
  <line x1="39" y1="50" x2="61" y2="50" stroke="#64B5F6" stroke-width="3"/>
</svg>"""

BEARING = """<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="46" fill="none" stroke="#BBDEFB" stroke-width="8"/>
  <circle cx="50" cy="50" r="22" fill="none" stroke="#BBDEFB" stroke-width="7"/>
  <circle cx="50" cy="50" r="34" fill="none" stroke="#64B5F6" stroke-width="1.2" stroke-dasharray="6 4"/>
  <circle cx="50" cy="11"  r="7.5" fill="#90CAF9"/>
  <circle cx="83" cy="27"  r="7.5" fill="#90CAF9"/>
  <circle cx="83" cy="73"  r="7.5" fill="#90CAF9"/>
  <circle cx="50" cy="89"  r="7.5" fill="#90CAF9"/>
  <circle cx="17" cy="73"  r="7.5" fill="#90CAF9"/>
  <circle cx="17" cy="27"  r="7.5" fill="#90CAF9"/>
  <circle cx="50" cy="50"  r="15" fill="#0D47A1" stroke="#64B5F6" stroke-width="2"/>
  <circle cx="50" cy="50"  r="5"  fill="#BBDEFB"/>
</svg>"""

BOLT = """<svg width="56" height="110" viewBox="0 0 60 115" xmlns="http://www.w3.org/2000/svg">
  <polygon points="30,4 56,19 56,49 30,64 4,49 4,19" fill="#1E88E5" stroke="#90CAF9" stroke-width="2"/>
  <polygon points="30,14 49,25 49,43 30,54 11,43 11,25" fill="#0D47A1" stroke="#64B5F6" stroke-width="1.5"/>
  <rect x="24" y="63" width="12" height="50" rx="3" fill="#BBDEFB" stroke="#90CAF9" stroke-width="1.5"/>
  <line x1="24" y1="72"  x2="36" y2="72"  stroke="#64B5F6" stroke-width="1.2"/>
  <line x1="24" y1="79"  x2="36" y2="79"  stroke="#64B5F6" stroke-width="1.2"/>
  <line x1="24" y1="86"  x2="36" y2="86"  stroke="#64B5F6" stroke-width="1.2"/>
  <line x1="24" y1="93"  x2="36" y2="93"  stroke="#64B5F6" stroke-width="1.2"/>
  <line x1="24" y1="100" x2="36" y2="100" stroke="#64B5F6" stroke-width="1.2"/>
  <line x1="24" y1="107" x2="36" y2="107" stroke="#64B5F6" stroke-width="1.2"/>
</svg>"""

ROTOR = """<svg width="96" height="96" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="50" cy="22" rx="9" ry="24" fill="#1E88E5" stroke="#90CAF9" stroke-width="1.5"/>
  <ellipse cx="50" cy="22" rx="9" ry="24" fill="#1E88E5" stroke="#90CAF9" stroke-width="1.5" transform="rotate(120 50 50)"/>
  <ellipse cx="50" cy="22" rx="9" ry="24" fill="#1E88E5" stroke="#90CAF9" stroke-width="1.5" transform="rotate(240 50 50)"/>
  <circle cx="50" cy="50" r="16" fill="#0D47A1" stroke="#90CAF9" stroke-width="2.5"/>
  <circle cx="50" cy="50" r="7"  fill="#BBDEFB" stroke="#64B5F6" stroke-width="1.5"/>
</svg>"""

SHAFT = """<svg width="44" height="110" viewBox="0 0 44 110" xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="0" width="16" height="110" rx="4" fill="#1E88E5" stroke="#90CAF9" stroke-width="1.5"/>
  <rect x="6"  y="10" width="32" height="12" rx="3" fill="#BBDEFB" stroke="#90CAF9" stroke-width="1.2"/>
  <rect x="6"  y="88" width="32" height="12" rx="3" fill="#BBDEFB" stroke="#90CAF9" stroke-width="1.2"/>
  <line x1="14" y1="35" x2="30" y2="35" stroke="#64B5F6" stroke-width="1"/>
  <line x1="14" y1="42" x2="30" y2="42" stroke="#64B5F6" stroke-width="1"/>
  <line x1="14" y1="55" x2="30" y2="55" stroke="#64B5F6" stroke-width="1"/>
  <line x1="14" y1="62" x2="30" y2="62" stroke="#64B5F6" stroke-width="1"/>
</svg>"""

def side_col(items):
    html = '<div class="gear-col">'
    for svg, label in items:
        html += svg
        html += f'<div class="gear-label">{label}</div>'
    html += '</div>'
    return html

# ── Initialise session state ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── STEP 1: If last message is unanswered user message → get reply FIRST ──────
#    This runs BEFORE any rendering so the answer is ready when we draw the chat
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Checking knowledge base..."):
        reply = run_agent(st.session_state.messages[-1]["content"])
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ── STEP 2: Page layout ───────────────────────────────────────────────────────
left, main, right = st.columns([1.2, 2.6, 1.2])

with left:
    with st.container(key="vx_left"):
        st.markdown(
            PANEL_CSS
            + "<p><b>The Problem:</b> Machine shops get dozens of calls a week asking about materials, lead times and order status.</p>"
            "<p><b>The Solution:</b> This AI agent answers customer questions instantly from real product data and order records, 24/7.</p>"
            "<p><b>Result:</b> Cuts repetitive support time by 60-80%. Try it in the chat with sample data.</p>"
            '<p class="vx-try"><b>Try asking:</b></p>',
            unsafe_allow_html=True,
        )
        for i, q in enumerate(SAMPLE_QUESTIONS):
            st.button(q, key=f"vx_sample_{i}", on_click=_ask_sample, args=(q,))

with right:
    with st.container(key="vx_right"):
        st.markdown(
            '<div class="vx-title">What This Would Look Like For Your Business</div>'
            "<ol>"
            "<li>You send me your product range, pricing, and FAQs</li>"
            "<li>I build and train the AI on YOUR specific content (3-4 days)</li>"
            "<li>I deploy it to your website, WhatsApp, or email</li>"
            "<li>Your customers get instant, accurate answers 24/7</li>"
            "</ol>"
            '<div class="vx-invest"><b>Investment:</b> Starting at <b>$99</b> for a basic setup. Includes 30 days of free support.</div>',
            unsafe_allow_html=True,
        )
with main:
    st.markdown(
        '<div class="vx-banner"><div class="vx-banner-title">⚙️ Vertex Precision Engineering Ltd</div>'
        '<p>CNC Machining &amp; Mechanical Components — West Midlands, UK</p></div>',
    unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="ask-line"><strong>Ask me about:</strong> products, materials, lead times, pricing, capabilities, certifications, or track your order.</p>',
        unsafe_allow_html=True
    )

    # ── STEP 3: Render all messages inside white box (ABOVE the input) ──────
    with st.container(border=True, key="vx_chat"):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ── STEP 4: Input box at the BOTTOM ──────────────────────────────────────
    user_input = st.chat_input("e.g. What materials do you work with? / Track order VPE-1003")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()   # → goes back to STEP 1, gets reply, then redraws everything

    st.markdown("---")
    st.caption("📍 Vertex Precision Engineering Ltd · West Midlands, UK ")