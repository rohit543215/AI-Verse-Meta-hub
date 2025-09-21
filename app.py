import streamlit as st
from tools import TOOLS, CATEGORIES

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="AI Tool Hub",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background-color: #f9fafb;
            color: #1f2937;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
            padding-top: 1rem;
        }
        /* Sidebar toggle (top-left button) */
        button[kind="header"] {
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 6px !important;
            padding: 6px 12px !important;
            border: none !important;
            font-weight: 500;
        }
        button[kind="header"]:hover {
            background-color: #1d4ed8 !important;
        }
        /* Top-right custom nav */
        .top-nav {
            position: fixed;
            top: 0.6rem;
            right: 1rem;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            padding: 6px 12px;
            display: flex;
            gap: 12px;
            align-items: center;
            font-size: 0.9rem;
            z-index: 9999;
        }
        .nav-item {
            cursor: pointer;
            color: #2563eb;
            font-weight: 500;
        }
        .nav-item:hover {
            text-decoration: underline;
        }
        /* Tool cards */
        .tool-card {
            background-color: #ffffff;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .tool-card:hover {
            transform: translateY(-3px);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
        }
        .tool-card h3 {
            margin: 0;
            color: #111827;
        }
        .tool-card p {
            font-size: 0.9rem;
            color: #4b5563;
        }
        /* Tags */
        .tag {
            display: inline-block;
            background-color: #e5f0ff;
            color: #1d4ed8;
            padding: 2px 8px;
            border-radius: 6px;
            margin-right: 5px;
            font-size: 0.8rem;
        }
        /* Buttons */
        .stLinkButton button {
            background-color: #2563eb !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 6px 10px;
            font-weight: 500;
        }
        .stLinkButton button:hover {
            background-color: #1d4ed8 !important;
        }
    </style>
""", unsafe_allow_html=True) [web:29]

# ---------------------------
# Fake top-right navigation (static)
# ---------------------------
st.markdown("""
<div class="top-nav">
    <span class="nav-item">🔄 Refresh</span>
    <span class="nav-item">🗂 Preview</span>
    <span class="nav-item">⚙️ Options</span>
</div>
""", unsafe_allow_html=True) [web:29]

# ---------------------------
# Header
# ---------------------------
st.title("🤖 AI Tool Hub") [web:31]
st.caption("⚡ A clean, modern directory of AI tools") [web:31]

# ---------------------------
# Sidebar Filters
# ---------------------------
with st.sidebar:
    st.header("🔍 Filters") [web:31]

    selected_category = st.selectbox(
        "Category",
        options=["All"] + CATEGORIES,
        index=0
    ) [web:31]

    selected_plan = st.radio(
        "Pricing Plan",
        options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"],
        index=0
    ) [web:31]

    search_query = st.text_input(
        "Search tools",
        placeholder="Type to search..."
    ).lower() [web:31]

    st.divider() [web:31]

    per_page = st.slider(
        "Tools per page",
        min_value=6,
        max_value=24,
        value=12,
        step=6
    ) [web:31]

# ---------------------------
# Tool Filtering Function
# ---------------------------
def filter_tools(tools, category, plan, query):
    filtered = []
    for tool in tools:
        if category != "All" and tool["category"] != category:
            continue
        if plan != "All" and tool["plan"] != plan:
            continue
        if query:
            searchable_text = (
                tool["name"].lower() + " " +
                tool.get("blurb", "").lower() + " " +
                " ".join(tool.get("tags", [])).lower()
            )
            if query not in searchable_text:
                continue
        filtered.append(tool)
    return filtered  [web:31]

# ---------------------------
# Filter + Paginate Tools
# ---------------------------
filtered_tools = filter_tools(TOOLS, selected_category, selected_plan, search_query) [web:31]
total_tools = len(filtered_tools) [web:31]
if total_tools > 0:
    total_pages = (total_tools - 1) // per_page + 1  [web:31]
    col1, col2, col3 = st.columns([2, 1, 2])  [web:31]
    with col2:
        current_page = st.number_input(
            f"Page (1-{total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1
        )  [web:31]

    start_idx = (current_page - 1) * per_page  [web:31]
    end_idx = min(start_idx + per_page, total_tools)  [web:31]
    page_tools = filtered_tools[start_idx:end_idx]  [web:31]

    st.write(f"**Showing {len(page_tools)} of {total_tools} tools**") [web:31]

    # Grid Display
    for i in range(0, len(page_tools), 3):
        cols = st.columns(3)  [web:31]
        for j, col in enumerate(cols):
            tool_idx = i + j
            if tool_idx < len(page_tools):
                tool = page_tools[tool_idx]
                with col:
                    # Card with logo + name row
                    logo_src = tool.get("logo", "")
                    st.markdown(f"""
                        <div class="tool-card">
                            <div style="display:flex; align-items:center; gap:10px;">
                                <img src="{logo_src}" alt="logo" style="width:28px; height:28px; object-fit:cover; border-radius:6px;" />
                                <h3 style="margin:0;">{tool['name']}</h3>
                            </div>
                            <p><b>{tool['category']} • {tool['plan']}</b></p>
                            <p>{tool.get('blurb', '')}</p>
                            {"".join([f'<span class="tag">#{tag}</span>' for tag in tool.get('tags', [])[:3]])}
                        </div>
                    """, unsafe_allow_html=True)  [web:29][web:16]

                    st.link_button("🚀 Launch Tool", tool["link"], use_container_width=True)  [web:31]

                    with st.expander("🔗 URL"):
                        st.code(tool["link"], language="text")  [web:29]
else:
    st.info("No tools found matching your filters. Try adjusting your search criteria.") [web:31]

# ---------------------------
# Footer
# ---------------------------
st.divider() [web:31]
st.caption("✨ Made with ❤️ using Streamlit • Find the perfect AI tool for your needs") [web:31]
