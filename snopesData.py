from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import csv
import array

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.set_window_size(1920,1080)

articleList = []
fullList = []

pagenum = 0
while pagenum <= 99:
    currentPage = "https://www.snopes.com/?s=COVID&hPP=10&idx=wp_live_searchable_posts&page=" + str(pagenum) + "&is_v=1"

    driver.get(currentPage)

    #driver.close() - Closes the tab
    #driver.quit() - Closes the window

    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result-list"))
        )
    except:
        print("Search Results did NOT load...")
        driver.quit()

    #print(results.text)
    #print(driver.title)

    articles = results.find_elements_by_class_name("ais-hits--item")
    
    for atricle in articles:
        articleTitle = atricle.find_element_by_class_name("heading")

        articleList.append(articleTitle.text)

    pagenum = pagenum + 1

print(articleList)

i = 0
while i <= len(articleList):
    try:
        driver.get("https://www.snopes.com/")
        time.sleep(5)
        search = driver.find_element_by_id("site-search")
        search.send_keys(articleList[i])
        search.send_keys(Keys.RETURN)
        time.sleep(5)

        searchResult = driver.find_element_by_class_name("ais-hits--item")
        searchResult.click()
        print("TEST")
        time.sleep(5)
        

        print(driver.title)

        articleRating = driver.find_element_by_xpath('//div[@class="media-body d-flex flex-column align-self-center"]')
        print(articleRating.find_element_by_xpath('.//span').text)
        print(" ")

        #push the title and rating into a List of Lists
        fullList.append([driver.title, articleRating.find_element_by_xpath('.//span').text])

        i = i + 1
        
    except ElementClickInterceptedException:
        if i != 0:
            i = i - 1
    except:
        print("No rating found")
        i = i + 1

print(fullList)

with open('file.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(fullList)