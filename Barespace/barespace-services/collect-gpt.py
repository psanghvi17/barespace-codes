import time
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

file_path = 'fresha-services-inp.csv'
csvfile = open(file_path, 'a', encoding='utf-8', newline='')
writer = csv.writer(csvfile)
writer.writerow(["Name", "Service", "Menu", "Description", "Duration", "Price", "Extra Time", "Staff","Online","Resources"])

def login():
    driver.get("https://partners.fresha.com/users/sign-in/") 
    time.sleep(10)   
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    email = "aoife+epiluxe@barespace.io"
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN) 
    time.sleep(10)   
    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
    password = "Password1"
    password_field.send_keys(password)
    time.sleep(1)
    password_field.send_keys(Keys.RETURN)

def click_services():
    system_definitions_link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]")))
    system_definitions_link.click()    
    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/services')]//div[text()='Services']")))
    products_link.click()

def click_catalog_link():
    try:
        catalog_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa='nav-d-catalog']")))
        catalog_link.click()
        print("Catalog link clicked successfully.")
    except WebDriverException as e:
        print(f"Error clicking on the catalog link: {e}")

def get_elements_by_css_selector(selector):
    try:
        return driver.find_elements(By.CSS_SELECTOR, selector)
    except WebDriverException as e:
        print(f"Error locating elements by selector '{selector}': {e}")
        return []

def get_element_value_by_name(name):
    try:
        element = driver.find_element(By.NAME, name)
        return element.get_attribute("value")
    except WebDriverException as e:
        print(e)
        return None

def get_element_attribute(selector, attribute):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute(attribute)
    except WebDriverException as e:
        print(f"Error locating or extracting attribute '{attribute}' from element '{selector}': {e}")
        return None

def get_element_text(selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except WebDriverException as e:
        print(f"Error extracting text from element '{selector}': {e}")
        return None

def get_selected_option_text(selector):
    try:
        select_element = driver.find_element(By.CSS_SELECTOR, selector)
        select = Select(select_element)
        return select.first_selected_option.text
    except WebDriverException as e:
        print(f"Error extracting selected option text from '{selector}': {e}")
        return None

def get_selected_team_member():
    try:
        team_member_divs = driver.find_elements(By.CSS_SELECTOR, "div[data-qa^='select-service']")
        for div in team_member_divs:
            checkbox = div.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            if checkbox.get_attribute("checked"):
                return checkbox.get_attribute("aria-label")
        return None  # No team member is selected
    except WebDriverException as e:
        print(f"Error locating selected team member: {e}")
        return None

def get_div_value(driver, div_class):
    try:
        div_element = driver.find_element(By.CLASS_NAME, div_class)
        span_element = div_element.find_element(By.TAG_NAME, "span")
        return span_element.text
    except Exception as e:
        print(f"Error retrieving value from div element: {e}")
        return None

def get_services(driver):
    services = []    
    service_elements = driver.find_elements(By.XPATH, "//div[@data-qa='package-form-services-list-item']")
    print(len(service_elements),"services found")
    for service in service_elements:            
        name = service.find_element(By.XPATH, ".//p[contains(@id, 'label-react-aria')]" ).text
        print("name",name)
        duration = service.find_element(By.XPATH, ".//p[contains(@id, 'description-react-aria')]" ).text
        print("duration",duration)
        price = service.find_element(By.XPATH, ".//span[@data-qa='retail-price']" ).text
        print("price",price)
        services.append({'name': name,'duration': duration,'price': price})            
    return services

def close_button():
    close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-close-modal-close-service-form")))
    close_button.click()
    time.sleep(1)

def close_button_package():
    close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "button-close-modal-package-close-button")))
    close_button.click()
    time.sleep(1)

def click_members():
    team_members_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-qa='team-members']")))
    team_members_button.click()

def team_members():
    checked_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox' and @checked]")
    checked_team_members = []
    for checkbox in checked_checkboxes:
        label = checkbox.find_element(By.XPATH, "../div/p").text  # Adjust if label structure changes
        checked_team_members.append(label)
    return checked_team_members

def click_online():
    online_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-qa='online-booking']")))
    online_button.click()

def check_online():
    checkbox = driver.find_element(By.ID, "input-onlineBookingEnabled")
    return checkbox.get_attribute("aria-checked") == "true"

def click_resources():
    resources_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@data-qa='resources']")))
    resources_button.click()

def get_resources():
    checked_checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox' and @checked]")
    checked_resources = []
    for checkbox in checked_checkboxes:
        label_element = checkbox.find_element(By.XPATH, "./ancestor::label")
        resource_name = label_element.find_element(By.XPATH, ".//p[contains(@class, 'font-default-body-s-regular')]").text.strip()
        checked_resources.append(resource_name)
    return checked_resources    

def get_all_services_for_multi():
    services = driver.find_elements(By.CSS_SELECTOR, "div.Zq2zgU")
    service_data = []
    for service in services:
        try:
            name = service.find_element(By.CSS_SELECTOR, "p._-wKRPF.rfrY5F").text
            duration = service.find_element(By.CSS_SELECTOR, "p._-wKRPF.u4xy3F").text
            price = service.find_element(By.CSS_SELECTOR, "span._-wKRPF.font-default-body-m-medium").text
            service_data.append({
                "name": name,
                "duration": duration,
                "price": price
            })
        except Exception as e:
            print(f"Error extracting data for a service: {e}")

def main():
    try:
        login()
        time.sleep(5)
        click_catalog_link()
        time.sleep(5)
        all_divs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[substring(@id, string-length(@id) - string-length('action') + 1) = 'action']")))
        print(f"Number of services found: {len(all_divs)}")
        time.sleep(5)
        for div in all_divs:
            try:
                time.sleep(5)
                driver.execute_script("arguments[0].scrollIntoView();", div)
                driver.execute_script("arguments[0].click();", div) 
                time.sleep(5)               
                header = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1")))
                header_text = header.text                
                print(header_text+'*******')
                if header_text == 'Edit package':
                    package_name = get_element_value_by_name("name")
                    print("package_name ",package_name)  
                    menu=get_div_value(driver, 'SF1fuo')
                    print("menu",menu)
                    description = get_element_attribute("textarea[data-qa='input-input-structure-package-description-input']", "value")
                    print("description ",description)
                    services = get_services(driver)
                    for service in services:
                        print(service)
                        writer.writerow([service['name']+' '+package_name, ' ', menu, description, service['duration'], service['price'], ""])
                    close_button_package()

                if header_text == 'Edit service':                 
                    full_name = get_element_value_by_name("name")
                    print("full_name",full_name)            
                    service = get_element_attribute("input[data-qa='input-input-structure-service-type']", "value")
                    print("service",service)
                    menu = get_element_text("div[data-qa='select-structure-value-menu-category'] span")
                    print("menu ",menu)
                    description = get_element_attribute("textarea[data-qa='input-input-structure-description']", "value")
                    print("description ",description)
                    duration = get_selected_option_text("select[data-qa='select-structure-native-select-duration']")
                    print("duration ",duration)
                    price = get_element_attribute("input[name='servicePricingLevels[0].price']", "value")
                    print("price ",price)
                        # services=get_all_services_for_multi()
                        # for service in services:
                        #     print(service)
                        #     writer.writerow([service['name']+' '+full_name, ' ', menu, description, service['duration'], service['price'], ""])
                    try:
                        extra_time = get_selected_option_text("select[name='extraTime.extraTimeInSeconds']")
                        print("extra_time ",extra_time)
                    except:
                        print("No Extra time")            
                    click_members()
                    members=team_members()
                    print(members)
                    click_online()
                    online=check_online()
                    print(online) 
                    click_resources()
                    resources=get_resources()
                    print(resources)                   
                    writer.writerow([full_name, service, menu, description, duration, price, extra_time,members,online,resources])                    
                    close_button()
                
            except Exception as e:
                print(e)
                print("Exception in",div)
                writer.writerow(["Exception","" , "","" ,"" ,"" ,"" ])
                # continue

    except Exception as e:
        print(f"An error occurred: {e}")
        

    finally:
        csvfile.close()
        driver.quit()

if __name__ == "__main__":
    main()
