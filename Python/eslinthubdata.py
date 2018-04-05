import mysql.connector
import argparse
import sys
#import ESLint

#Parse aguments
parser = argparse.ArgumentParser(description='Queries database for unprocessed repositories, then one at a time will pull then down and lint them with ESLint. Results stored in db.')

parser.add_argument('-u','--user', help='username for the mysql database login',required=True)
parser.add_argument('-p', '--password', help='password for the mysql database login', required=True)
parser.add_argument('-s', '--server', help='the server that contains the database(defaults to localhost)',dest='server', default='localhost')
parser.add_argument('-db' '--databasename', help='database name to connect to(defaults to eslinthub)', dest='dbname', default='eslinthub') 
args = parser.parse_args()

config={
	'user':str(args.user),
	'password':str(args.password),
	'host':str(args.server),
	'db':str(args.dbname),
	}
#creates the connection, username and password right now are just placeholders
connection = mysql.connector.connect (**config)

#adds cursor object
cursor = connection.cursor()

#exectues the SQL query on ut_repos
cursor.execute ("SELECT * FROM ut_repos WHERE coalesce(ESLint, '') <> 'Y'")

#fetch all rows from teh query
data = cursor.fetchall()

#print the rows
#close the connection
connection.close()
for row in data:
    #row[0]=repo_id
    #row[1]=repo_name
    #row[2]=html_url
    #row[3]=ESLint
    #row[4]=insert_dttm
    #row[5]=last_modified
    print row[0], row[1], row[2], row[3], row[4], row[5]

    #clone row[2] to working directory

    #create list of all .js files

    #for file in files:
        #ESlint -o lintresults.out filename.js
        
        #Wait for process to complete, then parse lintresults.out

        #store results in ut_eslint_issues one record per issue.

    #clear out working directory and process next row/repo




#close the cursor
cursor.close()
#close the program
sys.exit()
