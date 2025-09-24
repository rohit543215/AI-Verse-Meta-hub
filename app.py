import streamlit as st
import streamlit.components.v1 as components
from tools import TOOLS, CATEGORIES

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
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Clear filters safely before widgets mount
if st.session_state.clear_flag:
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.current_page = 1
    st.session_state.show_previews = False
    st.session_state.clear_flag = False
    st.rerun()

# ---------------------------
# Helpers
# ---------------------------
def reset_page():
    st.session_state.current_page = 1

def clear_all_filters():
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.current_page = 1
    st.session_state.show_previews = False
    st.rerun()

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
# CSS
# ---------------------------
st.markdown("""
<style>
:root { --bg:#FFFFFF; --card:#FFFFFF; --muted:#6B7280; --text:#111827; --accent:#2563EB; --ring:rgba(37,99,235,0.25); --border:#E5E7EB; }
html, body, .stApp { background:var(--bg); color:var(--text); font-family:Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
.app-header { text-align:center; margin:10px 0 22px; }
.app-header h1 { margin:6px 0; font-size:2rem; letter-spacing:0.2px; color:#0F172A; }
.app-header p { margin:0; color:var(--muted); font-size:0.98rem; }

.filters-card { position:sticky; top:0; z-index:5; background:#FFFFFFF2; border:1px solid var(--border); padding:14px; border-radius:14px; box-shadow:0 10px 30px rgba(17,24,39,0.05); margin-bottom:18px; backdrop-filter:blur(6px); }

.tool-card { background:var(--card); padding:16px; border-radius:14px; border:1px solid var(--border); box-shadow:0 6px 18px rgba(2,6,23,0.06); transition:transform 0.18s ease, box-shadow 0.18s ease, border 0.18s ease; margin-bottom:26px; }
.tool-card:hover { transform:translateY(-4px); box-shadow:0 14px 26px rgba(2,6,23,0.10); border-color:var(--ring); }
.tool-card h3 { margin:0; font-size:1.05rem; color:#0F172A; }
.tool-card p { margin:8px 0 6px; color:#374151; font-size:0.92rem; }

.badge { display:inline-flex; align-items:center; gap:6px; background:#EEF2FF; color:#3730A3; padding:4px 10px; border:1px solid #E0E7FF; border-radius:999px; font-size:0.74rem; font-weight:700; }
.badge.plan { background:#ECFDF5; color:#065F46; border-color:#D1FAE5; }
.tag { display:inline-block; background:#EEF2FF; color:#4338CA; padding:5px 10px; border-radius:999px; margin-right:6px; margin-top:6px; font-size:0.76rem; font-weight:700; border:1px solid #E0E7FF; }

.link-btn { display:inline-block; background:linear-gradient(180deg,#2563EB,#1D4ED8); color:#fff !important; padding:9px 12px; border-radius:10px; text-decoration:none; font-weight:700; border:0; box-shadow:0 8px 20px rgba(29,78,216,0.25); }
.soft-btn { display:inline-block; padding:8px 12px; border-radius:10px; border:1px solid var(--border); background:#F8FAFC; color:var(--text); font-weight:700; }
.link-btn:hover { filter:brightness(1.07); }
.soft-btn:hover { border-color:var(--ring); }

.pagination { position:sticky; bottom:12px; background:rgba(255,255,255,0.85); backdrop-filter:blur(6px); border:1px solid var(--border); border-radius:12px; padding:8px; text-align:center; margin:18px 0; }
.pagination .page-info { display:inline-block; margin:0 12px; color:var(--text); font-weight:700; }

.meta-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:4px; }
.empty-card { height:0.1px; margin-bottom:26px; }

.picks-card { background:#F8FAFF; border:1px solid #E0E7FF; border-radius:14px; padding:14px; box-shadow:0 6px 18px rgba(2,6,23,0.05); margin-bottom:14px; }
.picks-title { margin:0 0 10px; font-size:1.02rem; font-weight:800; background:linear-gradient(90deg,#2563EB 0%,#7C3AED 100%); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }
.pick-item { margin:6px 0; padding:8px 10px; border:1px dashed #E5E7EB; border-radius:10px; background:#FFFFFF; }
.pick-item .k { color:#64748B; font-weight:800; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px; }
.pick-item .v { color:#0F172A; font-weight:800; }
.pick-item .note { color:#475569; font-size:0.86rem; display:block; margin-top:4px; }

/* Why TORO under middle column */
.toro-card.big { background:linear-gradient(180deg,#E0F2FE 0%,#FFFFFF 70%); border:1px solid #93C5FD; border-radius:16px; padding:18px 16px; box-shadow:0 8px 22px rgba(2,6,23,0.06); margin-top:10px; }
.toro-card.big .toro-badge { background:#DBEAFE; color:#1E40AF; border:1px solid #BFDBFE; font-size:0.82rem; font-weight:900; padding:6px 12px; display:inline-block; border-radius:999px; }
.toro-card.big .toro-eyebrow { color:#0369A1; font-weight:900; font-size:0.9rem; letter-spacing:0.6px; text-transform:uppercase; margin:8px 0 2px; }
.toro-card.big .toro-title { margin:2px 0 6px; font-size:1.55rem; line-height:1.2; font-weight:1000; letter-spacing:0.1px; color:#0C4A6E; }
.toro-card.big .toro-sub { color:#0F172A; font-size:1.04rem; line-height:1.6; margin:4px 0 10px; }
.toro-card.big .toro-bullets { margin:10px 0 0; padding-left:18px; }
.toro-card.big .toro-bullets li { color:#0F172A; margin:10px 0; font-size:1.02rem; line-height:1.6; }
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
# Filters bar
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)

rail_col, main_col = st.columns([3.0, 9.0], gap="large", vertical_alignment="top")

with rail_col:
    st.markdown("Categories")
    cat_options = ["All"] + CATEGORIES
    current_cat = st.session_state.filter_category
    for c in cat_options:
        if st.button(f"{c}", key=f"cat_{c}", use_container_width=True):
            if c != current_cat:
                st.session_state.filter_category = c
                st.session_state.current_page = 1
                st.rerun()

with main_col:
    # Top controls: 3 columns
    top_l, top_m, top_r = st.columns([3.8, 4.4, 3.8], gap="large", vertical_alignment="top")

    # Left: Search + Clear filters (requested)
    with top_l:
        st.markdown("Search")
        st.text_input(
            "",
            placeholder="Search by name, tags, or description",
            key="filter_search",
            on_change=reset_page,
            label_visibility="collapsed",
        )
        if st.button("🗑️ Clear filters", use_container_width=True):
            st.session_state.clear_flag = True
            st.rerun()

    # Middle: Pricing + Toggle + Why TORO
    with top_m:
        st.markdown("Pricing")
        plans = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
        st.selectbox(
            "",
            options=plans,
            index=plans.index(st.session_state.filter_plan) if st.session_state.filter_plan in plans else 0,
            key="filter_plan",
            on_change=reset_page,
            label_visibility="collapsed",
        )
        st.toggle("Embeddable preview", value=st.session_state.show_previews, key="show_previews")

        st.markdown(
            """
            <div class="toro-card big">
              <div class="toro-badge">Why TORO?</div>
              <div class="toro-eyebrow">Faster discovery</div>
              <h3 class="toro-title">Find the right AI tool in minutes</h3>
              <p class="toro-sub">Browse by category, pricing, tags, and inline previews—optimized for quick decision‑making.</p>
              <ul class="toro-bullets">
                <li>Curated categories and pricing filters make discovery effortless.</li>
                <li>Card previews surface logos, blurbs, tags, and quick actions.</li>
                <li>Inline <em>Embeddable preview</em> to test tools without leaving TORO.</li>
                <li>Clean pagination keeps browsing smooth at 12 tools per page.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Right: Editor’s picks
    with top_r:
        st.markdown(
            """
            <div class="picks-card">
              <h3 class="picks-title">Editor’s picks</h3>

              <div class="pick-item">
                <span class="k">Best general assistant</span><br/>
                <span class="v">ChatGPT</span>
                <span class="note">Great all‑rounder for Q&A, coding help, and writing; broad plugin and ecosystem support.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best image generation</span><br/>
                <span class="v">Gemini</span>
                <span class="note">Strong multimodal grounding with solid text‑image prompting and safety features.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best video generation</span><br/>
                <span class="v">Runway</span>
                <span class="note">Reliable editing + generation workflow for creators and marketers.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best meeting assistant</span><br/>
                <span class="v">Otter</span>
                <span class="note">Live transcription and searchable summaries for teams.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best automation</span><br/>
                <span class="v">Zapier</span>
                <span class="note">Connect favorite apps and orchestrate AI workflows without code.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best research</span><br/>
                <span class="v">Perplexity</span>
                <span class="note">Answer engine with citations for quick discovery.</span>
              </div>

              <div class="pick-item">
                <span class="k">Best writing</span><br/>
                <span class="v">Grammarly</span>
                <span class="note">Clean rewrites, tone control, and grammar fixes.</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

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
            st.rerun()
    with p2:
        st.markdown(f'<div class="page-info">Page {st.session_state.current_page} of {total_pages} — {total_tools} tools</div>', unsafe_allow_html=True)
    with p3:
        if st.button("Next ➡", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
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
        cols = st.columns(3, gap="large", vertical_alignment="top")
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
                  <div style="display:flex; gap:12px; align-items:center; margin-bottom:8px;">
                    <img src="{logo}" alt="logo" style="width:44px; height:44px; object-fit:cover; border-radius:10px; border:1px solid #E5E7EB;" onerror="this.style.display='none'"/>
                    <div style="flex:1;">
                      <h3>{name}</h3>
                      <div class="meta-row">
                        <span class="badge">🗂 {meta}</span>
                        <span class="badge plan">💳 {plan}</span>
                      </div>
                    </div>
                  </div>
                  <p>{blurb}</p>
                  <div style="margin-top:6px;">{"".join([f'<span class="tag">#{t}</span>' for t in tags])}</div>
                  <div style="margin-top:12px; display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                    <a class="link-btn" href="{link}" target="_blank" rel="noreferrer noopener">🚀 Launch</a>
                    <a class="soft-btn" href="{link}" target="_blank" rel="nofollow noopener" style="text-decoration:none;">🔗 Visit</a>
                    {"<span class='badge'>🧩 Embeddable</span>" if emb else ""}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if emb and st.session_state.show_previews:
                    components.iframe(link, height=520, scrolling=True)

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.link_button("🎓 more tools for student", "https://free-tools-ijpl7qrhvjg4gdhvhnpvae.streamlit.app/", type="primary", icon="🧰", use_container_width=True)
st.caption("✨ Made with ❤️ • TORO - Find the perfect AI tool for every use case")

