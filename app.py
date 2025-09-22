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
# Initialize model state early
# ---------------------------
defaults = {
    "filter_category": "All",
    "filter_plan": "All",
    "filter_search": "",
    "filter_per_page": 9,
    "current_page": 1,
    "clear_flag": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# If a clear was requested, reset BEFORE widgets are created, then rerun
if st.session_state.clear_flag:
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.filter_per_page = 9
    st.session_state.current_page = 1
    st.session_state.clear_flag = False
    st.rerun()  # safe here since no widgets mounted yet [web:225]

# ---------------------------
# Helpers
# ---------------------------
def reset_page():
    st.session_state.current_page = 1

# ---------------------------
# CSS (spacing and visuals)
# ---------------------------
st.markdown(
    """
<style>
.stApp { background-color: #f7fafc; color: #111827; font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
.app-header { text-align: center; margin-bottom: 18px; }
.app-header h1 { margin: 4px 0; font-size: 1.9rem; color: #0f172a; }
.app-header p { margin: 0; color: #6b7280; font-size: 0.95rem; }
.filters-card { background: #fff; border: 1px solid #e6edf3; padding: 16px; border-radius: 12px; box-shadow: 0 3px 10px rgba(17,24,39,0.04); margin-bottom: 18px; }
.tool-card { background-color: #ffffff; padding: 14px; border-radius: 12px; box-shadow: 0 6px 18px rgba(2,6,23,0.06); transition: transform 0.18s ease, box-shadow 0.18s ease; margin-bottom: 26px; }
.tool-card:hover { transform: translateY(-6px); box-shadow: 0 12px 26px rgba(2,6,23,0.10); }
.tool-card h3 { margin: 0; font-size: 1.05rem; color: #0f172a; }
.tool-card p { margin: 6px 0; color: #475569; font-size: 0.9rem; }
.tool-meta { color: #6b7280; font-size: 0.85rem; margin-bottom: 10px; }
.tag { display: inline-block; background: #eef2ff; color: #4338ca; padding: 4px 8px; border-radius: 999px; margin-right: 6px; font-size: 0.75rem; font-weight: 600; }
.link-btn { display: inline-block; background: #2563eb; color: #fff !important; padding: 8px 12px; border-radius: 8px; text-decoration: none; font-weight: 600; border: none; }
.link-btn:hover { background: #1f4ed8; color: #fff !important; }
.pagination { text-align: center; margin: 18px 0; }
.pagination .page-info { display: inline-block; margin: 0 12px; color: #374151; font-weight: 600; }
.empty-card { height: 0.1px; margin-bottom: 26px; }
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
# Filters
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)
col_cat, col_search, col_plan = st.columns([2, 6, 2], gap="large")
with col_cat:
    st.markdown("**Category**")
    st.selectbox(
        "",
        options=["All"] + CATEGORIES,
        index=(["All"] + CATEGORIES).index(st.session_state.filter_category),
        key="filter_category",
        on_change=reset_page,
        label_visibility="collapsed",
    )
with col_search:
    st.markdown("**Search**")
    st.text_input(
        "",
        placeholder="Search tools by name, tags, or description",
        key="filter_search",
        on_change=reset_page,
        label_visibility="collapsed",
    )
with col_plan:
    st.markdown("**Pricing**")
    plans = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
    st.selectbox(
        "",
        options=plans,
        index=plans.index(st.session_state.filter_plan) if st.session_state.filter_plan in plans else 0,
        key="filter_plan",
        on_change=reset_page,
        label_visibility="collapsed",
    )
c1, c2, c3 = st.columns([2, 6, 2], gap="large")
with c1:
    st.slider("Tools / page", 6, 24, step=3, key="filter_per_page", on_change=reset_page)
with c2:
    st.write("")
with c3:
    # Set flag only; actual reset occurs before widget creation next run
    if st.button("Clear filters"):
        st.session_state.clear_flag = True
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Filtering logic
# ---------------------------
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
            searchable = " ".join(
                [tool.get("name", ""), tool.get("blurb", ""), " ".join(tool.get("tags", []))]
            ).lower()
            if query not in searchable:
                continue
        filtered.append(tool)
    return filtered

filtered_tools = filter_tools(TOOLS)
total_tools = len(filtered_tools)
per_page = st.session_state.filter_per_page
total_pages = (total_tools - 1) // per_page + 1 if total_tools > 0 else 1
if st.session_state.current_page > total_pages:
    st.session_state.current_page = total_pages

# ---------------------------
# Results + pagination
# ---------------------------
if total_tools == 0:
    st.info("No tools found matching your filters. Try broadening your search or clearing filters.")
else:
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    pcol1, pcol2, pcol3 = st.columns([1, 1, 1], gap="large")
    with pcol1:
        if st.button("⬅ Prev", key="prev_top") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()
    with pcol2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages} — {total_tools} tools</div>',
            unsafe_allow_html=True,
        )
    with pcol3:
        if st.button("Next ➡", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    start = (st.session_state.current_page - 1) * per_page
    end = min(start + per_page, total_tools)
    page_tools = filtered_tools[start:end]

    for i in range(0, len(page_tools), 3):
        row_tools = page_tools[i : i + 3]
        cols = st.columns(3, gap="large")
        while len(row_tools) < 3:
            row_tools.append(None)
        for col, tool in zip(cols, row_tools):
            with col:
                if tool is None:
                    st.markdown('<div class="empty-card"></div>', unsafe_allow_html=True)
                    continue

                logo = tool.get("logo", "")
                name = tool.get("name", "Unknown")
                blurb = tool.get("blurb", "")
                meta = f"{tool.get('category','')} • {tool.get('plan','')}"
                tags = tool.get("tags", [])[:4]

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True,
                )

                if tool.get("embeddable", False):
                    components.iframe(tool.get("link"), height=480, scrolling=True)

    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 1, 1], gap="large")
    with b1:
        if st.button("⬅ Prev (bottom)", key="prev_bottom") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()
    with b2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages}</div>',
            unsafe_allow_html=True,
        )
    with b3:
        if st.button("Next ➡ (bottom)", key="next_bottom") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("✨ Made with ❤️ using Streamlit • Find the perfect AI tool for your needs")
