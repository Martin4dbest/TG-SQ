import sqlite3

# Connect to the database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Delete all records from the users table
c.execute("DELETE FROM users")

# Optional: Reset auto-incrementing IDs
c.execute("DELETE FROM sqlite_sequence WHERE name='users'")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database cleared successfully!")
