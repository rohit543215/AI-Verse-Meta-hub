import streamlit as st
import streamlit.components.v1 as components
from tools import TOOLS, CATEGORIES

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Deep Store: For AI Tools",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
  body {
    font-family: 'Inter', sans-serif;
  }

  .stApp {
    background-color: #f8fafc;
    color: #1f2937;
  }

  /* Header */
  .app-header {
    text-align: center;
    margin-top: -30px;
    margin-bottom: 20px;
  }
  .app-header h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #111827;
  }
  .app-header p {
    font-size: 1rem;
    color: #6b7280;
  }

  /* Filters box */
  .filters-box {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
  }

  .filter-label {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 6px;
    color: #374151;
  }

  /* Plan pills */
  .plan-pill {
    display: inline-block;
    padding: 6px 12px;
    margin-right: 6px;
    margin-bottom: 6px;
    border-radius: 20px;
    border: 1px solid #d1d5db;
    background: #f9fafb;
    color: #374151;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .plan-pill.active {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
  }
  .plan-pill:hover {
    background: #2563eb;
    color: white;
  }

  /* Tool cards */
  .tool-card {
    background-color: #ffffff;
    padding: 1.4rem;
    border-radius: 14px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .tool-card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
  }
  .tool-card h3 {
    margin: 0;
    font-size: 1.2rem;
    color: #111827;
    font-weight: 600;
  }
  .tool-card p {
    font-size: 0.9rem;
    color: #4b5563;
    margin: 6px 0;
  }

  .tag {
    display: inline-block;
    background-color: #eff6ff;
    color: #2563eb;
    padding: 3px 8px;
    border-radius: 6px;
    margin-right: 4px;
    font-size: 0.75rem;
    font-weight: 500;
  }

  /* Pagination */
  .pagination {
    text-align: center;
    margin: 20px 0;
  }
  .pagination button {
    background: #2563eb !important;
    color: white !important;
    border-radius: 6px;
    border: none;
    padding: 6px 14px;
    margin: 0 5px;
    font-size: 0.9rem;
  }
  .pagination button:hover {
    background: #1d4ed8 !important;
  }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="app-header">
  <h1>🤖 Deep Store</h1>
  <p>Discover the best AI tools, organized and easy to explore</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Filters
# ---------------------------
st.markdown('<div class="filters-box">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 3])

with col1:
    st.markdown('<div class="filter-label">Category</div>', unsafe_allow_html=True)
    selected_category = st.selectbox(
        "",
        options=["All"] + CATEGORIES,
        index=0,
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="filter-label">Search</div>', unsafe_allow_html=True)
    search_query = st.text_input(
        "",
        placeholder="Search tools by name, tags, or description"
    ).lower()

# Pricing plan pills
st.markdown('<div class="filter-label">Pricing Plan</div>', unsafe_allow_html=True)
plan_options = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
plan_cols = st.columns(len(plan_options))
selected_plan = "All"

for i, plan in enumerate(plan_options):
    if plan_cols[i].button(plan, key=f"plan_{plan}"):
        selected_plan = plan

# Default selection if none pressed
if "selected_plan" not in st.session_state:
    st.session_state["selected_plan"] = "All"
if selected_plan != "All":
    st.session_state["selected_plan"] = selected_plan

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Tool Filtering Function
# ---------------------------
def filter_tools(tools, category, plan, query):
    filtered = []
    for tool in tools:
        if category != "All" and tool["category"] != category:
            continue
        if st.session_state["selected_plan"] != "All" and tool["plan"] != st.session_state["selected_plan"]:
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
# Filter + Paginate
# ---------------------------
per_page = 9
filtered_tools = filter_tools(TOOLS, selected_category, selected_plan, search_query)
total_tools = len(filtered_tools)

if total_tools > 0:
    total_pages = (total_tools - 1) // per_page + 1
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = 1

    # Pagination controls
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    prev, next = st.columns([1,1])
    with prev:
        if st.button("⬅ Prev") and st.session_state["current_page"] > 1:
            st.session_state["current_page"] -= 1
    with next:
        if st.button("Next ➡") and st.session_state["current_page"] < total_pages:
            st.session_state["current_page"] += 1
    st.markdown('</div>', unsafe_allow_html=True)

    start_idx = (st.session_state["current_page"] - 1) * per_page
    end_idx = min(start_idx + per_page, total_tools)
    page_tools = filtered_tools[start_idx:end_idx]

    # Grid Display
    for i in range(0, len(page_tools), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            tool_idx = i + j
            if tool_idx < len(page_tools):
                tool = page_tools[tool_idx]
                with col:
                    logo_src = tool.get("logo", "")
                    st.markdown(f"""
                        <div class="tool-card">
                            <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
                                <img src="{logo_src}" alt="logo" style="width:36px; height:36px; object-fit:cover; border-radius:8px;" />
                                <h3>{tool['name']}</h3>
                            </div>
                            <p><b>{tool['category']} • {tool['plan']}</b></p>
                            <p>{tool.get('blurb', '')}</p>
                            {"".join([f'<span class="tag">#{tag}</span>' for tag in tool.get('tags', [])[:4]])}
                        </div>
                    """, unsafe_allow_html=True)

                    st.link_button("🚀 Launch Tool", tool["link"], use_container_width=True)

                    if tool.get("embeddable", False):
                        components.iframe(tool["link"], height=520)
else:
    st.info("No tools found matching your filters. Try adjusting your search criteria.")

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.caption("✨ Made with ❤️ using Streamlit • Find the perfect AI tool for your needs")
