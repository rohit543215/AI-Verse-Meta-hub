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
        st.session_state[k] = v  # persists across reruns

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
# CSS (theme + components)
# ---------------------------
st.markdown(
    """
<style>
:root {
  --bg: #FFFFFF;
  --card: #FFFFFF;
  --muted: #6B7280;
  --text: #111827;
  --accent: #2563EB;
  --accent-2: #10B981;
  --ring: rgba(37,99,235,0.25);
  --border: #E5E7EB;
}

html, body, .stApp { 
  background-color: var(--bg); 
  color: var(--text); 
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; 
}

.app-header { 
  text-align: center; 
  margin: 10px 0 22px 0; 
}

.app-header h1 { 
  margin: 6px 0; 
  font-size: 2rem; 
  letter-spacing: 0.2px; 
  color: #0F172A; 
}

.app-header p { 
  margin: 0; 
  color: var(--muted); 
  font-size: 0.98rem; 
}

.filters-card {
  background: #FFFFFFF2; 
  border: 1px solid var(--border);
  padding: 14px; 
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(17,24,39,0.05);
  margin-bottom: 18px; 
  backdrop-filter: blur(6px);
}

.tool-card {
  background: var(--card);
  padding: 16px; 
  border-radius: 14px; 
  border: 1px solid var(--border);
  box-shadow: 0 6px 18px rgba(2,6,23,0.06);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border 0.18s ease;
  margin-bottom: 26px;
}

.tool-card:hover { 
  transform: translateY(-4px); 
  box-shadow: 0 14px 26px rgba(2,6,23,0.10); 
  border-color: var(--ring); 
}

.tool-card h3 { 
  margin: 0; 
  font-size: 1.05rem; 
  color: #0F172A; 
}

.tool-card p { 
  margin: 8px 0 6px 0; 
  color: #374151; 
  font-size: 0.92rem; 
}

.badge { 
  display: inline-flex; 
  align-items:center; 
  gap:6px; 
  background: #EEF2FF; 
  color: #3730A3; 
  padding: 4px 10px; 
  border: 1px solid #E0E7FF; 
  border-radius: 999px; 
  font-size: 0.74rem; 
  font-weight: 700; 
}

.badge.plan { 
  background: #ECFDF5; 
  color: #065F46; 
  border-color: #D1FAE5; 
}

.tag { 
  display: inline-block; 
  background: #EEF2FF; 
  color: #4338CA; 
  padding: 5px 10px; 
  border-radius: 999px; 
  margin-right: 6px; 
  margin-top: 6px; 
  font-size: 0.76rem; 
  font-weight: 700; 
  border: 1px solid #E0E7FF; 
}

.link-btn { 
  display: inline-block; 
  background: linear-gradient(180deg, #2563EB, #1D4ED8); 
  color: #fff !important; 
  padding: 9px 12px; 
  border-radius: 10px; 
  text-decoration: none; 
  font-weight: 700; 
  border: 0; 
  box-shadow: 0 8px 20px rgba(29,78,216,0.25); 
}

.link-btn:hover { 
  filter: brightness(1.07); 
}

.soft-btn { 
  display:inline-block; 
  padding: 8px 12px; 
  border-radius: 10px; 
  border: 1px solid var(--border); 
  background: #F8FAFC; 
  color: var(--text); 
  font-weight: 700; 
}

.soft-btn:hover { 
  border-color: var(--ring); 
}

.pagination {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(6px); 
  border: 1px solid var(--border); 
  border-radius: 12px;
  padding: 8px; 
  text-align: center; 
  margin: 18px 0;
}

.pagination .page-info { 
  display: inline-block; 
  margin: 0 12px; 
  color: var(--text); 
  font-weight: 700; 
}

.meta-row { 
  display:flex; 
  flex-wrap:wrap; 
  gap:8px; 
  align-items:center; 
  margin-top:4px;
}

.picks-card {
  background: #F8FAFF;
  border: 1px solid #E0E7FF;
  border-radius: 14px;
  padding: 14px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.05);
  margin-bottom: 20px;
}

.picks-title {
  margin: 0 0 10px 0;
  font-size: 1.02rem;
  font-weight: 800;
  background: linear-gradient(90deg, #2563EB 0%, #7C3AED 100%);
  -webkit-background-clip: text; 
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.pick-item { 
  margin: 6px 0; 
  padding: 8px 10px; 
  border: 1px dashed #E5E7EB; 
  border-radius: 10px; 
  background: #FFFFFF; 
}

.pick-item .k { 
  color:#64748B; 
  font-weight:800; 
  font-size:0.8rem; 
  text-transform:uppercase; 
  letter-spacing:0.5px;
}

.pick-item .v { 
  color:#0F172A; 
  font-weight:800; 
}

.pick-item .note { 
  color:#475569; 
  font-size:0.86rem; 
  display:block; 
  margin-top:4px; 
}

.toro-card {
  background: linear-gradient(180deg, #ECFEFF 0%, #FFFFFF 60%);
  border: 1px solid #BAE6FD;
  border-radius: 14px;
  padding: 14px;
  margin-top: 14px;
}

.toro-title { 
  margin: 0 0 8px 0; 
  font-size: 1.04rem; 
  font-weight: 900; 
  color: #0EA5E9; 
}

.toro-bullets { 
  margin: 8px 0 0 0; 
  padding-left: 16px; 
}

.toro-bullets li { 
  color:#0F172A; 
  margin: 6px 0; 
}

.toro-badge { 
  display:inline-block; 
  padding:4px 10px; 
  border-radius:999px; 
  background:#DBEAFE; 
  color:#1E40AF; 
  font-weight:800; 
  font-size:0.78rem; 
  border:1px solid #BFDBFE; 
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
<div class="app-header">
  <h1>🤖 TORO</h1>
  <p>Discover and explore AI tools by category and pricing. Launch quickly or preview inline when embeddable.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# About Section
# ---------------------------
st.markdown(
    """
<div class="about-card">
  <h2>Welcome to 🤖 TORO</h2>
  <p>TORO helps to <strong>discover and explore AI tools</strong> with ease.
  Use categories and pricing filters, browse cards, preview embeddable sites, and launch in one click.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Main Layout: Sidebar + Content
# ---------------------------
col_sidebar, col_content = st.columns([3, 8], gap="large")

with col_sidebar:
    st.markdown('<div class="filters-card">', unsafe_allow_html=True)

    # Categories Section
    st.markdown("### Categories")
    cat_options = ["All"] + CATEGORIES
    current_cat = st.session_state.filter_category

    for category in cat_options:
        clicked = st.button(
            f"📁 {category}" if category != "All" else "🗂️ All Categories",
            key=f"cat_{category}",
            use_container_width=True,
            type="primary" if category == current_cat else "secondary",
        )
        if clicked and category != current_cat:
            st.session_state.filter_category = category
            st.session_state.current_page = 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Editor's Picks Section
    st.markdown(
        """
        <div class="picks-card">
          <h3 class="picks-title">Editor's picks</h3>

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

    # TORO Info Section
    st.markdown(
        """
        <div class="toro-card">
          <div class="toro-badge">Why TORO?</div>
          <h3 class="toro-title">A faster way to find AI tools</h3>
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

with col_content:
    st.markdown('<div class="filters-card">', unsafe_allow_html=True)

    # Search and Pricing filters
    filter_col1, filter_col2 = st.columns([3, 2], gap="medium")

    with filter_col1:
        st.markdown("**Search**")
        st.text_input(
            "",
            placeholder="Search by name, tags, or description",
            key="filter_search",
            on_change=reset_page,
            label_visibility="collapsed",
        )

    with filter_col2:
        st.markdown("**Pricing**")
        st.selectbox(
            "",
            ["All", "Free", "Freemium", "Paid"],
            key="filter_plan",
            on_change=reset_page,
            label_visibility="collapsed",
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Filter and paginate tools
    filtered_tools = filter_tools(TOOLS)
    tools_per_page = 12
    total_pages = max(1, (len(filtered_tools) + tools_per_page - 1) // tools_per_page)

    # Ensure current page is valid
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages

    start_idx = (st.session_state.current_page - 1) * tools_per_page
    end_idx = start_idx + tools_per_page
    current_tools = filtered_tools[start_idx:end_idx]

    # Display results summary
    st.markdown(f"**Found {len(filtered_tools)} tools** (Page {st.session_state.current_page} of {total_pages})")

    # Display tools
    if current_tools:
        for tool in current_tools:
            with st.container():
                st.markdown('<div class="tool-card">', unsafe_allow_html=True)

                tool_col1, tool_col2 = st.columns([6, 2])
                with tool_col1:
                    st.markdown(f"### {tool.get('logo', '🔧')} {tool['name']}")
                    st.markdown(f"*{tool['blurb']}*")

                with tool_col2:
                    # Use the supported link button for reliable new-tab navigation
                    st.link_button(
                        f"Visit {tool['name']}",
                        tool['url'],
                        type="primary",
                        use_container_width=True,
                    )

                # Tool metadata
                st.markdown('<div class="meta-row">', unsafe_allow_html=True)
                st.markdown(
                    f'<span class="badge">{tool["category"]}</span> '
                    f'<span class="badge plan">{tool["plan"]}</span>',
                    unsafe_allow_html=True,
                )

                # Tags
                if tool.get("tags"):
                    tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in tool["tags"]])
                    st.markdown(f'<div style="margin-top: 8px;">{tags_html}</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)  # close meta-row
                st.markdown('</div>', unsafe_allow_html=True)  # close tool-card
    else:
        st.info("No tools found matching your criteria. Try adjusting your filters.")

    # Pagination
    if total_pages > 1:
        st.markdown('<div class="pagination">', unsafe_allow_html=True)
        pagination_col1, pagination_col2, pagination_col3 = st.columns([1, 2, 1])

        with pagination_col1:
            if st.button("← Previous", disabled=(st.session_state.current_page <= 1), use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()

        with pagination_col2:
            st.markdown(
                f'<div class="page-info">Page {st.session_state.current_page} of {total_pages}</div>',
                unsafe_allow_html=True,
            )

        with pagination_col3:
            if st.button("Next →", disabled=(st.session_state.current_page >= total_pages), use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # Clear filters button
    if st.button("🗑️ Clear All Filters", use_container_width=True):
        st.session_state.clear_flag = True
        st.rerun()
