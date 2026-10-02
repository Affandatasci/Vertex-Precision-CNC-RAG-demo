import streamlit as st
from agent import run_agent
from markdown import markdown as to_html

st.set_page_config(
    page_title="Vertex Precision Engineering — AI Assistant",
    page_icon="⚙️",
    layout="wide"
)

st.markdown("""
<style>
/* ── Background ── */
.stApp { background-color: #1455A4; }
section[data-testid="stSidebar"] { display: none; }

/* ── ALL text outside the chat box → white ── */
body, p, div, span, li, td, th, label          { color: #FFFFFF !important; }
.stMarkdown p, .stMarkdown li                   { color: #FFFFFF !important; font-size: 1.2rem !important; line-height: 1.7; }
h1                                              { color: #FFFFFF !important; font-size: 2.6rem !important; }
h2, h3                                          { color: #E3F2FD !important; }
strong, b                                       { color: #FFFFFF !important; }

/* ── Subtitle ── */
.stCaption, .stCaption p { color: #E3F2FD !important; font-size: 1.5rem !important; }

/* ── "Ask me about" line ── */
.ask-line { font-size: 1.5rem !important; color: #FFFFFF !important; margin-bottom: 14px; }
.ask-line strong { font-size: 1.5rem !important; color: #FFFFFF !important; }

/* ── WHITE CHAT BOX ── */
.chat-box {
    background-color: #FFFFFF;
    border: 2px solid #1455A4;
    border-radius: 14px;
    padding: 20px 24px;
    min-height: 200px;
    margin-bottom: 16px;
}

/* ── Dark text INSIDE the white box ── */
.chat-box p, .chat-box li, .chat-box ul, .chat-box ol,
.chat-box div, .chat-box span {
    color: #1a1a1a !important;
    font-size: 1.1rem !important;
    line-height: 1.7;
}
.chat-box strong, .chat-box b { color: #1a1a1a !important; }

/* ── Message bubbles ── */
.msg-user {
    background-color: #DBEAFE;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 14px;
}
.msg-bot {
    background-color: #F1F5F9;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 14px;
}
.msg-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 6px;
}
.msg-user .msg-label { color: #1D4ED8 !important; }
.msg-bot  .msg-label { color: #475569 !important; }
.chat-placeholder { color: #94A3B8 !important; text-align: center; padding: 40px 0; font-size: 1rem !important; }

/* ── Writing (input) box ── */
[data-testid="stChatInput"] textarea {
    font-size: 1.2rem   !important;
    min-height: 72px    !important;
    padding: 18px 24px  !important;
    background-color: rgba(10,40,110,0.75) !important;
    color: #FFFFFF       !important;
    border: 2px solid #64B5F6 !important;
    border-radius: 12px  !important;
    width: 100%          !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #90CAF9 !important; }
[data-testid="stChatInput"] button { background-color: #1E88E5 !important; border-radius: 8px !important; }

/* ── Divider ── */
hr { border-color: rgba(144,202,249,0.4) !important; }

/* ── Spinner ── */
.stSpinner > div { color: #90CAF9 !important; }

/* ── Gear column ── */
.gear-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 26px;
    padding-top: 64px;
}
.gear-label {
    color: #90CAF9 !important;
    font-size: 0.75rem;
    font-family: monospace;
    text-align: center;
    margin-top: -16px;
    opacity: 0.85;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)

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
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Checking knowledge base..."):
        reply = run_agent(st.session_state.messages[-1]["content"])
    st.session_state.messages.append({"role": "assistant", "content": reply})

# ── STEP 2: Page layout ───────────────────────────────────────────────────────
left, main, right = st.columns([0.6, 6, 0.6])

with left:
    st.markdown(side_col([
        (GEAR_BIG,  "SPUR GEAR"),
        (BEARING,   "BALL BEARING"),
        (BOLT,      "HEX BOLT"),
    ]), unsafe_allow_html=True)

with right:
    st.markdown(side_col([
        (ROTOR,     "PUMP ROTOR"),
        (GEAR_SMALL,"HELICAL GEAR"),
        (SHAFT,     "CNC SHAFT"),
    ]), unsafe_allow_html=True)

with main:
    st.title("⚙️ Vertex Precision Engineering Ltd")
    st.caption("CNC Machining & Mechanical Components — West Midlands, UK")
    st.markdown("---")
    st.markdown(
        '<p class="ask-line"><strong>Ask me about:</strong> products, materials, lead times, pricing, capabilities, certifications, or track your order.</p>',
        unsafe_allow_html=True
    )

    # ── STEP 3: Render all messages inside a WHITE HTML box ───────────────────
    chat_html = '<div class="chat-box">'
    if st.session_state.messages:
        for msg in st.session_state.messages:
            content_html = to_html(msg["content"])
            if msg["role"] == "user":
                chat_html += (
                    f'<div class="msg-user">'
                    f'<span class="msg-label">You</span>'
                    f'{content_html}</div>'
                )
            else:
                chat_html += (
                    f'<div class="msg-bot">'
                    f'<span class="msg-label">Assistant</span>'
                    f'{content_html}</div>'
                )
    else:
        chat_html += '<p class="chat-placeholder">Ask a question to get started...</p>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── STEP 4: Input box at the BOTTOM ──────────────────────────────────────
    user_input = st.chat_input("e.g. What materials do you work with? / Track order VPE-1003")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    st.markdown("---")
    st.caption("📍 Vertex Precision Engineering Ltd · West Midlands, UK · enquiries@vertexprecision.co.uk · +44 121 456 7890")
