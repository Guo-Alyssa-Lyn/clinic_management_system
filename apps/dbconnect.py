import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Establishes and returns a connection to the MySQL database.

    Returns:
        connection: MySQL database connection object
        or
        None: if the connection fails
    """ 
    try:
        connection = mysql.connector.connect(
            host='localhost',        # e.g., 'localhost' or your server's IP
            user='root',    # Your MySQL username
            password='',# Your MySQL password
            database='tumbocon' # Your database name
        )
        if connection.is_connected():
            print("Connection to MySQL database successful!")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """
    Closes the MySQL database connection.

    Args:
        connection: MySQL database connection object
    """
    if connection and connection.is_connected():
        connection.close()
        print("Connection to MySQL database closed.")
