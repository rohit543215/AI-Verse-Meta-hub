import streamlit as st
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
    "scroll_ticket": 0,
    "last_scrolled_ticket": -1,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# Helpers
# ---------------------------
def request_scroll():
    st.session_state.scroll_ticket += 1

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
# Early clear path
# ---------------------------
if st.session_state.clear_flag:
    st.session_state.filter_category = "All"
    st.session_state.filter_plan = "All"
    st.session_state.filter_search = ""
    st.session_state.current_page = 1
    st.session_state.show_previews = False
    st.session_state.clear_flag = False
    request_scroll()
    st.rerun()

# ---------------------------
# Enhanced CSS with beautiful styling
# ---------------------------
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
  --primary-bg: #FAFBFF;
  --card-bg: #FFFFFF;
  --surface-bg: #F8FAFC;
  --border-light: #E2E8F0;
  --border-medium: #CBD5E1;
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-muted: #64748B;
  --accent-primary: #3B82F6;
  --accent-secondary: #8B5CF6;
  --accent-hover: #2563EB;
  --success: #10B981;
  --success-light: #D1FAE5;
  --warning: #F59E0B;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-xl: 20px;
}

/* App base styling */
html, body, .stApp {
  background: var(--primary-bg);
  color: var(--text-primary);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  scroll-behavior: smooth;
  font-feature-settings: 'cv03', 'cv04', 'cv11';
}

/* Remove default Streamlit padding */
.block-container {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

/* Header styling */
.app-header {
  text-align: center;
  margin: 0 0 3rem;
  padding: 2rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--border-radius-xl);
  color: white;
  position: relative;
  overflow: hidden;
}

.app-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  pointer-events: none;
}

.app-header h1 {
  margin: 0 0 0.5rem;
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: -0.02em;
  background: linear-gradient(45deg, #fff, #e2e8f0);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
  z-index: 1;
}

.app-header p {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 400;
  opacity: 0.95;
  position: relative;
  z-index: 1;
}

/* About section */
.about-card {
  background: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.about-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}

.about-card h2 {
  margin: 0 0 1rem;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 1.5rem;
}

.about-card p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.6;
}

/* Filters bar */
.filters-card {
  position: sticky;
  top: 1rem;
  z-index: 10;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-lg);
}

/* Enhanced button styling */
.stButton > button {
  width: 100%;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-light);
  background: var(--card-bg);
  color: var(--text-primary);
  font-weight: 600;
  font-size: 0.95rem;
  padding: 0.75rem 1rem;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}

.stButton > button:hover {
  border-color: var(--accent-primary);
  background: var(--surface-bg);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.stButton > button:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

.stButton > button:focus {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

/* Section headers */
.section-label {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
}

/* Tool cards */
.tool-card {
  background: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-md);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.tool-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-accent);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: var(--border-medium);
}

.tool-card:hover::before {
  transform: scaleX(1);
}

.tool-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.tool-card p {
  margin: 0.75rem 0;
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.5;
}

/* Enhanced badges */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: var(--surface-bg);
  color: var(--text-secondary);
  padding: 0.375rem 0.75rem;
  border: 1px solid var(--border-light);
  border-radius: 9999px;
  font-size: 0.8125rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.badge.plan {
  background: var(--success-light);
  color: var(--success);
  border-color: var(--success);
}

.badge.category {
  background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%);
  color: var(--accent-primary);
  border-color: var(--accent-primary);
}

.tag {
  display: inline-block;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: var(--text-secondary);
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  margin: 0.25rem 0.375rem 0.25rem 0;
  font-size: 0.8125rem;
  font-weight: 500;
  border: 1px solid var(--border-light);
  transition: all 0.2s ease;
}

.tag:hover {
  background: var(--accent-primary);
  color: white;
  transform: translateY(-1px);
}

/* Enhanced action buttons */
.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--gradient-primary);
  color: white !important;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius-md);
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9375rem;
  box-shadow: var(--shadow-md);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
}

.link-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  filter: brightness(1.05);
}

.soft-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--border-radius-md);
  border: 1px solid var(--border-light);
  background: var(--card-bg);
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.soft-btn:hover {
  border-color: var(--accent-primary);
  background: var(--surface-bg);
  color: var(--accent-primary);
  transform: translateY(-1px);
}

/* Meta row styling */
.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
  margin-top: 0.5rem;
}

/* Enhanced Editor's Picks */
.picks-card {
  background: linear-gradient(135deg, #fdf4ff 0%, #faf5ff 100%);
  border: 1px solid #e9d5ff;
  border-radius: var(--border-radius-lg);
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}

.picks-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8b5cf6 0%, #a855f7 100%);
}

.picks-title {
  margin: 0 0 1.25rem;
  font-size: 1.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: center;
}

.pick-item {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: var(--border-radius-md);
  padding: 1rem;
  margin-bottom: 0.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.pick-item:hover {
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.15);
}

.pick-item:last-child {
  margin-bottom: 0;
}

.pick-item .k {
  color: var(--accent-secondary);
  font-weight: 700;
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: block;
  margin-bottom: 0.25rem;
}

.pick-item .v {
  color: var(--text-primary);
  font-weight: 800;
  font-size: 1.125rem;
  display: block;
  margin-bottom: 0.5rem;
}

.pick-item .note {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  line-height: 1.5;
  display: block;
}

/* Enhanced Why TORO section */
.toro-card.big {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #ffffff 100%);
  border: 1px solid #bae6fd;
  border-radius: var(--border-radius-lg);
  padding: 2rem 1.5rem;
  box-shadow: var(--shadow-lg);
  margin-top: 1rem;
  position: relative;
  overflow: hidden;
}

.toro-card.big::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #0ea5e9 0%, #3b82f6 100%);
}

.toro-badge {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border: 1px solid #93c5fd;
  font-size: 0.875rem;
  font-weight: 700;
  padding: 0.5rem 1rem;
  display: inline-block;
  border-radius: 9999px;
  margin-bottom: 1rem;
}

.toro-eyebrow {
  color: #0369a1;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin: 0 0 0.5rem;
}

.toro-title {
  margin: 0 0 1rem;
  font-size: 1.875rem;
  line-height: 1.2;
  font-weight: 800;
  color: #0c4a6e;
}

.toro-sub {
  color: var(--text-secondary);
  font-size: 1.125rem;
  line-height: 1.6;
  margin: 0 0 1.5rem;
}

.toro-bullets {
  margin: 0;
  padding-left: 1.5rem;
}

.toro-bullets li {
  color: var(--text-secondary);
  margin: 0.75rem 0;
  font-size: 1rem;
  line-height: 1.6;
}

/* Enhanced pagination */
.pagination {
  position: sticky;
  bottom: 1rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid var(--border-light);
  border-radius: var(--border-radius-lg);
  padding: 1rem;
  text-align: center;
  margin: 2rem 0;
  box-shadow: var(--shadow-lg);
}

.page-info {
  display: inline-block;
  margin: 0 1rem;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1rem;
}

/* Scroll target styling */
.results-anchor {
  position: relative;
  top: -100px;
  visibility: hidden;
}

/* Empty card placeholder */
.empty-card {
  height: 0.1px;
  margin-bottom: 1.5rem;
}

/* Responsive design */
@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2.5rem;
  }
  
  .app-header p {
    font-size: 1.125rem;
  }
  
  .filters-card {
    padding: 1rem;
  }
  
  .tool-card {
    padding: 1.25rem;
  }
  
  .toro-title {
    font-size: 1.5rem;
  }
}

/* Dark theme support */
[data-theme="dark"] {
  --primary-bg: #0f172a;
  --card-bg: #1e293b;
  --surface-bg: #334155;
  --border-light: #475569;
  --border-medium: #64748b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
}

[data-theme="dark"] .stButton > button {
  background: var(--card-bg);
  color: var(--text-primary);
  border-color: var(--border-light);
}

[data-theme="dark"] .stButton > button:hover {
  background: var(--surface-bg);
  border-color: var(--accent-primary);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Enhanced Header
# ---------------------------
st.markdown("""
<div class="app-header">
  <h1>🤖 TORO</h1>
  <p>Discover and explore the best AI tools with intelligent filtering and instant previews</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Enhanced About section
# ---------------------------
st.markdown("""
<div class="about-card">
  <h2>✨ Welcome to TORO</h2>
  <p>Your ultimate destination to <strong>discover, explore, and launch AI tools</strong> effortlessly. 
  Filter by categories and pricing, browse beautiful cards, preview embeddable sites, and launch tools in one click.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# Enhanced Filters bar
# ---------------------------
st.markdown('<div class="filters-card">', unsafe_allow_html=True)

rail_col, main_col = st.columns([3.0, 9.0], gap="large")

with rail_col:
    st.markdown('<div class="section-label">📂 Categories</div>', unsafe_allow_html=True)
    cat_options = ["All"] + CATEGORIES
    current_cat = st.session_state.filter_category
    for c in cat_options:
        if st.button(f"{c}", key=f"cat_{c}", use_container_width=True):
            if c != current_cat:
                st.session_state.filter_category = c
                st.session_state.current_page = 1
                request_scroll()
                st.rerun()

with main_col:
    top_l, top_m, top_r = st.columns([3.8, 4.4, 3.8], gap="large")

    with top_l:
        st.markdown('<div class="section-label">🔍 Search</div>', unsafe_allow_html=True)
        def on_search_change():
            reset_page()
            request_scroll()
        st.text_input(
            "",
            placeholder="Search by name, tags, or description...",
            key="filter_search",
            on_change=on_search_change,
            label_visibility="collapsed",
        )
        if st.button("🗑️ Clear all filters", use_container_width=True):
            st.session_state.clear_flag = True
            request_scroll()
            st.rerun()

    with top_m:
        st.markdown('<div class="section-label">💳 Pricing</div>', unsafe_allow_html=True)
        def on_plan_change():
            reset_page()
            request_scroll()
        plans = ["All", "Free", "Free + Paid", "Paid", "Credits + Paid"]
        st.selectbox(
            "",
            options=plans,
            index=plans.index(st.session_state.filter_plan) if st.session_state.filter_plan in plans else 0,
            key="filter_plan",
            on_change=on_plan_change,
            label_visibility="collapsed",
        )
        st.toggle("🖼️ Show embeddable previews", value=st.session_state.show_previews, key="show_previews")

        st.markdown(
            """
            <div class="toro-card big">
              <div class="toro-badge">✨ Why TORO?</div>
              <div class="toro-eyebrow">Faster Discovery</div>
              <h3 class="toro-title">Find the perfect AI tool in minutes</h3>
              <p class="toro-sub">Browse intelligently with advanced filters, stunning previews, and seamless navigation—designed for lightning-fast decision‑making.</p>
              <ul class="toro-bullets">
                <li>🎯 <strong>Smart Filtering:</strong> Category and pricing filters make discovery effortless</li>
                <li>🎨 <strong>Beautiful Cards:</strong> Rich previews with logos, descriptions, and interactive tags</li>
                <li>👁️ <strong>Instant Previews:</strong> Test embeddable tools without leaving TORO</li>
                <li>⚡ <strong>Smooth Navigation:</strong> Clean pagination with 12 tools per page for optimal browsing</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_r:
        st.markdown(
            """
            <div class="picks-card">
              <h3 class="picks-title">🏆 Editor's Choice</h3>
              <div class="pick-item">
                <span class="k">Best General Assistant</span>
                <span class="v">ChatGPT</span>
                <span class="note">Leading conversational AI with broad capabilities for writing, coding, analysis, and creative tasks</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Image Generation</span>
                <span class="v">Midjourney</span>
                <span class="note">Premium AI art generator known for stunning, high-quality visual creations and artistic styles</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Video Creation</span>
                <span class="v">Runway ML</span>
                <span class="note">Professional video editing and generation platform with cutting-edge AI capabilities</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Meeting Assistant</span>
                <span class="v">Otter.ai</span>
                <span class="note">Intelligent transcription service with real-time collaboration and searchable meeting notes</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Automation</span>
                <span class="v">Zapier</span>
                <span class="note">Connect 5000+ apps and automate workflows without coding, powered by AI integrations</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Research Tool</span>
                <span class="v">Perplexity AI</span>
                <span class="note">AI-powered search engine providing accurate answers with real-time citations and sources</span>
              </div>
              <div class="pick-item">
                <span class="k">Best Writing Assistant</span>
                <span class="v">Grammarly</span>
                <span class="note">Advanced writing enhancement with grammar checking, tone suggestions, and style improvements</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Results anchor with smooth scrolling
# ---------------------------
st.markdown('<div class="results-anchor" id="results-section"></div>', unsafe_allow_html=True)
st.header("🎯 Results", anchor="results")

# ---------------------------
# Data and pagination logic
# ---------------------------
filtered_tools = filter_tools(TOOLS)
total_tools = len(filtered_tools)
per_page = 12
total_pages = (total_tools - 1) // per_page + 1 if total_tools > 0 else 1
if st.session_state.current_page > total_pages:
    st.session_state.current_page = total_pages

# ---------------------------
# Enhanced scroll trigger with JavaScript
# ---------------------------
if st.session_state.scroll_ticket > st.session_state.last_scrolled_ticket:
    st.markdown("""
    <script>
        setTimeout(function() {
            const element = document.getElementById('results-section') || 
                           document.querySelector('[data-testid="stHeader"]') ||
                           document.querySelector('h1[id*="results"]');
            if (element) {
                element.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start',
                    inline: 'nearest'
                });
            }
        }, 150);
    </script>
    """, unsafe_allow_html=True)
    st.session_state.last_scrolled_ticket = st.session_state.scroll_ticket

# ---------------------------
# Enhanced pagination
# ---------------------------
if total_tools == 0:
    st.info("🔍 No tools found matching your criteria. Try broadening your search or clearing filters to see more results.")
else:
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1, 2, 1], gap="large")
    with p1:
        if st.button("⬅️ Previous", key="prev_top") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            request_scroll()
            st.rerun()
    with p2:
        st.markdown(
            f'<div class="page-info">📄 Page {st.session_state.current_page} of {total_pages} • {total_tools} tools found</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("Next ➡️", key="next_top") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            request_scroll()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # Enhanced results grid
    # ---------------------------
    start = (st.session_state.current_page - 1) * per_page
    end = min(start + per_page, total_tools)
    page_tools = filtered_tools[start:end]

    # Display tools in a beautiful grid layout
    for i in range(0, max(len(page_tools), 3), 3):
        row_tools = page_tools[i:i+3]
        cols = st.columns(3, gap="large")
        while len(row_tools) < 3:
            row_tools.append(None)
        
        for col, tool in zip(cols, row_tools):
            with col:
                if tool is None:
                    st.markdown('<div class="empty-card"></div>', unsafe_allow_html=True)
                    continue

                # Extract tool information
                logo = safe_str(tool.get("logo", ""))
                name = safe_str(tool.get("name", "Unknown Tool"))
                blurb = safe_str(tool.get("blurb", "No description available"))
                category = safe_str(tool.get('category', 'Uncategorized'))
                plan = safe_str(tool.get("plan", "Unknown"))
                tags = tool.get("tags", [])[:4]  # Limit to 4 tags for clean layout
                link = safe_str(tool.get("link", "#"))
                embeddable = bool(tool.get("embeddable", False))

                # Render enhanced tool card
                st.markdown(f"""
                <div class="tool-card">
                  <div style="display:flex; gap:1rem; align-items:flex-start; margin-bottom:1rem;">
                    <div style="flex-shrink:0;">
                      <img 
                        src="{logo}" 
                        alt="{name} logo" 
                        style="width:56px; height:56px; object-fit:cover; border-radius:12px; border:2px solid var(--border-light); box-shadow:var(--shadow-sm);" 
                        onerror="this.style.display='none'"
                      />
                    </div>
                    <div style="flex:1; min-width:0;">
                      <h3>{name}</h3>
                      <div class="meta-row">
                        <span class="badge category">📁 {category}</span>
                        <span class="badge plan">💰 {plan}</span>
                        {f'<span class="badge" style="background:linear-gradient(135deg,#ecfdf5 0%,#d1fae5 100%); color:#065f46; border-color:#10b981;">🧩 Embeddable</span>' if embeddable else ''}
                      </div>
                    </div>
                  </div>
                  
                  <p>{blurb}</p>
                  
                  <div style="margin:1rem 0;">
                    {"".join([f'<span class="tag">#{tag}</span>' for tag in tags])}
                  </div>
                  
                  <div style="display:flex; gap:0.75rem; align-items:center; flex-wrap:wrap; margin-top:1.5rem;">
                    <a class="link-btn" href="{link}" target="_blank" rel="noreferrer noopener">
                      🚀 Launch Tool
                    </a>
                    <a class="soft-btn" href="{link}" target="_blank" rel="nofollow noopener" style="text-decoration:none;">
                      🔗 Visit Site
                    </a>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Show embeddable preview if enabled
                if embeddable and st.session_state.show_previews:
                    with st.container():
                        st.components.v1.iframe(link, height=520, scrolling=True)

    # ---------------------------
    # Bottom pagination
    # ---------------------------
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1, 2, 1], gap="large")
    with p1:
        if st.button("⬅️ Previous", key="prev_bottom") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            request_scroll()
            st.rerun()
    with p2:
        st.markdown(
            f'<div class="page-info">📄 Page {st.session_state.current_page} of {total_pages} • {total_tools} tools found</div>',
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("Next ➡️", key="next_bottom") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            request_scroll()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# Enhanced Footer
# ---------------------------
st.markdown('<div style="margin-top:4rem;"></div>', unsafe_allow_html=True)
st.divider()

# Footer content
footer_col1, footer_col2 = st.columns([2, 1], gap="large")

with footer_col1:
    st.markdown("""
    <div style="padding:1rem 0;">
        <h4 style="margin:0 0 0.5rem; color:var(--text-primary); font-weight:700;">🎓 More Resources</h4>
        <p style="margin:0; color:var(--text-secondary); font-size:0.95rem;">
            Discover additional free tools and resources designed specifically for students and learners.
        </p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.link_button(
        "🧰 Student Tools Collection", 
        "https://free-tools-ijpl7qrhvjg4gdhvhnpvae.streamlit.app/", 
        type="primary", 
        use_container_width=True
    )

# Copyright and credits
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; border-top:1px solid var(--border-light); margin-top:2rem;">
    <p style="margin:0; color:var(--text-muted); font-size:0.9rem;">
        ✨ <strong>TORO</strong> - Your AI Tools Discovery Platform<br/>
        Made with ❤️ by <strong>Girish Joshi</strong> in India 🇮🇳
    </p>
    <p style="margin:0.5rem 0 0; color:var(--text-muted); font-size:0.8rem; opacity:0.8;">
        Find the perfect AI tool for every use case • Updated daily with the latest innovations
    </p>
</div>
""", unsafe_allow_html=True)
