# eslinthub

Purpose:

Scan GitHub for public repositories containing JavaScript, pull them down and run them through ESLint. Store results in MySQL database. 

The resulting list of issues will provide a good view of which projects I can contribute to by resolving these issues.

Potentially helping the GitHub community maintain strong(er) coding practices and quality products.


Stack:
Scripting: Python 2.7 (https://www.python.org)
Database: MySQL (https://www.mysql.com)
Linting: ESLint (https://eslint.org)



Setup:

sudo apt-get install nodejs
sudo apt-get install npm

npm install eslint --save-dev
sudo ln -s /usr/bin/nodejs /usr/bin/node

./node_modules/.bin/eslint --init

sudo apt-get install mysql-server
mysql_secure_installation

sudo systemctl start mysql.service

run the build script found in the SQL directory.
