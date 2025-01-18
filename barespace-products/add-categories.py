from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = "setup+jumelleskin&beauty@barespace.io"
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password") 
    password = "jumelleskin&beauty123"
    password_field.send_keys(password)      
    login_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']")
    time.sleep(2)
    login_button.click()


try:   
    login()
    system_definitions_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]")))
    system_definitions_link.click()   
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/products')]//div[text()='Products']")))
    products_link.click()
    categories_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn btn-icon bg-gray-600 text-white') and span[text()='Categories']]")))
    categories_button.click()
    file_path = 'categories.json'
    with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for obj in data:      
                print(obj)
                category=obj["attributes"]["name"]
                print(category)  
                input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "service_name")))
                input_field.send_keys(category)  
                plusButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and contains(@class, 'btn bg-secondary h-full')]")))
                plusButton.click() 
    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and text()='Save']")))
    time.sleep(100)
    save_button.click()     

except Exception as e:
    print(e)
    time.sleep(10)
finally:
    # Step 7: Close the browser
    driver.quit()  # Ensure the browser closes
