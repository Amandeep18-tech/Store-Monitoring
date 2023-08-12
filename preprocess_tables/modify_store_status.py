from utilities.sql_access import get_connection

def add_local_time_column():
    connection=get_connection()
    cursor = connection.cursor()
    # SQL statement to create the local_time column in Table-1
    create_column_sql = "ALTER TABLE store_status ADD COLUMN IF NOT EXISTS local_time DATETIME"

    # Execute the SQL statement to create the column
    cursor.execute(create_column_sql)
    
    
def update_menu_hours_to_utc():

    connection=get_connection()
    cursor = connection.cursor()

    # SQL statement to update local_time in Table-1 using JOIN with Table-3
    update_local_time_sql = """
        UPDATE store_status t1
        JOIN store_timezone t3 ON t1.store_id = t3.store_id
        SET t1.local_time = CONVERT_TZ(t1.timestamp_utc, '+00:00',t3.utc_offset)
    """
    
    # Execute the SQL statement to update local_time
    cursor.execute(update_local_time_sql)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    
def add_custom_day_column():

    connection=get_connection()
    cursor = connection.cursor()
    # Add the custom_day_number column to Table-1 if it doesn't exist
    add_column_sql = """
        ALTER TABLE store_status
        ADD COLUMN custom_day_number INT
    """

    # Execute the SQL statement to add the column
    cursor.execute(add_column_sql)
    connection.commit()
    cursor.close()
    connection.close()
    
def update_custom_day_number():
    connection=get_connection()
    cursor = connection.cursor()
    # Update the custom_day_number using the provided formula
    update_custom_day_sql = """
        UPDATE store_status
        SET custom_day_number = (DAYOFWEEK(local_time) + 5) % 7
    """

    # Execute the SQL statement to update custom_day_number
    cursor.execute(update_custom_day_sql)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def add_start_end_local_time_columns():
    

    connection=get_connection()
    cursor = connection.cursor()

    # Add the start_time_local and end_time_local columns to Table-1 if they don't exist
    add_columns_sql = """
        ALTER TABLE store_status
        ADD COLUMN start_time_local DATETIME,
        ADD COLUMN end_time_local DATETIME
    """

    # Execute the SQL statement to add the columns
    cursor.execute(add_columns_sql)
    connection.commit()
    cursor.close()
    connection.close()
    
def update_start_end_columns():
    connection=get_connection()
    cursor = connection.cursor()

    # Update start_time_local and end_time_local using the provided JOIN and CONCAT
    update_time_sql = """
        UPDATE store_status t1
        JOIN menu_hours t2 ON t1.store_id = t2.store_id AND t1.custom_day_number = t2.day
        SET t1.start_time_local = CONCAT(DATE(t1.local_time), ' ', t2.start_time_local),
            t1.end_time_local = CONCAT(DATE(t1.local_time), ' ', t2.end_time_local)
    """

    # Execute the SQL statement to update start_time_local and end_time_local
    cursor.execute(update_time_sql)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

# update_menu_hours_to_utc()
# add_custom_day_column()
# update_custom_day_number()

# add_start_end_local_time_columns()
update_start_end_columns()


