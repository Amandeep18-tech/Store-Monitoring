from utilities.sql_utilities import MySQLCRUDUtility
from sql_queries.dml_queries import DMLQueries
from sql_queries.ddl_queries import DDLQueries
import constants
import pytz
from datetime import datetime

class ModifyTimezoneTable:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.dml_queries=DMLQueries()
        self.ddl_queries=DDLQueries()
        
    def update_missing_timezones(self):
        """ update missing timezone with America/Chicago
        """
        self.my_sql_obj.connect()
        # Find missing store_id values in store_timezone
        missing_store_ids = [row[0] for row in self.my_sql_obj.read(self.dml_queries.missing_store_id_timezone())]
        data_list=[]
        for store_id in missing_store_ids:
            data=(store_id,)
            data_list.append(data)
        
        self.my_sql_obj.execute_insert_update_many(self.dml_queries.insert_query_update_missing_timezone(),data_list)
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()

    def add_column_offset(self):
        """add timezone offset column
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.alter_table_add_timezone_offset_column())
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
        
    def update_timezone_to_offset(self):
        """update timezone offset column with values
        """
        self.my_sql_obj.connect()
        # Fetch data from Table-3
        rows = self.my_sql_obj.read(self.dml_queries.select_query_store_timezone())
        # Step 2: Convert timezone_str to UTC offset and update the new column
        data_list=[]
        for row in rows:
            store_id = row[0]
            timezone_str = row[1]
            timezone_value= str(datetime.now(pytz.timezone(timezone_str)))
            len_time=len(timezone_value)
            timezone_offset=timezone_value[len_time-6:len_time]
            data=(timezone_offset, store_id)
            data_list.append(data)
            # Execute the SQL statement to update the utc_offset
        self.my_sql_obj.execute_insert_update_many(self.dml_queries.update_query_store_timezone(),data_list)
        # Commit the changes and close the connection
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()

update_timzone=ModifyTimezoneTable()
update_timzone.update_missing_timezones()
update_timzone.add_column_offset()
update_timzone.update_timezone_to_offset()