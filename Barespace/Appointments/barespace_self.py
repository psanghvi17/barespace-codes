from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import pandas as pd

start_index=1

out_csv_file_path = "client_appointments_25-11.csv"


out_csv_file = open(out_csv_file_path, mode='a', newline='')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["Ref","Channel","Created By","Client Name","Client Lastname","Service","Location","Duration","Staff Name","Staff Lastname","Price","Status","Scheduled on","Date Format","Guest Name","Guest Lastname","Resource"])

def login():
    driver.get('https://my.phorest.com')
    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys('beautiliciousu@gmail.com')  
    password_field = driver.find_element(By.NAME, 'password')  
    password_field.send_keys('Snoozers11') 
    password_field.send_keys(Keys.RETURN) 

def take_screenshot(driver, filename_prefix="screenshot"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")  # Generate a unique timestamp
    screenshot_name = f"{filename_prefix}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot saved as {screenshot_name}")

def click_appointment():
    clients_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "main-nav-appointments-link")))
    clients_link.click()    

def click_next_button():
    print('Next')
    next_day_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "appointment-calendar-next-day-button")))    
    try:
        ActionChains(driver).move_to_element(next_day_button).click().perform()    
    except Exception as e:        
        print(f"Error clicking the button: {e}")

def click_back_button():
    print('Back')
    try:
        back_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.NAME, "back")))
        back_button.click()         
        return 1  
    except Exception as e:        
        return 0

def process_event(date_text):  
    print('process event')  
    try:
        name_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//strong[contains(@class, 'font-semibold')]")))
        name = name_element.text        
        services = []
        service_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@name, 'edit-service')]")))        
        for service_element in service_elements:
            service_name = service_element.find_element(By.XPATH, ".//span[contains(@class, 'text-base')]").text
            service_time = service_element.find_element(By.XPATH, ".//button[@name='update-appointment-time']/span/span").text
            service_duration = service_element.find_element(By.XPATH, ".//button[@name='update-appointment-duration']/span/span").text
            service_price = service_element.find_element(By.XPATH, ".//button[@name='update-appointment-price']/span/span").text
            staff_name_element = driver.find_element(By.XPATH,"//div[contains(@class, 'p-2') and contains(@class, 'text-left')]//div[1]/span[2]")
            staff_name = staff_name_element.text.strip() 
            out_csv_file_writer.writerow(["Ref","Channel","Created By",name,name,service_name,"Location",service_duration,staff_name,staff_name,service_price,"Status",date_text+' '+service_time,"Date Format","Guest Name","Guest Lastname","Resource"])                            
        close_button = driver.find_element(By.XPATH, "//button[@name='close-panel-button']")
        close_button.click()        
    except:
        print(date_text+' Exception thrown')

def get_all_divs():
    print('Get all Div')
    try:
        div_elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'relative') and contains(@class, 'h-full') and contains(@class, 'z-10')]")))
        return div_elements
    except:        
        print('No Appointement found')
        return 0

def check_workday():
    print('check_workday')
    try:
        time.sleep(1)
        element = driver.find_element(By.XPATH, "//p[contains(@class, 'grow') and contains(@class, 'text-info-darker')]")
        print('Its not a working day')
        return 1
    except:
        print('Its a working day')
        return 0

def select_branch( branch_name):    
    try:
        # Click the branch selector button to open the dropdown
        branch_selector_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "branch-selector-button"))
        )
        branch_selector_button.click()

        # Wait for the dropdown to appear and locate the branch by its name
        branch_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(@class, 'ember-view') and span[text()='{branch_name}']]"))
        )
        branch_element.click()
        print(f"Branch '{branch_name}' clicked successfully!")
    except Exception as e:
        print(f"Error selecting branch '{branch_name}': {e}")

x=0
driver = webdriver.Chrome() 
action = ActionChains(driver)    
login()
click_appointment()
# time.sleep(5)
#select_branch('Queen Newbridge')
# driver.get('https://my.phorest.com/a/10443/appointments?start=2024-11-27')
time.sleep(1)
while x<365:  
    x=x+1
    # time.sleep(30)
    date_div = driver.find_element(By.XPATH, "//div[contains(@class, 'w-72') and contains(@class, 'whitespace-nowrap')]")
    date_text = date_div.text.strip()   
    print(f"Working Date: {date_text}") 
    try: 
        if check_workday()==1:
            click_next_button()  
            continue 
        div_elements=get_all_divs()
        if div_elements==0:
            click_next_button()  
            continue      
        for div in div_elements:
            action.double_click(div).perform()        
            z = click_back_button()
            if z==0:
                process_event(date_text)   
        click_next_button()
    except:
        print(date_text+' Excption in while')
driver.quit()