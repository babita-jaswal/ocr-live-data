import pyodbc
from .db_connection import get_db_connection
from app.database.db_connection import execute_query

def execute_query(query, params=[]):
    """Reusable function to execute a database query."""
    connection = get_db_connection()
    if not connection:
        return {"error": "Database connection failed"}

    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return rows
    except pyodbc.Error as err:
        print(f"Database error: {err}")
        return {"error": "Database query failed", "details": str(err)}
    finally:
        connection.close()


def fetch_all_data():
    """Fetch all data from the database."""
    query = "SELECT * FROM applicants"
    return execute_query(query)


def fetch_paginated_data(page, per_page):
    """Fetch paginated data from the database."""
    offset = (page - 1) * per_page
    query = "SELECT * FROM applicants ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    return execute_query(query, [offset, per_page])


def fetch_applicant_by_id(doc_id):
    """Fetch a specific applicant's data by ID."""
    query = "SELECT * FROM applicants WHERE id = ?"
    result = execute_query(query, [doc_id])
    return result[0] if result else None

def fetch_applicant_data_from_db(aadhaar_number=None, applicant_name=None, mobile_number=None,
                                 verified=None, page=1, page_size=10):
    """Fetch applicant data from the database using a stored procedure."""
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Debugging: Print parameters
        print("Parameters sent to stored procedure:")
        print(f"AadhaarNumber: {aadhaar_number}, ApplicantName: {applicant_name}, "
              f"MobileNumber: {mobile_number}, Verified: {verified}, "
              f"Page: {page}, PageSize: {page_size}")

        # Execute stored procedure
        cursor.execute("""
            EXEC SP_GetApplicants 
                @AadhaarNumber = ?, 
                @ApplicantName = ?, 
                @MobileNumber = ?, 
                @Verified = ?, 
                @Page = ?, 
                @PageSize = ?
        """, (aadhaar_number, applicant_name, mobile_number, verified, page, page_size))

        # Fetch and format results
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return results

    except pyodbc.Error as e:
        return {"error": f"Database error: {str(e)}"}

    finally:
        if connection:
            connection.close()

def update_document_in_db(applicant_id, updated_data):
    """
    Update the applicant document in the database.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE Applicants
    SET aadhaar_number = ?, applicant_name = ?, bank_account_number = ?, block = ?, category = ?,
        date_of_birth = ?, district = ?, employer_address = ?, father_name = ?,
        first_name = ?, gender = ?, ifsc_code = ?, is_other_state_registered = ?, jurisdiction_labour_office = ?,
        last_name = ?, marital_status = ?, mobile_number = ?, occupation = ?, ocr_result_id = ?,
        other_registered_state = ?, other_state_registration_number = ?, permanent_address = ?, pincode = ?,
        state = ?, updated_on = ?, working_days = ?
    WHERE id = ?
    """
    cursor.execute(query, [
        updated_data.get("aadhaar_number"),
        updated_data.get("applicant_name"),
        updated_data.get("bank_account_number"),
        updated_data.get("block"),
        updated_data.get("category"),
        updated_data.get("date_of_birth"),
        updated_data.get("district"),
        updated_data.get("employer_address"),
        updated_data.get("father_name"),
        updated_data.get("first_name"),
        updated_data.get("gender"),
        updated_data.get("ifsc_code"),
        updated_data.get("is_other_state_registered"),
        updated_data.get("jurisdiction_labour_office"),
        updated_data.get("last_name"),
        updated_data.get("marital_status"),
        updated_data.get("mobile_number"),
        updated_data.get("occupation"),
        updated_data.get("ocr_result_id"),
        updated_data.get("other_registered_state"),
        updated_data.get("other_state_registration_number"),
        updated_data.get("permanent_address"),
        updated_data.get("pincode"),
        updated_data.get("state"),
        updated_data.get("updated_on"),
        updated_data.get("working_days"),
        applicant_id
    ])
    connection.commit()
    cursor.close()
    connection.close()
