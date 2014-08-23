from bs4 import BeautifulSoup
import requests
import sys
import re
import os
import time

# receive a subreddit
# receive a topic
# search posts in subreddit for topic
# return links to posts and users who's contribution was significant

def openPage(url):
	time.sleep(1)
	return BeautifulSoup(requests.get(url).text)

# get posts against term, return links to posts
def searchPosts(page, term):
	posts = []
	postList = page.find_all('div', class_="entry")

	for post in postList:
		text = post.find(class_="title").text
		if(wordExists(term, text) == True):
			rawLink = post.find('a', class_="title")['href']
			link = "http://reddit.com" + rawLink
			posts.append(link)
	return posts

# search comments of  a post, return post and user
def searchComments(page, term):
	acceptedComments = []
	commentsList = page.find_all('div', class_='entry')
	if(len(commentsList) == 0):
		die(page)
	commentsList.pop(0) # remove question from comments array
	
	for comment in commentsList:
		text = comment.find('div', class_="usertext-body").find('p').text
		if(wordExists(term, text)):
			acceptedComments.append(comment)

	return acceptedComments

# check if popularity if high enough
def isPopularEnough(comment):
	popularityLine = comment.find(class_="tagline").find_all(class_='score')[1].text
	match = re.match("^[0-9].+\s", popularityLine)
	if not match:
		return False
		
	popularity = match.group().strip()

	if(int(popularity) >= 5):
		return True

	return False

def wordExists(needle, haystack):
	haystack = haystack.lower()
	needle = needle.lower()

	for word in re.finditer(r"\w+", haystack):
		if(word.group() == needle):
			return True
	return False

# generate html page (index.html) for content
def generateHtmlPage(comments, title):
	template = open('template.html', 'r')
	newFile = open(title + ".html", "w+")

	for line in template:
		edit = ""
		if "{{title}}" in line:
			edit = re.sub("{{[\w]+}}", title, line)

		if "{{posts}}" in line:
			html = generateHtmlForComments(comments)
			edit = re.sub('{{[\w]+}}', html, line)

		newFile.write(edit) if len(edit) > 0 else newFile.write(line)

	template.close()
	newFile.close()

def generateHtmlForComments(comments):
	html = "<ul class='list-group'>"

	for comment in comments:
		text = comment.find(class_='usertext-body').text
		user = comment.find(class_="author").text
		popularity = comment.find_all(class_="score")[1]

		html += "<li class='list-group-item'><b>" + user + "</b>  <p>" + text + "</p></li>"
	html += "</ul>"
	return html

#search through pages and comments for the term
def generateUsersAndComments(page, term):
	savedPosts = []
	postsLinks = searchPosts(page, term)

	for post in postsLinks:
		postPage = openPage(post)
		comments = searchComments(postPage, term)

		for comment in comments:
			if(isPopularEnough(comment)):
				savedPosts.append(comment)
	return savedPosts

def main():
	if(len(sys.argv) < 3):
		print('Please provide a subreddit and topic to search for')
		sys.exit()

	subreddit   = sys.argv[1]
	term       = sys.argv[2]
	url      =  'http://www.reddit.com/r/'  + subreddit

	page = openPage(url)
	domain = page.find_all(class_="domain")[0].find('a').text[5:]

	if( domain != subreddit):
		die('Please provide an actual subreddit')

	posts = generateUsersAndComments(page, term)

	generateHtmlPage(posts, subreddit)

	os.system('open ' + subreddit + ".html")
	

# for debigging...like php's die(var_dump())
def die(exp):
	print(exp)
	sys.exit()

if __name__ == '__main__':
	main()