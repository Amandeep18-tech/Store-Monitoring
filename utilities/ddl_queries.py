import constants

class DDLQueries():
    
    def create_table_store_status(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {constants.table_name_store_status} (
                store_id BIGINT,
                status VARCHAR(255),
                timestamp_utc DATETIME
            )
        """
        return create_table_query
    
    def create_table_menu_hours(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {constants.table_name_menu_hours} (
                store_id BIGINT,
                day INT,
                start_time_local TIME,
                end_time_local TIME
                )
            """
        return create_table_query
    
    def create_table_timezone(self):
        # Create the table (if it doesn't exist)
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {constants.table_name_store_timezone} (
                store_id BIGINT,
                timezone_str VARCHAR(255)
            )
            """
        return create_table_query
    
    def create_index_on_store_timezone(self):
    
        create_index_sql = "CREATE INDEX idx_store_id ON store_timezone (store_id)"
        return create_index_sql
    
    def create_index_on_menu_hours(self):
        create_index_sql = "CREATE INDEX idx_store_id ON menu_hours (store_id)"
        return create_index_sql
    
    def alter_table_add_timezone_offset_column(self):
        alter_table_sql = "ALTER TABLE store_timezone ADD COLUMN time_offset VARCHAR(10)"
        return alter_table_sql
    
    def alter_table_add_local_time_column(self):
        create_column_sql = "ALTER TABLE store_status ADD COLUMN local_time DATETIME"
        return create_column_sql
    
    def add_custom_day_column(self):
        add_column_sql = """
                ALTER TABLE store_status
                ADD COLUMN custom_day_number INT
            """
        return add_column_sql
    
    def add_start_end_time_column(self):
        
        add_columns_sql = """
            ALTER TABLE store_status
            ADD COLUMN start_time_local DATETIME,
            ADD COLUMN end_time_local DATETIME
        """
        return add_columns_sql
    
    def create_table_store_status_within_hours(self):
        query = """
                CREATE TABLE store_status_within_hours AS
                SELECT store_id, status, local_time, start_time_local, end_time_local, custom_day_number
                FROM store_status
                WHERE local_time < end_time_local AND local_time > start_time_local
            """
        return query
    
    def create_historical_data_table(self):
         # Create a new table to store the extrapolated intervals
        create_query='''
            CREATE TABLE IF NOT EXISTS historical_data (
                store_id BIGINT,
                start_time DATETIME,
                end_time DATETIME,
                status VARCHAR(255)
            )
        '''
        return create_query