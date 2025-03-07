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

out_csv_file_path = "customer_info.csv"
out_csv_file = open(out_csv_file_path, mode='a', newline='',encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["ID","First Name","Last Name","Phone Number","Email"])

in_csv_file_path = "BoombaeUKPhotoUpload.csv"
in_csv_file = open(in_csv_file_path, mode='r', newline='',encoding='utf-8')
csv_reader = csv.reader(in_csv_file)
next(csv_reader)


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    driver.get('https://my.phorest.com')
    time.sleep(1)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('georgie@laserclub.co.uk')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('My1Minnie!') 
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)

def get_input_value_by_partial_name(driver, partial_name):
    try:
        input_element = driver.find_element(By.XPATH, f"//input[contains(@name, '{partial_name}')]")
        return input_element.get_attribute("value")
    except Exception as e:
        print(f"Error locating or extracting value from input field with name containing '{partial_name}': {e}")
        return None


def collect_data(Phorest_Customer_ID):
    url="https://my.phorest.com/a/48600/clients/"+Phorest_Customer_ID+"/overview"
    driver.get(url)
    time.sleep(5)
    first_name=get_input_value_by_partial_name(driver, 'first-name')
    last_name=get_input_value_by_partial_name(driver, 'last-name')
    phone=get_input_value_by_partial_name(driver, 'phone-number')
    email=get_input_value_by_partial_name(driver, 'email')
    print([Phorest_Customer_ID,first_name,last_name,phone,email])
    out_csv_file_writer.writerow([Phorest_Customer_ID,first_name,last_name,phone,email])
login()
for row in csv_reader:    
    collect_data(row[0])    