import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def compute_semantic_similarity(resume_text: str, job_text: str) -> float:
    """
    Computes semantic similarity score (0.0 to 100.0) between resume and job description.
    Uses TF-IDF n-gram vectorizer + cosine similarity.
    """
    if not resume_text or not job_text:
        return 0.0
        
    try:
        corpus = [clean_corpus_text(resume_text), clean_corpus_text(job_text)]
        
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        raw_score = float(sim_matrix[0][0])
        # Scale to realistic 0 - 100 percentage
        scaled_score = round(min(raw_score * 100 * 1.5, 100.0), 1)
        return max(scaled_score, 10.0) if raw_score > 0.05 else round(raw_score * 100, 1)
        
    except Exception:
        return 50.0

def compute_keyword_relevance(resume_text: str, job_text: str) -> float:
    """
    Calculates keyword density & overlap score.
    """
    job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
    
    if not job_words:
        return 0.0
        
    # Filter out common stop words
    stop_words = {'the', 'and', 'for', 'with', 'you', 'that', 'this', 'from', 'are', 'have', 'will', 'must', 'with', 'your', 'about'}
    job_words = job_words - stop_words
    resume_words = resume_words - stop_words
    
    overlap = job_words.intersection(resume_words)
    score = (len(overlap) / len(job_words)) * 100.0 if job_words else 0.0
    return round(min(score * 1.25, 100.0), 1)

def clean_corpus_text(text: str) -> str:
    """Clean text for NLP vectorization."""
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text.lower()
