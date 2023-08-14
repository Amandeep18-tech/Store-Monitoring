import os
import csv
from tqdm import tqdm
from datetime import datetime
from utilities.sql_utilities import MySQLCRUDUtility
import constants
from sql_queries.dml_queries import DMLQueries
from sql_queries.ddl_queries import DDLQueries

class CSVUploader:
    def __init__(self):
        self.sql_obj= MySQLCRUDUtility(constants.db_config)
        self.dml_queries=DMLQueries()
        self.ddl_queries=DDLQueries()
        
    def upload_store_status(self):
        """ Function to upload code in store status table
        """
        
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(parent_directory, constants.csv_file_relative_path_store_status)

        # Read CSV and insert data into MySQL table with tqdm progress bar
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header if necessary
            self.sql_obj.connect()
            self.sql_obj.create_table(self.ddl_queries.create_table_store_status())
            
            # Use tqdm to create a progress bar for the loop
            total_rows = sum(1 for _ in csv_reader)
            csv_file.seek(0)  # Reset file cursor to the beginning
            next(csv_reader)  # Skip header again
            data_list=[]
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

                data = (store_id,status,timestamp_utc)
                data_list.append(data)
            self.sql_obj.execute_insert_update_many(self.dml_queries.insert_query_into_stores_status_table(),data_list)
            self.sql_obj.commit()
        self.sql_obj.disconnect()
        return True



    def upload_menu_hours(self):
        """
        Function to upload data in menu hours table
        """
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(parent_directory, constants.csv_file_relative_path_menu_hours  )
        self.sql_obj.connect()
        # Read CSV and insert data into MySQL table with tqdm progress bar
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header if necessary
    
            # Create the table (if it doesn't exist)
            self.sql_obj.create_table(self.ddl_queries.create_table_menu_hours())
            total_rows = sum(1 for _ in csv_reader)
            csv_file.seek(0)  # Reset file cursor to the beginning
            next(csv_reader)  # Skip header again
            data_list=[]
            for row in tqdm(csv_reader, total=total_rows, unit="rows"):
                store_id,day,start_time_local_str,end_time_local_str = row
                data = (store_id,day,start_time_local_str,end_time_local_str)
                data_list.append(data)
            self.sql_obj.execute_insert_update_many(self.dml_queries.insert_query_into_menu_hours_table(),data_list)
            self.sql_obj.commit()
        self.sql_obj.disconnect()
        return True

    def upload_timezone(self):
        """
        Function to upload data in store_timezone table
        """
        
        parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_file_path = os.path.join(parent_directory, constants.csv_file_relative_path_timezone)
        self.sql_obj.connect()
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header if necessary
            
            self.sql_obj.create_table(self.ddl_queries.create_table_timezone())
            data_list=[]
            
            for row in tqdm(csv_reader, unit="rows"):
                store_id, timezone_str = row
                data = (int(store_id), timezone_str)
                
                data_list.append(data)
            self.sql_obj.execute_insert_update_many(self.dml_queries.insert_query_into_store_timezone_table(),data_list)
            self.sql_obj.commit()
        self.sql_obj.disconnect()
        return True

    
csv_uploader=CSVUploader()
# csv_uploader.upload_store_status()
csv_uploader.upload_menu_hours()
# csv_uploader.upload_timezone()