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

out_csv_file_path = "supplier_info.csv"
out_csv_file = open(out_csv_file_path, mode='a', newline='', encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["Supplier"])

service = Service()
driver = webdriver.Chrome(service=service)


def login():
    driver.get('https://my.phorest.com')
    time.sleep(5)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('')
    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys('')
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)


def click_manager_link(id):
    print('Clicking using id '+id)
    manager_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, id)))
    manager_link.click()


def find_all_supplier_elements():
    try:
        supplier_elements = driver.find_elements(
            By.XPATH, '//td[@data-column-name="Company"]')
        print('Found '+str(len(supplier_elements))+' Rows')
        return supplier_elements
    except Exception as e:
        print(f"Error finding brand elements: {e}")
        return []


def click_back_button():
    try:
        retries = 3  # Number of retries for stale element
        for attempt in range(retries):
            try:
                back_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Back"]')))
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", back_button)
                back_button.click()
                print("Back button clicked successfully.\n\n")
                return
            except StaleElementReferenceException:
                print(f"Stale element exception on attempt {
                      attempt + 1}. Retrying...")
                continue  # Retry locating the element
        print("Failed to click the back button after retries.")
    except Exception as e:
        print(f"Error clicking the back button: {e}")


def click_next_page_button():
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "next-page")))
        print(f"Button Found: {next_page_button.get_attribute('outerHTML')}")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", next_page_button)
        driver.execute_script("arguments[0].click();", next_page_button)
        print("Next page button clicked successfully using JavaScript.")
        return 0
    except Exception as e:
        print(f"Error clicking the next page button: {e}")


login()
click_manager_link("main-nav-manager-link")
click_manager_link("suppliers")
time.sleep(5)

x = 0

while x == 0:
    supplier_elements = find_all_supplier_elements()
    for i in range(len(supplier_elements)):
        print(f"{i} Supplier: ", supplier_elements[i])

        suppilers = find_all_supplier_elements()
        supplier = suppilers[i]

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", supplier)
        supplier.click()
        time.sleep(5)
        click_back_button()
        time.sleep(5)

    x = click_next_page_button()
