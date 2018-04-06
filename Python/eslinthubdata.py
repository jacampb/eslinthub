import mysql.connector
import argparse
import sys
import os
import json
import string
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
    os.system('git clone %s' % str(row[2]))
    
    #create list of all .js files
    os.system('find . -name "*.js" > js.files')
    with open('js.files') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    #for file in files:
    for file in content:
        filesplit = file.split("/")
        filename = filesplit[-1]
        print(filename)
        #ESlint -o lintresults.out filename.js
        os.system('~/node_modules/.bin/eslint -c ~/.eslintrc.js --no-eslintrc -o lint.out %s' % str(file))
        #Wait for process to complete, then parse lintresults.out
        f=open('lint.out')
        lint_line = f.readline() # this discards the header row, find a better way
        lint_line = f.readline()
        lint_line = f.readline()
        conn=mysql.connector.connect(**config)
        inCur=conn.cursor()
        while lint_line:
            #insert file name and error line into ut_eslint_issues
            printable=set(string.printable)
            lint_line= filter(lambda x: x in printable,str(lint_line)) #Remove non printable characters
            lint_line= lint_line.replace('[22m',' ')
            lint_line= lint_line.replace('[2m',' ')
            lint_line= lint_line.replace('[39m', ' ')
            lint_line= lint_line.replace('[31m', ' ')
            lint_line= ' '.join(lint_line.split()) #replace multiple whitespace with a single space for cleaner formatting
            inCur.execute('INSERT INTO ut_eslint_issues (repo_id,issue_description,file_name) VALUES ("%s","%s","%s")' % (row[0],lint_line,filename))
            lint_line=f.readline()
        conn.commit()
        inCur.close()
        conn.close()

    #clear out working directory and process next row/repo
    os.system('rm -rf %s' % row[1])
    #update the ESLint field for the repo
    conn=mysql.connector.connect(**config)
    upCur=conn.cursor()
    upCur.execute('UPDATE ut_repos SET ESLint="Y" WHERE repo_id = %s' % row[0])
    upCur.close()
    conn.close()



#close the cursor
cursor.close()
#close the program
sys.exit()
