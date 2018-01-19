import time
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import mimetypes
import os, errno
import argparse

def createEmptyFolder(directory):
	try:
		if os.path.exists(directory):
			dirFiles = os.listdir(directory)
			if len(dirFiles) > 0:
				for file in dirFiles:
					os.remove(os.path.join(directory,file))
			os.rmdir(directory)
		os.makedirs(directory)
	except OSError as e:
		print('OSError ' + e.__traceback__.__str__())

def downloadImages(data, folderName):
	soup = BeautifulSoup(data, "lxml")
	i=1
	try:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		folder = os.path.join(dir_path, folderName)
		createEmptyFolder(folder)
	except OSError as e:
		print('OSError ' + e.__traceback__.__str__())
	for link in soup.find_all('img'):
		image = link.get("src")
		# question_mark = image.find("?")
		# image = image[:question_mark]
		# image_name = os.path.split(image)[1]
		# print(image_name)
		if 'http' not in image or 'https' not in image:
			image = 'http://' + folderName + '/' + image
		print('image url = ' + image)
		r2 = requests.get(image)
		content_type = r2.headers['content-type']
		extension = mimetypes.guess_extension(content_type)
		if (extension is None):
			extension = ''
		with open(folder + '/' + str(i) + extension, "wb") as f:
			f.write(r2.content)
			i = i + 1
	i = i - 1
	print('Downloaded ' + str(i) + ' files to ' + folder)

def startToScrape(url):
	i = 0
	folderName = url
	if '//' in url:
		folderName = url.split('//')[1].replace('/','')
	###browser = webdriver.PhantomJS("C:/Program Files/Python36/phantomjs-2.1.1-windows/bin/phantomjs.exe")
	browser = webdriver.Chrome('./chromedriver')
	browser.get(url)
	print(browser.title)
	browser.maximize_window()
	pause = 10

	lastHeight = browser.execute_script("return document.body.scrollHeight")
	print(lastHeight)
	browser.get_screenshot_as_file("test03_1_" + str(i) + ".png")
	while True:
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(pause)
		newHeight = browser.execute_script("return document.body.scrollHeight")
		print(newHeight)
		if newHeight == lastHeight:
			break
		lastHeight = newHeight
		i += 1
		data = browser.page_source
		downloadImages(data, folderName)
		browser.get_screenshot_as_file("test03_1_" + str(i) + ".png")

	browser.quit()

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input",
					help="path to the website to scrap images")
	args = vars(ap.parse_args())
	inputS = args['input']
	# inputS = "https://www.nytimes.com/"
	if inputS is not None:
		startToScrape(inputS)
