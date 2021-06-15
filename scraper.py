# import all the required libraries
import os
import json
import requests
from bs4 import BeautifulSoup

# folder to save the images
SAVE_FOLDER = 'images'

# base url for google image search
GOOGLE_IMAGE_URL = 'https://www.google.com/search?tbm=isch&q='

# base url for bing image search
BING_IMAGE_URL = 'http://www.bing.com/images/search?q='

# request headers
# a lot of websites have precautions to fend off scrapers from accessing their data, we can spoof 
# the headers we send along with our request to make our scraper look like a legitimate browser
# by telling the website what operating system we have, what web browser we have etc.
HEADERS = {
	'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


# create SAVE_FOLDER if it does not exist already
def checkAndCreateDir():
	if not os.path.isdir(SAVE_FOLDER):
		os.makedirs(SAVE_FOLDER)


# function to get image links from google images
def getGoogleImageLinks(query, num_images = 20):
	print('Start searching...')

	# generate the final url based on user query
	url = GOOGLE_IMAGE_URL + query	

	# get the webpage
	html_text = requests.get(url, headers = HEADERS).text
	
	# parse the html_text into a BeautifulSoup object, which allows easy manipulation 
	soup = BeautifulSoup(html_text, 'html.parser')

	# get all the <img> tags with class = 'rg_i Q4LuWd'
	results = soup.find_all('img', class_ = 'rg_i Q4LuWd', limit = num_images + 20)

	# list to store the links
	imagelinks = []

	# get the image link for each of the results
	for i, image in enumerate(results):
		if image.has_attr('data-src'):
			imagelinks.append(image['data-src'].encode('utf-8'))

	print(f'Found {len(imagelinks)} images.')
	return imagelinks


# function to get image links from bing images
def getBingImageLinks(query, num_images = 20):
	print('Start searching...')

	# list to store the links
	imagelinks = []

	# keep a count variable with increment of 35, because it can fetch only 35 links at a time
	for count in range(0, num_images, 35):

		# generate the final url based on user query and the current count
		url = BING_IMAGE_URL + '{}&first={}&form=HDRSC2'.format(query, count)

		# get the webpage
		html_text = requests.get(url, headers = HEADERS).text

		# parse the html_text into a BeautifulSoup object, which allows easy manipulation 
		soup = BeautifulSoup(html_text, 'html.parser')

		# get all the <a> tags with class = 'iusc'
		results = soup.find_all('a', class_ = 'iusc', limit = min(num_images - count, 35))

		# get the image link for each of the results
		for i, image in enumerate(results):
			imagelinks.append(json.loads(image['m'])['turl'])
		
	print(f'Found {len(imagelinks)} images.')
	return imagelinks


# function to save the images locally from the image links
def saveImages(imagelinks, query):
	print('Start downloading...')
	checkAndCreateDir()
	for i, link in enumerate(imagelinks):

		# get the webpage from the current link
		response = requests.get(link)

		# name of the current image
		imagename = SAVE_FOLDER + '/' + query + str(i + 1) + '.jpg'
		
		# store the image in the folder
		with open(imagename, 'wb') as file:
			file.write(response.content)

	print('Done!')


# integrate all the steps in one function
def searchAndDownload():
	query = str(input('Enter the search term: '))
	num_images = int(input('Enter the number of images: '))
	search_engine = int(input('Enter 1 for searching on google and 2 for bing: '))

	if search_engine == 1:
		imagelinks = getGoogleImageLinks(query, num_images)
	else:
		imagelinks = getBingImageLinks(query, num_images)
	
	saveImages(imagelinks, query)


if __name__ == '__main__':
	searchAndDownload()