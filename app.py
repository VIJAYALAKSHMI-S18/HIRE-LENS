import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="HIRELENS — AI RESUME ANALYZER & ATS COMPATIBILITY PLATFORM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.authentication import init_auth_session, is_logged_in, logout, render_login_signup
from utils.database import init_db
from utils.theme import apply_theme

from views import home, analyzer, dashboard, jobs, history, profile, settings, rewriter, explainability, skim, ab_testing

def main():
    # Initialize SQLite Database & Authentication State
    init_db()
    init_auth_session()

    # Apply Custom Premium Theme & Custom Cursor
    dark_mode = st.session_state.get("dark_mode", True)
    reduced_motion = st.session_state.get("reduced_motion", False)
    apply_theme(dark_mode=dark_mode, reduced_motion=reduced_motion)

    # Force UPPERCASE styling on sidebar and headings
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] button,
    section[data-testid="stSidebar"] span {
        text-transform: uppercase !important;
        letter-spacing: 0.5px;
    }
    h1, h2, h3, h4, .stButton > button {
        text-transform: uppercase !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Branding & Navigation
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        <h1 style='margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #4F8CFF 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🎯 HIRELENS
        </h1>
        <p style='margin: 4px 0 0 0; font-size: 0.85rem; color: #38BDF8; font-weight: 600;'>
            SEE YOUR RESUME THROUGH THE EYES OF RECRUITERS.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Account Session Status in Sidebar
    if is_logged_in():
        user = st.session_state.user
        st.sidebar.markdown(f"""
        <div style='background: rgba(79, 140, 255, 0.1); border: 1px solid rgba(79, 140, 255, 0.2); padding: 12px; border-radius: 12px; margin-bottom: 20px;'>
            <div style='font-size: 13px; color: #94A3B8;'>LOGGED IN AS:</div>
            <div style='font-weight: 700; color: #F8FAFC;'>{user['name'].upper()}</div>
            <div style='font-size: 12px; color: #38BDF8;'>{user['email'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.info("💡 LOG IN OR REGISTER TO SAVE YOUR ATS ANALYSES AND VIEW CAREER ANALYTICS.")

    # Page Selection Router
    pages_map = {
        "🏠 HOME": "home",
        "🔍 RESUME ANALYZER": "analyzer",
        "📊 DASHBOARD": "dashboard",
        "✨ BULLET REWRITER": "rewriter",
        "🔍 WHY THIS SCORE?": "explainability",
        "👁 RECRUITER SKIM": "skim",
        "📊 A/B TESTING": "ab_testing",
        "💼 COMPARE JOBS": "jobs",
        "🕘 HISTORY": "history",
        "👤 PROFILE": "profile",
        "⚙️ SETTINGS": "settings"
    }

    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    page_names = list(pages_map.keys())
    
    # Safely match current page
    curr_val = st.session_state.current_page
    current_key = "🏠 HOME"
    for k, v in pages_map.items():
        if v == curr_val:
            current_key = k
            break

    selected_page_name = st.sidebar.radio("NAVIGATION MENU", page_names, index=page_names.index(current_key), key="sidebar_nav")
    st.session_state.current_page = pages_map[selected_page_name]

    st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)

    # Auth buttons in sidebar
    if is_logged_in():
        if st.sidebar.button("🚪 LOGOUT", key="btn_sidebar_logout"):
            logout()
    else:
        if st.sidebar.button("🔑 LOGIN / SIGN UP", key="btn_sidebar_auth_modal"):
            st.session_state.show_auth_modal = not st.session_state.get("show_auth_modal", False)

    # Render Authentication Modal overlay if triggered and not logged in
    if not is_logged_in() and st.session_state.get("show_auth_modal", False):
        st.markdown("<br>", unsafe_allow_html=True)
        render_login_signup()
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # Render Selected Page Module
    curr = st.session_state.current_page
    if curr == "home":
        home.render()
    elif curr == "analyzer":
        analyzer.render()
    elif curr == "dashboard":
        dashboard.render()
    elif curr == "rewriter":
        rewriter.render()
    elif curr == "explainability":
        explainability.render()
    elif curr == "skim":
        skim.render()
    elif curr == "ab_testing":
        ab_testing.render()
    elif curr == "jobs":
        jobs.render()
    elif curr == "history":
        history.render()
    elif curr == "profile":
        profile.render()
    elif curr == "settings":
        settings.render()

if __name__ == "__main__":
    main()
