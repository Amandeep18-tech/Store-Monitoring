import os
import mysql.connector

def get_connection():

    # Retrieve environment variables
    host = "127.0.0.1"
    user = "root"
    password =os.environ.get("MYSQL_PASSWORD")  # Re trieve password from environment variable
    database = "StoreMonitoring"

    # Establish a connection
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return connection