import streamlit as st
from tools import TOOLS, CATEGORIES

# Page config
st.set_page_config(
    page_title="AI Tool Hub", 
    page_icon="🤖", 
    layout="wide"
)

# Title
st.title("🤖 AI Tool Hub")
st.caption("Fast directory of AI tools")

# Filters in sidebar
with st.sidebar:
    st.header("🔍 Filters")
    
    # Category filter
    selected_category = st.selectbox(
        "Category", 
        options=["All"] + CATEGORIES,
        index=0
    )
    
    # Plan filter
    selected_plan = st.radio(
        "Pricing Plan", 
        options=["All", "Free", "Free + Paid", "Paid", "Credits + Paid"],
        index=0
    )
    
    # Search filter
    search_query = st.text_input(
        "Search tools", 
        placeholder="Type to search..."
    ).lower()
    
    st.divider()
    
    # Results per page
    per_page = st.slider(
        "Tools per page", 
        min_value=6, 
        max_value=24, 
        value=12, 
        step=6
    )

# Filter tools function
def filter_tools(tools, category, plan, query):
    filtered = []
    
    for tool in tools:
        # Category filter
        if category != "All" and tool["category"] != category:
            continue
            
        # Plan filter
        if plan != "All" and tool["plan"] != plan:
            continue
            
        # Search filter
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

# Get filtered results
filtered_tools = filter_tools(TOOLS, selected_category, selected_plan, search_query)
total_tools = len(filtered_tools)

# Pagination
if total_tools > 0:
    total_pages = (total_tools - 1) // per_page + 1
    
    # Page selector
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        current_page = st.number_input(
            f"Page (1-{total_pages})", 
            min_value=1, 
            max_value=total_pages, 
            value=1
        )
    
    # Calculate slice indices
    start_idx = (current_page - 1) * per_page
    end_idx = min(start_idx + per_page, total_tools)
    page_tools = filtered_tools[start_idx:end_idx]
    
    # Results info
    st.write(f"**Showing {len(page_tools)} of {total_tools} tools**")
    
    # Display tools in grid
    for i in range(0, len(page_tools), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            tool_idx = i + j
            if tool_idx < len(page_tools):
                tool = page_tools[tool_idx]
                
                with col:
                    with st.container(border=True):
                        # Tool header
                        st.subheader(tool["name"])
                        st.caption(f"{tool['category']} • {tool['plan']}")
                        
                        # Description
                        if tool.get("blurb"):
                            st.write(tool["blurb"])
                        
                        # Tags
                        if tool.get("tags"):
                            tag_text = " ".join([f"#{tag}" for tag in tool["tags"][:3]])
                            st.caption(tag_text)
                        
                        # Launch button
                        st.link_button(
                            "🚀 Launch Tool", 
                            tool["link"], 
                            use_container_width=True
                        )
                        
                        # URL display
                        with st.expander("🔗 URL"):
                            st.code(tool["link"], language="text")
else:
    st.info("No tools found matching your filters. Try adjusting your search criteria.")

# Footer
st.divider()
st.caption("Made with ❤️ using Streamlit • Find the perfect AI tool for your needs")
