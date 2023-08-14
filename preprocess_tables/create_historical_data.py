from utilities.sql_utilities import MySQLCRUDUtility
from utilities.dml_queries import DMLQueries
from utilities.ddl_queries import DDLQueries
import constants

class HistoricalData:
    def __init__(self):
        self.my_sql_obj=MySQLCRUDUtility(constants.db_config)
        self.dml_queries=DMLQueries()
        self.ddl_queries=DDLQueries()
    def create_and_populate_historical_data(self):
        """Create and populate historical data set
        """
        self.my_sql_obj.connect()
        self.my_sql_obj.execute_query(self.ddl_queries.create_historical_data_table())
        self.my_sql_obj.commit()
        # Query the original data from your existing table (replace 'your_table' with your actual table name)
       
        rows=self.my_sql_obj.read(self.dml_queries.select_store_status_within_hours_sorted())
        
        current_store=None
        current_status=None
        curr_day=None
        interval_start=None
        interval_end=None
        
        store_id,local_time,status,start,end,day=rows[0]
        
        current_store=store_id
        current_status=status
        curr_day=day
        interval_start=start
        interval_end=local_time
        
        data_list=[]
        data_list.append((current_store, interval_start, interval_end, current_status))
        
        for i in range(1,len(rows)):
            store_id,local_time,status,start,end,day=rows[i]
       
            if current_store!=store_id or day!=curr_day:
                
                last_element=rows[i-1]
                last_end_time=last_element[-2]
                interval_start=interval_end
                interval_end=last_end_time
                data=(current_store, interval_start, interval_end, current_status)
                data_list.append(data)
                
                current_store=store_id
                current_status=status
                curr_day=day
                interval_start=start
                interval_end=local_time
                data=(current_store, interval_start, interval_end, current_status)
                
            else:
                interval_start=interval_end
                interval_end=local_time
                current_status=status
                curr_day=day
                data=(current_store, interval_start, interval_end, current_status)
                
            data_list.append(data)
       
        self.my_sql_obj.execute_insert_update_many(self.dml_queries.insert_data_in_historical_table(),data_list)
        self.my_sql_obj.commit()
        self.my_sql_obj.disconnect()


HistoricalData().create_and_populate_historical_data()