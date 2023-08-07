from utilities.sql_access import get_connection

def update_missing_timezones():
    print("Updating missing timezones")
    connection=get_connection()
    cursor = connection.cursor()
    
    # Update the timezone_str column for stores with missing data
    update_query = """
    UPDATE store_timezone
    SET timezone_str = 'America/Chicago'
    WHERE timezone_str IS NULL
    """

    cursor.execute(update_query)
    connection.commit()

    cursor.close()
    connection.close()

# Call the function to update missing timezones
update_missing_timezones()