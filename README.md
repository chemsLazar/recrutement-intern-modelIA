# AI Recommendation Microservice

## Project Structure

```
AI_Recommendation/
├── app/
│   ├── __init__.py           # App factory, blueprint registration
│   ├── api.py                # API endpoints (routes)
│   └── recommender.py        # Recommendation logic (algorithms)
├── data/
│   ├── job_offers.json       # Sample job offers data
│   └── user_profiles.json    # Sample user profiles data
├── scripts/
│   ├── batch_job_to_users.py # Batch testing script
│   └── test_recommendation.py
├── tests/
│   ├── setup_ml.py           # ML setup and configuration
│   ├── test_api.py           # API endpoint tests
│   ├── test_consistency.py   # Consistency tests
│   ├── test_improved_algorithm.py # Algorithm improvement tests
│   ├── test_ml_enhanced.py   # Enhanced ML tests
│   └── test_simple.py        # Simple functionality tests
├── requirements.txt          # Python dependencies
├── run.py                    # Application entry point
└── README.md                 # Project documentation
```

## How to Run the Flask App

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the Flask server:**
   ```bash
   python run.py
   ```
   The server will run at `http://127.0.0.1:5000`.

## How to Test the Recommendations

### A. Enhanced ML Testing

1. **Test the new ML-enhanced system:**
   ```bash
   python tests/test_ml_enhanced.py
   ```
2. **What you'll see:**
   - Detailed breakdown of Direct, TF-IDF, and ML model scores
   - Processing time and performance metrics
   - Enhanced quality assessment (Excellent/Good/Fair/Weak)

### B. Batch: Best Users for Each Job

1. In a new terminal, run:
   ```bash
   python scripts/batch_job_to_users.py
   ```
2. **What you'll see:**
   - For each job, all user scores are displayed first.
   - Then, only the best matches (score >= 70%) are shown.
   - If no strong match, a message is printed.

### C. Individual Testing

- Use the JSON files in `data/` with curl or Postman to test the endpoints:
  - `/recommend/jobs-for-candidate`
  - `/recommend/candidates-for-job`

## How to Interpret the Results

- **Score ≈ 100%:** Excellent match
- **Score ≈ 70–100%:** Strong match (displayed as best)
- **Score < 70%:** Weak or no match
- **Score never exceeds 100%**

## Algorithms Used

- **Hybrid ML Approach:**
  - **Direct Matching:** Exact skill matches for precise compatibility
  - **TF-IDF Vectorization:** Traditional text similarity using cosine similarity
  - **Pre-trained ML Model:** Advanced semantic understanding using sentence transformers
  - **LightGBM Learned Scoring (optionnel):** combine automatiquement tous les signaux lorsque vous fournissez un modèle entraîné.
  - **Weighted Combination:** Fallback heuristique lorsque le modèle LightGBM n'est pas disponible

- **Pre-trained Model:**
  - Uses `all-MiniLM-L6-v2` for multilingual semantic understanding
  - Provides better matching for related skills and competencies
  - Handles French and English text effectively
  

## How to Extend

- Add more users/jobs to the JSON files in `data/`.
- Add new rules or change thresholds in `app/recommender.py` or the scripts.
- Add new endpoints or logic in `app/api.py`.
- Add automated tests in the `tests/` directory.

---

**This structure keeps your project clean, modular, and easy to maintain or extend!**

## Utiliser LightGBM pour la mise en production

1. **Former un modèle** : collectez des exemples annotés (match réussi ou non) et extrayez pour chacun les caractéristiques disponibles dans `app/recommender.py` (scores direct/TF‑IDF/transformer, tailles de listes, etc.). Entraînez un modèle LightGBM et exportez-le au format texte (`model.save_model('lightgbm_matcher.txt')`).
2. **Déposer le modèle** : placez le fichier généré dans `models/lightgbm_matcher.txt` (ou indiquez un autre chemin via la variable d'environnement `LIGHTGBM_MODEL_PATH`).
3. **Installer la dépendance** : `pip install -r requirements.txt` installe désormais LightGBM.
4. **Exécuter vos scripts** : au démarrage, le moteur charge le modèle LightGBM s'il est présent et remplace la combinaison pondérée par la prédiction apprise. En l'absence de modèle, le système utilise automatiquement le mode heuristique historique.
