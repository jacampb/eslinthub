#Imports
import argparse
import time
import datetime
import pycurl
import mysql.connector
import json
from StringIO import StringIO


class Response:
	def __init__(self):
		self.header = ''
		self.body = ''

	def body_callback(self, buffer):
		self.body = self.body + buffer

	def header_callback(self, buffer):
		self.header = self.header + buffer

	def clear_all(self):
		self.header = ''
		self.body = ''

def callAPI(language, config):
	#Build url
	pagenum = 1
	URL = 'https://api.github.com/search/repositories?q=language:' + language + '&sort=stars&order=desc&page=' + str(pagenum)

	resp = Response()

	curl = pycurl.Curl()
	curl.setopt(curl.URL, URL)
	curl.setopt(curl.HEADERFUNCTION, resp.header_callback)
	curl.setopt(curl.WRITEFUNCTION, resp.body_callback)
	curl.perform()
	curl.close()


	#search resp.header to pull out the max page number for results. This is in the Link: header.
	headerlist = resp.header.split('page=')
	maxpage = headerlist[2].split('>')[0]

	#open connection to MySQL db
	conn=mysql.connector.connect(**config)
	cursor=conn.cursor()

	#do while pagenum <= the max page number found above
	while True:
		#parse the repo Names and URLs out of the response
		jsonresp = json.loads(resp.body)
		for item in jsonresp['items']:
			reponame=item['html_url'].split('/')
			reponame=reponame[-1]
			htmlurl=item['html_url']+'.git'
			#Insert into ut_repos any that don't already exist
			sql='INSERT INTO ' + args.dbname + '.ut_repos (repo_name, html_url, language, insert_dttm, last_modified) VALUES ("%s","%s","%s","%s","s")' % (reponame,htmlurl,language,datetime.datetime.now(),datetime.datetime.now())
			try:
				cursor.execute(sql)
			except mysql.connector.IntegrityError as err:
				print('Duplicate Repository Not Being Added: ' + reponame)
		#increment pagenum
		pagenum = pagenum + 1
		if int(pagenum) >int(maxpage):
			break
		#update URL with new pagenum
		URL = 'https://api.github.com/search/repositories?q=language:' + language + '&sort=stars&order=desc&page=' + str(pagenum)
		#get the next page 
		resp.clear_all()
		curl = pycurl.Curl()
		curl.setopt(curl.URL, URL)
		curl.setopt(curl.WRITEFUNCTION, resp.body_callback)
		time.sleep(6)
		curl.perform()
		curl.close()

	conn.commit()
	cursor.close()
	conn.close()

def main():
	#Parse aguments
	parser = argparse.ArgumentParser(description='Scan GitHub for public repositories to analyze with ESLint.')

	parser.add_argument('-L','--language', help='Specifies the language to scan for. Default is JavaScript. Supported languages: JavaScript', default='JavaScript')
	parser.add_argument('-u','--user', help='username for the mysql database login',required=True)
	parser.add_argument('-p', '--password', help='password for the mysql database login', required=True)
	parser.add_argument('-s', '--server', help='the server that contains the database(defaults to localhost)',dest='server', default='localhost')
	parser.add_argument('-db' '--databasename', help='database name to connect to(defaults to eslinthub)', dest='dbname', default='eslinthub') 
	args = parser.parse_args()
	
	language=args.language
	#db connection config
	config = {
		'user':str(args.user),
		'password':str(args.password),
		'host':str(args.server),
		'database':str(args.dbname),
		}
	
	callAPI(language, config)


main()