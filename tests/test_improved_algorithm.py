#!/usr/bin/env python3
"""
Test script for the improved AI recommendation algorithm
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.recommender import match_jobs_for_candidate, match_candidates_for_job

# Test data with new job offer structure
test_job_offers = [
    {
        "id": 1,
        "title": "Développeur Full Stack",
        "description": "Développement d'applications web modernes avec React et Spring Boot",
        "requiredSkills": ["React", "JavaScript", "Spring Boot", "Java", "PostgreSQL"],
        "requiredProfiles": [
            {
                "title": "Développeur Full Stack",
                "educationLevel": "BAC_PLUS_5",
                "yearsOfExperience": 3
            }
        ],
        "department": "IT",
        "pole": "Digital",
        "direction": "Technique",
        "location": "Casablanca"
    },
    {
        "id": 2,
        "title": "Analyste Financier",
        "description": "Analyse financière et reporting pour le département finance",
        "requiredSkills": ["Excel", "Audit", "Comptabilité", "PowerBI"],
        "requiredProfiles": [
            {
                "title": "Analyste Financier",
                "educationLevel": "BAC_PLUS_4",
                "yearsOfExperience": 2
            }
        ],
        "department": "Finance",
        "pole": "Administrative",
        "direction": "Finance",
        "location": "Rabat"
    },
    {
        "id": 3,
        "title": "Chef de Projet IT",
        "description": "Gestion de projets informatiques et coordination d'équipes",
        "requiredSkills": ["Gestion de projet", "Scrum", "Communication", "Leadership"],
        "requiredProfiles": [
            {
                "title": "Chef de Projet",
                "educationLevel": "BAC_PLUS_5",
                "yearsOfExperience": 5
            }
        ],
        "department": "IT",
        "pole": "Digital",
        "direction": "Management",
        "location": "Marrakech"
    }
]

test_user_profiles = [
    {
        "matricule": "U1001",
        "firstName": "Ali",
        "lastName": "Ben Salah",
        "email": "ali.bensalah@example.com",
        "phone": "0600000001",
        "position": "Développeur",
        "department": "IT",
        "competences": ["Python", "Django", "React", "JavaScript", "Spring Boot", "Java", "PostgreSQL"],
        "formations": [
            {"name": "Master Informatique", "etablissement": "Université Hassan II"}
        ],
        "experiences": [
            {"post": "Développeur Full Stack", "company": "TechCorp", "description": "Développement d'applications web"}
        ]
    },
    {
        "matricule": "U1002",
        "firstName": "Fatima",
        "lastName": "El Amrani",
        "email": "fatima.elamrani@example.com",
        "phone": "0600000002",
        "position": "Analyste",
        "department": "Finance",
        "competences": ["Excel", "Audit", "Comptabilité", "PowerBI"],
        "formations": [
            {"name": "Master Finance", "etablissement": "ESCA"}
        ],
        "experiences": [
            {"post": "Analyste Financier", "company": "BankCorp", "description": "Analyse financière et reporting"}
        ]
    },
    {
        "matricule": "U1003",
        "firstName": "Youssef",
        "lastName": "Kabbaj",
        "email": "youssef.kabbaj@example.com",
        "phone": "0600000003",
        "position": "Chef de Projet",
        "department": "IT",
        "competences": ["Gestion de projet", "Scrum", "Communication", "Leadership"],
        "formations": [
            {"name": "MBA Gestion", "etablissement": "HEC"}
        ],
        "experiences": [
            {"post": "Chef de Projet IT", "company": "TechCorp", "description": "Gestion de projets informatiques"}
        ]
    }
]

def test_job_recommendations():
    """Test job recommendations for candidates"""
    print("=== TESTING JOB RECOMMENDATIONS ===")
    
    for user in test_user_profiles:
        print(f"\n--- Testing for user: {user['firstName']} {user['lastName']} ---")
        recommendations = match_jobs_for_candidate(user, test_job_offers)
        
        print(f"Found {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
            job = rec['jobOffer']
            score = rec['score']
            print(f"  {i}. {job['title']} - Score: {score}%")

def test_candidate_recommendations():
    """Test candidate recommendations for jobs"""
    print("\n=== TESTING CANDIDATE RECOMMENDATIONS ===")
    
    for job in test_job_offers:
        print(f"\n--- Testing for job: {job['title']} ---")
        recommendations = match_candidates_for_job(job, test_user_profiles)
        
        print(f"Found {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
            user = rec['userProfile']
            score = rec['score']
            print(f"  {i}. {user['firstName']} {user['lastName']} - Score: {score}%")

if __name__ == "__main__":
    print("Testing Improved AI Recommendation Algorithm")
    print("=" * 50)
    
    test_job_recommendations()
    test_candidate_recommendations()
    
    print("\n=== TEST COMPLETED ===") 