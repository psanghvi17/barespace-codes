from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import json
import re
import ast
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)


file_path = './staff_and_break.json'


def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = ""
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password")
    password = ""
    password_field.send_keys(password)
    login_button = driver.find_element(
        By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']")
    time.sleep(2)
    login_button.click()


def click_anywhere_inside_table():
    try:
        div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-timegrid-cols"))
        )

        time.sleep(3)

        table = div.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_element(By.TAG_NAME, "tr")
        tds = rows.find_elements(By.TAG_NAME, "td")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(tds[0])
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", tds[0])
        ActionChains(driver).move_to_element(tds[0]).click().perform()

        time.sleep(3)

    except Exception as e:
        print("Exception on click anywhere inside table: ", e)
        time.sleep(5)


def toggle_blocked_time_button():
    try:
        button = driver.find_element(
            By.XPATH, "//button[contains(@id, 'headlessui-switch-')]")

        button.click()

    except Exception as e:

        print("Exception on toggle blocked button: ", e)
        time.sleep(5)


def select_dropdown_option(driver, option_text):
    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, ".multiselect__tags"
            ))
        )
        try:
            dropdown.click()

        except Exception as e:
            driver.execute_script("arguments[0].click();", dropdown)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".multiselect__content")))

        try:
            option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text))
                ))
            option.click()

        except Exception as e:
            option = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[contains(@class, 'multiselect__content')]//span[contains(text(), '{}')]".format(option_text))
                ))
            driver.execute_script("arguments[0].click();", option)
    except Exception as e:
        print(f"Error selecting dropdown option: {e}")


def format_date(date_raw):
    date_raw = "Friday 18 April 2025"
    words = date_raw.split()
    month_number = datetime.strptime(words[2], "%B").month

    date = words[1]
    date += "/" + str(month_number)
    date += "/" + words[3]

    return date


def set_date(date):
    try:
        input_field = driver.find_element(
            By.CSS_SELECTOR,
            'div.form-item.relative input.input')

        time.sleep(1)
        input_field.send_keys(date.strip())
        time.sleep(2)

    except Exception as e:
        print(f"Error occurred during setting date: {e}")


def set_date2(input_date):
    input_date = "2025-04-07"
    try:
        input_field = driver.find_element(
            By.CSS_SELECTOR,
            'div.form-item.relative input.input')

        input_field.click()

        vc_title_span = driver.find_element(By.CSS_SELECTOR, '.vc-title span')
        button_text = vc_title_span.text.strip()

        print(f"\nButton text: {button_text}")

        if button_text != input_date:
            next_button = driver.find_element(
                By.CSS_SELECTOR, '.vc-arrow.vc-next.vc-focus')
            next_button.click()
            print("Clicked next button to navigate to the next date.")
        else:
            print("The date inside the button matches the input date.")
        time.sleep(3)
    except Exception as e:
        print(f"Error occurred during setting date: {e}")


def convert_to_24hr_format(time_str):
    time_obj = ""
    try:
        time_obj = datetime.strptime(time_str, '%I %p')
    except Exception as e:
        print(f"Error converting time format: {e}")
        time_obj = datetime.strptime(time_str, '%I:%M %p')

    return time_obj.strftime('%H:%M')


def set_time(staff_time, block):

    try:
        time_in_24h = convert_to_24hr_format(staff_time.strip())
        print(f"Setting time.......: {time_in_24h}")
        parent_div = driver.find_element(By.ID, block)

        time_input = parent_div.find_element(
            By.CSS_SELECTOR, "input[type='time']")

        time_input.send_keys(time_in_24h)

        time.sleep(2)

    except Exception as e:
        print(f"Error occurred: {e}")


def click_submit_button():
    retries = 3
    for attempt in range(retries):
        try:
            print(
                f"Attempt {attempt + 1}: Locating and clicking the button...")
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and text()='Submit']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(button))
            button.click()
            print("Button clicked successfully.")
            break
        except StaleElementReferenceException:
            print("Stale element encountered. Retrying...")
            time.sleep(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    else:
        print("Failed to click the button after retries.")


def extract_digit(number_str):
    number = re.sub(r'(st|nd|rd|th)', '', number_str)
    return int(number)


def go_to_date_format():

    try:
        h4_element = driver.find_element(
            By.XPATH,
            "//h4[contains(@class, 'mx-auto') and contains(@class, 'font-normal')]")

        date_raw = h4_element.text.split(' ')
        # print("H4 elements: ", date_raw)
        bs_date = str(extract_digit(date_raw[1]))
        bs_date += ' ' + date_raw[3]
        bs_date += ' ' + date_raw[4]

        return bs_date
    except Exception as e:
        print(f"Error at go_to_date_format: {e}")


def phorest_date(raw_date):
    words = raw_date.split(' ')
    date = words[1]
    date += ' ' + words[2]
    date += ' ' + words[3]

    return date


def click_cancel_button():
    retries = 3
    for attempt in range(retries):
        try:
            print(
                f"Attempt {attempt + 1}: Locating and clicking the Close button...")
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class, 'btn-danger') and text()='Close']")))
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(button))
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


def format_date_page(date):
    formatted_date = ''
    words = date.split(' ')

    formatted_date += words[1]


def go_to_next_date():
    try:

        driver.execute_script("window.scrollBy(0, -1000);")

        h4_element = driver.find_element(
            By.XPATH,
            "//h4[contains(@class, 'mx-auto') and contains(@class, 'font-normal')]")

        svg_element = h4_element.find_elements(
            By.CSS_SELECTOR, '.btn-round')
        svg_element[1].click()
        print("Clicked on next date button....")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def set_blocked_title(text):
    try:
        input_element = driver.find_element(By.ID, "title")
        input_element.clear()
        input_element.send_keys(text)
    except Exception as e:
        print(f"An unexpected error at blocked title : {e}")


def check_dropdown_value():
    try:
        name_element = driver.find_elements(
            By.CSS_SELECTOR, "span.multiselect__single")

        name_text = name_element[2].text

        # Print the result
        print(name_text)
        return name_text
    except Exception as e:
        print(f"An unexpected error at blocked title : {e}")


login()
time.sleep(1)

with open(file_path, 'r', encoding='utf-8') as file:

    data = json.load(file)

    for document in data:

        print(f"\n\nDate: {document}")

        staffs = data[document].keys()

        time.sleep(2)
        ph_date_raw = format_date(document)
        time.sleep(1)
        bs_date = go_to_date_format()
        ph_date = phorest_date(document)

        while bs_date != ph_date:
            go_to_next_date()
            bs_date = go_to_date_format()
            print(f"\nBS Date: {bs_date}     PHorest date: {ph_date}")
            time.sleep(2)

        for staff in staffs:
            print(f"{staff} :   {data[document][staff]}")

            breaks = data[document][staff]

            if not breaks:
                print("No break found for : ")
                print(f"  {staff}")
                continue

            for staff_break in breaks:
                print(f"Break : {staff_break}")

                try:
                    driver.refresh()
                    print("\nRefreshing calender page.....")
                    time.sleep(2)
                    click_anywhere_inside_table()
                    time.sleep(2)
                    toggle_blocked_time_button()
                    time.sleep(2)

                    name_text = check_dropdown_value()

                    print(f"Comparing => {
                          name_text.strip()} : * {staff.strip()}")
                    if name_text.strip() != staff.strip():
                        select_dropdown_option(driver, staff.strip())
                        time.sleep(2)

                    times = staff_break.split('\n')[1].split('-')

                    time.sleep(1)
                    set_time(times[0], "block-time-undefined")
                    time.sleep(1)
                    set_time(times[1], "block-end-time-undefined")
                    time.sleep(1)

                    set_blocked_title(staff_break.split('\n')[0])

                    # print("Clicking Submit button....")
                    # click_submit_button()

                    print("Clicking Cancel button....")
                    click_cancel_button()
                    time.sleep(3)
                    driver.refresh()
                    print("Refreshing calender page.....\n")
                    time.sleep(1)

                except Exception as e:
                    print("Exception on main: ", e)
                    time.sleep(10)
