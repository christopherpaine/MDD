import os
import mysql.connector

# Load the database credentials from a configuration file or environment variables
if "CLEARDB_DATABASE_URL" in os.environ:
    # Production environment: use environment variables
    url = os.environ['CLEARDB_DATABASE_URL']
    parts = url.split(":")
    user = parts[1][2:]
    password = parts[2].split("@")[0]
    host = parts[2].split("@")[1]
    database = parts[3].split("/")[1]
else:
    # Local environment: use a configuration file
    import config
    user = config.user
    password = config.password
    host = config.host
    database = config.database

# Connect to the database
cnx = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor
cursor = cnx.cursor()

# Execute a query
query = "SELECT * FROM table"
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print the results
print(results)

# Close the connection
cnx.close()
