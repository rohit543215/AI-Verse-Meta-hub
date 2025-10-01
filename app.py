import streamlit as st
from tools import TOOLS, CATEGORIES
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="TORO: AI Tools Directory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------
# Initialize state early
# ---------------------------
defaults = {
    "filter_category": "All",
    "filter_plan": "All",
    "filter_search": "",
    "current_page": 1,
    "clear_flag": False,
    "show_previews": False,
    "scroll_ticket": 0,
    "last_scrolled_ticket": -1,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------------------------
# Helpers
# ---------------------------
def request_scroll():
    st.session_state.scroll_ticket += 1


def reset_page():
    st.session_state.current_page = 1


def safe_str(x):
    return x if isinstance(x, str) else ""


def filter_tools(tools):
    category = st.session_state.filter_category
    plan = st.session_state.filter_plan
    query = st.session_state.filter_search.strip().lower()
    filtered = []
    for tool in tools:
        if category != "All" and tool.get("category", "") != category:
            continue
        if plan != "All" and tool.get("plan", "") != plan:
            continue
        if query:
            searchable = " ".join([
                safe_str(tool.get("name", "")),
                safe_str(tool.get("blurb", "")),
                " ".join(tool.get("tags", [])),
            ]).lower()
            if query not in searchable:
                continue
        filtered.append(tool)
    return filtered


# ---------------------------
# Early clear path
# ---------------------------
if st.session_state.clear_flag:
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.current_page = 1
    st.session_state.show_previews = False
    st.session_state.clear_flag = False
    request_scroll()
    st.rerun()


# ---------------------------
# Enhanced CSS with modern design
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');


:root {
    /* Light theme colors */
    --bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --card-bg: rgba(255, 255, 255, 0.95);
    --card-hover: rgba(255, 255, 255, 1);
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --text-muted: #718096;
    --accent: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-light: rgba(102, 126, 234, 0.1);
    --border: rgba(226, 232, 240, 0.8);
    --shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 20px 40px rgba(0, 0, 0, 0.15);
    --ring: rgba(102, 126, 234, 0.4);
}


/* Global styles */
.stApp {
    background: var(--bg);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}


.main .block-container {
    padding-top: 2rem;
    max-width: 1400px;
}


/* Header styles */
.app-header {
    text-align: center;
    margin: 0 0 3rem 0;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}


.app-header h1 {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.5rem 0;
    text-shadow: none;
}


.app-header p {
    font-size: 1.2rem;
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}


/* About section */
.about-card {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}


.about-card h2 {
    color: var(--text-primary);
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
}


.about-card p {
    color: var(--text-secondary);
    font-size: 1.1rem;
    line-height: 1.6;
    margin: 0;
}


/* Filters section */
.filters-card {
    position: sticky;
    top: 1rem;
    z-index: 100;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}


/* Streamlit components styling */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 2px solid transparent;
    border-radius: 12px;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.75rem 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
}


.stButton > button:before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transition: left 0.5s;
}


.stButton > button:hover:before {
    left: 100%;
}


.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.25);
    border-color: var(--ring);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}


.stButton > button:active {
    transform: translateY(0);
}


/* Text input styling */
.stTextInput > div > div > input {
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease;
}


.stTextInput > div > div > input:focus {
    border-color: var(--ring);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    outline: none;
}


/* Selectbox styling */
.stSelectbox > div > div > select {
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    background: rgba(255, 255, 255, 0.9);
}


/* Toggle styling */
.stCheckbox > label {
    font-weight: 600;
    color: var(--text-primary);
}


/* Tool cards */
.tool-card {
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}


.tool-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--accent);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}


.tool-card:hover::before {
    transform: scaleX(1);
}


.tool-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--shadow-hover);
    background: var(--card-hover);
    border-color: var(--ring);
}


.tool-card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
}


.tool-card p {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.6;
    margin: 0.5rem 0 1rem 0;
}


/* Badges and tags */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    border: 2px solid transparent;
    transition: all 0.3s ease;
}


.badge:nth-of-type(1) {
    background: linear-gradient(135deg, #e0f2fe 0%, #b3e5fc 100%);
    color: #0277bd;
    border-color: #81d4fa;
}


.badge.plan {
    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
    color: #2e7d32;
    border-color: #a5d6a7;
}


.tag {
    display: inline-block;
    background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
    color: #6a1b9a;
    padding: 0.4rem 0.8rem;
    border-radius: 50px;
    margin: 0.25rem 0.25rem 0.25rem 0;
    font-size: 0.8rem;
    font-weight: 600;
    border: 2px solid #ce93d8;
    transition: all 0.3s ease;
}


.tag:hover {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(106, 27, 154, 0.3);
}


/* Buttons */
.link-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--accent);
    color: white !important;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
}


.link-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    filter: brightness(1.1);
}


.soft-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(102, 126, 234, 0.1);
    color: var(--text-primary) !important;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    border: 2px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
}


.soft-btn:hover {
    background: rgba(102, 126, 234, 0.2);
    border-color: rgba(102, 126, 234, 0.4);
    transform: translateY(-1px);
}


/* Pagination */
.pagination {
    position: sticky;
    bottom: 1rem;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    margin: 2rem 0;
    box-shadow: var(--shadow);
}


.page-info {
    display: inline-block;
    margin: 0 1rem;
    color: var(--text-primary);
    font-weight: 600;
    font-size: 1.1rem;
}


/* Editor's picks */
.picks-card {
    background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);
    border: 2px solid #d8b4fe;
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
}


.picks-title {
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 1rem 0;
}


.pick-item {
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 12px;
    border: 1px solid rgba(139, 92, 246, 0.2);
}


.pick-item .k {
    font-weight: 700;
    color: #7c3aed;
    font-size: 0.9rem;
}


.pick-item .v {
    font-weight: 800;
    color: #1a202c;
    font-size: 1.1rem;
}


.pick-item .note {
    color: #4a5568;
    font-size: 0.85rem;
    display: block;
    margin-top: 0.25rem;
    line-height: 1.4;
}


/* Why TORO section */
.toro-card.big {
    background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
    border: 2px solid #60a5fa;
    border-radius: 24px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: var(--shadow);
}


.toro-badge {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white;
    font-size: 0.9rem;
    font-weight: 800;
    padding: 0.5rem 1rem;
    display: inline-block;
    border-radius: 50px;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
}


.toro-eyebrow {
    color: #93c5fd;
    font-weight: 900;
    font-size: 0.95rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 1rem 0 0.5rem 0;
}


.toro-title {
    font-size: 2rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0.5rem 0;
    line-height: 1.2;
}


.toro-sub {
    color: #d1d5db;
    font-size: 1.1rem;
    line-height: 1.6;
    margin: 1rem 0;
}


.toro-bullets {
    margin: 1rem 0 0 0;
    padding-left: 1.5rem;
}


.toro-bullets li {
    color: #e5e7eb;
    margin: 0.75rem 0;
    font-size: 1rem;
    line-height: 1.6;
}


/* Empty card */
.empty-card {
    height: 1px;
    margin-bottom: 2rem;
}


/* Logo images */
img {
    border-radius: 12px;
    border: 2px solid var(--border);
    transition: all 0.3s ease;
}


img:hover {
    border-color: var(--ring);
    transform: scale(1.05);
}


/* Results header */
h1[data-testid="stHeader"] {
    background: var(--accent);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}


/* Responsive design */
@media (max-width: 768px) {
    .app-header h1 {
        font-size: 2.5rem;
    }
    
    .app-header p {
        font-size: 1rem;
    }
    
    .tool-card {
        margin-bottom: 1.5rem;
    }
    
    .filters-card {
        padding: 1.5rem;
    }
}


/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}


/* Loading animation */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}


.loading {
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="app-header">
  <h1>🤖 TORO</h1>
  <p>Discover and explore AI tools by category and pricing. Launch quickly or preview inline when embeddable.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# About
# ---------------------------
st.markdown("""
<div class="about-card">
  <h2>Welcome to 🤖 TORO</h2>
  <p>TORO helps to <strong>discover and explore AI tools</strong> with ease.
  Use categories and pricing filters, browse cards, preview embeddable sites, and launch in one click.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Added Chatbot Section here
# ---------------------------
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_knowledge():
    knowledge = []
    data_folder = "data"
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            if file.endswith(".md"):
                with open(os.path.join(data_folder, file), encoding="utf-8") as f:
                    text = f.read()
                    parts = text.split("\n\n")  # Split by paragraphs
                    knowledge.extend([p.strip() for p in parts if p.strip()])
    return knowledge

KNOWLEDGE = load_knowledge()

@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

model = load_model()
knowledge_embeddings = model.encode(KNOWLEDGE, convert_to_tensor=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.header("Ask TORO Chatbot")

query = st.text_input("Your question")
if st.button("Ask") and query.strip():
    query_emb = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_emb.cpu(), knowledge_embeddings.cpu())[0]
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
    if best_score > 0.5:
        response = KNOWLEDGE[best_idx]
    else:
        response = "I don't know that yet. Try asking about TORO or AI tools."
    st.markdown(f"**Answer:** {response}")

# ---------------------------
# Filters bar
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)

rail_col, main_col = st.columns([3.0, 9.0], gap="large")

with rail_col:
    st.markdown("**Categories**")
    cat_options = ["All"] + CATEGORIES
    current_cat = st.session_state.filter_category
    for c in cat_options:
        if st.button(f"{c}", key=f"cat_{c}", use_container_width=True):
            if c != current_cat:
                st.session_state.filter_category = c
                st.session_state.current_page = 1
                request_scroll()
                st.rerun()

with main_col:
    top_l, top_m, top_r = st.columns([3.8, 4.4, 3.8], gap="large")

    with top_l:
        st.markdown("**Search**")
        def on_search_change():
            reset_page()
            request_scroll()
        st.text_input(
            "",
            placeholder="Search by name, tags, or description",
            key="filter_search",
            on_change=on_search_change,
            label_visibility="collapsed",
        )
        if st.button("🗑️ Clear filters", use_container_width=True):
            st.session_state.clear_flag = True
            request_scroll()
            st.rerun()

    with top_m:
        st.markdown("**Pricing**")
        def on_plan_change():
            reset_page()
            request_scroll()
        plans = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
        st.selectbox(
            "",
            options=plans,
            index=plans.index(st.session_state.filter_plan) if st.session_state.filter_plan in plans else 0,
            key="filter_plan",
            on_change=on_plan_change,
            label_visibility="collapsed",
        )
        st.toggle("Embeddable preview", value=st.session_state.show_previews, key="show_previews")

    with top_r:
        st.markdown(
            """
            <div class="picks-card">
              <h3 class="picks-title">Editor's picks</h3>
              <div class="pick-item"><span class="k">Best general assistant</span><br/><span class="v">ChatGPT</span><span class="note">Great all‑rounder for Q&A, coding help, and writing; broad plugin and ecosystem support.</span></div>
              <div class="pick-item"><span class="k">Best image generation</span><br/><span class="v">Gemini</span><span class="note">Strong multimodal grounding with solid text‑image prompting and safety features.</span></div>
              <div class="pick-item"><span class="k">Best video generation</span><br/><span class="v">Runway</span><span class="note">Reliable editing + generation workflow for creators and marketers.</span></div>
              <div class="pick-item"><span class="k">Best meeting assistant</span><br/><span class="v">Otter</span><span class="note">Live transcription and searchable summaries for teams.</span></div>
              <div class="pick-item"><span class="k">Best automation</span><br/><span class="v">Zapier</span><span class="note">Connect favorite apps and orchestrate AI workflows without code.</span></div>
              <div class="pick-item"><span class="k">Best research</span><br/><span class="v">Perplexity</span><span class="note">Answer engine with citations for quick discovery.</span></div>
              <div class="pick-item"><span class="k">Best writing</span><br/><span class="v">Grammarly</span><span class="note">Clean rewrites, tone control, and grammar fixes.</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Results anchor (native)
# ---------------------------
st.header("Results", anchor="results")

# ---------------------------
# Data and pagination
# ---------------------------
filtered_tools = filter_tools(TOOLS)
total_tools = len(filtered_tools)
per_page = 12
total_pages = (total_tools - 1) // per_page + 1 if total_tools > 0 else 1
if st.session_state.current_page > total_pages:
    st.session_state.current_page = total_pages

# ---------------------------
# Trigger scroll via URL fragment (JS-free)
# ---------------------------
if st.session_state.scroll_ticket > st.session_state.last_scrolled_ticket:
    qp = dict(st.query_params)
    qp["section"] = "results"  # harmless param to "touch" the fragment
    st.query_params.clear()
    st.query_params.update(qp)
    st.session_state.last_scrolled_ticket = st.session_state.scroll_ticket

# ---------------------------
# Top pagination
# ---------------------------
if total_tools == 0:
    st.info("No tools found. Try broadening search or clearing filters.")
else:
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1, 2, 1], gap="large")
    with p1:
        if st.button("⬅ Prev", key="prev_top") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            request_scroll()
            st.rerun()
    with p2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages} — {total_tools} tools</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("Next ➡", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            request_scroll()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # Results grid
    # ---------------------------
    start = (st.session_state.current_page - 1) * per_page
    end = min(start + per_page, total_tools)
    page_tools = filtered_tools[start:end]

    for i in range(0, max(len(page_tools), 3), 3):
        row_tools = page_tools[i:i+3]
        cols = st.columns(3, gap="large")
        while len(row_tools) < 3:
            row_tools.append(None)
        for col, tool in zip(cols, row_tools):
            with col:
                if tool is None:
                    st.markdown('<div class="empty-card"></div>', unsafe_allow_html=True)
                    continue

                logo = safe_str(tool.get("logo", ""))
                name = safe_str(tool.get("name", "Unknown"))
                blurb = safe_str(tool.get("blurb", ""))
                meta = safe_str(tool.get('category',''))
                plan = safe_str(tool.get("plan", ""))
                tags = tool.get("tags", [])[:4]
                link = safe_str(tool.get("link", "#"))
                emb = bool(tool.get("embeddable", False))

                st.markdown(f"""
                <div class="tool-card">
                  <div style="display:flex; gap:12px; align-items:center; margin-bottom:12px;">
                    <img src="{logo}" alt="logo" style="width:48px; height:48px; object-fit:cover; border-radius:12px;" onerror="this.style.display='none'"/>
                    <div style="flex:1;">
                      <h3>{name}</h3>
                      <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:8px;">
                        <span class="badge">🗂 {meta}</span>
                        <span class="badge plan">💳 {plan}</span>
                      </div>
                    </div>
                  </div>
                  <p>{blurb}</p>
                  <div style="margin-top:12px;">{"".join([f'<span class="tag">#{t}</span>' for t in tags])}</div>
                  <div style="margin-top:16px; display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
                    <a class="link-btn" href="{link}" target="_blank" rel="noreferrer noopener">🚀 Launch</a>
                    <a class="soft-btn" href="{link}" target="_blank" rel="nofollow noopener" style="text-decoration:none;">🔗 Visit</a>
                    {"<span class='badge' style='background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%); color: #92400e; border-color: #f59e0b;'>🧩 Embeddable</span>" if emb else ""}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if emb and st.session_state.show_previews:
                    st.components.v1.iframe(link, height=520, scrolling=True)

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.link_button("🎓 more tools for student", "https://free-tools-ijpl7qrhvjg4gdhvhnpvae.streamlit.app/", type="primary", icon="🧰", use_container_width=True)
st.caption("✨ Made with ❤️ by Girish Joshi in INDIA • TORO - Find the perfect AI tool for every use case")

