from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import pandas as pd
import os

start_index=1

in_csv_file_path = 'Batch2Queens.csv'
out_csv_file_path = "client_notes_Batch2Queens.csv"
except_csv_file_path='exception.csv'

in_csv_file = open(in_csv_file_path, mode='r', newline='',encoding='utf-8')
in_csv_reader = csv.reader(in_csv_file)
header = next(in_csv_reader)

out_csv_file = open(out_csv_file_path, mode='a', newline='',encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["First Name","Last Name","Phone","Email" ,"Note"])

exception_file = open(except_csv_file_path, mode='w', newline='',encoding='utf-8')
exception_csv_writer = csv.writer(exception_file)

def login():
    driver.get('https://my.phorest.com')
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('aoife+queen@barespace.io')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Aoife@1') 
    password_field.send_keys(Keys.RETURN) 

def click_client():
    clients_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-clients-link")))
    clients_link.click()    

def process_row(row):
    print(row)
    try:
        phone_input = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Phone number"]')))
        phone_input.clear()
        phone_input.send_keys('0'+row[3])
        phone_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//td[@data-column-name="Phone"]')))
        phone_element.click()
        notes_textarea = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "notes")))        
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_value = email_input.get_attribute("value")
        notes_value = notes_textarea.get_attribute("value")
        out_csv_file_writer.writerow([row[0],row[1],row[3],email_value,notes_value])
    except:
        out_csv_file_writer.writerow([row[0],row[1],row[3]])
    finally:
        back_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "back")))
        back_button.click()
          
def process_batch(batch):
    global driver
    chrome_options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    login()
    click_client()
    for row in batch:
        try:
            process_row(row)
        except Exception as e:
            exception_csv_writer.writerow(row[2])
            print(f"An error occurred: {e}")
            continue
    driver.quit()
    
batch_size = 1
batch = []
tot=1939
for row_number, row in enumerate(in_csv_reader, start=1):
    batch.append(row)
    if len(batch) == batch_size or row_number % batch_size == 0 or row_number == start_index or row_number==tot:
        process_batch(batch)
        batch = []
