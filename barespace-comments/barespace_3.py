import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# File paths
csv_file_path = 'PhoneNumbers.csv'
out_csv_file = "client_notes.csv"
exception_file = open('exception.csv', mode='w', newline='')
exception_csv_writer = csv.writer(exception_file)
# Selenium WebDriver setup
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

try:
    # Open the Phorest login page
    driver.get('https://my.phorest.com')
    
    # Locate and interact with the username field
    username_field = driver.find_element(By.NAME, 'email')  # Update the locator if needed
    username_field.send_keys('aoife+queen@barespace.io')  # Replace 'username' with your actual username
    
    # Locate and interact with the password field
    password_field = driver.find_element(By.NAME, 'password')  # Update the locator if needed
    password_field.send_keys('Aoife@1')  # Replace 'password' with your actual password
    # Submit the form
    password_field.send_keys(Keys.RETURN)  # Simulates pressing the "Enter" key
    # Wait for the login to complete
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-clients-link"))).click()
    
    # Read input CSV in chunks of 500 rows
    chunk_size = 50
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        
        # Ensure output file has a header row
        with open(out_csv_file, mode="w", newline="", encoding="utf-8") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(["First Name", "Last Name", "Phone", "Note"])
        
        chunk = []
        for row_number, row in enumerate(csv_reader, start=1):
            chunk.append(row)
            
            # Process the chunk when it reaches the defined size
            if len(chunk) == chunk_size or (row_number == 1):  # Write the last chunk if it's smaller
                with open(out_csv_file, mode="a", newline="", encoding="utf-8") as out_file:
                    writer = csv.writer(out_file)
                    
                    for chunk_row in chunk:
                        print(chunk_row)
                        if chunk_row[3] == '':  # Check for empty value in the 4th column
                            try:
                                # Automate retrieval of notes
                                phone_input = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Phone number"]')))
                                phone_input.clear()
                                phone_input.send_keys(chunk_row[2])
                                
                                WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, '//td[@data-column-name="Phone"]'))).click()
                                
                                notes_textarea = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.ID, "notes")))
                                notes_value = notes_textarea.get_attribute("value")
                                
                                # Write retrieved data
                                writer.writerow([chunk_row[0], chunk_row[1], chunk_row[2], notes_value])
                                
                                # Navigate back
                                WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.ID, "back"))).click()
                            except Exception as e:
                                print(f"Error for phone number {chunk_row[2]}: {e}")
                                csv_writer.writerow([chunk_row[2]])
                                continue
                
                # Clear chunk for the next set
                chunk = []

except Exception as e:
   
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
