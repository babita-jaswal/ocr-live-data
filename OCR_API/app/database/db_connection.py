import pyodbc
from config.config import DB_CONFIG

def get_db_connection():
    """Establish and return a database connection."""
    connection = pyodbc.connect(
         f"DRIVER={DB_CONFIG['driver']};"
            f"SERVER={DB_CONFIG['server']};"
            f"DATABASE={DB_CONFIG['database']};"
            f"UID={DB_CONFIG['uid']};"
            f"PWD={DB_CONFIG['pwd']}"
    )
    return connection

def execute_query(query, params=None):
    """Execute a query on the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        connection.close()
