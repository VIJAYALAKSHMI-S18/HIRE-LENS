def calculate_ats_score(
    skill_score: float,
    semantic_score: float,
    keyword_score: float,
    experience_score: float,
    education_score: float,
    weights: dict = None
) -> dict:
    """
    Calculates weighted ATS compatibility score (0 - 100%).
    Default weights:
    - Skill match: 35%
    - Semantic match: 25%
    - Keyword relevance: 15%
    - Experience relevance: 15%
    - Education relevance: 10%
    """
    if weights is None:
        weights = {
            "skill": 0.35,
            "semantic": 0.25,
            "keyword": 0.15,
            "experience": 0.15,
            "education": 0.10
        }

    ats_score = (
        (skill_score * weights["skill"]) +
        (semantic_score * weights["semantic"]) +
        (keyword_score * weights["keyword"]) +
        (experience_score * weights["experience"]) +
        (education_score * weights["education"])
    )

    ats_score = round(max(0.0, min(100.0, ats_score)), 1)
    interpretation = get_score_interpretation(ats_score)

    return {
        "overall_ats_score": ats_score,
        "breakdown": {
            "skill_score": round(skill_score, 1),
            "semantic_score": round(semantic_score, 1),
            "keyword_score": round(keyword_score, 1),
            "experience_score": round(experience_score, 1),
            "education_score": round(education_score, 1)
        },
        "weights": weights,
        "interpretation": interpretation
    }

def get_score_interpretation(score: float) -> dict:
    if score >= 80.0:
        return {
            "level": "Excellent Match",
            "color": "#22C55E",
            "summary": "Your resume aligns exceptionally well with the job description. High probability of passing ATS filters.",
            "badge": "🏆 TOP TIER CANDIDATE"
        }
    elif score >= 60.0:
        return {
            "level": "Good Match",
            "color": "#4F8CFF",
            "summary": "Strong alignment with key requirements. Minor additions of target keywords will boost your ranking.",
            "badge": "⭐ STRONG CONTENDER"
        }
    elif score >= 40.0:
        return {
            "level": "Moderate Match",
            "color": "#F59E0B",
            "summary": "Partial match detected. Highlight specific missing technical skills and tools to improve compatibility.",
            "badge": "⚠️ REQUIRES OPTIMIZATION"
        }
    else:
        return {
            "level": "Low Match",
            "color": "#EF4444",
            "summary": "Significant skill gap and keyword variance. Consider tailoring your resume heavily for this specific role.",
            "badge": "🚨 LOW ATS FIT"
        }
