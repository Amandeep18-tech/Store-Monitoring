from utilities.sql_utilities import MySQLCRUDUtility
from utilities.dml_queries import DMLQueries
import constants

class UpdateMenuHoursTable:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.dml_queries=DMLQueries()
    def update_missing_fields(self):
        """Update missing store_ids and make them available 24*7
        """
        self.my_sql_obj.connect()
        # Find missing store_id values in store_timezone
        missing_store_ids = [row[0] for row in self.my_sql_obj.read(self.dml_queries.missing_store_ids_query_menu_hours())]
        # Insert missing values in menu_hours for 24/7 operation
        data_list=[]
        for store_id in missing_store_ids:
            for dayOfWeek in range(7):  # 0 to 6 representing days of the week
                data=(store_id, dayOfWeek)
                data_list.append(data)
        print(len(data_list))
        self.my_sql_obj.execute_insert_update_many(self.dml_queries.insert_query_full_availability_menu_hours(),data_list)
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()
    
        print("Missing values inserted into menu_hours for 24/7 operation.")


menu_hours = UpdateMenuHoursTable()
menu_hours.update_missing_fields()