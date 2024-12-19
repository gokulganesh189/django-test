import mysql.connector
from mysql.connector import Error

# Database connection details
host = "localhost"
database = "equipo_patient360"
user = "root"
password = "Shift$09"

try:
    # Establish the connection
    connection = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    if connection.is_connected():
        print("Connected to the database")

        # Create a cursor object
        cursor = connection.cursor()

        # Define the SQL query
        query = """
        UPDATE patient_vital 
        SET tempColumn = createDate 
        WHERE id IS NOT NULL
        """

        # Execute the query
        cursor.execute(query)

        # Commit the changes
        connection.commit()
        print("Query executed successfully!")

except Error as e:
    print(f"Error: {e}")
    if connection.is_connected():
        connection.rollback()  # Rollback if any error occurs
        print("Rolled back the transaction")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
