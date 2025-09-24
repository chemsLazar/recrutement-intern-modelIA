import requests
import json
import os

# Adjust paths for new structure
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')

with open(os.path.join(data_dir, "user_profiles.json"), "r", encoding="utf-8") as f:
    user_profiles = json.load(f)

with open(os.path.join(data_dir, "job_offers.json"), "r", encoding="utf-8") as f:
    job_offers = json.load(f)

url = "http://127.0.0.1:5000/recommend/candidates-for-job"

BEST_MATCH_THRESHOLD = 70.0  # percent

for job in job_offers:
    payload = {
        "jobOffer": job,
        "userProfiles": user_profiles
    }
    response = requests.post(url, json=payload)
    print(f"\n=== {job['titre_de_poste']} ({job['departement']}) ===")
    if response.status_code == 200:
        results = response.json()
        print("-- All Scores --")
        for rec in results:
            user = rec['userProfile']
            print(f"  - {user['matricule']} | {user['firstName']} {user['lastName']} | Score: {rec['score']}%")
        print("-- Best Matches (score >= 70%) --")
        
        best_matches = [rec for rec in results if rec['score'] >= BEST_MATCH_THRESHOLD]
        if best_matches:
            for rec in best_matches:
                user = rec['userProfile']
                print(f"  - {user['matricule']} | {user['firstName']} {user['lastName']} | Score: {rec['score']}%")
        else:
            print("  Aucun profil fortement compatible trouvé (score >= 70%)")
    else:
        print(f"  Error: {response.status_code} {response.text}") 