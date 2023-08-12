from utilities.sql_access import get_connection
from datetime import datetime, timedelta
def create_and_populate_historical_data():
    connection=get_connection()
    cursor = connection.cursor()


    # Create a new table to store the extrapolated intervals
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historical_data (
            store_id BIGINT,
            start_time DATETIME,
            end_time DATETIME,
            status VARCHAR(255)
        )
    ''')

    # Query the original data from your existing table (replace 'your_table' with your actual table name)
    cursor.execute('SELECT store_id, local_time, status,start_time_local,end_time_local,custom_day_number FROM store_status_within_hours ORDER BY store_id, local_time')
    # cursor.execute("SELECT store_id, local_time, status,start_time_local,end_time_local,custom_day_number FROM store_status_within_hours WHERE store_id = '8190313151562460' ORDER BY store_id, local_time;")

    
    rows = cursor.fetchall()

    # Define the threshold to distinguish between active and inactive intervals (e.g., 15 minutes)
    threshold = timedelta(minutes=30)
    current_store=None
    current_status=None
    curr_day=None
    interval_start=None
    interval_end=None
    
    for i in range(0,len(rows)):
        store_id,local_time,status,start,end,day=rows[i]
        
        if current_store is None:
            current_store=store_id
            current_status=status
            curr_day=day
            interval_start=start
            interval_end=local_time
        else:
            if current_store!=store_id or day!=curr_day:
                last_element=rows[i-1]
               
                last_end_time=last_element[-2]
                interval_start=interval_end
                interval_end=last_end_time
                insert_query='''
                    INSERT INTO historical_data (store_id, start_time, end_time, status)
                    VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(insert_query,(current_store, interval_start, interval_end, current_status))
                current_store=store_id
                current_status=status
                curr_day=day
                interval_start=start
                interval_end=local_time
            else:
                interval_start=interval_end
                interval_end=local_time
                current_status=status
                curr_day=day

        if current_store is not None:
            insert_query='''
                INSERT INTO historical_data (store_id, start_time, end_time, status)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(insert_query,(current_store, interval_start, interval_end, current_status))
        

    # Commit the changes to the database
    connection.commit()
    cursor.close()
    # Close the database connection
    connection.close()

create_and_populate_historical_data()