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


out_csv_file_path = "services_info_get_inbetwen.csv"
out_csv_file = open(out_csv_file_path, mode='a', newline='', encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(["Name", "Category", "Service Price", "Service Duration",
                             "Preparation Time", "Online", "Description", "Facilities", "Rooms", "Employee"])

service = Service()
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
driver.maximize_window()


def login():
    driver.get('https://my.phorest.com')
    time.sleep(2)
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


def click_link_by_text(link_text):
    try:
        link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, f'//a[.//span[text()="{link_text}"]]')))
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", link)
        link.click()
        print(f"Clicked link with text: {link_text}")
    except Exception as e:
        print(f"Error clicking link with text '{link_text}': {e}")


def get_all_category_names():
    try:
        category_names = set()
        time.sleep(10)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//table[@class="_table_16dtgq"]')))
        rows = driver.find_elements(
            By.XPATH, '//table[@class="_table_16dtgq"]//tbody/tr[not(contains(@class, "lt-is-loading"))]')
        print(str(len(rows))+" Rows Found")
        for row in rows:
            try:
                category_name = row.find_element(
                    By.XPATH, './/td[2]/span').text.strip()
                print(category_name)
                out_csv_file_writer.writerow(category_name)
                if category_name:
                    category_names.add(category_name)
            except Exception as e:
                print(f"Error extracting category from row: {e}")
                continue

        print(f"Total categories found: {len(category_names)}")
        return list(category_names)

    except Exception as e:
        print(f"Error retrieving category names: {e}")
        return []


def click_service_names():
    service_links = driver.find_elements(By.CSS_SELECTOR, "a.ember-view")
    link_text = ""
    for link in service_links:
        try:
            link_text = link.text
            print(f"Clicking on: {link_text}")
            ActionChains(driver).move_to_element(link).click().perform()
            time.sleep(2)
            driver.back()
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "a.ember-view")))
        except Exception as e:
            print(f"Error clicking on {link_text}: {e}")


def get_input_value(input_name, attribute):
    try:
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"input[name='{input_name}']")))
        input_value = input_element.get_attribute(attribute)
        return input_value
    except Exception as e:
        print(f"Error retrieving value for input with name '{
              input_name}': {e}")
        return None


def get_div_value(css_selector):
    try:
        wait = WebDriverWait(driver, 10)
        div_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_selector)))
        span_element = div_element.find_element(
            By.CSS_SELECTOR, "span._option_st4q28")
        return span_element.text.strip()
    except Exception as e:
        print(f"Error retrieving value from div with selector '{
              css_selector}': {e}")
        return None


def click_staff_tab():
    try:
        staff_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "branch-service-staff-tab"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", staff_tab)
        staff_tab.click()
        print("Successfully clicked the 'Staff' tab.")
    except Exception as e:
        print(f"Error clicking the 'Staff' tab: {e}")


def click_general_tab():
    try:
        staff_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "branch-service-general-tab"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", staff_tab)
        staff_tab.click()
        print("Successfully clicked the 'general' tab.")
    except Exception as e:
        print(f"Error clicking the 'general' tab: {e}")


def get_employee_details():
    try:
        employee_details = []
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//table[contains(@class, "_table_16dtgq")]')))
        rows = driver.find_elements(
            By.XPATH, '//table[contains(@class, "_table_16dtgq")]//tbody/tr[not(contains(@class, "lt-is-loading"))]')
        print(f"Found {len(rows)} employees.")
        for row in rows:
            try:
                name_element = row.find_element(By.XPATH, './/td[2]')
                rate_element = row.find_element(By.XPATH, './/td[3]')
                duration_element = row.find_element(By.XPATH, './/td[4]')
                name = name_element.text.strip() if name_element else "N/A"
                rate = rate_element.text.strip() if rate_element else "N/A"
                duration = duration_element.text.strip() if rate_element else "N/A"
                print(name, rate)
                try:
                    toggle_button = row.find_element(
                        By.XPATH, './/td[5]//div[contains(@class, "toggle-btn")]')
                    is_enabled = toggle_button.get_attribute(
                        "aria-checked") is not None
                    print(is_enabled)
                except:
                    is_enabled = False

                if rate:
                    employee_details.append(
                        {"Name": name, "Rate": rate, "Duration": duration, "Qualified": 'Yes'})

            except Exception as e:
                print(f"Error extracting data for a row: {e}")
                continue

        return employee_details

    except Exception as e:
        print(f"Error retrieving employee details: {e}")
        return []


def click_online_tab():
    try:
        online_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "online-tab"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", online_tab)
        online_tab.click()
        print("Successfully clicked the 'Online & App' tab.")
    except Exception as e:
        print(f"Error clicking the 'Online & App' tab: {e}")


def is_service_available_online():
    try:
        # Wait for the toggle button to be present
        toggle_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "branch-service-available-online"))
        )

        is_enabled = toggle_button.get_attribute(
            "aria-checked") is not None

        print(f"Service available online: {is_enabled}")
        return is_enabled

    except Exception as e:
        print(f"Error checking online availability: {e}")
        return "Unknown"


def get_service_description():
    try:
        description_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea[name='internet-description']"))
        )

        service_description = str(
            description_box.get_attribute("value")).strip()

        print(f"Service Description: {service_description}")
        return service_description

    except Exception as e:
        print(f"Error retrieving service description: {e}")
        return None


def click_facilities_tab():
    try:
        facilities_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "facilities-tab"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", facilities_tab)
        facilities_tab.click()
        print("Successfully clicked the 'Facilities' tab.")
    except Exception as e:
        print(f"Error clicking the 'Facilities' tab: {e}")


def get_enabled_facilities():
    try:
        enabled_facilities = []
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//table[contains(@class, "_table_16dtgq")]')))
        rows = driver.find_elements(
            By.XPATH, '//table[contains(@class, "_table_16dtgq")]//tbody/tr[not(contains(@class, "lt-is-loading"))]')
        print(f"Found {len(rows)} facilities.")
        for row in rows:
            try:
                name_element = row.find_element(By.XPATH, './/td[1]')
                facility_name = name_element.text.strip() if name_element else "N/A"
                try:
                    toggle_button = row.find_element(
                        By.XPATH, './/td[3]//div[contains(@class, "toggle-btn")]')
                    is_enabled = toggle_button.get_attribute(
                        "aria-checked") is not None
                except:
                    is_enabled = False

                if is_enabled:
                    enabled_facilities.append(facility_name)

            except Exception as e:
                print(f"Error extracting data for a row: {e}")
                continue

        print(f"Enabled Facilities: {enabled_facilities}")
        return enabled_facilities

    except Exception as e:
        print(f"Error retrieving enabled facilities: {e}")
        return []


def click_rooms_tab():
    try:
        rooms_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "rooms-tab"))
        )
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", rooms_tab)
        rooms_tab.click()
        print("Successfully clicked the 'Rooms' tab.")
    except Exception as e:
        print(f"Error clicking the 'Rooms' tab: {e}")


def get_enabled_rooms():
    try:
        enabled_rooms = []
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//table[contains(@class, "_table_16dtgq")]')))
        rows = driver.find_elements(
            By.XPATH, '//table[contains(@class, "_table_16dtgq")]//tbody/tr[not(contains(@class, "lt-is-loading"))]')

        print(f"Found {len(rows)} rooms.")

        for row in rows:
            try:
                name_element = row.find_element(By.XPATH, './/td[1]')
                facility_name = name_element.text.strip() if name_element else "N/A"
                try:
                    toggle_button = row.find_element(
                        By.XPATH, './/td[3]//div[contains(@class, "toggle-btn")]')
                    is_enabled = toggle_button.get_attribute(
                        "aria-checked") is not None
                except:
                    is_enabled = False

                if is_enabled:
                    enabled_rooms.append(facility_name)

            except Exception as e:
                print(f"Error extracting data for a row: {e}")
                continue

        print(f"Enabled Rooms: {enabled_rooms}")
        return enabled_rooms

    except Exception as e:
        print(f"Error retrieving enabled rooms: {e}")
        return []


def click_back_button(driver):
    """Clicks the 'Back' button on the webpage."""
    try:
        wait = WebDriverWait(driver, 10)
        back_button = wait.until(EC.element_to_be_clickable((By.ID, "back")))
        back_button.click()
        return True
    except Exception as e:
        print(f"Error clicking back button: {e}")
        return False


def get_category_name():
    span_text = ""
    try:
        span_element = driver.find_element(
            By.XPATH, "//div[@name='service-category']//span[@class='_option_st4q28']")
        span_text = span_element.text
        print("Category name: ", span_text)
    except Exception as e:
        print(f"Error getting category: {e}")

    return span_text


def scroll_to_load_all_rows(driver):
    """Scrolls to load all rows dynamically."""
    max_attempts = 15
    previous_count = 0

    for _ in range(max_attempts):
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lt-body")))
        rows = table_body.find_elements(By.CSS_SELECTOR, "tr.lt-row")

        if len(rows) > previous_count:
            previous_count = len(rows)
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'end'});", rows[-1])
            time.sleep(2)
        else:
            break

    return previous_count


login()
click_manager_link("main-nav-manager-link")
click_manager_link("services")
time.sleep(20)
wait = WebDriverWait(driver, 10)

iframe = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "iframe[src*='https://app.phorest.com']")))
driver.switch_to.frame(iframe)

total_rows = scroll_to_load_all_rows(driver)
time.sleep(2)

table_body_to_find_length = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "lt-body")))

rows_len = table_body_to_find_length.find_elements(
    By.CSS_SELECTOR, "tr.lt-row")
print("Row length: ", len(rows_len))
print("Total rows: ", total_rows)

start_from_row = 208

for i in range(total_rows):
    try:
        table_body = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "lt-body")))
        rows = table_body.find_elements(By.CSS_SELECTOR, "tr.lt-row")
        link = rows[i].find_element(By.CSS_SELECTOR, "a")
        print(len(rows))

        if i < start_from_row:
            print(f"Skipping row {i+1}")
            i += 1
            continue

        link = rows[i].find_element(By.CSS_SELECTOR, "a")

        ActionChains(driver).move_to_element(link).perform()
        link.click()
        name = get_input_value("service-name", "value")
        category = get_category_name()
        service_price = get_input_value("service-price", "value")
        service_duration = get_input_value("service-duration", "value")
        development_time = get_input_value("service-gap-time", "value")
        time.sleep(1)

        click_online_tab()
        time.sleep(1)
        online = is_service_available_online()
        description = get_service_description()

        click_facilities_tab()
        time.sleep(1)
        enabled_facilities = get_enabled_facilities()

        click_rooms_tab()
        time.sleep(1)
        enabled_rooms = get_enabled_rooms()

        click_staff_tab()
        time.sleep(1)
        employees = get_employee_details()

        click_general_tab()
        print(f"### Data:  {
              name}, {category}, {service_price}, {service_duration}, {
              development_time}, {online}, {description}, {
              enabled_facilities}, {enabled_rooms}, {employees}"
              )

        out_csv_file_writer.writerow([
            name, category, service_price, service_duration,
            development_time, online, description, enabled_facilities,
            enabled_rooms, employees
        ])
        print("Back button clicked\n\n")
        time.sleep(1)
        click_back_button(driver)

        time.sleep(2)

        total_rows = scroll_to_load_all_rows(
            driver)

        time.sleep(2)
    except Exception as e:
        print(f"Error processing row {i+1}: {e}")
