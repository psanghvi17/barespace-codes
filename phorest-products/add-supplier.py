from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import csv
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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = "setup+dollhousehair&beauty@barespace.io"
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password") 
    password = "dollhousehair&beauty123"
    password_field.send_keys(password)      
    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']")
    time.sleep(2)
    login_button.click()

def select_dropdown_option(driver, option_text):
        try:
            dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".multiselect__tags")))            
            try:
                dropdown.click()
            except:
                driver.execute_script("arguments[0].click();", dropdown)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".multiselect__content")))            
            try:
                option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text)))                )
                option.click()
            except Exception as e:
                option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text)))                )
                driver.execute_script("arguments[0].click();", option)        
        except Exception as e:
            print(f"Error selecting dropdown option: {e}")

def select_dropdown_option_location(driver, option_text):
        try:
            dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".multiselect__tags"))            )
            try:
                dropdown.click()
            except:
                driver.execute_script("arguments[0].click();", dropdown)            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".multiselect__content"))            )            
            try:
                option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text)))                )
                option.click()
            except Exception as e:
                option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text)))                )
                driver.execute_script("arguments[0].click();", option)        
        except Exception as e:
            print(f"Error selecting dropdown option: {e}")

try:
    login()
    system_definitions_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]")))
    system_definitions_link.click()   
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/supplier')]//div[text()='Supplier']")))
    products_link.click()
    file_path = 'supplier_info.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:      
            print(row["Brand"])                     
            add_product_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Supplier']]")))
            driver.execute_script("arguments[0].click();", add_product_button)
                        
            product_name_input=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "name")))
            product_name_input.send_keys(row["Brand"].title())

            product_name_input=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "contact_first_name")))
            product_name_input.send_keys(row["Brand"].title())                          
            
            print("Adding Phone")
            phone_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='form-item relative']//input[@type='tel' and contains(@class, 'vti__input')]")))
            driver.execute_script("arguments[0].scrollIntoView();", phone_input)
            phone_input.clear()
            phone_input.send_keys("+3538712345678")            
            
            
            add_supplier_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn btn-primary') and text()='Add Supplier']")))
            add_supplier_button.click()
            time.sleep(5)
            # break
except Exception as e:
    print(e)
    time.sleep(10)
finally:
    # Step 7: Close the browser
    driver.quit()  # Ensure the browser closes
