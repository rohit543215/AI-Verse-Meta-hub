import streamlit as st
import streamlit.components.v1 as components
from tools import TOOLS, CATEGORIES

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Deep Store: For AI Tools",
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
    "filter_per_page": 12,
    "current_page": 1,
    "clear_flag": False,
    "show_previews": False,  # toggle to render iframes
    "sort_by": "Relevance",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v  # persists across reruns [web:79]

# Clear filters safely before widgets mount
if st.session_state.clear_flag:
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.filter_per_page = 12
    st.session_state.current_page = 1
    st.session_state.sort_by = "Relevance"
    st.session_state.show_previews = False
    st.session_state.clear_flag = False
    st.rerun()  # safe pre-widget rerun [web:79]

# ---------------------------
# Helpers
# ---------------------------
def reset_page():
    st.session_state.current_page = 1  # keep pagination coherent on filter changes [web:79]

def safe_str(x):
    return x if isinstance(x, str) else ""

def sort_tools(tools, by):
    if by == "Name A→Z":
        return sorted(tools, key=lambda t: safe_str(t.get("name", "")).lower())
    if by == "Name Z→A":
        return sorted(tools, key=lambda t: safe_str(t.get("name", "")).lower(), reverse=True)
    if by == "Plan (Free first)":
        order = {"Free": 0, "Free + Paid": 1, "Credits + Paid": 2, "Paid": 3}
        return sorted(tools, key=lambda t: order.get(t.get("plan", "Paid"), 99))
    return tools  # Relevance: preserve curated order [web:79]

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
    return filtered  # stateful filter pattern [web:79]

# ---------------------------
# CSS (light theme palette)
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
html, body, .stApp { background-color: var(--bg); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; }
.app-header { text-align: center; margin: 10px 0 22px 0; }
.app-header h1 { margin: 6px 0; font-size: 2rem; letter-spacing: 0.2px; color: #0F172A; }
.app-header p { margin: 0; color: var(--muted); font-size: 0.98rem; }

.filters-card {
  position: sticky; top: 0; z-index: 5;
  background: #FFFFFFF2; border: 1px solid var(--border);
  padding: 14px; border-radius: 14px;
  box-shadow: 0 10px 30px rgba(17,24,39,0.05);
  margin-bottom: 18px; backdrop-filter: blur(6px);
}

.tool-card {
  background: var(--card);
  padding: 16px; border-radius: 14px; border: 1px solid var(--border);
  box-shadow: 0 6px 18px rgba(2,6,23,0.06);
  transition: transform 0.18s ease, box-shadow 0.18s ease, border 0.18s ease;
  margin-bottom: 26px;
}
.tool-card:hover { transform: translateY(-4px); box-shadow: 0 14px 26px rgba(2,6,23,0.10); border-color: var(--ring); }
.tool-card h3 { margin: 0; font-size: 1.05rem; color: #0F172A; }
.tool-card p { margin: 8px 0 6px 0; color: #374151; font-size: 0.92rem; }
.tool-meta { color: #6B7280; font-size: 0.83rem; margin-top: 2px; }

.badge { display: inline-flex; align-items:center; gap:6px; background: #EEF2FF; color: #3730A3; padding: 4px 10px; border: 1px solid #E0E7FF; border-radius: 999px; font-size: 0.74rem; font-weight: 700; }
.badge.plan { background: #ECFDF5; color: #065F46; border-color: #D1FAE5; }

.tag { display: inline-block; background: #EEF2FF; color: #4338CA; padding: 5px 10px; border-radius: 999px; margin-right: 6px; margin-top: 6px; font-size: 0.76rem; font-weight: 700; border: 1px solid #E0E7FF; }

.link-btn { display: inline-block; background: linear-gradient(180deg, #2563EB, #1D4ED8); color: #fff !important; padding: 9px 12px; border-radius: 10px; text-decoration: none; font-weight: 700; border: 0; box-shadow: 0 8px 20px rgba(29,78,216,0.25); }
.link-btn:hover { filter: brightness(1.07); }

.soft-btn { display:inline-block; padding: 8px 12px; border-radius: 10px; border: 1px solid var(--border); background: #F8FAFC; color: var(--text); font-weight: 700; }
.soft-btn:hover { border-color: var(--ring); }

.pagination {
  position: sticky; bottom: 12px; background: rgba(255,255,255,0.85);
  backdrop-filter: blur(6px); border: 1px solid var(--border); border-radius: 12px;
  padding: 8px; text-align: center; margin: 18px 0;
}
.pagination .page-info { display: inline-block; margin: 0 12px; color: var(--text); font-weight: 700; }

.kbd { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-size: 0.78rem; padding: 2px 6px; border: 1px solid var(--border); border-bottom-width: 2px; border-radius: 6px; background: #F3F4F6; color: #374151; }

.meta-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-top:4px;}
.empty-card { height: 0.1px; margin-bottom: 26px; }
</style>
""",
    unsafe_allow_html=True,
)  # light colors align with Streamlit light theme [web:79]

# ---------------------------
# Header
# ---------------------------
st.markdown(
    """
<div class="app-header">
  <h1>🤖 Deep Store</h1>
  <p>Discover high-quality AI tools — filter, preview, and launch fast.</p>
</div>
""",
    unsafe_allow_html=True,
)  # header [web:79]

# ---------------------------
# Filters
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)
fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([2.2, 3.8, 2.0, 2.0, 2.0], gap="large")
with fcol1:
    st.markdown("Category")
    st.selectbox(
        "",
        options=["All"] + CATEGORIES,
        index=(["All"] + CATEGORIES).index(st.session_state.filter_category),
        key="filter_category",
        on_change=lambda: reset_page(),
        label_visibility="collapsed",
    )  # state usage [web:79]
with fcol2:
    st.markdown("Search")
    st.text_input(
        "",
        placeholder="Search by name, tags, or description  ⌘/Ctrl+K",
        key="filter_search",
        on_change=lambda: reset_page(),
        label_visibility="collapsed",
    )  # search pattern [web:79]
with fcol3:
    st.markdown("Pricing")
    plans = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
    st.selectbox(
        "",
        options=plans,
        index=plans.index(st.session_state.filter_plan) if st.session_state.filter_plan in plans else 0,
        key="filter_plan",
        on_change=lambda: reset_page(),
        label_visibility="collapsed",
    )  # pricing filter [web:79]
with fcol4:
    st.markdown("Sort")
    st.selectbox(
        "",
        options=["Relevance", "Name A→Z", "Name Z→A", "Plan (Free first)"],
        key="sort_by",
        on_change=lambda: reset_page(),
        label_visibility="collapsed",
    )  # sorting [web:79]
with fcol5:
    st.markdown("Per page")
    st.slider("", 6, 24, step=3, key="filter_per_page", on_change=lambda: reset_page(), label_visibility="collapsed")  # page size [web:79]

tcol1, tcol2, tcol3 = st.columns([2, 5, 3], gap="large")
with tcol1:
    st.toggle("Embeddable preview", value=st.session_state.show_previews, key="show_previews")  # preview gate [web:15]
with tcol2:
    st.write("")
with tcol3:
    c1, c2 = st.columns([1, 1])
    with c1:
        st.caption("Tip: Press")
        st.markdown('<span class="kbd">Ctrl</span> + <span class="kbd">K</span> to focus search', unsafe_allow_html=True)  # hint [web:79]
    with c2:
        if st.button("Clear filters"):
            st.session_state.clear_flag = True
            st.rerun()  # reset + rerun [web:79]
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Data
# ---------------------------
filtered_tools = sort_tools(filter_tools(TOOLS), st.session_state.sort_by)
total_tools = len(filtered_tools)
per_page = st.session_state.filter_per_page
total_pages = (total_tools - 1) // per_page + 1 if total_tools > 0 else 1
if st.session_state.current_page > total_pages:
    st.session_state.current_page = total_pages  # safety [web:79]

# ---------------------------
# Top pagination
# ---------------------------
if total_tools == 0:
    st.info("No tools found. Try broadening search or clearing filters.")
else:
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    pcol1, pcol2, pcol3 = st.columns([1, 2, 1], gap="large")
    with pcol1:
        if st.button("⬅ Prev", key="prev_top") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()  # immediate update [web:79]
    with pcol2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages} — {total_tools} tools</div>',
            unsafe_allow_html=True,
        )
    with pcol3:
        if st.button("Next ➡", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()  # immediate update [web:79]
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # Results grid
    # ---------------------------
    start = (st.session_state.current_page - 1) * per_page
    end = min(start + per_page, total_tools)
    page_tools = filtered_tools[start:end]

    for i in range(0, max(len(page_tools), 3), 3):
        row_tools = page_tools[i: i + 3]
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
                meta = f"{safe_str(tool.get('category',''))}"
                plan = safe_str(tool.get("plan", ""))
                tags = tool.get("tags", [])[:4]
                link = safe_str(tool.get("link", "#"))
                emb = bool(tool.get("embeddable", False))

                st.markdown(
                    f"""
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
                    """,
                    unsafe_allow_html=True,
                )

                # Embeddable preview toggle
                if emb and st.session_state.show_previews:
                    # Use explicit height and allow scrolling for safer UX in iframes [web:15]
                    components.iframe(link, height=520, scrolling=True)

    # ---------------------------
    # Bottom pagination
    # ---------------------------
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 2, 1], gap="large")
    with b1:
        if st.button("⬅ Prev (bottom)", key="prev_bottom") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()  # update page [web:79]
    with b2:
        st.markdown(
            f'<div class="page-info">Page {st.session_state.current_page} of {total_pages}</div>',
            unsafe_allow_html=True,
        )
    with b3:
        if st.button("Next ➡ (bottom)", key="next_bottom") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()  # update page [web:79]
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Footer CTA + footer
# ---------------------------
st.divider()
st.link_button(
    "🎓 more tools for student",
    "https://free-tools-ijpl7qrhvjg4gdhvhnpvae.streamlit.app/",
    type="primary",
    icon="🧰",
    use_container_width=True,
)  # opens external URL in a new tab [web:55]
st.caption("✨ Made with ❤️ By Girish Joshi • Find the perfect AI tool for every use case")

