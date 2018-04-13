import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import mimetypes
import os, errno
import argparse
from selenium.webdriver.support.wait import WebDriverWait
from pip.index import Link
import threading
from PIL import Image
import logging
from future.backports.http.server import args
# from pstats import browser

def slice_image(dest_folder, image_file, height, width, step):
	createEmptyFolder(dest_folder)
	im = Image.open(image_file)
	imgwidth, imgheight = im.size;
	count = 0;
	if height > imgheight or width > imgwidth:
		try:
			im.save(os.path.join(dest_folder, "sliced.png"))
		except Exception as e:
			logging.exception(e.__str__())
		finally:
			return
	x_stop = imgwidth - width
	print('slicing')
	y_stop = imgheight - height
	for i in range(0, x_stop, step):		
		for j in range(0, y_stop, step):
			box = (i, j, width+i, height+j)
			a = im.crop(box)
			count =count + 1			
			try:
				a.save(os.path.join(dest_folder, "sliced-IMG-%s.png" % count))
			except:
				pass

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
		logging.exception('OSError ' + e.__str__())

def downloadImages(data, folderName):
	soup = BeautifulSoup(data, "html.parser")
	index=1
	try:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		folder = os.path.join(dir_path, folderName)
		createEmptyFolder(folder)
	except OSError as e:
		logging.exception('OSError ' + e.__traceback__.__str__())
	link_array = soup.find_all('img');
	count = len(link_array)
	first_links = []
	second_links = []
	thrid_links = []
	forth_links = []
	if count >= 4:
		quater_num = int(round(count/4))
		first_links = link_array[:quater_num]
		second_links = link_array[quater_num : 2*quater_num]
		thrid_links = link_array[2*quater_num : 3 * quater_num]
		forth_links = link_array[3 * quater_num :]
		t1 = threading.Thread(target=saveImages, args=(folderName, folder, first_links, 1))
		t2 = threading.Thread(target=saveImages, args=(folderName, folder, second_links, quater_num + 1))
		t3 = threading.Thread(target=saveImages, args=(folderName, folder, thrid_links, 2 * quater_num + 1))
		t4 = threading.Thread(target=saveImages, args =(folderName, folder, forth_links, 3 * quater_num + 1))
		
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		
		t1.join()
		t2.join()
		t3.join()
		t4.join()	
	else:
		saveImages(link_array, index)

def saveImages(url_folderName, folder, links, index):
	try:
		for link in links:
			image = link.get("src")
			if 'http' not in image or 'https' not in image:
					image = 'http://' + url_folderName + '/' + image
			print('image url = ' + image)
			r2 = requests.get(image)
			content_type = r2.headers['content-type']
			extension = mimetypes.guess_extension(content_type)
			if (extension is None):
				extension = ''
			with open(folder + '/' + str(index) + extension, "wb") as f:
				f.write(r2.content)
				index = index + 1
	except Exception as e:
		logging.exception(e.__str__())
		pass
			
def startToScrape(url):
	i = 0
	folderName = url
	if '//' in url:
		folderName = url.split('//')[1].replace('/','')
	###browser = webdriver.PhantomJS("C:/Program Files/Python36/phantomjs-2.1.1-windows/bin/phantomjs.exe")
# 	browser = webdriver.Chrome('./chromedriver.exe')
	browser = webdriver.PhantomJS("./phantomjs.exe")
	browser.get(url)
	print(browser.title)
	browser.maximize_window()
	pause = 10

	lastHeight = browser.execute_script("return document.body.scrollHeight")
	print(lastHeight)
# 	browser.get_screenshot_as_file("test03_1_" + str(i) + ".png")
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	newHeight = browser.execute_script("return document.body.scrollHeight")
	try:
		WebDriverWait(browser, 30).until(lambda x: x.find_element_by_xpath("//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')][" + str(elemsCount + 1) + "]"))
	except:
	    pass
	finally:
		lastHeight = newHeight
		data = browser.page_source
		screenshot_name = folderName.replace('.', '_') + ".png"
		downloadImages(data, folderName)
		browser.get_screenshot_as_file(screenshot_name)
		browser.quit()
		# slice image, be cautious that it requires bug space
		#slice_image(os.path.join(folderName, "slices"), screenshot_name, 300,300,10)


if __name__ == "__main__":
	start_time = time.time()
	logging.basicConfig(filename='log')
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input",
					help="path to the website to scrap images")
	args = vars(ap.parse_args())
	inputS = args['input']
# 	inputS = "https://www.straitstimes.com/"
	if inputS is not None:
		startToScrape(inputS)
		print("--- %s seconds ---" % (time.time() - start_time))
	else:
		print("Please input url")