import os
import csv
from tqdm import tqdm
from datetime import datetime
from utilities.sql_access import get_connection

def upload_store_status():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_relative_path = "csv_files/store_status.csv"
    csv_file_path = os.path.join(parent_directory, csv_file_relative_path)
    table_name = "store_status"

    # Read CSV and insert data into MySQL table with tqdm progress bar
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header if necessary
        connection=get_connection()
        cursor = connection.cursor()

        # Create the table (if it doesn't exist)
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                store_id BIGINT,
                status VARCHAR(255),
                timestamp_utc DATETIME
            )
        """
        cursor.execute(create_table_query)

        insert_query = f"""
            INSERT INTO {table_name} (store_id, status, timestamp_utc)
            VALUES (%(store_id)s, %(status)s, %(timestamp_utc)s)
        """
        # Use tqdm to create a progress bar for the loop
        total_rows = sum(1 for _ in csv_reader)
        csv_file.seek(0)  # Reset file cursor to the beginning
        next(csv_reader)  # Skip header again
        for row in tqdm(csv_reader, total=total_rows, unit="rows"):
            store_id, status, timestamp_utc_str = row
            # Convert timestamp_utc to the proper datetime format
            timestamp_utc_str = timestamp_utc_str.replace(" UTC", "")
            
            # Check if the timestamp has milliseconds
            if "." in timestamp_utc_str:
                timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
            else:
                timestamp_format = '%Y-%m-%d %H:%M:%S'
            
            # Convert timestamp_utc to the proper datetime format
            timestamp_utc = datetime.strptime(timestamp_utc_str, timestamp_format)

            data = {
                "store_id": store_id,
                "status": status,
                "timestamp_utc": timestamp_utc
            }
            cursor.execute(insert_query, data)


        connection.commit()
        cursor.close()

    connection.close()
    return True



def upload_menu_hours():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_relative_path = "csv_files/Menu_hours.csv"
    csv_file_path = os.path.join(parent_directory, csv_file_relative_path)
    table_name = "menu_hours"
    
    # Read CSV and insert data into MySQL table with tqdm progress bar
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header if necessary
        connection=get_connection()
        cursor = connection.cursor()

        # Create the table (if it doesn't exist)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            store_id BIGINT,
            day INT,
            start_time_local TIME,
            end_time_local TIME
            )
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = f"""
            INSERT INTO {table_name} (store_id, day, start_time_local, end_time_local)
            VALUES (%(store_id)s, %(day)s, %(start_time_local)s, %(end_time_local)s)
            """
        total_rows = sum(1 for _ in csv_reader)
        csv_file.seek(0)  # Reset file cursor to the beginning
        next(csv_reader)  # Skip header again
        for row in tqdm(csv_reader, total=total_rows, unit="rows"):
            store_id,day,start_time_local_str,end_time_local_str = row
            data = {
                "store_id": store_id,
                "day": day,
                "start_time_local": start_time_local_str,
                "end_time_local": end_time_local_str
            }
            cursor.execute(insert_query, data)


        connection.commit()
        cursor.close()

    connection.close()
    return True

def upload_timezone():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file_relative_path = "csv_files/bq_results.csv"
    csv_file_path = os.path.join(parent_directory, csv_file_relative_path)
    table_name = "store_timezone"
    
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header if necessary
        
        connection = get_connection()
        cursor = connection.cursor()

        # Create the table (if it doesn't exist)
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            store_id BIGINT,
            timezone_str VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = f"""
            INSERT INTO {table_name} (store_id, timezone_str)
            VALUES (%s, %s)
            """
        
        for row in tqdm(csv_reader, unit="rows"):
            store_id, timezone_str = row
            data = (int(store_id), timezone_str)
            cursor.execute(insert_query, data)

        connection.commit()
        cursor.close()
        connection.close()
    return True

print(upload_menu_hours())
