from utilities.sql_access import get_connection
import mysql.connector
import pytz
from datetime import datetime, timedelta
def update_missing_timezones():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Find missing store_id values in store_timezone
        missing_store_ids_query = """
        SELECT DISTINCT(store_id)
        FROM store_status
        WHERE store_id NOT IN (SELECT store_id FROM store_timezone)
        """
        cursor.execute(missing_store_ids_query)
        missing_store_ids = [row[0] for row in cursor.fetchall()]

        # Insert missing store_id values with default timezone_str
        insert_query = """
        INSERT INTO store_timezone (store_id, timezone_str)
        VALUES (%s, 'America/Chicago')
        """
        for store_id in missing_store_ids:
            cursor.execute(insert_query, (store_id,))
            connection.commit()

    except mysql.connector.Error as err:
        print("Error:", err)
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def update_timezone_to_offset():
  
    connection = get_connection()
    cursor = connection.cursor()


    # Step 1: Add a new column to Table-3 to store the UTC offset
    alter_table_sql = "ALTER TABLE store_timezone ADD COLUMN utc_offset VARCHAR(10)"

    # Execute the SQL statement to add the new column
    cursor.execute(alter_table_sql)

    # Fetch data from Table-3
    select_data_sql = "SELECT store_id, timezone_str FROM store_timezone"
    cursor.execute(select_data_sql)
    rows = cursor.fetchall()

    # Step 2: Convert timezone_str to UTC offset and update the new column
    update_utc_offset_sql = "UPDATE store_timezone SET utc_offset = %s WHERE store_id = %s"

    for row in rows:
        store_id = row[0]
        timezone_str = row[1]
        timezone_value= str(datetime.now(pytz.timezone(timezone_str)))
        len_time=len(timezone_value)
        timezone_offset=timezone_value[len_time-6:len_time]
        
        # Execute the SQL statement to update the utc_offset
        cursor.execute(update_utc_offset_sql, (timezone_offset, store_id))

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

# Call the function to update missing timezones
# update_missing_timezones()
update_timezone_to_offset()