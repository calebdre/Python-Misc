from bs4 import BeautifulSoup
import urllib2

def main():
	url = ''
	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)


main()