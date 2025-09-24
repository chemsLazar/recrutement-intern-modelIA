import requests
import random

# Generate test data
user_profiles = [
    {
        "matricule": f"U{1000+i}",
        "firstName": name,
        "lastName": surname,
        "email": f"{name.lower()}.{surname.lower()}@example.com",
        "phone": f"06000000{str(i).zfill(2)}",
        "position": position,
        "department": department,
        "experiences": experiences,
        "formations": formations,
        "competences": competences
    }
    for i, (name, surname, position, department, experiences, formations, competences) in enumerate([
        ("Ali", "Ben Salah", "Développeur", "IT", ["Développement web", "Gestion de projet"], ["Master Informatique"], ["Python", "React", "Gestion de projet"]),
        ("Fatima", "El Amrani", "Analyste", "Finance", ["Analyse financière", "Audit"], ["Master Finance"], ["Excel", "Audit", "Comptabilité"]),
        ("Youssef", "Kabbaj", "RH", "Ressources Humaines", ["Recrutement", "Formation"], ["Master RH"], ["Communication", "Gestion RH"]),
        ("Sara", "Mouline", "Chef de Projet", "IT", ["Gestion de projet", "Déploiement"], ["MBA Gestion"], ["Scrum", "Gestion de projet", "Leadership"]),
        ("Omar", "Berrada", "Technicien", "Maintenance", ["Maintenance industrielle", "Sécurité"], ["BTS Maintenance"], ["Électricité", "Sécurité", "Réparation"]),
    ])
]

job_offers = [
    {
        "titre_de_poste": "Développeur Python",
        "description": "Développement d'applications backend.",
        "localisation": "Casablanca",
        "departement": "IT",
        "competences_requises": ["Python", "Django", "API REST"]
    },
    {
        "titre_de_poste": "Chef de Projet IT",
        "description": "Gestion de projets informatiques.",
        "localisation": "Rabat",
        "departement": "IT",
        "competences_requises": ["Gestion de projet", "Scrum", "Communication"]
    },
    {
        "titre_de_poste": "Analyste Financier",
        "description": "Analyse et reporting financier.",
        "localisation": "Casablanca",
        "departement": "Finance",
        "competences_requises": ["Excel", "Audit", "Comptabilité"]
    },
    {
        "titre_de_poste": "Responsable RH",
        "description": "Gestion des ressources humaines.",
        "localisation": "Marrakech",
        "departement": "Ressources Humaines",
        "competences_requises": ["Gestion RH", "Communication", "Recrutement"]
    },
    {
        "titre_de_poste": "Technicien Maintenance",
        "description": "Maintenance des équipements industriels.",
        "localisation": "Tanger",
        "departement": "Maintenance",
        "competences_requises": ["Électricité", "Sécurité", "Réparation"]
    },
    {
        "titre_de_poste": "Développeur Frontend",
        "description": "Développement d'interfaces utilisateur.",
        "localisation": "Agadir",
        "departement": "IT",
        "competences_requises": ["React", "JavaScript", "CSS"]
    },
    {
        "titre_de_poste": "Formateur RH",
        "description": "Formation et développement RH.",
        "localisation": "Fès",
        "departement": "Ressources Humaines",
        "competences_requises": ["Formation", "Gestion RH", "Communication"]
    },
    {
        "titre_de_poste": "Contrôleur de Gestion",
        "description": "Contrôle et suivi budgétaire.",
        "localisation": "Rabat",
        "departement": "Finance",
        "competences_requises": ["Comptabilité", "Excel", "Audit"]
    },
]

# Test each user against all job offers
url = "http://127.0.0.1:5000/recommend/jobs-for-candidate"

for user in user_profiles:
    payload = {
        "userProfile": user,
        "jobOffers": job_offers
    }
    response = requests.post(url, json=payload)
    print(f"\nRecommendations for {user['firstName']} {user['lastName']}:")
    if response.status_code == 200:
        for rec in response.json():
            job = rec['jobOffer']
            print(f"  - {job['titre_de_poste']} (score: {rec['score']:.2f})")
    else:
        print(f"  Error: {response.status_code} {response.text}") 