import os
import streamlit as st
from tools import TOOLS, CATEGORIES

st.set_page_config(page_title="AI Tool Hub", page_icon="🤖", layout="wide")
st.title("AI Tool Hub — fast directory of AI tools")

# --------- Safe logo without file dependency ---------
def safe_logo(src: str | None, width: int = 60):
    """
    Try to show a logo from a local path or URL.
    If anything fails, render a lightweight HTML placeholder (no file needed).
    """
    try:
        if not src:
            raise FileNotFoundError("no src")
        if src.startswith(("http://", "https://")):
            import requests
            from io import BytesIO
            r = requests.get(src, timeout=4)
            r.raise_for_status()
            st.image(BytesIO(r.content), width=width)
        else:
            path = src if os.path.isabs(src) else os.path.join("", src)
            if os.path.exists(path):
                st.image(path, width=width)
            else:
                raise FileNotFoundError(path)
    except Exception:
        st.markdown(
            f"<div style='width:{width}px;height:{width}px;border-radius:8px;"
            "background:#eef;display:flex;align-items:center;justify-content:center;"
            "font-size:26px;border:1px solid #dde;'>🧩</div>",
            unsafe_allow_html=True,
        )

# --------- Matching and card UI ----------
def matches(t, cat, plan, q):
    if cat != "All" and t["category"] != cat:
        return False
    if plan != "All" and not t["plan"].lower().startswith(plan.lower()):
        return False
    if q.strip():
        qq = q.lower()
        if qq not in t["name"].lower() and all(qq not in tag for tag in t.get("tags", [])):
            return False
    return True

def tool_card(tool, allow_preview=False):
    with st.container(border=True):
        cols = st.columns([1,3,2])
        with cols[0]:
            safe_logo(tool.get("logo"), width=60)
        with cols[1]:
            st.subheader(tool["name"])
            st.caption(f'{tool["category"]} • {tool["plan"]}')
            if tool.get("blurb"):
                st.write(tool["blurb"])
        with cols[2]:
            st.link_button("Launch in new tab", tool["link"], use_container_width=True)
            st.code(tool["link"], language="text")
        if allow_preview and tool.get("embeddable", False):
            with st.expander("Open preview (may be blocked)"):
                st.components.v1.iframe(src=tool["link"], height=600)

# --------- Sidebar filters ----------
with st.sidebar:
    st.header("Filters")
    cat = st.selectbox("Category", options=["All"] + CATEGORIES)
    plan = st.radio("Plan", options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"])
    q = st.text_input("Search (name or tags)")
    allow_preview = st.toggle("Enable in-app previews", value=False, help="Off by default for speed.")
    st.divider()
    PAGE_SIZE = st.slider("Cards per page", min_value=6, max_value=24, value=12, step=3)

# --------- Filter + paginate ----------
results = [t for t in TOOLS if matches(t, cat, plan, q)]
total = len(results)
page_count = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)

col_a, col_b, col_c = st.columns([2,2,6])
with col_a:
    page = st.number_input("Page", min_value=1, max_value=page_count, value=1, step=1)
with col_b:
    st.write(f"Total tools: {total}")

start = (page - 1) * PAGE_SIZE
end = min(start + PAGE_SIZE, total)
page_results = results[start:end]

st.write(f"Showing {len(page_results)} of {total} tool(s)")

if not page_results:
    st.info("No tools match the current filters.")
else:
    grid_cols = st.columns(3)
    for idx, t in enumerate(page_results):
        with grid_cols[idx % 3]:
            tool_card(t, allow_preview=allow_preview)

st.caption("Logos render instantly if stored locally in assets/; remote URLs fall back to a built‑in placeholder.")
