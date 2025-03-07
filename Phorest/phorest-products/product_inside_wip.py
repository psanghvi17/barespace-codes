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
out_csv_file_writer.writerow(["Name","Brand","Category","InventoryType","CostPrice","SalePrice"])

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

def get_input_value_by_partial_name(partial_name):
    print(f'get_input_value_by_partial_name: {partial_name}')
    retries = 3  # Number of retries for stale element exception
    for attempt in range(retries):
        try:
            input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//input[contains(@name, '{partial_name}')]")))            
            input_element = driver.find_element(By.XPATH, f"//input[contains(@name, '{partial_name}')]")
            val = input_element.get_attribute("value")
            print(f'Value Found: {val}')
            return val
        except StaleElementReferenceException:
            print(f"Stale element exception on attempt {attempt + 1}, retrying...")
            continue 
        except Exception as e:
            print(f"Error locating or extracting value from input field with name containing '{partial_name}': {e}")
            return None
    print(f"Failed to get value after {retries} attempts.")
    return None

def find_all_brand_elements():    
    try:        
        brand_elements = driver.find_elements(By.XPATH, '//td[@data-column-name="Brand"]')
        print('Found '+str(len(brand_elements))+' Rows')
        return brand_elements 
    except Exception as e:
        print(f"Error finding brand elements: {e}")
        return []

def get_input_value(id):
    try:
        print("Getting value for "+id)
        input_element = driver.find_element(By.ID, id)        
        input_value = input_element.get_attribute("value")
        print('Value Found '+input_value)
        return input_value
    except Exception as e:
        print(f"Error retrieving input value: {e}")
        return None

def get_button_text_by_aria_label(name):
    try:      
        print("Getting value for "+name) 
        button_element = driver.find_element(By.NAME, name)        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button_element) 
        button_text = button_element.text
        return button_text
    except Exception as e:
        print(f"Error retrieving button text: {e}")
        return None

def find_checked_radio():
    try:        
        parent = driver.find_element(By.XPATH, '//div[@role="radiogroup"]')        
        checked_radio = parent.find_element(By.XPATH, './/div[@role="radio" and @aria-checked="true"]')        
        radio_label = checked_radio.get_attribute("aria-label")
        return radio_label
    except Exception as e:
        print(f"Error finding checked radio button: {e}")
        return None

def click_back_button():
    try:
        retries = 3  # Number of retries for stale element
        for attempt in range(retries):
            try:
                back_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Back"]')))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_button)                
                back_button.click()
                print("Back button clicked successfully.")
                return
            except StaleElementReferenceException:
                print(f"Stale element exception on attempt {attempt + 1}. Retrying...")
                continue  # Retry locating the element
        print("Failed to click the back button after retries.")
    except Exception as e:
        print(f"Error clicking the back button: {e}")

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
    rows=find_all_brand_elements()
    for i in range(len(rows)):
        rows=find_all_brand_elements()
        row=rows[i]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", row)
        row.click()
        time.sleep(5)
        name=get_input_value("name")
        brand=get_button_text_by_aria_label("brand-search-button")
        category=get_button_text_by_aria_label("category-search-button")
        inventory_type=find_checked_radio()
        cost_price=get_input_value_by_partial_name('cost-price')
        sale_price=get_input_value_by_partial_name('sale-price')
        out_csv_file_writer.writerow([name,brand,category,inventory_type,cost_price,sale_price])
        click_back_button()
        time.sleep(5)
    x=click_next_page_button()