#!/usr/bin/env python3
"""
Simple test script to demonstrate the AI recommendation system
"""

import requests
import json

def test_simple_recommendation():
    """Test with simple, clear data"""
    
    print("🧪 Testing AI Recommendation System")
    print("=" * 50)
    
    # Simple test data
    test_data = {
        "jobOffer": {
            "titre_de_poste": "Développeur Python",
            "competences_requises": ["Python", "Django", "API REST"],
            "departement": "IT"
        },
        "userProfiles": [
            {
                "matricule": "DEV001",
                "firstName": "Ahmed",
                "lastName": "Alami", 
                "competences": ["Python", "Django", "API REST", "PostgreSQL"],
                "department": "IT"
            },
            {
                "matricule": "DEV002",
                "firstName": "Fatima",
                "lastName": "Benali",
                "competences": ["Java", "Spring Boot", "MySQL"],
                "department": "IT"
            },
            {
                "matricule": "RH001",
                "firstName": "Sara",
                "lastName": "Mouline",
                "competences": ["Gestion RH", "Communication"],
                "department": "Ressources Humaines"
            }
        ]
    }
    
    try:
        print("📡 Sending request to AI system...")
        response = requests.post(
            'http://127.0.0.1:5000/recommend/candidates-for-job',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Success! Got {len(results)} recommendations")
            print("\n🎯 AI RECOMMENDATIONS:")
            print("-" * 40)
            
            for i, rec in enumerate(results, 1):
                user = rec['userProfile']
                score = rec['score']
                
                # Determine match quality
                if score >= 70:
                    quality = "🌟 EXCELLENT"
                elif score >= 50:
                    quality = "⭐ GOOD"
                elif score >= 30:
                    quality = "📈 FAIR"
                else:
                    quality = "📉 WEAK"
                
                print(f"{i}. {user['matricule']} | {user['firstName']} {user['lastName']}")
                print(f"   Score: {score:.1f}% | Quality: {quality}")
                print(f"   Skills: {', '.join(user['competences'])}")
                print()
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error - Make sure the Flask server is running")
        print("   Run: python run.py")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    test_simple_recommendation()
