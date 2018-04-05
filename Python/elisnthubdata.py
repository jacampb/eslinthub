import MySQLdb
import sys
import ESLint

#creates the connection, username and password right now are just placeholders
connection = mySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "password", db = "eslinthub")
#adds cursor object
cursor = connection.cursor ()

#exectues the SQL query on ut_repos
cursor.execute ("select * from ut_repos")
#fetch all rows from teh query
data = cursor.fetchall ()
#print the rows
#close the connection
connection.close()
for row in data :
    print row[0], row[1], row[2], row[3], row[4], row[5]
#close the cursor
cursor.close()
#close the program
sys.exit()
