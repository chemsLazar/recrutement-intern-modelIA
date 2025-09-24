import requests
import json

# Test data with more detailed profiles
test_payload = {
    "jobOffer": {
        "titre_de_poste": "Fullstack Python Developer",
        "competences_requises": ["Python", "JavaScript", "React", "Django", "SQL"],
        "departement": "IT",
        "localisation": "Casablanca"
    },
    "userProfiles": [
        # Perfect match candidate
        {
            "matricule": "dev001",
            "competences": ["Python", "Django", "JavaScript", "React", "SQL", "Git"],
            "formations": ["Master en Informatique Université Mohammed V", "Certification Python Django"],
            "experiences": ["Développeur Python Django 3 ans chez TechCorp", "Développeur Fullstack 2 ans chez WebSolutions"],
            "department": "IT",
            "position": "Développeur Senior"
        },
        # Good match candidate
        {
            "matricule": "dev002", 
            "competences": ["Python", "JavaScript", "HTML", "CSS"],
            "formations": ["Licence en Informatique"],
            "experiences": ["Développeur Junior Python 1 an"],
            "department": "IT",
            "position": "Développeur Junior"
        }
    ]
}

try:
    print("Testing Flask API with detailed profiles...")
    print(f"Sending payload with {len(test_payload['userProfiles'])} users")
    
    response = requests.post('http://127.0.0.1:5000/recommend/candidates-for-job', 
                           json=test_payload,
                           headers={'Content-Type': 'application/json'})
    
    print(f"Status Code: {response.status_code}")
    print(f"Raw Response: {response.text}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Parsed JSON: {data}")
            print(f"Success! Got {len(data)} recommendations")
            
            if data:
                print("\nAll recommendations:")
                for i, rec in enumerate(data):
                    matricule = rec['userProfile']['matricule']
                    score = rec['score']
                    print(f"  {i+1}. {matricule} - Score: {score}%")
                    
                # Analyze score distribution
                scores = [rec['score'] for rec in data]
                print(f"\nScore Analysis:")
                print(f"  Highest: {max(scores)}%")
                print(f"  Lowest: {min(scores)}%")
                print(f"  Average: {sum(scores)/len(scores):.1f}%")
                
                # Suggest thresholds
                print(f"\nRecommended Thresholds:")
                excellent = [s for s in scores if s >= 70]
                good = [s for s in scores if 50 <= s < 70]
                fair = [s for s in scores if 30 <= s < 50]
                poor = [s for s in scores if s < 30]
                
                print(f"  Excellent (≥70%): {len(excellent)} candidates")
                print(f"  Good (50-69%): {len(good)} candidates") 
                print(f"  Fair (30-49%): {len(fair)} candidates")
                print(f"  Poor (<30%): {len(poor)} candidates")
            else:
                print("No recommendations returned!")
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Request failed: {e}") 