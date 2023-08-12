import mysql.connector
from utilities.sql_access import get_connection

def create_index_on_store_timezone():
# Connect to the MySQL database

    connection=get_connection()
    cursor = connection.cursor()

    # SQL statement to create an index on the store_id column
    create_index_sql = "CREATE INDEX idx_store_id ON store_timezone (store_id)"

    # Execute the SQL statement
    cursor.execute(create_index_sql)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def create_index_on_menu_hours():
# Connect to the MySQL database

    connection=get_connection()
    cursor = connection.cursor()

    # SQL statement to create an index on the store_id column
    create_index_sql = "CREATE INDEX idx_store_id ON menu_hours (store_id)"

    # Execute the SQL statement
    cursor.execute(create_index_sql)

    # Commit the changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    
# create_index_on_store_timezone()
create_index_on_menu_hours()
