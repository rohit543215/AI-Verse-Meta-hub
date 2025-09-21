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
# Custom CSS for Dark Theme
# ---------------------------
st.markdown("""
    <style>
        /* Background */
        .stApp {
            background-color: #0d1117;
            color: #e6edf3;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }

        /* Titles */
        h1, h2, h3, h4 {
            color: #58a6ff !important;
        }

        /* Tool cards */
        .tool-card {
            background-color: #161b22;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
            margin-bottom: 1rem;
        }

        .tool-card h3 {
            margin: 0;
            color: #f0f6fc;
        }

        .tool-card p {
            font-size: 0.9rem;
            color: #8b949e;
        }

        .tag {
            display: inline-block;
            background-color: #21262d;
            color: #58a6ff;
            padding: 2px 8px;
            border-radius: 6px;
            margin-right: 5px;
            font-size: 0.8rem;
        }

        /* Buttons */
        .stLinkButton button {
            background-color: #238636 !important;
            color: white !important;
            border-radius: 10px;
            border: none;
            padding: 6px 10px;
        }

        .stLinkButton button:hover {
            background-color: #2ea043 !important;
        }

        /* Expander */
        [data-testid="stExpander"] {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
        }

    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.title("🤖 AI Tool Hub")
st.caption("⚡ A fast, beautiful directory of AI tools")

# ---------------------------
# Sidebar Filters
# ---------------------------
with st.sidebar:
    st.header("🔍 Filters")
    
    selected_category = st.selectbox(
        "Category", 
        options=["All"] + CATEGORIES,
        index=0
    )
    
    selected_plan = st.radio(
        "Pricing Plan", 
        options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"],
        index=0
    )
    
    search_query = st.text_input(
        "Search tools", 
        placeholder="Type to search..."
    ).lower()
    
    st.divider()
    
    per_page = st.slider(
        "Tools per page", 
        min_value=6, 
        max_value=24, 
        value=12, 
        step=6
    )

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
    return filtered

# ---------------------------
# Filter + Paginate Tools
# ---------------------------
filtered_tools = filter_tools(TOOLS, selected_category, selected_plan, search_query)
total_tools = len(filtered_tools)

if total_tools > 0:
    total_pages = (total_tools - 1) // per_page + 1
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        current_page = st.number_input(
            f"Page (1-{total_pages})", 
            min_value=1, 
            max_value=total_pages, 
            value=1
        )
    
    start_idx = (current_page - 1) * per_page
    end_idx = min(start_idx + per_page, total_tools)
    page_tools = filtered_tools[start_idx:end_idx]
    
    st.write(f"**Showing {len(page_tools)} of {total_tools} tools**")
    
    # Grid Display
    for i in range(0, len(page_tools), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            tool_idx = i + j
            if tool_idx < len(page_tools):
                tool = page_tools[tool_idx]
                with col:
                    st.markdown(f"""
                        <div class="tool-card">
                            <h3>{tool['name']}</h3>
                            <p><b>{tool['category']} • {tool['plan']}</b></p>
                            <p>{tool.get('blurb', '')}</p>
                            {"".join([f'<span class="tag">#{tag}</span>' for tag in tool.get('tags', [])[:3]])}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.link_button("🚀 Launch Tool", tool["link"], use_container_width=True)
                    
                    with st.expander("🔗 URL"):
                        st.code(tool["link"], language="text")
else:
    st.info("No tools found matching your filters. Try adjusting your search criteria.")

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.caption("🌙 Made with ❤️ using Streamlit • Explore the best AI tools in style")
