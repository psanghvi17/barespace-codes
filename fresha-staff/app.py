import time
import json
import ast
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = "setup+studio75@barespace.ioo"
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password") 
    password = "studio75123"
    password_field.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']")
    time.sleep(2)
    login_button.click()

def click_services():
    system_definitions_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]")))
    system_definitions_link.click()   
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/staff-groups')]//div[text()='Services']")))
    products_link.click()


try: 
    time.sleep(2)
    login()   
    click_services()     
    in_csv_file_path = 'fresha-services-inp.csv'
    in_csv_file = open(in_csv_file_path, mode='r', newline='',encoding='utf-8')
    in_csv_reader = csv.reader(in_csv_file)
    header = next(in_csv_reader)    
    for row_number, row in enumerate(in_csv_reader, start=1):
            print(row[0])
            add_product_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Service']]")))
            driver.execute_script("arguments[0].click();", add_product_button)            
            fill_text_input(driver, "service_name", row[0].title())
            print("service_name")
            time.sleep(1)
            select_multiselect_option(driver, "Service Categories", row[2])       
            print("Service Categories")            
            select_multiselect_option(driver, "Location", "Jumelle Skin & Beauty")                
            print("Location") 
            staff_list = ast.literal_eval(row[7])             
            for staff in staff_list:                 
                select_multiselect_option(driver, "Staff Group", staff.split(' ')[0])                       
            fill_text_input(driver, "service_price", row[5])             
            fill_text_input(driver, "service_duration", row[4])            
            print("service_duration")
            resource_list = ast.literal_eval(row[7]) 
            for resource in resource_list:                 
                select_multiselect_option(driver, "Resource", resource.split(' ')[0])             
            if len(row[3])>0:
                print("Description")
                fill_ck_editor(row[3])
                time.sleep(5)
            if row[8] == 'FALSE': 
                print("Checkbox")                   
                uncheck_box()
            print("Submit")
            click_create_new_service()
            time.sleep(10)
except Exception as e:
    print(e)
finally:
    driver.quit()  # Ensure the browser closes
    print()
