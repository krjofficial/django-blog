import mysql.connector

dataBase = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
)

# superuser username = crm_architect 
# superuser password = 123

# prepare a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute("CREATE DATABASE blogdb2")

print("Database created")


