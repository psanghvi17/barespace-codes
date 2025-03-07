import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import itertools

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

def collect_data(driver, out_csv_writer, Phorest_Customer_ID):
    url = f"https://my.phorest.com/a/48600/clients/{Phorest_Customer_ID}/overview"
    driver.get(url)
    time.sleep(5)
    first_name = get_input_value_by_partial_name(driver, 'first-name')
    last_name = get_input_value_by_partial_name(driver, 'last-name')
    phone = get_input_value_by_partial_name(driver, 'phone-number')
    email = get_input_value_by_partial_name(driver, 'email')
    print([Phorest_Customer_ID, first_name, last_name, phone, email])
    out_csv_writer.writerow([Phorest_Customer_ID, first_name, last_name, phone, email])

# Input and output file paths
in_csv_file_path = "BoombaeUKPhotoUpload.csv"
out_csv_file_path = "customer_info.csv"

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Login to the system
login()

# Open input and output files
with open(in_csv_file_path, mode='r', newline='') as in_csv_file, \
     open(out_csv_file_path, mode='a', newline='') as out_csv_file:

    csv_reader = csv.reader(in_csv_file)
    out_csv_writer = csv.writer(out_csv_file)

    # Write headers to the output file if starting fresh
    out_csv_writer.writerow(["ID", "First Name", "Last Name", "Phone Number", "Email"])

    # Skip the header row of the input file
    next(csv_reader)

    while True:
        # Process rows in chunks of 500
        chunk = list(itertools.islice(csv_reader, 500))
        if not chunk:
            break  # Exit loop if no more rows to process

        for row in chunk:
            try:
                collect_data(driver, out_csv_writer, row[0])
            except WebDriverException as e:
                print(f"Error processing ID {row[0]}: {e}")
                continue

        # Save progress and avoid resource exhaustion
        out_csv_file.flush()

        # Optional: Sleep between chunks to reduce load
        time.sleep(10)

# Close the WebDriver
driver.quit()
