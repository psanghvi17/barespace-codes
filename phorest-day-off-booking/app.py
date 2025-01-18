from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import re
from bs4 import BeautifulSoup
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
    driver.get('https://my.phorest.com')
    time.sleep(1)
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('aoife+queen@barespace.io')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Aoife@1') 
    time.sleep(1)
    password_field.send_keys(Keys.RETURN)

def click_manager_link():
    try:
        manager_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-manager-link")))        
        driver.execute_script("arguments[0].scrollIntoView(true);", manager_link)        
        manager_link.click()
        print("Manager link clicked successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def click_staff_rosters_link():
    try:
        staff_rosters_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "rosters")))        
        driver.execute_script("arguments[0].scrollIntoView(true);", staff_rosters_link)
        staff_rosters_link.click()
        print("Staff Rosters link clicked successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def click_trail_button():
    try:
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        print("click_trail_button")
        # Wait for the button to be present and clickable
        trail_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "trail-button"))
        )
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", trail_button)
        
        # Click the button
        trail_button.click()
        print("Trail button clicked successfully.")
    
    except TimeoutException:
        print("The Trail button was not found or not clickable within the timeout.")
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_all_rows_before_nov_1():
    all_rows = []
    last_row_count = 0

    while True:
        rows = driver.find_elements(By.XPATH, "//tr[contains(@class, 'lt-row')]")
        for row in rows[last_row_count:]:
            try:
                row_text = row.text
                lines = row_text.split("\n")
                date_text = lines[0].strip()
                row_date = datetime.strptime(date_text, "%a, %d/%m/%Y, %I:%M %p")
                if row_date < datetime(2024, 11, 1):
                    print("Stopping: Reached date before November 1.")
                    return all_rows
                all_rows.append(row_text)
            except Exception as e:
                print(f"Error processing row: {e}")
        last_row_count = len(rows)

        time.sleep(5)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(20)  # Wait for new rows to load

        # Stop if no new rows are loaded
        if len(rows) == last_row_count:
            print("No more rows to load.")
            break

    return all_rows

def parse_row_content(row_content):
    try:
        # Split content into lines and normalize
        lines = row_content.strip().splitlines()
        lines = [line.strip() for line in lines if line.strip()] 
        parsed_data = {
            "Date and Time": lines[0],            
            "Staff Roster": None,
            "Branch": None,
            "Type": None,
            "Start Date": None,
            "Start Time": None,
            "End Time": None,
            "Repeating": None,
        }

        # Extract staff roster details
        details = "\n".join(lines[2:])  # Combine remaining lines for easier parsing
        parsed_data["Staff Roster"] = details.split("\n")[1]  # First line after "Staff Roster"

        # Use BeautifulSoup for structured parsing
        soup = BeautifulSoup(details, "html.parser")
        
        # Extract all key-value pairs dynamically
        keys = ["Branch", "Type", "Start Date", "Start Time", "End Time", "Repeating"]
        for key in keys:            
            value = details.split(key)[1].split("\n")[1] if key in details else None
            print(key,':',value)
            parsed_data[key] = value       
        return parsed_data
    except Exception as e:
        print(f"Error parsing row content: {e}")
        return None

def extract_and_write_to_csv(file_name="output.csv"):  
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)  
        time.sleep(60)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")           
        rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tr[contains(@class, 'lt-row')]")))
        # rows=fetch_all_rows_before_nov_1()
        print(f"Found {len(rows)} rows.")
        with open(file_name, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["DateTime",  "StaffRoster", "Branch", "Type", "StartDate", "StartTime", "EndTime", "Repeating"])
            for row in rows:
                try:
                    date_time_str = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(1)").text.strip()
                    print(date_time_str,'-----')
                    date_time_obj = datetime.strptime(date_time_str.split(",")[1].strip(), "%d/%m/%Y")
                    if date_time_obj < datetime(2024, 11, 1):
                        print("Date is less than 1 Nov 2024. Breaking the loop.")
                        break                    
                    name = row.find_element(By.CSS_SELECTOR, "td:nth-of-type(3)").text.strip()   
                    print(name,'/////')                
                    row_html = row.get_attribute('outerHTML')
                    soup = BeautifulSoup(row_html, 'html.parser')
                    row_content=soup.get_text(separator="\n")
                    print("Row Content:", row_content)
                    parsed_data = parse_row_content(row_content)   
                    print(parsed_data)                 
                    writer.writerow([parsed_data["Date and Time"],parsed_data["Staff Roster"],parsed_data["Branch"][1:],parsed_data["Type"][1:],parsed_data["Start Date"][1:],parsed_data["Start Time"][1:],parsed_data["End Time"][1:],parsed_data["Repeating"][1:]])                                        
                except Exception as row_error:
                    print(f"Error processing row: {row_error}")
                    break
                    
        print(f"Data successfully written to {file_name}.")        

login()
click_manager_link()
click_staff_rosters_link()
time.sleep(20)
# click_trail_button()
extract_and_write_to_csv()
