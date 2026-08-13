import os
import sqlite3
import hashlib
import json
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "hirelens.db")

def init_db():
    """Ensure database directory and tables exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Analyses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        ats_score REAL NOT NULL,
        skill_score REAL NOT NULL,
        semantic_score REAL NOT NULL,
        keyword_score REAL NOT NULL,
        experience_score REAL NOT NULL,
        education_score REAL NOT NULL,
        matched_skills TEXT NOT NULL,
        missing_skills TEXT NOT NULL,
        additional_skills TEXT NOT NULL,
        recommendations TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # Resume A/B Tests Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ab_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_a_name TEXT NOT NULL,
        resume_b_name TEXT NOT NULL,
        job_title TEXT NOT NULL,
        score_a REAL NOT NULL,
        score_b REAL NOT NULL,
        winner_label TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password using SHA-256 with fixed salt."""
    salt = "HireLens_Salt_2026_Secure"
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

def register_user(name: str, email: str, password: str):
    """Registers a new user into the database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), pwd_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, "Account created successfully!", user_id
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Email address already registered.", None
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}", None

def authenticate_user(email: str, password: str):
    """Authenticates email and password."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pwd_hash = hash_password(password)

    cursor.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password_hash = ?",
        (email.strip().lower(), pwd_hash)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return True, {"id": user[0], "name": user[1], "email": user[2]}
    return False, None

def save_analysis(user_id: int, resume_name: str, job_title: str, results: dict):
    """Saves completed analysis results to DB."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analyses (
        user_id, resume_name, job_title, ats_score, skill_score,
        semantic_score, keyword_score, experience_score, education_score,
        matched_skills, missing_skills, additional_skills, recommendations
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        resume_name,
        job_title or "Target Position",
        results["ats_score"],
        results["skill_score"],
        results["semantic_score"],
        results["keyword_score"],
        results["experience_score"],
        results["education_score"],
        json.dumps(results["matched_skills"]),
        json.dumps(results["missing_skills"]),
        json.dumps(results["additional_skills"]),
        json.dumps(results["recommendations"])
    ))

    analysis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return analysis_id

def get_user_analyses(user_id: int):
    """Retrieves all past analyses for a specific user."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, resume_name, job_title, ats_score, skill_score, semantic_score,
           keyword_score, experience_score, education_score, matched_skills,
           missing_skills, additional_skills, recommendations, created_at
    FROM analyses
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r[0],
            "resume_name": r[1],
            "job_title": r[2],
            "ats_score": r[3],
            "skill_score": r[4],
            "semantic_score": r[5],
            "keyword_score": r[6],
            "experience_score": r[7],
            "education_score": r[8],
            "matched_skills": json.loads(r[9]),
            "missing_skills": json.loads(r[10]),
            "additional_skills": json.loads(r[11]),
            "recommendations": json.loads(r[12]),
            "created_at": r[13]
        })
    return history

def delete_analysis(analysis_id: int, user_id: int):
    """Deletes a specific analysis record."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ? AND user_id = ?", (analysis_id, user_id))
    conn.commit()
    conn.close()

def clear_user_history(user_id: int):
    """Clears all analysis history for user."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def update_user_profile(user_id: int, new_name: str, new_password: str = None):
    """Updates user profile information."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_password:
        pwd_hash = hash_password(new_password)
        cursor.execute("UPDATE users SET name = ?, password_hash = ? WHERE id = ?", (new_name.strip(), pwd_hash, user_id))
    else:
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (new_name.strip(), user_id))

    conn.commit()
    conn.close()

def save_ab_test(user_id: int, resume_a_name: str, resume_b_name: str, job_title: str, score_a: float, score_b: float, winner_label: str):
    """Saves A/B test comparison result to DB."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ab_tests (user_id, resume_a_name, resume_b_name, job_title, score_a, score_b, winner_label)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, resume_a_name, resume_b_name, job_title or "Target Position", score_a, score_b, winner_label))

    ab_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ab_id

def get_user_ab_tests(user_id: int):
    """Retrieves all past A/B comparison records for a specific user."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, resume_a_name, resume_b_name, job_title, score_a, score_b, winner_label, created_at
    FROM ab_tests
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    tests = []
    for r in rows:
        tests.append({
            "id": r[0],
            "resume_a_name": r[1],
            "resume_b_name": r[2],
            "job_title": r[3],
            "score_a": r[4],
            "score_b": r[5],
            "winner_label": r[6],
            "created_at": r[7]
        })
    return tests

