import json
import re
import os

SKILLS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills.json")

def load_skills_database() -> dict:
    """Loads skill taxonomy from json."""
    try:
        with open(SKILLS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def extract_skills_from_text(text: str) -> dict:
    """
    Extracts tech skills grouped by category from text.
    """
    skills_db = load_skills_database()
    found_skills = set()
    category_matches = {}
    
    text_clean = text.lower()
    
    for category, skills_list in skills_db.items():
        category_matches[category] = []
        for skill in skills_list:
            # Word boundary regex matching to avoid substring false positives
            escaped_skill = re.escape(skill.lower())
            pattern = r'(?:\b|_)' + escaped_skill + r'(?:\b|_)'
            
            if re.search(pattern, text_clean):
                found_skills.add(skill)
                category_matches[category].append(skill)
                
    return {
        "all_skills": sorted(list(found_skills)),
        "by_category": category_matches
    }

def estimate_experience_years(text: str) -> float:
    """
    Estimates total years of experience from resume text.
    """
    patterns = [
        r'(\d+|\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|work)',
        r'(?:experience|worked for)\s*[:\-]?\s*(\d+)\+?\s*(?:years?|yrs?)'
    ]
    
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    max_years = 0.0
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match.isdigit():
                val = float(match)
            elif match.lower() in word_to_num:
                val = float(word_to_num[match.lower()])
            else:
                val = 0.0
            if val > max_years and val <= 40:
                max_years = val
                
    if max_years == 0:
        # Check year spans e.g., 2020 - 2024
        year_spans = re.findall(r'\b(20[0-9]{2}|19[9][0-9])\s*[-–\text{to}]+\s*(20[0-9]{2}|present|current)\b', text, re.IGNORECASE)
        total = 0
        current_year = 2026
        for start, end in year_spans:
            try:
                s_year = int(start)
                e_year = current_year if end.lower() in ['present', 'current'] else int(end)
                if e_year >= s_year and (e_year - s_year) < 25:
                    total += (e_year - s_year)
            except ValueError:
                pass
        if total > 0:
            max_years = min(float(total), 30.0)
            
    return max_years

def detect_education(text: str) -> list:
    """Detects degree types in text."""
    degrees = [
        "Ph.D", "PhD", "Doctor of Philosophy",
        "Master of Science", "M.S.", "M.Tech", "MCA", "M.E.", "MBA", "Masters",
        "Bachelor of Science", "B.S.", "B.Tech", "B.E.", "BCA", "B.A.", "Bachelors"
    ]
    
    found = []
    text_lower = text.lower()
    for degree in degrees:
        escaped = re.escape(degree.lower())
        pattern = r'\b' + escaped + r'\b'
        if re.search(pattern, text_lower):
            found.append(degree)
            
    return list(set(found))
