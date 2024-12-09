from .db_connection import get_db_connection
from .database import fetch_all_data, fetch_paginated_data, fetch_applicant_by_id, fetch_applicant_data_from_db, update_document_in_db 
from .db_connection import get_db_connection

# Import the functions from database.py
from .database import (
    fetch_all_data,
    fetch_paginated_data,
    fetch_applicant_by_id,
    fetch_applicant_data_from_db,
    update_document_in_db
)

# Expose the necessary functions at the package level
__all__ = [
    "get_db_connection",
    "fetch_all_data",
    "fetch_paginated_data",
    "fetch_applicant_by_id",
    "fetch_applicant_data_from_db",
    "update_document_in_db"
]
