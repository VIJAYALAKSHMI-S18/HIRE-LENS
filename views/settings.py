import streamlit as st
from utils.database import clear_user_history

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>⚙️ APPLICATION SETTINGS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>CONFIGURE PLATFORM THEME, VISUAL CURSOR EFFECTS, AND DATA PRIVACY OPTIONS.</p>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>🎨 APPEARANCE THEME</h3>", unsafe_allow_html=True)
    
    current_dark = st.session_state.get("dark_mode", True)
    theme_choice = st.radio(
        "SELECT VISUAL THEME",
        options=["🌙 DARK MODE (PREMIUM AI SAAS)", "☀️ LIGHT MODE (CLEAN EXECUTIVE)"],
        index=0 if current_dark else 1,
        key="radio_theme"
    )
    
    new_dark = "DARK MODE" in theme_choice
    if new_dark != current_dark:
        st.session_state.dark_mode = new_dark
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>♿ ACCESSIBILITY & MOTION CONTROLS</h3>", unsafe_allow_html=True)
    
    curr_reduced = st.session_state.get("reduced_motion", False)
    reduced_motion = st.checkbox(
        "ENABLE REDUCED MOTION (DISABLES MAGNETIC CUSTOM CURSOR & FLOATING ANIMATIONS)",
        value=curr_reduced,
        key="chk_reduced_motion"
    )
    
    if reduced_motion != curr_reduced:
        st.session_state.reduced_motion = reduced_motion
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("user"):
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>🗑️ DATA MANAGEMENT</h3>", unsafe_allow_html=True)
        st.markdown("CLEAR ALL SAVED RESUME ANALYSES FROM DATABASE HISTORY.")
        
        if st.button("CLEAR MY ANALYSIS HISTORY", key="btn_clear_hist"):
            clear_user_history(st.session_state.user["id"])
            st.success("HISTORY CLEARED.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-transform: uppercase;'>ℹ️ ABOUT HIRELENS</h3>", unsafe_allow_html=True)
    st.markdown("""
    **HIRELENS V1.0.0** — *SEE YOUR RESUME THROUGH THE EYES OF RECRUITERS.*
    
    BUILT WITH PYMUPDF, SCIKIT-LEARN TF-IDF SEMANTIC VECTORIZERS, PLOTLY ANALYTICS, AND SQLITE.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
