import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By

browser = webdriver.PhantomJS("phantomjs")
# browser.get("https://twitter.com/StackStatus")
browser.get("http://www.straitstimes.com/")  # shorter, so that ending can be tested
browser.maximize_window()
print(browser.title)
i = 0
browser.get_screenshot_as_file("test03_2_" + str(i) + ".jpg")
while True:
    print
    "i", i
    elemsCount = browser.execute_script("return document.querySelectorAll('.stream-items > li.stream-item').length")
    # print "c", elemsCount

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # element = WebDriverWait(browser, 20).until(
    #	EC.presence_of_element_located((By.XPATH,
    #		"//*[contains(@class,'GridTimeline-items')]/li[contains(@class,'stream-item')]["+str(elemsCount+1)+"]")))
    try:
        WebDriverWait(browser, 20).until(
            lambda x: x.find_element_by_xpath(
                "//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')][" + str(elemsCount + 1) + "]"))
    except:
        break

    i += 1
    browser.get_screenshot_as_file("test03_2_" + str(i) + ".jpg")

browser.quit()