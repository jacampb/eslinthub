#Imports
import argparse
import time
import pycurl
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

#Parse aguments
parser = argparse.ArgumentParser(description='Scan GitHub for public repositories to analyze with ESLint.')

parser.add_argument('-L','--language', help='Specifies the language to scan for. Default is JavaScript. Supported languages: JavaScript', default='JavaScript')

args = parser.parse_args()


#Build url
pagenum = 1
URL = 'https://api.github.com/search/repositories?q=language:' + args.language + '&sort=stars&order=desc&page=' + str(pagenum)

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

print('pagenum: ' + str(maxpage))
#open connectio to MySQL db

#do while pagenum <= the max page number found above
while True:
	#parse the repo Names and URLs out of the response
	
	#Insert into ut_repos any that don't already exist

	#increment pagenum
	pagenum = pagenum + 1
	if int(pagenum) >int(maxpage):
		break
	#update URL with new pagenum
	URL = 'https://api.github.com/search/repositories?q=language:' + args.language + '&sort=stars&order=desc&page=' + str(pagenum)
	#get the next page 
	resp.clear_all()
	curl = pycurl.Curl()
	curl.setopt(curl.URL, URL)
	curl.setopt(curl.WRITEFUNCTION, resp.body_callback)
	time.sleep(6)
	curl.perform()
	curl.close()
	print(pagenum)
