import streamlit as st
import urllib.parse
from tools import TOOLS, CATEGORIES

st.set_page_config(page_title="AI Tool Hub", page_icon="🤖", layout="wide")
st.title("AI Tool Hub — find and launch the right AI tool")

with st.sidebar:
    st.header("Filters")
    cat = st.selectbox("What do you want to do?", options=["All"] + CATEGORIES)
    plan = st.radio("Plan", options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"], horizontal=True)
    q = st.text_input("Search (name or tags)")
    allow_preview = st.toggle("Preview in app when possible", value=True, help="Some sites block embedding.")

def matches(t):
    if cat != "All" and t["category"] != cat:
        return False
    if plan != "All" and not t["plan"].lower().startswith(plan.lower()):
        return False
    if q.strip():
        qq = q.lower()
        if qq not in t["name"].lower() and all(qq not in tag for tag in t.get("tags", [])):
            return False
    return True

results = [t for t in TOOLS if matches(t)]

def tool_card(tool):
    with st.container(border=True):
        cols = st.columns([1,3,2])
        with cols[0]:
            st.image(tool.get("logo", "assets/default.png"), width=60)
        with cols[1]:
            st.subheader(tool["name"])
            st.caption(f'{tool["category"]} • {tool["plan"]}')
            if tool.get("blurb"):
                st.write(tool["blurb"])
        with cols[2]:
            st.link_button("Launch in new tab", tool["link"], use_container_width=True)
            url = tool["link"]
            st.code(url, language="text")
        if allow_preview and tool.get("embeddable", False):
            st.markdown("Preview")
            st.components.v1.iframe(src=tool["link"], height=600)

if not results:
    st.info("No tools match the current filters. Try clearing search or changing plan.")
else:
    st.write(f"Showing {len(results)} tool(s).")
    for t in results:
        tool_card(t)

st.divider()
st.caption("Tip: Use the sidebar to refine by category, plan, and search. Add more tools in tools.py.")
