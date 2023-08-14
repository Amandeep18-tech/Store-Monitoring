import os

csv_file_relative_path_store_status= "csv_files/store_status.csv"
table_name_store_status = "store_status"

csv_file_relative_path_menu_hours = "csv_files/Menu_hours.csv"
table_name_menu_hours = "menu_hours"

csv_file_relative_path_timezone = "csv_files/bq_results.csv"
table_name_store_timezone = "store_timezone"


upload_folder_output =  '/Users/amansingh/OneDrive/Job/Store_Monitoring'

current_max_time = '2023-01-25 14:13:22'
one_hour_ago = 'DATE_SUB("' + current_max_time + '", INTERVAL 1 HOUR)'
one_day_ago = 'DATE_SUB("' + current_max_time + '", INTERVAL 1 DAY)'
one_week_ago = 'DATE_SUB("' + current_max_time + '", INTERVAL 1 WEEK)'
    

db_config = {
        'host': '127.0.0.1',
        'user': "root",
        'password': os.environ.get("MYSQL_PASSWORD"),
        'database':"StoreMonitoring"
    }
