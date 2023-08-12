
from utilities.sql_access import get_connection


def make_table_store_status_within_hours_table():
    
    connection = get_connection()
    cursor = connection.cursor()

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Build and execute the CREATE TABLE query
    query = """
        CREATE TABLE store_status_within_hours AS
        SELECT store_id, status, local_time, start_time_local, end_time_local, custom_day_number
        FROM store_status
        WHERE local_time < end_time_local AND local_time > start_time_local
    """

    cursor.execute(query)

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

make_table_store_status_within_hours_table()