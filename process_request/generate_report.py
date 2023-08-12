import csv
from math import ceil
from utilities.sql_access import get_connection
from . import celery_config

def generate_csv(report_id):
    # Define the current time and intervals
    current_time = '2023-01-25 14:13:22'
    one_hour_ago = 'DATE_SUB("' + current_time + '", INTERVAL 1 HOUR)'
    one_day_ago = 'DATE_SUB("' + current_time + '", INTERVAL 1 DAY)'
    one_week_ago = 'DATE_SUB("' + current_time + '", INTERVAL 1 WEEK)'
    
    # Calculate results for different time intervals and statuses
    result_one_hour_ago_active = calculate_total_time_query_active(one_hour_ago, current_time, 'active')
    result_one_day_ago_active = calculate_total_time_query_active(one_day_ago, current_time, 'active')
    result_one_week_ago_active = calculate_total_time_query_active(one_week_ago, current_time, 'active')
    
    result_one_hour_ago_inactive = calculate_total_time_query_active(one_hour_ago, current_time, 'inactive')
    result_one_day_ago_inactive = calculate_total_time_query_active(one_day_ago, current_time, 'inactive')
    result_one_week_ago_inactive = calculate_total_time_query_active(one_week_ago, current_time, 'inactive')
    
    # Prepare the data for CSV
    data = {}
    
    for result in result_one_hour_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['uptime_last_hour(in minutes)'] = round(ceil(result[1] / 60),2)
    
    for result in result_one_day_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['uptime_last_day(in hours)'] =round(ceil(result[1]/3600),2)
    
    for result in result_one_week_ago_active:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['update_last_week(in hours)'] = round(ceil(result[1]/3600),2)
    
    for result in result_one_hour_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_hour(in minutes)'] = round(ceil(result[1] / 60),2)
    
    for result in result_one_day_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_day(in hours)'] =round(ceil(result[1]/3600),2)
    
    for result in result_one_week_ago_inactive:
        store_id = result[0]
        if store_id not in data:
            data[store_id] = {}
        data[store_id]['downtime_last_week(in hours)'] = round(ceil(result[1]/3600),2)
    file_name="result"+str(report_id)+".csv"
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
    
def calculate_total_time_query_active(time_interval,current_time,status):
    connection=get_connection()
    cursor = connection.cursor()
    query = f'''
    SELECT 
    store_id,
    SUM(TIMESTAMPDIFF(SECOND, GREATEST({time_interval}, start_time), LEAST(end_time, "{current_time}"))) AS uptime 
    FROM historical_data
    WHERE status = "{status}"
    AND start_time < "{current_time}"
    AND end_time > {time_interval}
    GROUP BY store_id;
    '''
    cursor.execute(query)
   
    return cursor.fetchall()