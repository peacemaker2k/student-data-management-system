import sqlite3

# Connect to the database
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Run the ALTER TABLE query to add a password column
cursor.execute('UPDATE students SET password = "temp";')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Query Executed successfully!")