import time
import json
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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = "setup+studio75@barespace.io"
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
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/services')]//div[text()='Services']")))
    products_link.click()



try: 
    login()   
    click_services() 
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-danger') and contains(., 'Delete')]")))   
    while button is not None:
        button.click() 
        confirm_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Confirm']")))
        confirm_button.click()      
        time.sleep(1)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-danger') and contains(., 'Delete')]")))   
except Exception as e:
    print(e)
finally:
    driver.quit()  # Ensure the browser closes
