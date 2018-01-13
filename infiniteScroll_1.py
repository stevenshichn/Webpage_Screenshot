import selenium
import time
from selenium import webdriver

browser = webdriver.PhantomJS("phantomjs")

browser.get("http://www.straitstimes.com/")
print (browser.title)
browser.maximize_window()
pause = 3

lastHeight = browser.execute_script("return document.body.scrollHeight")
print(lastHeight)
i = 0
browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")
while True:
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(pause)
	newHeight = browser.execute_script("return document.body.scrollHeight")
	print(newHeight)
	if newHeight == lastHeight:
		break
	lastHeight = newHeight
	i += 1
	browser.get_screenshot_as_file("test03_1_"+str(i)+".jpg")

browser.quit()