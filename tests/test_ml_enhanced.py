#!/usr/bin/env python3
"""
Test script for the enhanced ML-powered recommendation system
Tests the hybrid approach: Direct matching + TF-IDF + Pre-trained ML model
"""

import requests
import json
import time

def test_ml_enhanced_recommendations():
    """Test the enhanced ML recommendation system"""
    
    print("🚀 Testing Enhanced ML Recommendation System")
    print("=" * 60)
    
    # Test data with more complex competency matching
    test_payload = {
        "jobOffer": {
            "titre_de_poste": "Développeur Full Stack Senior",
            "competences_requises": ["Python", "JavaScript", "React", "Django", "PostgreSQL", "Docker", "Git"],
            "departement": "IT",
            "localisation": "Casablanca",
            "description": "Développement d'applications web complètes avec Python/Django et React"
        },
        "userProfiles": [
            # Perfect match candidate
            {
                "matricule": "DEV001",
                "firstName": "Ahmed",
                "lastName": "Alami",
                "competences": ["Python", "Django", "JavaScript", "React", "PostgreSQL", "Docker", "Git", "API REST"],
                "formations": ["Master Informatique", "Certification AWS"],
                "experiences": ["Développeur Full Stack 4 ans", "Lead Developer 2 ans"],
                "department": "IT",
                "position": "Développeur Senior"
            },
            # Good match with some missing skills
            {
                "matricule": "DEV002",
                "firstName": "Fatima",
                "lastName": "Benali",
                "competences": ["Python", "JavaScript", "HTML", "CSS", "MySQL"],
                "formations": ["Licence Informatique"],
                "experiences": ["Développeur Frontend 2 ans"],
                "department": "IT",
                "position": "Développeur"
            },
            # Partial match with different tech stack
            {
                "matricule": "DEV003",
                "firstName": "Youssef",
                "lastName": "Kabbaj",
                "competences": ["Java", "Spring Boot", "Angular", "Oracle", "Maven"],
                "formations": ["Master Génie Logiciel"],
                "experiences": ["Développeur Java 3 ans"],
                "department": "IT",
                "position": "Développeur Java"
            },
            # Weak match - different domain
            {
                "matricule": "RH001",
                "firstName": "Sara",
                "lastName": "Mouline",
                "competences": ["Gestion RH", "Communication", "Recrutement", "Formation"],
                "formations": ["Master RH"],
                "experiences": ["Responsable RH 5 ans"],
                "department": "Ressources Humaines",
                "position": "Responsable RH"
            }
        ]
    }
    
    try:
        print("📡 Sending request to enhanced ML API...")
        start_time = time.time()
        
        response = requests.post(
            'http://127.0.0.1:5000/recommend/candidates-for-job',
            json=test_payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"⏱️ Processing time: {processing_time:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success! Got {len(data)} recommendations")
                
                if data:
                    print("\n🎯 ENHANCED ML RECOMMENDATIONS:")
                    print("-" * 60)
                    
                    for i, rec in enumerate(data, 1):
                        user = rec['userProfile']
                        score = rec['score']
                        
                        # Determine match quality
                        if score >= 80:
                            quality = "🌟 EXCELLENT"
                        elif score >= 60:
                            quality = "⭐ GOOD"
                        elif score >= 40:
                            quality = "📈 FAIR"
                        else:
                            quality = "📉 WEAK"
                        
                        print(f"{i}. {user['matricule']} | {user['firstName']} {user['lastName']}")
                        print(f"   Score: {score:.1f}% | Quality: {quality}")
                        print(f"   Skills: {', '.join(user['competences'][:5])}...")
                        print()
                    
                    # Analyze score distribution
                    scores = [rec['score'] for rec in data]
                    print("📈 SCORE ANALYSIS:")
                    print(f"   Highest: {max(scores):.1f}%")
                    print(f"   Lowest: {min(scores):.1f}%")
                    print(f"   Average: {sum(scores)/len(scores):.1f}%")
                    
                    # Enhanced threshold analysis
                    excellent = [s for s in scores if s >= 80]
                    good = [s for s in scores if 60 <= s < 80]
                    fair = [s for s in scores if 40 <= s < 60]
                    weak = [s for s in scores if s < 40]
                    
                    print(f"\n🎯 ENHANCED THRESHOLDS:")
                    print(f"   🌟 Excellent (≥80%): {len(excellent)} candidates")
                    print(f"   ⭐ Good (60-79%): {len(good)} candidates")
                    print(f"   📈 Fair (40-59%): {len(fair)} candidates")
                    print(f"   📉 Weak (<40%): {len(weak)} candidates")
                    
                    # ML Model Performance Analysis
                    print(f"\n🤖 ML MODEL PERFORMANCE:")
                    print(f"   Processing time: {processing_time:.2f}s")
                    print(f"   Recommendations generated: {len(data)}")
                    print(f"   Average score: {sum(scores)/len(scores):.1f}%")
                    
                    if len(excellent) > 0:
                        print(f"   ✅ Found {len(excellent)} excellent matches!")
                    else:
                        print(f"   ⚠️ No excellent matches found")
                        
                else:
                    print("❌ No recommendations returned!")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON: {e}")
                print(f"Raw response: {response.text}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - ML model might be loading")
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error - Make sure the Flask server is running")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

def test_model_loading():
    """Test if the ML model loads correctly"""
    print("\n🔧 Testing ML Model Loading...")
    
    try:
        from app.recommender import ML_MODEL
        if ML_MODEL is not None:
            print("✅ Pre-trained ML model loaded successfully!")
            print(f"   Model: {ML_MODEL}")
        else:
            print("⚠️ ML model not loaded - using fallback mode")
    except Exception as e:
        print(f"❌ Error loading ML model: {e}")

if __name__ == "__main__":
    print("🧪 ML Enhanced Recommendation System Test")
    print("=" * 60)
    
    # Test model loading first
    test_model_loading()
    
    # Test the enhanced recommendations
    test_ml_enhanced_recommendations()
    
    print("\n✨ Test completed!")
