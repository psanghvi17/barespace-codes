from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import json
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


start_from_row = 10

out_json_file_path = "staff_and_break_bombshell.json"

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


def get_category_name():
    span_text = ""
    try:
        span_element = driver.find_element(
            By.XPATH,
            "//div[@name='service-category']//span[@class='_option_st4q28']"
        )
        span_text = span_element.text
        print("Category name: ", span_text)
    except Exception as e:
        print(f"Error getting category: {e}")

    return span_text


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


def is_service_available_online():
    try:
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
            By.XPATH,
            '//table[contains(@class, "_table_16dtgq")]//tbody/tr[not(contains(@class, "lt-is-loading"))]')

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


def click_category_button():
    try:
        dropdown_trigger = driver.find_element(
            By.CLASS_NAME, "ember-power-select-trigger"
        )

        dropdown_trigger.click()

    except Exception as e:
        print(f"Unable to cilck on Category button {e}")


def click_on_appointment_today():
    try:
        button = driver.find_element(
            By.NAME, "appointment-calendar-today-button")
        button.click()
        print("Clicked on Today's appointment button....\n")
    except Exception as e:
        print(f"Unable to cilck on Today appointment button {e}")


def click_on_next_day_button():
    try:
        button = driver.find_element(
            By.NAME, "appointment-calendar-next-day-button")
        button.click()
        print("Next day button clicked......\n")
    except Exception as e:
        print(f"Unable to cilck next day button {e}")


def table_data(staff_name):

    total_data = {}

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.fc-scrollgrid.fc-scrollgrid-liquid"))
    )

    table = driver.find_element(
        By.CSS_SELECTOR, "table.fc-scrollgrid.fc-scrollgrid-liquid")

    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fc-timegrid-cols"))
    )

    table = div_element.find_element(By.TAG_NAME, "table")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    tr = tbody.find_element(By.TAG_NAME, "tr")
    td_elements = tr.find_elements(By.TAG_NAME, "td")  # gets inner td

    print("Td elements length: ", len(td_elements))

    i = 0
    for td_element in td_elements:
        staff_breaks = []
        try:
            break_elements = td_element.find_elements(
                By.XPATH,
                ".//div//a[@style='border-color: rgb(49, 49, 49); background-color: rgb(89, 89, 89);']")

            print(f"For staff: {staff_name[i]}   Break elements: {
                  len(break_elements)}")
            for break_element in break_elements:
                print(f"\nBreak data: {break_element.text}")
                staff_breaks.append(break_element.text)

        except Exception as e:
            print(f"\nBreak not found: {div_element.text.strip()}")
            staff_breaks.append('-')

        total_data[staff_name[i]] = staff_breaks
        i += 1

    return total_data


def table_header():

    staffs = []

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "table.fc-scrollgrid.fc-scrollgrid-liquid"))
        )

        table = driver.find_element(
            By.CSS_SELECTOR, "table.fc-scrollgrid.fc-scrollgrid-liquid"
        )

        headers = table.find_elements(
            By.XPATH, "//div[@name='menu-with-icons']")

        for header in headers:
            span = header.find_element(
                By.XPATH, ".//span[@data-resource-name]")
            span_text = span.text.strip()

            staffs.append(span_text)

        return staffs

    except Exception as e:
        print(f"Unable to get staff names {e}")


def get_date():
    try:
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "w-72.whitespace-nowrap"))
        )

        div_text = div_element.text.strip()
        print("Date : ", div_text)

        return div_text
    except Exception as e:
        print(f"Unable to get current date {e}")


login()
time.sleep(2)
click_on_appointment_today()
time.sleep(1)

start_from = 0
index = 0

while True:

    current_date = get_date()
    time.sleep(1)
    staff_name = table_header()
    time.sleep(3)
    staff_break = table_data(staff_name)
    time.sleep(5)

    tmp = {
        current_date: staff_break
    }

    print(tmp)

    data = {}
    with open(out_json_file_path, 'r') as file:
        data = json.load(file)

    print("\n\nExisting data: ", data)
    data.update(tmp)

    with open(out_json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    click_on_next_day_button()
    time.sleep(3)
