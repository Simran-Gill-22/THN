import time
from bs4 import BeautifulSoup
from selenium import webdriver

#this function gets scrapes the rsi site
def Scraper():
        #url to scrape
        url = 'https://robertsspaceindustries.com/funding-goals'
        #options for the selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        #driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        #set those options
        driver = webdriver.Chrome(chrome_options=options)
        #call the url
        driver.get(url)
        #wait for the complete page to load
        time.sleep(10)
        #save the source of the page
        html = driver.page_source
        #parse this source
        soup = BeautifulSoup(html, 'html.parser')
        #find the container we are looking for
        moneySpent = soup.find(class_='digits js-digits')
        #format the value we have found
        value = moneySpent.get_text().replace(",", "")
        #close the webpage
        driver.quit()
        #return the found value
        return value