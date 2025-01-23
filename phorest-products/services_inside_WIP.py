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
wait = WebDriverWait(driver, 10)

def login():
    driver.get('https://my.phorest.com')
    time.sleep(5)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('aoife+dollhouse@barespace.io')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Password1') 
    password_field.send_keys(Keys.RETURN)
    time.sleep(10)

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

def click_service_names():
    service_links = driver.find_elements(By.CSS_SELECTOR, "a.ember-view")
    for link in service_links:
        try:
            link_text = link.text
            print(f"Clicking on: {link_text}")
            ActionChains(driver).move_to_element(link).click().perform()
            time.sleep(2)
            driver.back()
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.ember-view")))
        except Exception as e:
            print(f"Error clicking on {link_text}: {e}")

def get_input_value(input_name):    
    try:
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"input[name='{input_name}']")))
        input_value = input_element.get_attribute("value")
        return input_value
    except Exception as e:
        print(f"Error retrieving value for input with name '{input_name}': {e}")
        return None

def get_div_value(css_selector):
    try:
        wait = WebDriverWait(driver, 10)
        div_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        span_element = div_element.find_element(By.CSS_SELECTOR, "span._option_st4q28")
        return span_element.text.strip()
    except Exception as e:
        print(f"Error retrieving value from div with selector '{css_selector}': {e}")
        return None

login()
click_manager_link("main-nav-manager-link")
click_manager_link("services")
time.sleep(20)     
wait = WebDriverWait(driver, 10)
iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='https://app.phorest.com']")))
driver.switch_to.frame(iframe)
table_body = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lt-body")))
rows = table_body.find_elements(By.CSS_SELECTOR, "tr.lt-row")
print(f"Loaded rows: {len(rows)}")    
for i, row in enumerate(rows):
    try:
        print(1)
        link = row.find_element(By.CSS_SELECTOR, "a")        
        print(2)
        ActionChains(driver).move_to_element(link).perform()
        print(3)
        link.click()   
        print(4)
        name=get_input_value("service-name") 
        print(f"Name : {name}")    
        div_selector = "div.ember-view.ember-basic-dropdown-trigger.ember-power-select-trigger._trigger_st4q28"
        category = get_div_value(div_selector)
        print(f"category : {category}")   
        service_price=get_input_value("service-price") 
        print(f"service_price : {service_price}")   
        time.sleep(20)        
    except Exception as e:
        print(f"Error processing row {i+1}: {e}")
        time.sleep(20)        
    
