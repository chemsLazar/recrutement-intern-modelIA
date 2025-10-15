from flask import Blueprint, request, jsonify
from .recommender import match_jobs_for_candidate, match_candidates_for_job
import traceback

api_bp = Blueprint('api', __name__)

@api_bp.route('/recommend/jobs-for-candidate', methods=['POST'])
def recommend_jobs_for_candidate():
    try:
        print('\n=== JOBS FOR CANDIDATE REQUEST ===')
        data = request.get_json(force=True)
        print('Received payload keys:', list(data.keys()) if data else 'None')
        print('Payload size:', len(str(data)) if data else 0, 'characters')
        
        # Validate payload
        if not data or 'userProfile' not in data or 'jobOffers' not in data:
            print('ERROR: Missing required fields')
            return jsonify({'error': 'Payload must contain userProfile and jobOffers'}), 400

        user_profile = data['userProfile']
        job_offers = data['jobOffers']
        
        print('User profile matricule:', user_profile.get('matricule', 'N/A'))
        print('Number of job offers:', len(job_offers))

        # Defensive: Ensure all required fields exist and are the right type
        if not isinstance(job_offers, list):
            print('ERROR: jobOffers is not a list')
            return jsonify({'error': 'jobOffers must be a list'}), 400
        if not isinstance(user_profile, dict):
            print('ERROR: userProfile is not a dict')
            return jsonify({'error': 'userProfile must be an object'}), 400

        print('Starting recommendation process...')
        results = match_jobs_for_candidate(user_profile, job_offers)
        print('Recommendation completed, returning', len(results), 'results')
        return jsonify(results)
        
    except Exception as e:
        print('ERROR in recommend_jobs_for_candidate:', str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/recommend/candidates-for-job', methods=['POST'])
def recommend_candidates_for_job():
    try:
        print('\n=== CANDIDATES FOR JOB REQUEST ===')
        data = request.get_json(force=True)
        print('Received payload keys:', list(data.keys()) if data else 'None')
        print('Payload size:', len(str(data)) if data else 0, 'characters')
        
        if not data or 'jobOffer' not in data or 'userProfiles' not in data:
            print('ERROR: Missing required fields')
            return jsonify({'error': 'Payload must contain jobOffer and userProfiles'}), 400

        job_offer = data['jobOffer']
        user_profiles = data['userProfiles']
        
        print('Job offer title:', job_offer.get('titre_de_poste', 'N/A'))
        print('Number of user profiles:', len(user_profiles))

        if not isinstance(user_profiles, list):
            print('ERROR: userProfiles is not a list')
            return jsonify({'error': 'userProfiles must be a list'}), 400
        if not isinstance(job_offer, dict):
            print('ERROR: jobOffer is not a dict')
            return jsonify({'error': 'jobOffer must be an object'}), 400

        print('Starting recommendation process...')
        results = match_candidates_for_job(job_offer, user_profiles)
        print('Recommendation completed, returning', len(results), 'results')
        return jsonify(results)
        
    except Exception as e:
        print('ERROR in recommend_candidates_for_job:', str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500 