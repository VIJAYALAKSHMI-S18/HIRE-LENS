import streamlit as st

# Set Streamlit Page Configuration
from PIL import Image as _PIL_Image
import os as _os
_logo_path = _os.path.join(_os.path.dirname(__file__), "assets", "hirelens_logo.jpg")
_page_icon = _PIL_Image.open(_logo_path) if _os.path.exists(_logo_path) else "🎯"

st.set_page_config(
    page_title="HIRELENS — AI RESUME ANALYZER & ATS COMPATIBILITY PLATFORM",
    page_icon=_page_icon,
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

    # Sidebar text color adapts to theme so labels are always readable
    sidebar_text   = "#F8FAFC" if dark_mode else "#0F172A"
    sidebar_subtext = "#94A3B8" if dark_mode else "#475569"

    st.markdown(f"""
    <style>
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {{
        text-transform: uppercase !important;
        letter-spacing: 0.5px;
        color: {sidebar_text} !important;
    }}
    /* Radio option text */
    section[data-testid="stSidebar"] .stRadio label p {{
        color: {sidebar_text} !important;
    }}
    /* Info box text */
    section[data-testid="stSidebar"] .stAlert p {{
        color: {sidebar_subtext} !important;
    }}
    h1, h2, h3, h4, .stButton > button {{
        text-transform: uppercase !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Branding & Navigation
    import base64 as _b64, os as _os2
    _lp = _os2.path.join(_os2.path.dirname(__file__), "assets", "hirelens_logo.jpg")
    if _os2.path.exists(_lp):
        with open(_lp, "rb") as _f:
            _logo_b64 = _b64.b64encode(_f.read()).decode()
        _logo_img = f"<img src='data:image/jpeg;base64,{_logo_b64}' style='width:72px;height:72px;border-radius:16px;margin-bottom:10px;object-fit:cover;box-shadow:0 4px 20px rgba(79,140,255,0.3);' />"
    else:
        _logo_img = "<div style='font-size:3rem;'>🎯</div>"

    wordmark_color = "#FFFFFF" if dark_mode else "#0F172A"
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 10px 0 20px 0;'>
        {_logo_img}
        <h1 style='margin: 0; font-size: 1.8rem; font-weight: 800; color: {wordmark_color}; letter-spacing: 3px;'>
            HIRELENS
        </h1>
        <p style='margin: 4px 0 0 0; font-size: 0.75rem; color: #38BDF8; font-weight: 600; letter-spacing: 0.5px;'>
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
    
    # Sync sidebar radio to current_page BEFORE rendering the widget.
    # Without this, the keyed radio ignores `index=` on reruns and
    # overwrites current_page back to whatever it last showed.
    curr_val = st.session_state.current_page
    for k, v in pages_map.items():
        if v == curr_val:
            st.session_state["sidebar_nav"] = k
            break

    selected_page_name = st.sidebar.radio("NAVIGATION MENU", page_names, key="sidebar_nav")
    st.session_state.current_page = pages_map[selected_page_name]

    st.sidebar.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)

    # ── Persistent Theme Toggle ──────────────────────────────────────
    theme_icon  = "☀️" if dark_mode else "🌙"
    theme_label = "SWITCH TO LIGHT MODE" if dark_mode else "SWITCH TO DARK MODE"
    theme_hint  = "Currently: Dark" if dark_mode else "Currently: Light"

    st.sidebar.markdown(
        f"<div style='font-size:11px; color:#94A3B8; text-align:center; "
        f"margin-bottom:6px; letter-spacing:0.5px;'>{theme_hint}</div>",
        unsafe_allow_html=True
    )
    if st.sidebar.button(f"{theme_icon} {theme_label}", key="btn_sidebar_theme"):
        st.session_state.dark_mode = not dark_mode
        st.rerun()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

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
