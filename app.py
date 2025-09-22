# app.py
import streamlit as st
import streamlit.components.v1 as components
from tools import TOOLS, CATEGORIES

st.set_page_config(
    page_title="Deep Store: For AI Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------
# Helpers / Callbacks
# ---------------------------
def reset_page():
    st.session_state["current_page"] = 1

def clear_filters():
    st.session_state["category"] = "All"
    st.session_state["plan"] = "All"
    st.session_state["search"] = ""
    st.session_state["per_page"] = 9
    st.session_state["current_page"] = 1

# initialize session state defaults
if "category" not in st.session_state:
    st.session_state["category"] = "All"
if "plan" not in st.session_state:
    st.session_state["plan"] = "All"
if "search" not in st.session_state:
    st.session_state["search"] = ""
if "per_page" not in st.session_state:
    st.session_state["per_page"] = 9
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1

# ---------------------------
# CSS (clean + minimal)
# ---------------------------
st.markdown(
    """
<style>
/* Basic app background & font */
.stApp {
  background-color: #f7fafc;
  color: #111827;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* Header area */
.app-header {
  text-align: center;
  margin-bottom: 18px;
}
.app-header h1 {
  margin: 4px 0;
  font-size: 1.9rem;
  color: #0f172a;
}
.app-header p {
  margin: 0;
  color: #6b7280;
  font-size: 0.95rem;
}

/* Filters container */
.filters-card {
  background: #fff;
  border: 1px solid #e6edf3;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(17,24,39,0.04);
  margin-bottom: 18px;
}

/* Make the native widgets integrate better visually */
.stSelectbox, .stTextInput, .stSlider, .stNumberInput {
  border-radius: 10px;
}

/* Tool cards */
.tool-card {
  background-color: #ffffff;
  padding: 14px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(2,6,23,0.06);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.tool-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 26px rgba(2,6,23,0.10);
}
.tool-card h3 {
  margin: 0;
  font-size: 1.05rem;
  color: #0f172a;
}
.tool-card p {
  margin: 6px 0;
  color: #475569;
  font-size: 0.9rem;
}
.tool-meta {
  color: #6b7280;
  font-size: 0.85rem;
  margin-bottom: 10px;
}

/* tags */
.tag {
  display: inline-block;
  background: #eef2ff;
  color: #4338ca;
  padding: 4px 8px;
  border-radius: 999px;
  margin-right: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Link-button (styled anchor) */
.link-btn {
  display: inline-block;
  background: #2563eb;
  color: #fff !important;
  padding: 8px 12px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  border: none;
}
.link-btn:hover {
  background: #1f4ed8;
  color: #fff !important;
}

/* Pagination */
.pagination {
  text-align: center;
  margin: 18px 0;
}
.pagination .page-info {
  display: inline-block;
  margin: 0 12px;
  color: #374151;
  font-weight: 600;
}

/* Responsive tweaks */
@media (max-width: 900px) {
  .tool-card { padding: 12px; }
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
  <h1>🤖 Deep Store</h1>
  <p>Discover the best AI tools — filter, preview, and launch quickly.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------
# Filters area (single row; responsive)
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)
col_cat, col_search, col_plan = st.columns([2, 6, 2], gap="large")

with col_cat:
    st.markdown("**Category**")
    # uses session_state key so we can reset with clear_filters
    st.selectbox(
        "",
        options=["All"] + CATEGORIES,
        index=0 if st.session_state["category"] == "All" else (["All"] + CATEGORIES).index(st.session_state["category"]),
        key="category",
        on_change=reset_page,
        label_visibility="collapsed",
    )

with col_search:
    st.markdown("**Search**")
    st.text_input(
        "",
        placeholder="Search tools by name, tags, or description",
        key="search",
        on_change=reset_page,
        label_visibility="collapsed",
    )

with col_plan:
    st.markdown("**Pricing**")
    st.selectbox(
        "",
        options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"],
        index=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"].index(st.session_state["plan"]) if st.session_state["plan"] in ["All","Free","Free + Paid","Paid","Credits + Paid"] else 0,
        key="plan",
        on_change=reset_page,
        label_visibility="collapsed",
    )

# small control row: per_page + clear button
c1, c2, c3 = st.columns([2, 6, 2])
with c1:
    per_page = st.slider("Tools / page", 6, 24, st.session_state["per_page"], step=3, key="per_page")
with c2:
    # center area we provide an inline control
    st.write("")  # spacer
with c3:
    if st.button("Clear filters"):
        clear_filters()

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Filtering logic
# ---------------------------
def filter_tools(tools):
    category = st.session_state["category"]
    plan = st.session_state["plan"]
    query = st.session_state["search"].strip().lower()
    filtered = []
    for tool in tools:
        if category != "All" and tool.get("category", "") != category:
            continue
        if plan != "All" and tool.get("plan", "") != plan:
            continue
        if query:
            searchable = " ".join(
                [
                    tool.get("name", ""),
                    tool.get("blurb", ""),
                    " ".join(tool.get("tags", [])),
                ]
            ).lower()
            if query not in searchable:
                continue
        filtered.append(tool)
    return filtered

filtered_tools = filter_tools(TOOLS)
total_tools = len(filtered_tools)

# reset current page if total_pages changed lower than current
total_pages = (total_tools - 1) // st.session_state["per_page"] + 1 if total_tools > 0 else 1
if st.session_state["current_page"] > total_pages:
    st.session_state["current_page"] = total_pages

# ---------------------------
# Display results / pagination
# ---------------------------
if total_tools == 0:
    st.info("No tools found matching your filters. Try broadening your search or clearing filters.")
else:
    # pagination controls top
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    pcol1, pcol2, pcol3 = st.columns([1, 1, 1])
    with pcol1:
        if st.button("⬅ Prev"):
            if st.session_state["current_page"] > 1:
                st.session_state["current_page"] -= 1
    with pcol2:
        st.markdown(f'<div class="page-info">Page {st.session_state["current_page"]} of {total_pages} — {total_tools} tools</div>', unsafe_allow_html=True)
    with pcol3:
        if st.button("Next ➡"):
            if st.session_state["current_page"] < total_pages:
                st.session_state["current_page"] += 1
    st.markdown("</div>", unsafe_allow_html=True)

    # compute page subset
    start = (st.session_state["current_page"] - 1) * st.session_state["per_page"]
    end = min(start + st.session_state["per_page"], total_tools)
    page_tools = filtered_tools[start:end]

    # show grid: 3 columns. If less than 3 in a row, blank columns are fine.
    for i in range(0, len(page_tools), 3):
        row_tools = page_tools[i : i + 3]
        cols = st.columns(3, gap="large")
        for col, tool in zip(cols, row_tools):
            with col:
                logo = tool.get("logo", "")
                name = tool.get("name", "Unknown")
                blurb = tool.get("blurb", "")
                meta = f"{tool.get('category','')} • {tool.get('plan','')}"
                tags = tool.get("tags", [])[:4]

                # card
                html = f"""
                <div class="tool-card">
                  <div style="display:flex; gap:12px; align-items:center; margin-bottom:8px;">
                    <img src="{logo}" alt="logo" style="width:44px; height:44px; object-fit:cover; border-radius:10px; border:1px solid #eef2ff;" onerror="this.style.display='none'"/>
                    <div style="flex:1;">
                      <h3>{name}</h3>
                      <div class="tool-meta">{meta}</div>
                    </div>
                  </div>
                  <p>{blurb}</p>
                  <div style="margin-top:8px;">{"".join([f'<span class="tag">#{t}</span>' for t in tags])}</div>
                  <div style="margin-top:12px;">
                    <a class="link-btn" href="{tool.get('link')}" target="_blank" rel="noreferrer">🚀 Launch</a>
                    {"<span style='margin-left:10px; color:#6b7280; font-weight:600;'>Embeddable</span>" if tool.get("embeddable", False) else ""}
                  </div>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)

                # optional iframe preview (only if embeddable)
                if tool.get("embeddable", False):
                    try:
                        components.iframe(tool.get("link"), height=420)
                    except Exception:
                        # some sites block embedding — ignore silently
                        pass

    # bottom pagination (same as top)
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 1, 1])
    with b1:
        if st.button("⬅ Prev (bottom)"):
            if st.session_state["current_page"] > 1:
                st.session_state["current_page"] -= 1
    with b2:
        st.markdown(f'<div class="page-info">Page {st.session_state["current_page"]} of {total_pages}</div>', unsafe_allow_html=True)
    with b3:
        if st.button("Next ➡ (bottom)"):
            if st.session_state["current_page"] < total_pages:
                st.session_state["current_page"] += 1
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.divider()
st.caption("✨ Made with ❤️ using Streamlit • Find the perfect AI tool for your needs")
