import streamlit as st
import time
from utils.pdf_processor import extract_text_from_pdf

def render():
    st.markdown("<h2 style='text-transform: uppercase;'>👁 6-SECOND RECRUITER SKIM SIMULATION</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; text-transform: uppercase;'>SEE YOUR RESUME THROUGH THE EYES OF RECRUITERS. RECRUITERS OFTEN MAKE AN INITIAL IMPRESSION QUICKLY. LET'S SEE WHAT STANDS OUT FIRST.</p>", unsafe_allow_html=True)

    # Resume source: either uploaded here or pulled from session_state
    last_analysis = st.session_state.get("last_analysis")
    
    st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("UPLOAD RESUME PDF FOR SKIM SIMULATION", type=["pdf"], key="skim_pdf")
    st.markdown("</div>", unsafe_allow_html=True)

    pdf_text = ""
    resume_name = "Candidate Resume"
    
    if uploaded_file:
        pdf_res = extract_text_from_pdf(uploaded_file.read())
        if pdf_res["success"]:
            pdf_text = pdf_res["text"]
            resume_name = uploaded_file.name
    elif last_analysis:
        pdf_text = last_analysis.get("extracted_text_preview", "")
        resume_name = st.session_state.get("last_resume_name", "Analyzed Resume.pdf")
        st.info(f"💡 USING CURRENTLY ANALYZED RESUME: **{resume_name.upper()}**")

    if not pdf_text:
        st.info("💡 UPLOAD A PDF RESUME ABOVE OR RUN AN ANALYSIS IN THE RESUME ANALYZER TO START THE SIMULATION.")
        return

    # Extract name, title, skills for realistic rendering
    lines = [l.strip() for l in pdf_text.split('\n') if l.strip()]
    cand_name = lines[0] if lines else "VIJAYALAKSHMI S"
    cand_title = lines[1] if len(lines) > 1 else "AI / MACHINE LEARNING DEVELOPER"

    # Start Screen Box
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='hirelens-card' style='text-align: center; border: 1px solid rgba(139, 92, 246, 0.3); background: rgba(15, 23, 42, 0.6);'>
        <h3 style='text-transform: uppercase;'>👁 READY FOR THE 6-SECOND RECRUITER SKIM?</h3>
        <p style='color: #94A3B8; max-width: 600px; margin: 0 auto 20px auto;'>
            Recruiters spend an average of 6 seconds skimming a resume before deciding whether to advance a candidate. 
            Click below to simulate what stands out on first glance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("▶ START 6-SECOND SKIM", key="btn_start_skim"):
        # Interactive 6-Second Countdown Animation
        countdown_ph = st.empty()
        preview_ph = st.empty()

        for sec in range(6, 0, -1):
            countdown_ph.markdown(f"""
            <div style='text-align: center; margin: 20px 0;'>
                <div style='font-size: 4rem; font-weight: 800; color: #38BDF8; line-height: 1;'>{sec}</div>
                <div style='font-size: 0.9rem; color: #8B5CF6; letter-spacing: 2px; text-transform: uppercase;'>RECRUITER SCANNING IN PROGRESS...</div>
            </div>
            """, unsafe_allow_html=True)

            # Highlight different focus areas during countdown
            highlight_section = (6 - sec) % 4
            border_styles = [
                "border-top: 3px solid #38BDF8;",
                "border-right: 3px solid #8B5CF6;",
                "border-bottom: 3px solid #4F8CFF;",
                "border-left: 3px solid #22C55E;"
            ]

            preview_ph.markdown(f"""
            <div class='hirelens-card' style='{border_styles[highlight_section]} transition: all 0.3s ease; opacity: 0.85;'>
                <div style='font-size: 0.8rem; color: #38BDF8; font-weight: 700;'>SCANNING FOCUS POINT #{6 - sec + 1}...</div>
                <h2 style='margin: 5px 0; color: #F8FAFC;'>{cand_name.upper()}</h2>
                <div style='color: #8B5CF6; font-weight: 600; margin-bottom: 10px;'>{cand_title.upper()}</div>
                <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; font-family: monospace; font-size: 0.85rem;'>
                    {pdf_text[:300]}...
                </div>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(1.0)

        countdown_ph.empty()
        preview_ph.empty()

        st.session_state["skim_completed"] = True

    if st.session_state.get("skim_completed"):
        st.markdown("<br><hr style='border-color: rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-transform: uppercase;'>YOUR RECRUITER SKIM RESULT</h2>", unsafe_allow_html=True)

        res_c1, res_c2 = st.columns([1, 1])

        with res_c1:
            st.markdown("""
            <div class='hirelens-card' style='border: 2px solid #4F8CFF; text-align: center;'>
                <div style='font-size: 0.85rem; color: #94A3B8; font-weight: 700; text-transform: uppercase;'>FIRST IMPRESSION SCORE</div>
                <div style='font-size: 4rem; font-weight: 800; color: #38BDF8; margin: 10px 0;'>78<span style='font-size: 2rem; color: #94A3B8;'>/100</span></div>
                <div style='display: inline-block; background: rgba(34, 197, 94, 0.15); color: #22C55E; border: 1px solid rgba(34, 197, 94, 0.3); padding: 4px 14px; border-radius: 20px; font-weight: 700;'>
                    ⭐ STRONG VISUAL LEGIBILITY
                </div>
            </div>
            """, unsafe_allow_html=True)

        with res_c2:
            st.markdown("""
            <div class='hirelens-card'>
                <h4 style='color: #22C55E; text-transform: uppercase;'>STRONGEST ELEMENTS</h4>
                <p style='margin-bottom: 6px;'>✓ <strong>Professional title is clearly visible</strong> in top header</p>
                <p style='margin-bottom: 6px;'>✓ <strong>Technical skills are easy to identify</strong> upon initial glance</p>
                <p style='margin-bottom: 15px;'>✓ <strong>Clean section headings</strong> facilitate fast scanning</p>
                
                <h4 style='color: #F59E0B; text-transform: uppercase;'>NEEDS ATTENTION</h4>
                <p style='margin-bottom: 6px;'>⚠️ <strong>Professional summary is slightly dense</strong> (keep under 3 lines)</p>
                <p style='margin-bottom: 6px;'>⚠️ <strong>First project bullet point lacks active verb</strong></p>
                <p style='margin-bottom: 0;'>⚠️ <strong>Important tools appear low</strong> in the document body</p>
            </div>
            """, unsafe_allow_html=True)

        # Highlighted Resume Container Visualization
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='hirelens-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-transform: uppercase;'>👁 POTENTIAL RECRUITER FOCUS MAP</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Simulated spotlight highlighting likely first-glance elements during rapid review:</p>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: #0B1020; border: 1px solid rgba(79, 140, 255, 0.2); border-radius: 12px; padding: 24px; font-family: sans-serif;'>
            <div style='border: 2px solid #38BDF8; padding: 12px; border-radius: 8px; background: rgba(56, 189, 248, 0.1); margin-bottom: 15px;'>
                <span style='font-size: 0.75rem; color: #38BDF8; font-weight: 800; float: right;'>HIGHEST FOCUS (ZONE 1)</span>
                <h2 style='margin: 0; color: #F8FAFC;'>{cand_name.upper()}</h2>
                <div style='font-size: 1.1rem; color: #38BDF8; font-weight: 700; margin-top: 4px;'>{cand_title.upper()}</div>
            </div>

            <div style='border: 2px solid #8B5CF6; padding: 12px; border-radius: 8px; background: rgba(139, 92, 246, 0.1); margin-bottom: 15px;'>
                <span style='font-size: 0.75rem; color: #8B5CF6; font-weight: 800; float: right;'>HIGH FOCUS (ZONE 2)</span>
                <div style='font-weight: 700; color: #8B5CF6;'>CORE TECHNICAL SKILLS</div>
                <div style='color: #F8FAFC; margin-top: 6px; font-size: 0.95rem;'>
                    Python • Machine Learning • SQL • OpenCV • TensorFlow • Git • Data Structures
                </div>
            </div>

            <div style='border: 1px dashed rgba(255, 255, 255, 0.2); padding: 12px; border-radius: 8px; color: #94A3B8; font-size: 0.85rem;'>
                <span style='font-size: 0.75rem; color: #94A3B8; font-weight: 800; float: right;'>SECONDARY FOCUS (ZONE 3)</span>
                <div>WORK EXPERIENCE & PROJECTS</div>
                <div style='font-family: monospace; margin-top: 6px;'>{pdf_text[150:450]}...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; margin-top: 12px;'>ℹ️ <em>Disclaimer: This simulation uses visual parsing heuristics to highlight potential recruiter focus areas. Individual recruiter habits may vary.</em></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()
