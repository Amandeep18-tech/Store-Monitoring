from utilities.sql_access import get_connection
import mysql.connector

def update_missing_fields():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Find missing store_id values in store_timezone
        missing_store_ids_query = """
        select distinct(store_id) from store_status where store_id not in(SELECT store_id FROM menu_hours);
        """
        cursor.execute(missing_store_ids_query)
        missing_store_ids = [row[0] for row in cursor.fetchall()]
        # Insert missing values in menu_hours for 24/7 operation
        insert_query = """
        INSERT INTO menu_hours (store_id, day, start_time_local,end_time_local)
        VALUES (%s, %s, '00:00:00', '23:59:59')
        """
    
        for store_id in missing_store_ids:
            for dayOfWeek in range(7):  # 0 to 6 representing days of the week
                cursor.execute(insert_query, (store_id, dayOfWeek))
                connection.commit()

    except mysql.connector.Error as err:
        print("Error:", err)
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

    print("Missing values inserted into menu_hours for 24/7 operation.")



# update_menu_hours_to_utc()


update_missing_fields()