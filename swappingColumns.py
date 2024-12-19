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

        # Step 1: Add a temporary column to hold the original 'create_date'
        add_temp_column_query = "alter table equipo_patient360.patient_vital add column tempColumn datetime default NULL after modifiedOn;"
        cursor.execute(add_temp_column_query)
        print("Temporary column 'temp_date' added")

        # Step 2: Copy the value of 'create_date' into 'temp_date'
        copy_create_to_temp_query = "UPDATE patient_vital SET tempColumn = createDate WHERE source ='patient';"
        cursor.execute(copy_create_to_temp_query)
        print("Copied 'create_date' to 'temp_date'")

        # Step 3: Copy the value of 'update_date' into 'create_date'
        copy_update_to_create_query = "UPDATE patient_vital SET create_date = update_date"
        cursor.execute(copy_update_to_create_query)
        print("Copied 'update_date' to 'create_date'")

        # Step 4: Copy the value of 'temp_date' (original 'create_date') into 'update_date'
        copy_temp_to_update_query = "UPDATE patient_vital SET update_date = temp_date"
        cursor.execute(copy_temp_to_update_query)
        print("Copied 'temp_date' (original 'create_date') to 'update_date'")

        # Step 5: Drop the temporary column
        drop_temp_column_query = "ALTER TABLE patient_vital DROP COLUMN temp_date"
        cursor.execute(drop_temp_column_query)
        print("Temporary column 'temp_date' dropped")

        # Commit the changes
        connection.commit()
        print("Transaction committed successfully!")

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
