from utilities.sql_utilities import MySQLCRUDUtility
from sql_queries.dml_queries import DMLQueries
from sql_queries.ddl_queries import DDLQueries
import constants

class ModifyStoreStatusTable:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.dml_queries=DMLQueries()
        self.ddl_queries=DDLQueries()
        
    def add_local_time_column(self):
        """Add local time column to store status table
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.alter_table_add_local_time_column())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
        
    def update_menu_hours_to_local_time(self):
        """update utc time to local time
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.dml_queries.update_menu_hours_to_local_timezone())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
    def add_custom_day_column(self):
        """add custom day number to store status
        """
        
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.add_custom_day_column())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
        
    def update_custom_day_number(self):
        """update custom day number
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.dml_queries.update_custom_day())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        # Update the custom_day_number using the provided formula
        
        
    def add_start_end_local_time_columns(self):
        """add column start time and end time to store status
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.add_start_end_time_column())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
    def update_start_end_columns(self):
        """update start time and end time columns in store status"""
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.dml_queries.update_store_status_start_end_time())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()



modify_store_status=ModifyStoreStatusTable()
# modify_store_status.add_local_time_column()
# modify_store_status.add_custom_day_column()
modify_store_status.add_start_end_local_time_columns()

# modify_store_status.update_menu_hours_to_local_time()
# modify_store_status.update_custom_day_number()
modify_store_status.update_start_end_columns()