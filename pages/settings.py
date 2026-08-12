import streamlit as st
from utils.database import clear_user_history

def render():
    st.markdown("<h2>⚙️ Application Settings</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8;'>Configure platform theme, visual cursor effects, and data privacy options.</p>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("### 🎨 Appearance Theme")
    
    current_dark = st.session_state.get("dark_mode", True)
    theme_choice = st.radio(
        "Select Visual Theme",
        options=["🌙 Dark Mode (Premium AI SaaS)", "☀️ Light Mode (Clean Executive)"],
        index=0 if current_dark else 1,
        key="radio_theme"
    )
    
    new_dark = "Dark Mode" in theme_choice
    if new_dark != current_dark:
        st.session_state.dark_mode = new_dark
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("### ♿ Accessibility & Motion Controls")
    
    curr_reduced = st.session_state.get("reduced_motion", False)
    reduced_motion = st.checkbox(
        "Enable Reduced Motion (Disables magnetic custom cursor & floating animations)",
        value=curr_reduced,
        key="chk_reduced_motion"
    )
    
    if reduced_motion != curr_reduced:
        st.session_state.reduced_motion = reduced_motion
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("user"):
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("### 🗑️ Data Management")
        st.markdown("Clear all saved resume analyses from database history.")
        
        if st.button("Clear My Analysis History", key="btn_clear_hist"):
            clear_user_history(st.session_state.user["id"])
            st.success("History cleared.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("### ℹ️ About HireLens")
    st.markdown("""
    **HireLens v1.0.0** — *See your resume through the eyes of recruiters.*
    
    Built with PyMuPDF, spaCy/NLTK tokenization, Scikit-learn TF-IDF semantic vectorizers, Plotly analytics, and SQLite.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
