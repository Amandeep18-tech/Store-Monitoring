from utilities.sql_utilities import MySQLCRUDUtility
from utilities.ddl_queries import DDLQueries
import constants

class CreateIndex:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.ddl_queries=DDLQueries()
    def create_index_on_store_timezone(self):
        """Create index on store timezone table
        """

        self.my_sql_obj.connect()

        # SQL statement to create an index on the store_id column
        # Execute the SQL statement
        self.my_sql_obj.execute_query(self.ddl_queries.create_index_on_store_timezone())

        # Commit the changes and close the connection
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
        
    def create_index_on_menu_hours(self):
        """Create index on menu hours table
        """

        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.create_index_on_menu_hours())

        # Commit the changes and close the connection
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()

create_index=CreateIndex()
# create_index.create_index_on_menu_hours()
create_index.create_index_on_store_timezone()