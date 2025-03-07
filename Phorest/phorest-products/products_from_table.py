from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

out_csv_file_path = "product_info.csv"
out_csv_file = open(out_csv_file_path, mode='a', newline='',encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["Brand","Category","Name","Vol","Barcode","Stock","Ordered","Min","Max","CostPrice","SalePrice"])

service = Service()
driver = webdriver.Chrome(service=service)

def login():
    driver.get('https://my.phorest.com')
    time.sleep(5)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('aoife+dollhouse@barespace.io')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Password1') 
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)

def click_manager_link(id):
        print('Clicking using id '+id)
        manager_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, id)))
        manager_link.click()

def click_next_page_button():
    try:
        next_page_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "next-page")))
        print(f"Button Found: {next_page_button.get_attribute('outerHTML')}")        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_page_button)
        driver.execute_script("arguments[0].click();", next_page_button)
        print("Next page button clicked successfully using JavaScript.")
        return 0
    except Exception as e:
        print(f"Error clicking the next page button: {e}")

login()
click_manager_link("main-nav-manager-link")
click_manager_link("stock")
time.sleep(10)
x=0

while x==0:
    table_rows = driver.find_elements(By.CSS_SELECTOR, "tbody > tr")
    for row in table_rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        row_data = [column.text.strip() for column in columns]
        out_csv_file_writer.writerow(row_data)

    x=click_next_page_button()