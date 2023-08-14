import mysql.connector
import traceback

class MySQLCRUDUtility:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))
    def disconnect(self):
        try:
            if self.connection and self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))

    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))
            
    def execute_query(self, query, data=None):
        try:
            self.connect()
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))
        

    def fetch_query(self, query, data=None):
        try:
            self.connect()
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))
        
        return result

    def create_table(self, query):
        try:
            self.connect()
            self.execute_query(query)
            
        except Exception as e:
            print("Error: {0}\nException: {1}".format(e, traceback.format_exc()))

    def read(self, query, data=None):
        return self.fetch_query(query, data)

    def update(self, query, data):
        self.execute_query(query, data)

    def delete(self, query, data):
        self.execute_query(query, data)
        
    def execute_insert_update_many(self, query, data):
        self.connect()
        self.cursor.executemany(query,data)