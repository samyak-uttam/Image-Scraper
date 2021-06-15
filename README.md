# Image Scrapper

**Image scraping** is a subset of the **web scraping** (to extract content and data from a website) used mostly but not only, for generating a dataset to train your model on, in Machine Learning and Deep Learning.

In this repository, I've used Beautiful Soup, one of the most used python's library for Image Scraping, to implement an image scraper which can be used to download images from both Google and Bing Images.

## Steps for running the file

1. First of all, download or clone the repo to use it locally, type the following command in cmd
	```
	git clone git@github.com:samyak-uttam/Image-Scraper.git
	```
2. Install Beautiful Soup
	```
	pip install beautifulsoup4
	```
3. Install requests (used to handle HTTP requests)
	```
	pip install requests
	```
4. After the above steps you're all set to run the file, type
	```
	python scrapper.py
	```

## Output
All the downloaded images will be present in the images folder.