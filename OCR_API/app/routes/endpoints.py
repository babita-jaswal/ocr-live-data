from flask import Blueprint, request, jsonify
from app.routes.services import (
    get_all_applicants,
    get_paginated_applicants,
    get_applicant_by_id,
    update_applicant_document
   )
from app.auth import require_auth
from .services import fetch_filtered_applicant_data

# Create Blueprint for routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/api/ocr-data/applicants', methods=['GET'])
@require_auth
def fetch_all_data():
    """Fetch all applicant data."""
    data = get_all_applicants()
    if not data:
        return jsonify({"error": "No data found"}), 404
    return jsonify(data)

@main_bp.route('/api/ocr-data/applicants/page', methods=['GET'])
@require_auth
def fetch_paginated_data():
    """Fetch paginated applicant data."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    data = get_paginated_applicants(page, per_page)
    if not data:
        return jsonify({"error": "No data found"}), 404

    total_items = len(get_all_applicants())
    total_pages = (total_items + per_page - 1) // per_page

    return jsonify({
        "data": data,
        "total": total_items,
        "pages": total_pages,
        "current_page": page
    })

@main_bp.route('/api/ocr-data/applicants/filter', methods=['GET'])
@require_auth
def get_filtered_applicant_data():
    """Fetch filtered applicant data based on query parameters including verification status."""
    try:
        # Fetch query parameters
        aadhaar_number = request.args.get('aadhaarNumber', type=str)
        applicant_name = request.args.get('applicantName', type=str)
        mobile_number = request.args.get('mobileNumber', type=str)
        verified = request.args.get('verified', type=lambda v: v.lower() == 'true', default=None)
        page = request.args.get('pageNum', 1, type=int)
        page_size = request.args.get('pageSize', 10, type=int)

        # Fetch data from the service
        data = fetch_filtered_applicant_data(
            aadhaar_number=aadhaar_number,
            applicant_name=applicant_name,
            mobile_number=mobile_number,
            verified=verified,
            page=page,
            page_size=page_size
        )

        if isinstance(data, dict) and "error" in data:
            return jsonify(data), 500

        if not data:
            return jsonify({"message": "No data found"}), 404

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main_bp.route('/api/ocr-data/applicants/<int:applicant_id>', methods=['GET', 'PUT'])
@require_auth
def handle_applicant(applicant_id):
    """Handle fetching and updating applicant data by ID."""
    if request.method == 'GET':
        # Fetch applicant data from the database
        applicant_data = get_applicant_by_id(applicant_id)
        if applicant_data:
            return jsonify(applicant_data), 200
        else:
            return jsonify({"error": f"No applicant found with ID {applicant_id}"}), 404

    if request.method == 'PUT':
        # Get update data from the request body
        update_data = request.json
        if not update_data:
            return jsonify({"error": "No data provided for update"}), 400

        # Merge and validate data
        applicant_data = get_applicant_by_id(applicant_id)
        if not applicant_data:
            return jsonify({"error": "Applicant not found"}), 404
        
        updated_applicant_data = {**applicant_data, **update_data}

        # Update the database
        success = update_applicant_document(applicant_id, updated_applicant_data)
        if success:
            return jsonify({"message": "Applicant updated successfully", "data": updated_applicant_data}), 200
        else:
            return jsonify({"error": "Failed to update applicant"}), 500