import sqlite3
import sys

try:
    # Establish connections to both databases
    conn_artemis = sqlite3.connect('Artemis.db')
    conn_running_analysis = sqlite3.connect('RunningAnalysis.db')

    # Create cursors
    cursor_artemis = conn_artemis.cursor()
    cursor_running_analysis = conn_running_analysis.cursor()

    # Select the specific columns from Artemis database
    cursor_artemis.execute('''
        SELECT runingdatacolumn1, runningdataacolumn2 
        FROM some_table  # Replace with actual table name
    ''')

    # Fetch all the rows
    rows = cursor_artemis.fetchall()

    # Insert the data into running_session table in RunningAnalysis database
    cursor_running_analysis.executemany('''
        INSERT INTO running_session (column1, column2) 
        VALUES (?, ?)
    ''', rows)

    # Commit the changes
    conn_running_analysis.commit()

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
    # Rollback any changes if an error occurs
    conn_running_analysis.rollback()

finally:
    # Always close the connections
    if conn_artemis:
        conn_artemis.close()
    if conn_running_analysis:
        conn_running_analysis.close()

print("Data transfer completed successfully!")