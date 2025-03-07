import os
import csv

def login():
    driver.get('https://my.phorest.com')
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('aoife+queen@barespace.io')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Aoife@1') 
    password_field.send_keys(Keys.RETURN) 

def click_client():
    clients_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-clients-link")))
    clients_link.click()    

def process_row(row):
    print(row)
    phone_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Phone number"]')))
    phone_input.clear()
    phone_input.send_keys(row[2])
    phone_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//td[@data-column-name="Phone"]')))
    phone_element.click()
    notes_textarea = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "notes")))
    notes_value = notes_textarea.get_attribute("value")
    out_csv_file_writer.writerow([row[0],row[1],row[2],notes_value])
    back_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "back")))
    back_button.click()


def process_csv_files_in_folder(folder_name):
    csv_files = [file for file in os.listdir(folder_name) if file.endswith('.csv')]
    for csv_file in csv_files:
        global driver
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        login()
        click_client()
        file_path = os.path.join(folder_name, csv_file)
        print(f"Processing file: {csv_file}")

        with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader) 
            for row in reader:
                process_row(row)
        driver.quit()

    print("All files processed successfully.")

# Example usage
folder_path = './split_files'
process_csv_files_in_folder(folder_path)
