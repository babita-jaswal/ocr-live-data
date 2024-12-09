from app.database import fetch_all_data, fetch_paginated_data, fetch_applicant_by_id, fetch_applicant_data_from_db, update_document_in_db

def get_all_applicants():
    """Fetch all applicant data."""
    return fetch_all_data()

def get_paginated_applicants(page, per_page):
    """Fetch paginated applicant data."""
    return fetch_paginated_data(page, per_page)

def get_applicant_by_id(doc_id):
    """Fetch a single applicant by ID."""
    return fetch_applicant_by_id(doc_id)

def fetch_filtered_applicant_data(aadhaar_number=None, applicant_name=None, mobile_number=None, verified=None, page=1, page_size=10):
    """Service to fetch filtered applicant data."""
    try:
        return fetch_applicant_data_from_db(
            aadhaar_number=aadhaar_number,
            applicant_name=applicant_name,
            mobile_number=mobile_number,
            verified=verified,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        return {"error": str(e)}
    
def update_applicant_document(applicant_id, updated_data):
    """
    Update the applicant document in the database.
    """
    try:
        update_document_in_db(applicant_id, updated_data)
        return True
    except Exception as e:
        print(f"Error updating document: {e}")
        return False

