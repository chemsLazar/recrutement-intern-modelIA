import requests
import json

# Test data
test_user = {
    "matricule": "dev001",
    "competences": ["Python", "Django", "JavaScript", "React", "SQL"],
    "formations": ["Master en Informatique"],
    "experiences": ["Développeur Python Django 3 ans chez TechCorp"],
    "department": "IT",
    "position": "Développeur Senior"
}

test_job = {
    "id": 1,
    "titre_de_poste": "Développeur Python Senior", 
    "competences_requises": ["Python", "Django", "JavaScript", "SQL"],
    "departement": "IT",
    "localisation": "Casablanca"
}

def test_score_consistency():
    """Test that scores are identical in both directions"""
    
    print("=== TESTING SCORE CONSISTENCY ===\n")
    
    # Test 1: Jobs for Candidate
    print("1. Testing Jobs for Candidate:")
    jobs_payload = {
        "userProfile": test_user,
        "jobOffers": [test_job]
    }
    
    try:
        response1 = requests.post(
            "http://127.0.0.1:5000/recommend/jobs-for-candidate",
            json=jobs_payload,
            headers={'Content-Type': 'application/json'}
        )

        if response1.status_code == 200:
            jobs_result = response1.json()
            if jobs_result and len(jobs_result) > 0:
                score_direction1 = jobs_result[0]['score']
                print(f"   User {test_user['matricule']} -> Job {test_job['titre_de_poste']}: {score_direction1}%")
            else:
                print("   No results returned")
                return
        else:
            print(f"   Error: {response1.status_code} - {response1.text}")
            return
            
    except Exception as e:
        print(f"   Request failed: {e}")
        return
    
    # Test 2: Candidates for Job 
    print("\n2. Testing Candidates for Job:")
    candidates_payload = {
        "jobOffer": test_job,
        "userProfiles": [test_user]
    }
    
    try:
        response2 = requests.post(
            "http://127.0.0.1:5000/recommend/candidates-for-job",
            json=candidates_payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response2.status_code == 200:
            candidates_result = response2.json()
            if candidates_result and len(candidates_result) > 0:
                score_direction2 = candidates_result[0]['score']
                print(f"   Job {test_job['titre_de_poste']} -> User {test_user['matricule']}: {score_direction2}%")
            else:
                print("   No results returned")
                return
        else:
            print(f"   Error: {response2.status_code} - {response2.text}")
            return
            
    except Exception as e:
        print(f"   Request failed: {e}")
        return
    
    # Compare scores
    print(f"\n=== CONSISTENCY CHECK ===")
    print(f"Direction 1 (Jobs for Candidate): {score_direction1}%")
    print(f"Direction 2 (Candidates for Job): {score_direction2}%")
    
    if score_direction1 == score_direction2:
        print("✅ SUCCESS: Scores are identical!")
        print("✅ The unified scoring system is working correctly!")
    else:
        print("❌ FAILURE: Scores are different!")
        print(f"❌ Difference: {abs(score_direction1 - score_direction2)}%")
        
    return score_direction1 == score_direction2

if __name__ == "__main__":
    test_score_consistency() 