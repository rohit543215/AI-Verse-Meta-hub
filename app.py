import streamlit as st
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tools import TOOLS, CATEGORIES

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="TORO: AI Tools Directory & Chatbot",
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
# Load knowledge base
# ---------------------------
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

# Load Sentence Transformer model once
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()
knowledge_embeddings = model.encode(KNOWLEDGE, convert_to_tensor=True)

# ---------------------------
# CSS Styling - insert your full CSS code here
# ---------------------------
st.markdown("""
<style>
/* Paste your full enhanced CSS styles here */
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header and About
# ---------------------------
st.markdown("""
<div class="app-header">
  <h1>🤖 TORO</h1>
  <p>Discover and explore AI tools by category and pricing. Launch quickly or preview inline when embeddable.</p>
</div>

<div class="about-card">
  <h2>Welcome to 🤖 TORO</h2>
  <p>TORO helps to <strong>discover and explore AI tools</strong> with ease.
  Use categories and pricing filters, browse cards, preview embeddable sites, and launch in one click.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Chatbot Section
# ---------------------------
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
else:
    st.write("Enter a question and press Ask")

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
                st.experimental_rerun()

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
            st.experimental_rerun()

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
        st.checkbox("Embeddable preview", value=st.session_state.show_previews, key="show_previews")

    with top_r:
        st.markdown("""
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
        """, unsafe_allow_html=True)

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
    qp["section"] = "results"
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
            st.experimental_rerun()
    with p2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages} — {total_tools} tools</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("Next ➡", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            request_scroll()
            st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
