from celery_config import create_app
from celery import shared_task
import uuid
from math import ceil
import csv
import constants
from utilities.sql_utilities import MySQLCRUDUtility
from utilities.dml_queries import DMLQueries

sql_obj=MySQLCRUDUtility(constants.db_config)
dml_queries=DMLQueries()
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

# Define a Celery task

@shared_task(ignore_result=False)
def generate_csv():
    report_id = str(uuid.uuid4())
    # Define the current time and intervals
   
    # Calculate results for different time intervals and statuses
    result_one_hour_ago_active = calculate_total_time_query_active(constants.one_hour_ago , constants.current_max_time, 'active')
    result_one_day_ago_active = calculate_total_time_query_active(constants.one_day_ago , constants.current_max_time, 'active')
    result_one_week_ago_active = calculate_total_time_query_active(constants.one_week_ago , constants.current_max_time, 'active')
    
    result_one_hour_ago_inactive = calculate_total_time_query_active(constants.one_hour_ago , constants.current_max_time, 'inactive')
    result_one_day_ago_inactive = calculate_total_time_query_active(constants.one_day_ago , constants.current_max_time, 'inactive')
    result_one_week_ago_inactive = calculate_total_time_query_active(constants.one_week_ago , constants.current_max_time, 'inactive')
    
    # Prepare the data for CSV
    data = {}
    sql_obj.disconnect()
    for result in result_one_hour_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['uptime_last_hour(in minutes)'] = round(result[1] / 60,2)
    
    for result in result_one_day_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['uptime_last_day(in hours)'] =round(result[1]/3600,2)
    
    for result in result_one_week_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['update_last_week(in hours)'] = round(result[1]/3600,2)
    
    for result in result_one_hour_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_hour(in minutes)'] = round(result[1] / 60,2)
    
    for result in result_one_day_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_day(in hours)'] =round(result[1]/3600,2)
    
    for result in result_one_week_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_week(in hours)'] = round(result[1]/3600,2)
    file_name="result_"+str(report_id)+".csv"
    
    # Write results to CSV
    with open(file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header row
        result_columns = ['store_id', 'uptime_last_hour(in minutes)', 'uptime_last_day(in hours)',
                          'update_last_week(in hours)', 'downtime_last_hour(in minutes)',
                          'downtime_last_day(in hours)', 'downtime_last_week(in hours)']
        csv_writer.writerow(result_columns)
        
        # Write data rows
        for store_id, values in data.items():
            csv_writer.writerow([store_id,
                                 values.get('uptime_last_hour(in minutes)', 0),
                                 values.get('uptime_last_day(in hours)', 0),
                                 values.get('update_last_week(in hours)', 0),
                                 values.get('downtime_last_hour(in minutes)', 0),
                                 values.get('downtime_last_day(in hours)', 0),
                                 values.get('downtime_last_week(in hours)', 0)])
    

    return file_name

#query to get uptime and downtime 
def calculate_total_time_query_active(time_interval,current_time,status):
    sql_obj.connect()
    return sql_obj.read(dml_queries.query_data_in_historical_table(time_interval,current_time,status))




