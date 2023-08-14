import constants

class DMLQueries:
    def insert_query_into_stores_status_table(self):
        insert_query = f"""
                INSERT INTO {constants.table_name_store_status} (store_id, status, timestamp_utc)
                VALUES (%s, %s, %s)
            """
            
        return insert_query

    def insert_query_into_menu_hours_table(self):
        # Insert data into the table
        insert_query = f"""
            INSERT INTO {constants.table_name_menu_hours} (store_id, day, start_time_local, end_time_local)
            VALUES (%s, %s, %s, %s)
            """
            
        return insert_query
    
    def insert_query_into_store_timezone_table(self):
        insert_query = f"""
                INSERT INTO {constants.table_name_store_timezone} (store_id, timezone_str)
                VALUES (%s, %s)
                """
                
        return insert_query
    
    def missing_store_ids_query_menu_hours(self):
        missing_store_ids_query = """
                select distinct(store_id) from store_status where store_id not in(SELECT store_id FROM menu_hours);
                """
                
        return missing_store_ids_query

    def insert_query_full_availability_menu_hours(self):
        insert_query = """
        INSERT INTO menu_hours (store_id, day, start_time_local,end_time_local)
        VALUES (%s, %s, '00:00:00', '23:59:59')
        """
        return insert_query
    
    def missing_store_id_timezone(self):
        missing_store_ids_query = """
        SELECT DISTINCT(store_id)
        FROM store_status
        WHERE store_id NOT IN (SELECT store_id FROM store_timezone)
        """
        return missing_store_ids_query
    
    def insert_query_update_missing_timezone(self):
        # Insert missing store_id values with default timezone_str
        insert_query = """
        INSERT INTO store_timezone (store_id, timezone_str)
        VALUES (%s, 'America/Chicago')
        """
        return insert_query
    
    def select_query_store_timezone(self):
        select_data_sql = "SELECT store_id, timezone_str FROM store_timezone"
        return select_data_sql
    
    def update_query_store_timezone(self):
        update_utc_offset_sql = "UPDATE store_timezone SET time_offset = %s WHERE store_id = %s"
        return update_utc_offset_sql
    
    def update_menu_hours_to_local_timezone(self):
        update_local_time_sql = """
            UPDATE store_status t1
            JOIN store_timezone t3 ON t1.store_id = t3.store_id
            SET t1.local_time = CONVERT_TZ(t1.timestamp_utc, '+00:00',t3.time_offset)
        """
        return update_local_time_sql
    
    def update_custom_day(self):
        update_custom_day_sql = """
            UPDATE store_status
            SET custom_day_number = (DAYOFWEEK(local_time) + 5) % 7
        """
        return update_custom_day_sql
    
    def update_store_status_start_end_time(self):
        update_time_sql = """
            UPDATE store_status t1
            JOIN menu_hours t2 ON t1.store_id = t2.store_id AND t1.custom_day_number = t2.day
            SET t1.start_time_local = CONCAT(DATE(t1.local_time), ' ', t2.start_time_local),
            t1.end_time_local = CONCAT(DATE(t1.local_time), ' ', t2.end_time_local)
        """
        return update_time_sql
    
    def select_store_status_within_hours_sorted(self):
        query='''SELECT store_id, local_time, status,start_time_local,end_time_local,custom_day_number 
        FROM store_status_within_hours 
        ORDER BY store_id, local_time'''
        return query
    
    def insert_data_in_historical_table(self):
        query=f'''INSERT INTO historical_data (store_id, start_time, end_time, status)
                    VALUES (%s, %s, %s, %s)
                '''
        return query
    def query_data_in_historical_table(self,time_interval,current_time,status):
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
        return query
    
    
    
    