import sys
from time import sleep
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyshadow.main import Shadow


webdriver_path = '/Users/mehdi-mac/JupyterNotebooks/Axross-Exerecise/chromedriver' # Enter the file directory of the Chromedriver
url = 'https://shopee.co.id/'

#Read list of items from a CSV file
df_items = pd.read_csv('list_of_items.csv')
search_items=df_items["Items"].tolist()

# Lists to store the scraped data in
Product_general_name=[]
Product_name = []
Product_Price = []



# Select custom Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_argument('start-maximized') 
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

# Open the Chrome browser
driver = webdriver.Chrome(webdriver_path, options=options)
driver.get(url)
driver.implicitly_wait(60)

time.sleep(3)

# Close Graphical pop up in the first page
shadow = Shadow(driver)
element1 = shadow.find_element(".shopee-popup__close-btn")
element1.click()
# Search Item in main page
search_bar_main=driver.find_element(By.CSS_SELECTOR,".shopee-searchbar-input__input")
search_bar_main.send_keys(search_items[0])
driver.find_element(By.CSS_SELECTOR,".btn.btn-solid-primary.btn--s.btn--inline.shopee-searchbar__search-button").click()


time.sleep(3)
i=1

while i <=len(search_items):
 print(i)
 if driver.find_elements(By.XPATH,"//div[@class='_10Wbs- _2STCsK _3IqNCf']"):
  Price_lis = driver.find_elements(By.XPATH,"//div[@class='zp9xm9 kNGSLn l-u0xK']") #Price
  Prod_lis = driver.find_elements(By.XPATH,"//div[@class='_10Wbs- _2STCsK _3IqNCf']") #Product_name
  if len(Prod_lis)>=3:
    n=3
  else:
    n=len(Prod_lis)
  #Extract top 3 hits products info:
  for x in range (0,n):
   print(Prod_lis[x].text)
   print(Price_lis[x].text)
   Product_general_name.append(search_items[i-1])   
   Product_name.append(Prod_lis[x].text)  
   Product_Price.append(Price_lis[x].text)
 else:  
   Product_general_name.append(search_items[i-1])   
   Product_name.append('Product no exist')  
   Product_Price.append('Product no exist')     
        
 time.sleep(2)
       
 #CLear The Search Field text
 searchForMovie = WebDriverWait (driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="shopee-searchbar-input__input"]')))
 searchForMovie.click()
 searchForMovie.clear()
 time.sleep(2)
 Search_bar=driver.find_element(By.XPATH,'//input[@class="shopee-searchbar-input__input"]')
 for z in range (0,len(search_items[i-1])):
  Search_bar.send_keys(Keys.BACKSPACE)
  time.sleep(0.1)
 time.sleep(1)

 # Search for second items and onwards   
 if i<len(search_items):   
  Search_bar.send_keys(search_items[i])
  driver.find_element(By.CSS_SELECTOR,".btn.btn-solid-primary.btn--s.btn--inline.shopee-searchbar__search-button").click()
 i=i+1
 time.sleep(2)
df = pd.DataFrame({'Product_General_Name':Product_general_name,
                   'Product_Detail_Name': Product_name,
                                 'Price': Product_Price
                        })  
df.to_csv('Shopee-Scraped-data.csv',index=False) 
