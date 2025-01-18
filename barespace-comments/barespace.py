from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

csv_file_path = 'PhoneNumbers.csv'
out_csv_file = "client_notes.csv"
exception_file = open('exception.csv', mode='w', newline='')
exception_csv_writer = csv.writer(exception_file)
# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed and in PATH
def read_csv_in_chunks(file_path, chunk_size=500):
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header
        yield header
        chunk = []
        for row in csv_reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk  # Yield the remaining ro

try:
    # Open the Phorest login page
    driver.get('https://my.phorest.com')
    
    # Wait for the page to load
    time.sleep(2)
    
    # Locate and interact with the username field
    username_field = driver.find_element(By.NAME, 'email')  # Update the locator if needed
    username_field.send_keys('aoife+queen@barespace.io')  # Replace 'username' with your actual username
    
    # Locate and interact with the password field
    password_field = driver.find_element(By.NAME, 'password')  # Update the locator if needed
    password_field.send_keys('Aoife@1')  # Replace 'password' with your actual password
    
    # Submit the form
    password_field.send_keys(Keys.RETURN)  # Simulates pressing the "Enter" key
    time.sleep(5)  # Wait for the login process to complete (adjust as necessary)    
    clients_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-clients-link")))
    clients_link.click()
    time.sleep(2)

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        with open(out_csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["First Name","Last Name","Phone" ,"Note"])        
            
            # Process CSV in chunks
        for chunk in read_csv_in_chunks(csv_file_path, chunk_size=500):
            if isinstance(chunk, list):  # Skip header chunk
                for row_number, row in enumerate(chunk, start=1):
                    # Skip empty rows or rows with insufficient columns
                    if not row or len(row) < 4:
                        print(f"Skipping row {row_number}: insufficient data {row}")
                        continue

                    # Check if note column is empty
                    if row[3] == '':  
                        try:
                            print(row)    
                            phone_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Phone number"]')))
                            phone_input.clear()  # Clears any pre-filled text
                            phone_input.send_keys(row[2])
                            phone_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//td[@data-column-name="Phone"]')))
                            phone_element.click()
                            notes_textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "notes")))
                            notes_value = notes_textarea.get_attribute("value")
                            writer.writerow([row[0],row[1],row[2],notes_value])
                            back_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.ID, "back")))
                            back_button.click()

                        except Exception as e:
                            print(f"Phone number {row[2]} not found or another error occurred: {e}")
                            csv_writer.writerow([row[2]])
                            continue
    

    
except Exception as e:
    print(f"An error occurred: {e}")
    
finally:
    # Close the browser
    driver.quit()
