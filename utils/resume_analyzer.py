from utils.pdf_processor import extract_text_from_pdf
from utils.skill_extractor import extract_skills_from_text, estimate_experience_years, detect_education
from utils.semantic_matcher import compute_semantic_similarity, compute_keyword_relevance
from utils.ats_calculator import calculate_ats_score

def analyze_resume_against_job(pdf_bytes: bytes, job_description: str, job_title: str = "") -> dict:
    """
    Main analysis pipeline processing resume PDF bytes against job description text.
    """
    # Step 1: PDF Extraction
    pdf_res = extract_text_from_pdf(pdf_bytes)
    if not pdf_res["success"]:
        return {
            "success": False,
            "error": pdf_res["error"]
        }

    resume_text = pdf_res["text"]
    
    # Step 2: Skill Extraction
    resume_skills_res = extract_skills_from_text(resume_text)
    job_skills_res = extract_skills_from_text(job_description)

    resume_skill_set = set(resume_skills_res["all_skills"])
    job_skill_set = set(job_skills_res["all_skills"])

    matched_skills = sorted(list(resume_skill_set.intersection(job_skill_set)))
    missing_skills = sorted(list(job_skill_set - resume_skill_set))
    additional_skills = sorted(list(resume_skill_set - job_skill_set))

    # Skill Score Calculation
    if job_skill_set:
        skill_score = (len(matched_skills) / len(job_skill_set)) * 100.0
    else:
        skill_score = 70.0 # Default if job desc doesn't have standard explicit skill tags

    skill_score = round(min(skill_score, 100.0), 1)

    # Step 3: Semantic & Keyword Matching
    semantic_score = compute_semantic_similarity(resume_text, job_description)
    keyword_score = compute_keyword_relevance(resume_text, job_description)

    # Step 4: Experience & Education Matching
    res_exp = estimate_experience_years(resume_text)
    job_exp = estimate_experience_years(job_description)

    if job_exp > 0:
        experience_score = min((res_exp / job_exp) * 100.0, 100.0)
    else:
        experience_score = 85.0

    res_edu = detect_education(resume_text)
    job_edu = detect_education(job_description)

    if job_edu:
        edu_match = any(e in res_edu for e in job_edu)
        education_score = 100.0 if edu_match else 60.0
    else:
        education_score = 80.0 if res_edu else 60.0

    # Step 5: Overall ATS Score
    ats_res = calculate_ats_score(
        skill_score=skill_score,
        semantic_score=semantic_score,
        keyword_score=keyword_score,
        experience_score=experience_score,
        education_score=education_score
    )

    # Step 6: Skill Gap Analysis & AI Recommendations
    skill_gaps_by_cat = categorize_skill_gaps(missing_skills)
    recommendations = generate_ai_recommendations(
        ats_score=ats_res["overall_ats_score"],
        missing_skills=missing_skills,
        skill_score=skill_score,
        semantic_score=semantic_score,
        res_exp=res_exp,
        job_exp=job_exp,
        sections=pdf_res["sections"]
    )

    return {
        "success": True,
        "job_title": job_title or "Target Position",
        "ats_score": ats_res["overall_ats_score"],
        "interpretation": ats_res["interpretation"],
        "skill_score": skill_score,
        "semantic_score": semantic_score,
        "keyword_score": keyword_score,
        "experience_score": round(experience_score, 1),
        "education_score": round(education_score, 1),
        "resume_experience_years": res_exp,
        "job_experience_years": job_exp,
        "resume_education": res_edu,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "skill_gaps_by_category": skill_gaps_by_cat,
        "recommendations": recommendations,
        "pages": pdf_res["pages"],
        "extracted_text_preview": resume_text[:1000] + ("..." if len(resume_text) > 1000 else "")
    }

def categorize_skill_gaps(missing_skills: list) -> dict:
    """Categorizes missing skills into tech domains."""
    from utils.skill_extractor import load_skills_database
    skills_db = load_skills_database()
    
    gaps = {}
    for skill in missing_skills:
        found_cat = "Other / General"
        for cat, s_list in skills_db.items():
            if skill in s_list:
                found_cat = cat
                break
        if found_cat not in gaps:
            gaps[found_cat] = []
        gaps[found_cat].append(skill)
    return gaps

def generate_ai_recommendations(
    ats_score: float,
    missing_skills: list,
    skill_score: float,
    semantic_score: float,
    res_exp: float,
    job_exp: float,
    sections: dict
) -> list:
    """Generates personalized actionable improvement recommendations."""
    recs = []

    if missing_skills:
        top_missing = ", ".join(missing_skills[:4])
        recs.append({
            "category": "Skill Enhancement",
            "icon": "🧩",
            "title": f"Incorporate Key Missing Technical Skills: {top_missing}",
            "text": f"If you have hands-on experience or academic exposure to {top_missing}, explicitly list them in your technical skills and project descriptions."
        })

    if semantic_score < 70.0:
        recs.append({
            "category": "Context & Terminology",
            "icon": "🧠",
            "title": "Optimize Bullet Points for Contextual Alignment",
            "text": "Your semantic similarity score is under 70%. Replace generic phrasing with industry-standard terminology present in the job posting."
        })

    if job_exp > 0 and res_exp < job_exp:
        recs.append({
            "category": "Experience Framing",
            "icon": "💼",
            "title": "Emphasize Project Impact & Leadership",
            "text": f"The job targets ~{job_exp} years of experience. Quantify your accomplishments with metrics (e.g., 'Improved performance by 35%') to demonstrate senior-level impact."
        })

    if not sections.get("projects"):
        recs.append({
            "category": "Resume Formatting",
            "icon": "📄",
            "title": "Add a Dedicated Projects Section",
            "text": "Highlighting 2-3 key technical projects with tools, role, and measurable outcomes significantly increases ATS parser score."
        })

    recs.append({
        "category": "ATS Optimization",
        "icon": "🎯",
        "title": "Use Clear Standard Section Headings",
        "text": "Ensure your resume uses clean headings like 'Work Experience', 'Education', 'Technical Skills', and 'Projects' for seamless ATS parsing."
    })

    return recs
