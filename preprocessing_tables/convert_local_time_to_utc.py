from utilities.sql_access import get_connection
import mysql.connector
from datetime import datetime
import pytz

def get_offset(timezone_str):
    timezone_value= datetime.now(pytz.timezone(timezone_str))

    parts = str(timezone_value).split("-")

    # Extract the time zone offset part (last element of the split)
    time_zone_offset = "-" + parts[-1]
    return time_zone_offset
def update_menu_hours_to_utc():
    connection=get_connection()
    cursor = connection.cursor()
    # Fetch store_id and timezone_str from store_timezone table
    
    alter_table_query = """
    ALTER TABLE menu_hours
    ADD COLUMN start_time_utc TIME,
    ADD COLUMN end_time_utc TIME
    """
    try:
        cursor.execute(alter_table_query)
    except mysql.connector.Error as err:
        print("Error:", err)

    select_query = """
    SELECT store_id, timezone_str
    FROM store_timezone
    """
    cursor.execute(select_query)
    store_timezones = cursor.fetchall()
    print("store_timezones:", store_timezones)
    
     # Update menu_hours table with UTC values
    update_query = """
    UPDATE menu_hours
    SET start_time_utc = CONVERT_TZ(TIME(start_time_local), %s, '+00:00'),
        end_time_utc = CONVERT_TZ(TIME(end_time_local), %s, '+00:00')
    WHERE store_id = %s
    """

    for store_id, timezone_str in store_timezones:
        try:
            print(f"Updating store_id: {store_id} with timezone: {timezone_str}")
            offset = get_offset(timezone_str)
            print(offset)
            cursor.execute(update_query, (offset, offset, store_id,))
            connection.commit()
            print("Update committed")
        except Exception as e:
            print(f"Error updating store_id: {store_id}, Error: {str(e)}")
    
    cursor.close()
    connection.close()
    
update_menu_hours_to_utc()