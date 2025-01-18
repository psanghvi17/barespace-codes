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

def remove_non_bmp_chars(text):
    """Remove characters outside the Basic Multilingual Plane (BMP)."""
    return re.sub(r'[^\u0000-\uFFFF]', '', text)

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

def fill_text_input(driver, field_name, value):
    if value is not None:
        field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, field_name)) )
        field.clear()
        field.send_keys(value)

def select_multiselect_option(driver, field_label, option_text):
    print('select_multiselect_option',field_label)
    if len(option_text)>0:
        label = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{field_label}')]/following-sibling::div"))   )
        dropdown = label.find_element(By.CLASS_NAME, "multiselect__tags")
        dropdown.click()

        options = WebDriverWait(driver, 10).until( EC.presence_of_all_elements_located((By.CLASS_NAME, "multiselect__option")))
        for option in options:
            if option_text in option.text:
                option.click()
                break

def select_dropdown_option(driver, option_text):
        try:
            dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".multiselect__tags")))
            try:
                dropdown.click()
            except:
                driver.execute_script("arguments[0].click();", dropdown)            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".multiselect__content")))
            try:
                option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text))))
                option.click()
            except Exception as e:
                option = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text))))
                driver.execute_script("arguments[0].click();", option)        
        except Exception as e:
            print(f"Error selecting dropdown option: {e}")

def fill_ck_editor(text):
    # Locate CKEditor editable content area
    editor_area = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ck-editor__editable"))
    )
    
    # Scroll to editor and click
    driver.execute_script("arguments[0].scrollIntoView(true);", editor_area)
    ActionChains(driver).move_to_element(editor_area).click().perform()
    
    # Clear CKEditor content using JavaScript
    driver.execute_script("arguments[0].innerHTML = '';", editor_area)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", editor_area)
    
    # Send the new text in one go
    editor_area.send_keys(text)
    
    # Trigger the blur event to finalize input
    driver.execute_script("arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));", editor_area)

def click_create_new_service():
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Locating and clicking the button...")            
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and text()='Create new service']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)  
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
            button.click()
            print("Button clicked successfully.")
            break
        except StaleElementReferenceException:
            print("Stale element encountered. Retrying...")
            time.sleep(1)  # Short delay before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    else:
        print("Failed to click the button after retries.")

def uncheck_box():
    try:
        checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='show_online']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        if checkbox.is_selected():
            print("Checkbox is checked. Attempting to uncheck...")
            checkbox.click()
            print("Checkbox successfully unchecked.")
        else:
            print("Checkbox is already unchecked.")

    except Exception as e:
        print(f"An error occurred: {e}")

try: 
    time.sleep(2)
    login()   
    click_services()     
    in_csv_file_path = 'fresha-services-inp.csv'
    in_csv_file = open(in_csv_file_path, mode='r', newline='',encoding='utf-8')
    in_csv_reader = csv.reader(in_csv_file)
    header = next(in_csv_reader)    
    for row_number, row in enumerate(in_csv_reader, start=1):
        if len(row[5])>0:
            print(row[0])
            add_product_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Service']]")))
            driver.execute_script("arguments[0].click();", add_product_button)            
            fill_text_input(driver, "service_name", row[0].title())
            print("service_name")
            time.sleep(1)
            select_multiselect_option(driver, "Service Categories", row[2].title())   
            print("Service Categories")            
            select_multiselect_option(driver, "Location", "Studio 75")                
            print("Location") 
            if len(row[7])>0:
                staff_list = ast.literal_eval(row[7])             
                for staff in staff_list:                 
                    select_multiselect_option(driver, "Staff Group", staff.split(' ')[0])                       
            fill_text_input(driver, "service_price", row[5])             
            fill_text_input(driver, "service_duration", row[4])            
            print("service_duration")
            if len(row[9])>0:
                resource_list = ast.literal_eval(row[9]) 
                for resource in resource_list:                 
                    select_multiselect_option(driver, "Resource", resource.split(' ')[0]) 
            print("Resource")
            if len(row[3])>0:
                print("Description")
                fill_ck_editor(remove_non_bmp_chars(row[3]))
                time.sleep(5)
            print("Desc done, checkbox start")
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
