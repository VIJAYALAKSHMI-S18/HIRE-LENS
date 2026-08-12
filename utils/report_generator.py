import json
from datetime import datetime

def generate_html_report(results: dict, candidate_name: str = "Candidate", resume_filename: str = "Resume.pdf") -> str:
    """Generates styled printable HTML report."""
    analysis_date = datetime.now().strftime("%B %d, %Y - %H:%M")
    job_title = results.get("job_title", "Target Position")
    ats_score = results.get("ats_score", 0)
    interpretation = results.get("interpretation", {})
    
    matched_skills = results.get("matched_skills", [])
    missing_skills = results.get("missing_skills", [])
    additional_skills = results.get("additional_skills", [])
    recommendations = results.get("recommendations", [])

    matched_html = "".join([f"<span class='badge matched'>{s}</span>" for s in matched_skills]) or "<i>None detected</i>"
    missing_html = "".join([f"<span class='badge missing'>{s}</span>" for s in missing_skills]) or "<i>None missing</i>"
    additional_html = "".join([f"<span class='badge extra'>{s}</span>" for s in additional_skills]) or "<i>None</i>"

    recs_html = ""
    for r in recommendations:
        recs_html += f"""
        <div class="rec-item">
            <strong>{r.get('icon', '💡')} {r.get('title', '')}</strong>
            <p>{r.get('text', '')}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>HireLens Analysis Report - {candidate_name}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                color: #1E293B;
                background: #FFFFFF;
                padding: 40px;
                max-width: 850px;
                margin: auto;
            }}
            .header {{
                border-bottom: 3px solid #4F8CFF;
                padding-bottom: 20px;
                margin-bottom: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .logo {{
                font-size: 28px;
                font-weight: 800;
                color: #4F8CFF;
            }}
            .score-box {{
                background: #F1F5F9;
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                margin-bottom: 30px;
                border-left: 6px solid {interpretation.get('color', '#4F8CFF')};
            }}
            .score-num {{
                font-size: 48px;
                font-weight: 800;
                color: {interpretation.get('color', '#4F8CFF')};
            }}
            .badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 12px;
                font-weight: 600;
                margin: 3px;
            }}
            .matched {{ background: #DCFCE7; color: #15803D; }}
            .missing {{ background: #FEE2E2; color: #B91C1C; }}
            .extra {{ background: #E0F2FE; color: #0369A1; }}
            .section {{
                margin-bottom: 28px;
            }}
            .section h3 {{
                color: #0F172A;
                border-bottom: 1px solid #E2E8F0;
                padding-bottom: 8px;
            }}
            .rec-item {{
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 10px;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #E2E8F0;
                text-align: center;
                font-size: 12px;
                color: #64748B;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div class="logo">🎯 HireLens</div>
                <div>Resume Intelligence & ATS Compatibility Report</div>
            </div>
            <div style="text-align: right; font-size: 13px; color: #64748B;">
                Date: {analysis_date}<br>
                Candidate: {candidate_name}<br>
                File: {resume_filename}
            </div>
        </div>

        <div class="score-box">
            <div>TARGET ROLE: <strong>{job_title}</strong></div>
            <div class="score-num">{ats_score}%</div>
            <div style="font-weight: 700; font-size: 18px; color: {interpretation.get('color', '#4F8CFF')};">
                {interpretation.get('badge', '')} - {interpretation.get('level', '')}
            </div>
            <p style="font-size: 14px; margin-top: 8px;">{interpretation.get('summary', '')}</p>
        </div>

        <div class="section">
            <h3>📊 Score Breakdown</h3>
            <p>
                <strong>Skills Match:</strong> {results.get('skill_score', 0)}% |
                <strong>Semantic Similarity:</strong> {results.get('semantic_score', 0)}% |
                <strong>Keyword Relevance:</strong> {results.get('keyword_score', 0)}%<br>
                <strong>Experience Match:</strong> {results.get('experience_score', 0)}% |
                <strong>Education Match:</strong> {results.get('education_score', 0)}%
            </p>
        </div>

        <div class="section">
            <h3>✅ Matched Skills ({len(matched_skills)})</h3>
            <div>{matched_html}</div>
        </div>

        <div class="section">
            <h3>❌ Missing Required Skills ({len(missing_skills)})</h3>
            <div>{missing_html}</div>
        </div>

        <div class="section">
            <h3>➕ Additional Resume Skills ({len(additional_skills)})</h3>
            <div>{additional_html}</div>
        </div>

        <div class="section">
            <h3>💡 AI Recommendations</h3>
            <div>{recs_html}</div>
        </div>

        <div class="footer">
            Generated automatically by HireLens AI Career Platform • See your resume through the eyes of recruiters.
        </div>
    </body>
    </html>
    """
    return html

def generate_txt_report(results: dict, candidate_name: str = "Candidate", resume_filename: str = "Resume.pdf") -> str:
    """Generates plain text summary report."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    job_title = results.get("job_title", "Target Position")
    
    txt = f"""==================================================
HIRELENS RESUME ANALYSIS REPORT
==================================================
Candidate Name : {candidate_name}
Resume File    : {resume_filename}
Target Job     : {job_title}
Date           : {date_str}
--------------------------------------------------
OVERALL ATS SCORE: {results.get('ats_score', 0)}%
Status          : {results.get('interpretation', {}).get('level', 'Analyzed')}
--------------------------------------------------
SCORE BREAKDOWN:
- Skill Score        : {results.get('skill_score', 0)}%
- Semantic Match     : {results.get('semantic_score', 0)}%
- Keyword Overlap    : {results.get('keyword_score', 0)}%
- Experience Match   : {results.get('experience_score', 0)}%
- Education Match    : {results.get('education_score', 0)}%

MATCHED SKILLS ({len(results.get('matched_skills', []))}):
{', '.join(results.get('matched_skills', [])) or 'None'}

MISSING SKILLS ({len(results.get('missing_skills', []))}):
{', '.join(results.get('missing_skills', [])) or 'None'}

ADDITIONAL SKILLS ({len(results.get('additional_skills', []))}):
{', '.join(results.get('additional_skills', [])) or 'None'}

RECOMMENDATIONS:
"""
    for idx, r in enumerate(results.get("recommendations", []), 1):
        txt += f"\n{idx}. [{r.get('category', 'General')}] {r.get('title', '')}\n   {r.get('text', '')}\n"

    txt += "\n==================================================\nHireLens • See your resume through the eyes of recruiters.\n"
    return txt
