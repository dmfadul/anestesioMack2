import sqlite3

# Establish a connection to the database
conn = sqlite3.connect('path_to_your_database.db')
cursor = conn.cursor()

# Retrieve the values, sorting them by year
cursor.execute("SELECT year, month FROM your_table_name ORDER BY year ASC")
data = cursor.fetchall()

# Write these results to a text file
with open("output.txt", "w") as file:
    for entry in data:
        file.write(f"{entry[0]}, {entry[1]}\n")

# Close the connection
conn.close()

print("The task is complete, mon ami!")

# Latin insight:
# The verb "to write" in Latin is "scribere". In the present tense, first person singular, it is "scribo".
