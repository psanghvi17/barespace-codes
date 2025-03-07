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
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/products')]//div[text()='Products']")))
    products_link.click()
    file_path = 'product_info.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:      
            print(row["Name"])                     
            add_product_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Product']]")))
            driver.execute_script("arguments[0].click();", add_product_button)
                        
            product_name_input=WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "product_name")))
            product_name_input.send_keys(row["Name"].title())                
            
            print("full-price",str(row["SalePrice"]))
            price_input = driver.find_element(By.NAME, "price")
            price_input.send_keys(str(row["SalePrice"]))                

            print("cost-price",row["CostPrice"])
            cost_price_input = driver.find_element(By.NAME, "cost_price")            
            if len(row["CostPrice"])==0:
                print("cost-price is None")
            else:                                
                cost_price_input.send_keys(row["CostPrice"])

            print("category",row["Category"])
            if len(row["Category"])>0:
                select_dropdown_option(driver, row["Category"].title())
            # else:
            #     select_dropdown_option(driver, 'Uncategorized')
            
            print("supplier")
            if len(row["Brand"])>0:
                select_dropdown_option(driver, (row["Brand"].title()+' Supplier'))                
            
            print("location")
            select_dropdown_option_location(driver, "Dollhouse Hair & Beauty")   

            print("barcode")
            if len(row["Barcode"])==0:
                print("Barcode is None. Check your data source.")
            else:
                barcode = driver.find_element(By.NAME, "barcode")
                barcode.send_keys(row["Barcode"])

            select_element = driver.find_element(By.ID, "usage")
            dropdown = Select(select_element)
            if row['SalePrice']!='0.00':
                dropdown.select_by_value("retail")
                print("Retails selected")
            else:
                dropdown.select_by_value("professional")
                print("Professional selected")
            
            button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.flex-1.order-1.lg\\:order-2")
            print("Button found")
            time.sleep(1)
            button.click()
            print("button clicked")
            time.sleep(5)
            # break
except Exception as e:
    print(e)
    time.sleep(10)
finally:
    # Step 7: Close the browser
    driver.quit()  # Ensure the browser closes
