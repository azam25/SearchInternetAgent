# app.py — SearchInternetAgent Chat (clean status)
# - Robust presentation-mode parsing (JSON or "JSON-ish" in code fences)
# - Source pill inline at the end of each section
# - Title big; user message normal size; DO NOT change source pill size

import streamlit as st
import json, re, sys, os, time
from datetime import datetime
from urllib.parse import urlparse

# ── Page config FIRST
st.set_page_config(
    page_title="SearchInternetAgent - AI-Powered Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit header and menu (kept from your version)
st.markdown("""
<script>
    window.addEventListener('load', function() {
        const header = document.querySelector('header');
        if (header) header.style.display = 'none';
        const deployBtn = document.querySelector('[data-testid="stDeployButton"]');
        if (deployBtn) deployBtn.style.display = 'none';
        const menuBtn = document.querySelector('[data-testid="stMainMenu"]');
        if (menuBtn) menuBtn.style.display = 'none';
    });
</script>
""", unsafe_allow_html=True)

# ── Import your agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from SearchInternetAgent import SearchAgent
except Exception as e:
    st.error(f"❌ Could not import `SearchInternetAgent`: {e}")
    st.stop()

# ── Global CSS (keeps title big, user normal, assistant compact; chip unchanged)
st.markdown("""
<style>
:root{
  --scale: 0.85; /* used only for assistant text compactness */
  --primary:#1a1a1a; --bg:#ffffff; --muted:#f6f7f9; --border:#e4e7ec;
  --accent:#0b75c9; --text:#1a1a1a; --sub:#666;
}
/* Header */
.header{
  background:linear-gradient(135deg,var(--primary),#2d2d2d);
  padding:26px 0;
  margin:-16px -16px 12px -16px;
  border-radius:0 0 16px 16px;
  box-shadow:0 4px 14px rgba(0,0,0,.15)
}
.header h1{
  color:#fff; text-align:center; margin:0;
  font-size:2.3rem; font-weight:700;  /* BIG title */
}
.header p{
  color:#c9c9c9; text-align:center; margin:.3rem 0 0;
  font-size:1.05rem;
}
/* Chat container & messages */
.chat{background:var(--bg); border:1px solid var(--border); border-radius:12px; padding:10px 12px;
  box-shadow:0 3px 12px rgba(0,0,0,.06)}
.msg{margin:8px 0; padding:10px 12px; border-radius:10px; border:1px solid var(--border)}
.user{
  background:linear-gradient(135deg,var(--accent),#005a8b);
  color:#fff; margin-left:12%;
  font-size:1rem; line-height:1.5;
}
.assistant{
  background:var(--muted); color:var(--text); margin-right:12%;
  font-size:calc(.95rem*var(--scale)); line-height:1.5
}
.assistant h1,.assistant h2,.assistant h3,.assistant h4{color:var(--accent); margin:.45rem 0 .25rem}
.assistant h1{font-size:calc(1.25rem*var(--scale))}
.assistant h2{font-size:calc(1.12rem*var(--scale))}
.assistant h3{font-size:calc(1.05rem*var(--scale))}
.assistant p{margin:.25rem 0}
.assistant ul,.assistant ol{margin:.25rem 0 .35rem .95rem}
.assistant li{margin:.12rem 0}
.assistant code{background:#eef3f7; padding:1px 5px; border-radius:4px; font-size:calc(.88rem*var(--scale))}
.assistant pre{background:#eef3f7; border:1px solid var(--border); padding:10px; border-radius:8px; overflow:auto}

/* ChatGPT-like blue source chip — KEEPING current size exactly */
.src-chip{
  display:inline-flex; align-items:center; gap:6px;
  padding:4px 9px; border-radius:999px; font-size:.78rem; line-height:1;
  text-decoration:none; border:1px solid #cfe7fa; background:#e9f4fd; color:#0b75c9;
  transition:all .15s ease-in-out; vertical-align:baseline;
}
.src-chip:hover{filter:brightness(.97); border-color:#b7ddfa}
.src-chip .src-dot{width:6px; height:6px; border-radius:999px; background:#0b75c9; opacity:.85}
.src-chip-count{background:#eef1f4;border:1px solid #e3e7ec;color:#4a5568}

/* Inline placement at end of paragraph */
.src-after{ display:inline-block; margin-left:.5rem; }
.clear{clear:both}
footer{visibility:hidden}

/* Hide Streamlit's default header and deploy button */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
.stApp > header {display: none;}

/* Additional space optimization */
.block-container { padding-top: 1rem; padding-bottom: 1rem; }
.main .block-container { padding-top: .5rem; padding-bottom: .5rem; }

/* Hide additional Streamlit UI elements */
.stApp > div[data-testid="stToolbar"] {display: none;}
.stApp > div[data-testid="stDecoration"] {display: none;}
.stApp > div[data-testid="stStatusWidget"] {display: none;}

/* Maximize content area */
.stApp { padding-top: 0; padding-bottom: 0; }

/* Optimize sidebar spacing */
.sidebar .sidebar-content { padding-top: .5rem; }

/* ── Minimal, single-line status with animated dots */
.status-bar{
  display:flex; align-items:center; gap:.6rem;
  padding:.6rem .9rem; border:1px solid var(--border);
  border-radius:10px; background:var(--muted);
  font-weight:600; color:#0b75c9;
  box-shadow:0 2px 8px rgba(0,0,0,.04);
}
.status-bar .spinner{
  width:14px; height:14px; border-radius:50%;
  border:2px solid #b7ddfa; border-top-color:#0b75c9;
  animation:spin 1s linear infinite;
}
@keyframes spin {to{transform:rotate(360deg)}}
/* animated ellipsis: 0→3 dots repeatedly */
.status-bar .dots{
  display:inline-block; overflow:hidden; width:0ch;
  animation:ellipsis 1s steps(4, end) infinite;
}
@keyframes ellipsis { from { width:0ch } to { width:3ch } }
</style>
""", unsafe_allow_html=True)

# ── State
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "mode" not in st.session_state: st.session_state.mode = "precise"
if "debug_mode" not in st.session_state: st.session_state.debug_mode = False
if "response_cache" not in st.session_state: st.session_state.response_cache = {}

# ── Helpers (robust parsing)
CODE_BLOCK_JSON = re.compile(r"```json\s*([\s\S]*?)\s*```", re.IGNORECASE)
CODE_BLOCK_ANY  = re.compile(r"```\s*([\s\S]*?)\s*```")

def extract_code_blocks(md: str):
    blocks = CODE_BLOCK_JSON.findall(md) or []
    generic = CODE_BLOCK_ANY.findall(md) or []
    for g in generic:
        if g not in blocks:
            blocks.append(g)
    return blocks

def try_strict_json_parse(block: str):
    out = []
    try:
        data = json.loads(block)
        if isinstance(data, dict):
            if "text" in data and (("source" in data and "url" in data) or "sources" in data):
                out.append(data)
            elif "slides" in data and isinstance(data["slides"], list):
                for s in data["slides"]:
                    if "text" in s: out.append(s)
        elif isinstance(data, list):
            for s in data:
                if isinstance(s, dict) and "text" in s:
                    out.append(s)
    except Exception:
        return []
    return out

TEXT_FIELD_RE   = re.compile(r'\btext\s*:\s*"(.*?)"', re.DOTALL)
SOURCE_FIELD_RE = re.compile(r'\bsource\s*:\s*"(.*?)"', re.DOTALL|re.IGNORECASE)
URL_FIELD_RE    = re.compile(r'\burl\s*:\s*"(.*?)"', re.DOTALL|re.IGNORECASE)

def try_lenient_slide_extract(block: str):
    chunks = re.split(r'\}\s*,\s*\{', block.strip().strip('`'))
    sections = []
    for raw in chunks:
        text_m = TEXT_FIELD_RE.search(raw)
        if not text_m: continue
        text = text_m.group(1).strip()
        src_m = SOURCE_FIELD_RE.search(raw)
        url_m = URL_FIELD_RE.search(raw)
        sec = {"text": text}
        if src_m: sec["source"] = src_m.group(1).strip()
        if url_m: sec["url"] = url_m.group(1).strip()
        sections.append(sec)
    return sections

HEADER_RE = re.compile(r'^\s{0,3}##\s+(.+)$', re.MULTILINE)

def split_markdown_into_sections(md: str):
    if not HEADER_RE.search(md):
        return [{"text": md}]
    sections = []
    parts = HEADER_RE.split(md)
    prefix = parts[0]
    if prefix.strip():
        sections.append({"text": prefix.strip()})
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i+1] if i+1 < len(parts) else ""
        text = f"## {header}\n{body.strip()}"
        src = None; url = None
        for line in body.splitlines():
            l = line.strip()
            if l.lower().startswith("source:") or l.lower().startswith("source :"):
                src = l.split(":",1)[1].strip().strip('"')
            if l.lower().startswith("url:") or l.lower().startswith("url :"):
                url = l.split(":",1)[1].strip().strip('"')
        sec = {"text": text}
        if src: sec["source"] = src
        if url: sec["url"] = url
        sections.append(sec)
    return sections

def parse_response_for_sections(text: str):
    if not isinstance(text, str):
        return [{"text": str(text)}]
    sections = []
    for block in extract_code_blocks(text):
        strict = try_strict_json_parse(block)
        if strict:
            sections.extend(strict); continue
        loose = try_lenient_slide_extract(block)
        if loose:
            sections.extend(loose)
    if sections:
        return sections
    return split_markdown_into_sections(text)

# ---- source chips / placement ----
def _domain(u:str) -> str:
    try:
        d = urlparse(u).netloc
        return d.replace("www.", "") if d else u
    except Exception:
        return u

def normalize_sources(section: dict):
    items = []
    if not isinstance(section, dict): return items
    if "sources" in section and isinstance(section["sources"], list):
        for s in section["sources"]:
            if isinstance(s, dict) and s.get("url"):
                items.append({"name": s.get("name") or _domain(s["url"]), "url": s["url"]})
    elif section.get("url"):
        items.append({"name": section.get("source") or _domain(section["url"]), "url": section["url"]})
    elif section.get("source"):
        items.append({"name": section.get("source"), "url": "#"})
    return items

def render_inline_chip(chips):
    if not chips: return ""
    max_show = 1
    html = []
    for src in chips[:max_show]:
        url_attr = src.get("url") or "#"
        html.append(
            f'<a class="src-chip" href="{url_attr}" target="_blank" title="{_domain(url_attr)}">'
            f'  <span class="src-dot"></span>{src["name"]}'
            f'</a>'
        )
    if len(chips) > max_show:
        html.append(f'<span class="src-chip src-chip-count">+{len(chips)-max_show}</span>')
    return "".join(html)

def render_message(role: str, content: str, qtype: str | None = None):
    if role == "user":
        st.markdown(f'<div class="msg user"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
        return
    sections = parse_response_for_sections(content)
    st.markdown(
        f'''
        <div class="msg assistant">
          <strong>🔍 SearchInternetAgent</strong>
          <small style="color:var(--sub)"> ({qtype or "AI Answer"})</small><br><br>
        ''',
        unsafe_allow_html=True,
    )
    for s in sections:
        chips = normalize_sources(s)
        chip_html = render_inline_chip(chips)
        text_md = (s.get("text") or "").rstrip()
        if text_md.strip().startswith("```") and text_md.strip().endswith("```"):
            inner = CODE_BLOCK_ANY.findall(text_md)
            if inner: text_md = inner[0]
        st.markdown(f'{text_md} <span class="src-after">{chip_html}</span>', unsafe_allow_html=True)
        st.markdown('<div class="clear"></div>', unsafe_allow_html=True)
    if st.session_state.debug_mode:
        with st.expander("🐛 Debug"):
            st.write("Parsed sections:", sections)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Header
st.markdown(
    '<div class="header"><h1>🔍 SearchInternet AI-Agent</h1>'
    '<p>AI-Powered Internet Search & Analysis</p></div>',
    unsafe_allow_html=True
)

# ── Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Mode")
    st.session_state.mode = st.radio(
        "Choose response style",
        ["precise", "deepSearch", "presentation", "webContext"],
        index=["precise","deepSearch","presentation","webContext"].index(st.session_state.mode),
        captions=[
            "2–3 line concise",
            "Comprehensive write-up",
            "Slide-ready bullets",
            "Only web context (scraped)"
        ],
    )
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history.clear()
            st.rerun()
    with col_b:
        st.session_state.debug_mode = st.toggle("🐛 Debug", value=st.session_state.debug_mode)

    st.markdown("---")
    st.markdown("### 🗄️ Cache Management")
    st.markdown(f"**Cached Responses:** {len(st.session_state.response_cache)}")
    col_cache1, col_cache2 = st.columns(2)
    with col_cache1:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.session_state.response_cache.clear()
            st.rerun()
    with col_cache2:
        if st.button("📊 Cache Stats", use_container_width=True):
            st.json(st.session_state.response_cache)

# ── Chat history width + center
st.markdown(
    """
    <style>
    .chat-wrapper { max-width: 30%; margin: auto; }
    </style>
    """,
    unsafe_allow_html=True
)
left, center, right = st.columns([0.2, 0.8, 0.2])
with center:
    st.markdown('<div class="chat">', unsafe_allow_html=True)
    for m in st.session_state.chat_history:
        render_message(m["role"], m["content"], m.get("query_type"))
    st.markdown('</div>', unsafe_allow_html=True)

# ── Minimal status helper
def set_status(ph, message: str):
    ph.markdown(
        f'''
        <div class="status-bar">
          <span class="spinner"></span>
          <span>{message}</span><span class="dots">...</span>
        </div>
        ''',
        unsafe_allow_html=True
    )

# ── Single sticky input
prompt = st.chat_input("Ask me anything… (Enter to send)")

# ── Handle submission (CLEAN status: single line, no emoji clutter)
if prompt:
    st.session_state.chat_history.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now(),
    })

    agent_mode    = "scraped" if st.session_state.mode == "webContext" else "llm"
    display_mode  = st.session_state.mode if st.session_state.mode != "webContext" else "Web Context"
    internal_mode = st.session_state.mode if st.session_state.mode != "webContext" else "precise"

    try:
        status_box = st.empty()  # single compact status bar

        cache_key  = f"{prompt}_{internal_mode}_{agent_mode}"
        start_time = datetime.now()

        if cache_key in st.session_state.response_cache:
            set_status(status_box, "Loading previous result")
            response = st.session_state.response_cache[cache_key]
        else:
            set_status(status_box, "Processing your request")
            response = SearchAgent(prompt, internal_mode, agent_mode)
            st.session_state.response_cache[cache_key] = response

        # finished → clear status line
        status_box.empty()

        # append assistant message
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "query_type": display_mode,
            "timestamp": datetime.now(),
        })

    except Exception as e:
        status_box.empty()
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"❌ Error: {e}",
            "query_type": "System",
            "timestamp": datetime.now(),
        })

    st.rerun()

st.caption("Developed by Mohd Azam • SearchInternetAgent Chatbot")