# eslinthub

### Purpose:

We are designing a tool around the existing ESLint project that will scan GitHub for public JavaScript repositories, pull them down, lint them, and store the results of the linting in the database. The results will be periodically pulled out in reports so we can determine what files have which issues so we can contribute to these projects by resolving them. Being able to query all files that contain the same type of issue may allow remidiating in batches leading to faster resolutions across the board. This is primarily a pet project as it seems like a fun way to jump start my open source contirbutions.

### Design:

This will lay out my current plan or ideas. This is open to change as the development moves forward and we run into obstacles or learn better ways to accomplish the goal. Version 1 will only support searching for JavaScript but my intent is to add support for other languages and linters once v1 is working.

There will be 3 main python scripts.

##### eslinthub.py:
Required Parameters: -u <database username>, -p <database password> (EX:python eslinthub.py -u root -p root1234)

-Take in parameters to control the language we search for (-L) and database connectivity info like user (-u), password (-p), server name (-s), and database name (-db).
-Query the REST API and parse the response to gather all repository names and urls that meet our search criteria.
-Store the resulting list of repositories in a MySQL table where we can quickly grab the url to git clone while enforcing uniqueness.

##### eslinthubdata.py:
Required Parameters: -u <database username>, -p <database password> (EX:python eslinthubdata.py -u root -p root1234)
  
-Query the database for a list of all repositories that have not been linted yet. 
-Iterate through the list and process each repository one at a time.
-git clone the repository into a working directory.
-Enumerate all .js files.
-For each .js file, call ESLint on it and store any reported issues in the table.
-When all files have been processed, delete everything from the working directory, and update the ut_repos table to have the ESLint field indicate Y for processed.
-Repeat these steps for every unprocessed repository.

##### Script3:
-Possibly unnecessary but I was thinking of some kind of report generator.
-Query the database and output .csv report showing distinct issues and number of files found with that issue.
-Query the database and output .csv report showing all files and issues grouped by issue and sorted by count of each issue descending.
-Query the database and output .csv report showing distinct repositories and number of issues.




### Stack:
1. OS: Ubuntu 16.04 LTS
2. Scripting: Python 2.7 (https://www.python.org)
3. Database: MySQL (https://www.mysql.com)
4. Linting: ESLint (https://eslint.org)



### Setup:
1. sudo apt-get install nodejs
2. sudo apt-get install npm
3. npm init
4. npm install eslint --save-dev
5. sudo ln -s /usr/bin/nodejs /usr/bin/node
6. ./node_modules/.bin/eslint --init
7. sudo apt-get install mysql-server
8. mysql_secure_installation
9. sudo systemctl start mysql.service
10. pip install pycurl
11. pip install mysql-connector
