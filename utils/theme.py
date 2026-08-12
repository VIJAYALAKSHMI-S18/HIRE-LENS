import streamlit as st
import streamlit.components.v1 as components

def apply_theme(dark_mode=True, reduced_motion=False):
    """
    Injects custom HireLens styling into Streamlit:
    - Premium AI SaaS Theme (Dark & Light)
    - Magnetic dual-layer glowing cursor (AI Reticle & Lens Trailing)
    - Neon click ripple bloom & touch response
    - Glassmorphism cards and smooth metric badges
    """
    if dark_mode:
        bg_primary = "#0B1020"
        bg_secondary = "#111827"
        bg_card = "#151C2E"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        border_color = "rgba(79, 140, 255, 0.18)"
        accent_blue = "#4F8CFF"
        accent_purple = "#8B5CF6"
        accent_cyan = "#38BDF8"
        shadow_style = "0 10px 30px rgba(0, 0, 0, 0.45)"
        cursor_outer_color = "rgba(139, 92, 246, 0.25)"
        cursor_inner_color = "#38BDF8"
    else:
        bg_primary = "#F8FAFC"
        bg_secondary = "#FFFFFF"
        bg_card = "#FFFFFF"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        border_color = "rgba(59, 130, 246, 0.2)"
        accent_blue = "#2563EB"
        accent_purple = "#7C3AED"
        accent_cyan = "#0284C7"
        shadow_style = "0 10px 25px rgba(0, 0, 0, 0.08)"
        cursor_outer_color = "rgba(124, 58, 237, 0.2)"
        cursor_inner_color = "#2563EB"

    theme_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: {bg_primary} !important;
        color: {text_primary} !important;
    }}

    /* Hide standard header decoration */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Main container styling */
    .block-container {{
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        max-width: 1200px !important;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {bg_secondary} !important;
        border-right: 1px solid {border_color} !important;
    }}

    /* Theme-Tailored Custom Magnetic Pointer Styles */
    #hirelens-cursor-outer {{
        position: fixed;
        top: -16px;
        left: -16px;
        width: 32px;
        height: 32px;
        border: 2px solid {accent_purple};
        background: {cursor_outer_color};
        border-radius: 50%;
        pointer-events: none;
        z-index: 999999;
        transition: width 0.2s ease, height 0.2s ease, border-color 0.2s ease, background 0.2s ease, top 0.2s ease, left 0.2s ease;
        backdrop-filter: blur(2px);
        box-shadow: 0 0 15px {accent_purple}66;
    }}

    #hirelens-cursor-inner {{
        position: fixed;
        top: -4px;
        left: -4px;
        width: 8px;
        height: 8px;
        background-color: {cursor_inner_color};
        border-radius: 50%;
        pointer-events: none;
        z-index: 999999;
        box-shadow: 0 0 10px {accent_cyan}, 0 0 4px #FFFFFF;
    }}

    /* Hover reticle expansion over interactive elements */
    button:hover ~ #hirelens-cursor-outer,
    .stButton:hover ~ #hirelens-cursor-outer,
    .hirelens-card:hover ~ #hirelens-cursor-outer {{
        width: 44px;
        height: 44px;
        top: -22px;
        left: -22px;
        border-color: {accent_cyan};
        background: rgba(56, 189, 248, 0.2);
    }}

    .hirelens-click-ripple {{
        position: fixed;
        width: 40px;
        height: 40px;
        border: 2px solid {accent_cyan};
        background: radial-gradient(circle, {accent_blue} 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(0.2);
        pointer-events: none;
        z-index: 999998;
        animation: ripple-bloom 0.4s ease-out forwards;
    }}

    @keyframes ripple-bloom {{
        to {{
            transform: translate(-50%, -50%) scale(2.5);
            opacity: 0;
        }}
    }}

    /* Custom Glass Cards */
    .hirelens-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: {shadow_style};
        transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    }}

    .hirelens-card:hover {{
        transform: translateY(-3px);
        border-color: {accent_blue};
        box-shadow: 0 15px 35px rgba(79, 140, 255, 0.15);
    }}

    /* Primary Gradient Button */
    .stButton > button {{
        background: linear-gradient(135deg, {accent_blue} 0%, {accent_purple} 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 4px 15px rgba(79, 140, 255, 0.3) !important;
        transition: all 0.25s ease !important;
        width: 100%;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.45) !important;
        filter: brightness(1.1) !important;
    }}

    /* Badges */
    .skill-badge-matched {{
        display: inline-block;
        background: rgba(34, 197, 94, 0.15);
        color: #22C55E;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }}

    .skill-badge-missing {{
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }}

    .skill-badge-extra {{
        display: inline-block;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }}

    /* Metric cards */
    [data-testid="stMetricValue"] {{
        color: {accent_cyan} !important;
        font-weight: 800 !important;
        font-size: 2rem !important;
    }}

    [data-testid="stMetricLabel"] {{
        color: {text_secondary} !important;
        font-weight: 600 !important;
    }}
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)

    if not reduced_motion:
        cursor_js_code = f"""
        <script>
        (function() {{
            const pDoc = window.parent.document;
            if (window.parent.innerWidth < 768) return; // Mobile check

            let outer = pDoc.getElementById('hirelens-cursor-outer');
            let inner = pDoc.getElementById('hirelens-cursor-inner');

            if (!outer) {{
                outer = pDoc.createElement('div');
                outer.id = 'hirelens-cursor-outer';
                pDoc.body.appendChild(outer);
            }}
            if (!inner) {{
                inner = pDoc.createElement('div');
                inner.id = 'hirelens-cursor-inner';
                pDoc.body.appendChild(inner);
            }}

            let mouseX = 0, mouseY = 0;
            let outerX = 0, outerY = 0;

            pDoc.addEventListener('mousemove', function(e) {{
                mouseX = e.clientX;
                mouseY = e.clientY;
                inner.style.transform = 'translate3d(' + mouseX + 'px, ' + mouseY + 'px, 0)';
            }});

            function loop() {{
                outerX += (mouseX - outerX) * 0.18;
                outerY += (mouseY - outerY) * 0.18;
                outer.style.transform = 'translate3d(' + outerX + 'px, ' + outerY + 'px, 0)';
                window.parent.requestAnimationFrame(loop);
            }}
            loop();

            pDoc.addEventListener('click', function(e) {{
                let ripple = pDoc.createElement('div');
                ripple.className = 'hirelens-click-ripple';
                ripple.style.left = e.clientX + 'px';
                ripple.style.top = e.clientY + 'px';
                pDoc.body.appendChild(ripple);

                setTimeout(function() {{ ripple.remove(); }}, 400);
            }});
        }})();
        </script>
        """
        components.html(cursor_js_code, height=0, width=0)

def get_plotly_colors(dark_mode=True):
    if dark_mode:
        return {
            "bg": "rgba(21, 28, 46, 0.8)",
            "text": "#F8FAFC",
            "grid": "rgba(255, 255, 255, 0.08)",
            "blue": "#4F8CFF",
            "purple": "#8B5CF6",
            "cyan": "#38BDF8",
            "green": "#22C55E",
            "red": "#EF4444",
            "yellow": "#F59E0B"
        }
    else:
        return {
            "bg": "#FFFFFF",
            "text": "#0F172A",
            "grid": "rgba(0, 0, 0, 0.08)",
            "blue": "#2563EB",
            "purple": "#7C3AED",
            "cyan": "#0284C7",
            "green": "#16A34A",
            "red": "#DC2626",
            "yellow": "#D97706"
        }
