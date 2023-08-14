from utilities.sql_utilities import MySQLCRUDUtility
from sql_queries.ddl_queries import DDLQueries
import constants

class CreateTableStoreStatusWithinHours:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.ddl_queries=DDLQueries()
    def make_table_store_status_within_hours_table(self):
        """Function to make and store table within business hours
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.create_table_store_status_within_hours())
        # Build and execute the CREATE TABLE query
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()

        

CreateTableStoreStatusWithinHours().make_table_store_status_within_hours_table()