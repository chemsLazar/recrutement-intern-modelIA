from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Any
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to load pre-trained model (optional)
ML_MODEL = None
try:
    from sentence_transformers import SentenceTransformer
    # Using a small, fast model that downloads quickly
    ML_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Pre-trained ML model loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load pre-trained model: {e}")
    print("🔄 Using enhanced TF-IDF mode instead")
    ML_MODEL = None

# --- Helper functions for competency matching ---
def normalize_text(text: str) -> str:
    """Normalize text for better matching"""
    if not text:
        return ""
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_competencies_from_user(user: Dict[str, Any]) -> List[str]:
    """Extract competencies from user profile - focus on main competences"""
    competencies = []
    
    # Add user competences (main field)
    if user.get('competences'):
        if isinstance(user['competences'], list):
            competencies.extend([normalize_text(comp) for comp in user['competences']])
        elif isinstance(user['competences'], str):
            competencies.append(normalize_text(user['competences']))
    
    return list(set(competencies))  # Remove duplicates

def extract_competencies_from_job(job: Dict[str, Any]) -> List[str]:
    """Extract competencies from job offer - focus on required skills"""
    competencies = []
    
    # Check multiple possible field names for job skills
    skill_fields = ['requiredSkills', 'competences_requises', 'skills', 'competencies']
    
    for field in skill_fields:
        if job.get(field):
            if isinstance(job[field], list):
                competencies.extend([normalize_text(skill) for skill in job[field]])
            elif isinstance(job[field], str):
                competencies.append(normalize_text(job[field]))
    
    return list(set(competencies))  # Remove duplicates

def calculate_competency_match(user_competencies: List[str], job_competencies: List[str]) -> float:
    """Calculate competency match score using HYBRID approach with pre-trained ML model"""
    if not user_competencies or not job_competencies:
        return 0.0
    
    try:
        # First, calculate direct matching (more reliable for short lists)
        direct_matches = 0
        total_job_competencies = len(job_competencies)
        
        for job_comp in job_competencies:
            for user_comp in user_competencies:
                job_normalized = normalize_text(job_comp)
                user_normalized = normalize_text(user_comp)
                
                # Check for exact match
                if job_normalized == user_normalized:
                    direct_matches += 1
                    break
                # Check if one contains the other
                elif job_normalized in user_normalized or user_normalized in job_normalized:
                    direct_matches += 0.8
                    break
                # Check for word overlap
                else:
                    job_words = set(job_normalized.split())
                    user_words = set(user_normalized.split())
                    if job_words.intersection(user_words):
                        direct_matches += 0.5
                        break
        
        direct_percentage = (direct_matches / total_job_competencies) * 100 if total_job_competencies > 0 else 0.0
        
        # Calculate TF-IDF similarity
        tfidf_score = calculate_tfidf_similarity(user_competencies, job_competencies)
        
        # Calculate pre-trained ML model similarity
        pretrained_score = calculate_pretrained_similarity(user_competencies, job_competencies)
        
        # HYBRID SCORING: Combine all three approaches
        if direct_matches == 0:
            # If no direct matches, rely on ML models
            if pretrained_score > 0:
                return max(tfidf_score, pretrained_score) * 0.8  # Cap at 80% without direct matches
            else:
                return tfidf_score * 0.6  # Lower confidence without ML model
        
        # Weighted combination of all three methods
        weights = {
            'direct': 0.4,      # Direct matching is most reliable
            'pretrained': 0.4,   # Pre-trained model provides semantic understanding
            'tfidf': 0.2         # TF-IDF as backup
        }
        
        # Calculate weighted score
        final_score = (
            direct_percentage * weights['direct'] +
            pretrained_score * weights['pretrained'] +
            tfidf_score * weights['tfidf']
        )
        
        # Ensure score doesn't exceed 100%
        return min(final_score, 100.0)
        
    except Exception as e:
        print(f"Error calculating competency match: {e}")
        return 0.0

def calculate_tfidf_similarity(user_competencies: List[str], job_competencies: List[str]) -> float:
    """Calculate TF-IDF similarity for competency matching"""
    try:
        # Combine all competencies into text for TF-IDF
        user_text = ' '.join(user_competencies)
        job_text = ' '.join(job_competencies)
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=1,
            max_df=1.0,
            stop_words=None  # Keep all words for competency matching
        )
        
        # Fit and transform the texts
        texts = [user_text, job_text]
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to percentage (0-100)
        return similarity * 100
        
    except Exception as e:
        print(f"Error calculating TF-IDF similarity: {e}")
        return 0.0

def calculate_pretrained_similarity(user_competencies: List[str], job_competencies: List[str]) -> float:
    """Calculate similarity using pre-trained sentence transformer model"""
    if ML_MODEL is None:
        return 0.0
    
    try:
        # Combine competencies into meaningful text
        user_text = ' '.join(user_competencies)
        job_text = ' '.join(job_competencies)
        
        # Get embeddings from pre-trained model
        embeddings = ML_MODEL.encode([user_text, job_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        # Convert to percentage (0-100)
        return similarity * 100
        
    except Exception as e:
        print(f"Error calculating pre-trained similarity: {e}")
        return 0.0

def calculate_user_job_score(user_profile: Dict[str, Any], job_offer: Dict[str, Any]) -> float:
    """
    Calculate match score between user and job offer.
    Uses HYBRID approach: Direct matching + TF-IDF + Pre-trained ML model
    """
    print(f"\n=== CALCULATING HYBRID ML SCORE ===")
    print(f"User: {user_profile.get('matricule', 'N/A')}")
    print(f"Job: {job_offer.get('title', job_offer.get('titre_de_poste', 'N/A'))}")
    
    # Extract competencies
    user_competencies = extract_competencies_from_user(user_profile)
    job_competencies = extract_competencies_from_job(job_offer)
    
    print(f"User competencies: {user_competencies}")
    print(f"Job competencies: {job_competencies}")
    
    # Calculate individual scores for debugging
    direct_matches = 0
    total_job_competencies = len(job_competencies)
    
    for job_comp in job_competencies:
        for user_comp in user_competencies:
            job_normalized = normalize_text(job_comp)
            user_normalized = normalize_text(user_comp)
            if job_normalized == user_normalized:
                direct_matches += 1
                break
    
    direct_percentage = (direct_matches / total_job_competencies) * 100 if total_job_competencies > 0 else 0.0
    tfidf_score = calculate_tfidf_similarity(user_competencies, job_competencies)
    pretrained_score = calculate_pretrained_similarity(user_competencies, job_competencies)
    
    print(f"Direct match: {direct_percentage:.1f}%")
    print(f"TF-IDF score: {tfidf_score:.1f}%")
    print(f"Pre-trained ML score: {pretrained_score:.1f}%")
    
    # Calculate final hybrid score
    competency_score = calculate_competency_match(user_competencies, job_competencies)
    
    print(f"🎯 FINAL HYBRID SCORE: {competency_score:.1f}%")
    print("=" * 50)
    
    return competency_score

def match_jobs_for_candidate(user_profile: Dict[str, Any], job_offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Find matching jobs for a candidate using ADVANCED competency-based scoring.
    """
    print(f"\n=== JOBS FOR CANDIDATE: {user_profile.get('matricule', '')} ===")
    print(f"Processing {len(job_offers)} job offers")
    
    results = []
    
    for job in job_offers:
        score = calculate_user_job_score(user_profile, job)
        results.append({
            'jobOffer': job,
            'score': score
        })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Filter out very low scores (below 10%)
    results = [r for r in results if r['score'] >= 10.0]
    
    print(f"Returning {len(results)} job recommendations (filtered)")
    return results

def match_candidates_for_job(job_offer: Dict[str, Any], user_profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Find matching candidates for a job using ADVANCED competency-based scoring.
    """
    print(f"\n=== CANDIDATES FOR JOB: {job_offer.get('title', job_offer.get('titre_de_poste', ''))} ===")
    print(f"Processing {len(user_profiles)} user profiles")
    
    results = []
    
    for user in user_profiles:
        score = calculate_user_job_score(user, job_offer)
        results.append({
            'userProfile': user,
            'score': score
        })
    
    # Sort by score (highest first)
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Filter out very low scores (below 10%)
    results = [r for r in results if r['score'] >= 10.0]
    
    print(f"Returning {len(results)} candidate recommendations (filtered)")
    return results 