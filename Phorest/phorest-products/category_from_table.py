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

out_csv_file_path = "category_info.csv"
out_csv_file = open(out_csv_file_path, mode='a', newline='',encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["Category"])

service = Service()
driver = webdriver.Chrome(service=service)

def login():
    driver.get('https://my.phorest.com')
    time.sleep(5)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('info@greenroomskendal.co.uk')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('KellySolo0412') 
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

def click_link_by_text(link_text):
    try:
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//a[.//span[text()="{link_text}"]]')))        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
        link.click()
        print(f"Clicked link with text: {link_text}")
    except Exception as e:
        print(f"Error clicking link with text '{link_text}': {e}")

def get_all_category_names():
    try:
        category_names = set()        
        time.sleep(10) 
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//table[@class="_table_16dtgq"]')))       
        rows = driver.find_elements(By.XPATH, '//table[@class="_table_16dtgq"]//tbody/tr[not(contains(@class, "lt-is-loading"))]')
        print(str(len(rows))+" Rows Found")
        for row in rows:
            try:
                category_name = row.find_element(By.XPATH, './/td[2]/span').text.strip()
                print(category_name)
                out_csv_file_writer.writerow(category_name)
                if category_name:
                    category_names.add(category_name)                    
            except Exception as e:
                print(f"Error extracting category from row: {e}")
                continue          
        
        print(f"Total categories found: {len(category_names)}")
        return list(category_names)
    
    except Exception as e:
        print(f"Error retrieving category names: {e}")
        return []

login()
click_manager_link("main-nav-manager-link")
click_manager_link("categories")
time.sleep(5)
click_link_by_text("Product Categories")
time.sleep(10)
x=0
categories = get_all_category_names()
# for cat in categories:
#     out_csv_file_writer.writerow(cat)
