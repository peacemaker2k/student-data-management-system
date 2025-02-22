import sqlite3

# Connect to the database
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Run the ALTER TABLE query to add a password column
cursor.execute('ALTER TABLE students_new RENAME TO students;')

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Query Executed successfully!")