from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
import json
import time

out_json_file_path = 'blocked_hours.json'

service = Service()
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
driver.maximize_window()


def login():
    driver.get("https://partners.fresha.com/")
    time.sleep(4)
    email_field = driver.find_element(By.NAME, 'email')
    email = ""
    email_field.send_keys(email)
    email_field.send_keys(Keys.RETURN)
    time.sleep(2)
    password_field = driver.find_element(By.NAME, "password")
    password = ""
    password_field.send_keys(password)
    time.sleep(1)
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)
    password_field.send_keys(Keys.RETURN)


def click_calendar_link():
    try:
        catalogue_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[data-qa="nav-d-calendar"]'))
        )
        catalogue_link.click()
    except Exception as e:
        print(f"Error clicking calendar link: {e}")


def remove_banner():
    # Locate the element using XPath
    remind_me_later = driver.find_element(
        By.XPATH, "//span[text()='Remind me later']")

    if remind_me_later:
        remind_me_later.click()

    time.sleep(2)


def accept_cookie():
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bXwggy")))

    accept_button.click()


def get_data(qa):
    try:
        span_element = driver.find_element(
            By.XPATH, f"//span[@data-qa='{qa}']")
        inner_content = span_element.text
        return inner_content
    except Exception as e:
        print(f"❌ Error getting product name: {e}")


def close_offcanvas():
    try:
        close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-qa="close-button"]')))
        close_button.click()
        print("🔒 Offcanvas closed")
    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def get_current_date():
    try:

        buttons = driver.find_elements(
            By.CSS_SELECTOR, "button.bXwggy._Xdiwu.util-focusRing-overrides._0HR1xu.AmWvcn.uSvrkn.JKAJxn.I-85qn.a5L3kq")

        print("Date: ", buttons[1].text)

        return buttons[1].text.strip()

    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def get_to_next_page():
    try:

        buttons = driver.find_elements(
            By.CSS_SELECTOR, "button.bXwggy._Xdiwu.util-focusRing-overrides._0HR1xu.AmWvcn.xR_RUn.uSvrkn.JKAJxn.I-85qn.a5L3kq")

        buttons[1].click()

    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def get_user_name():
    try:
        calendar_timeline_headelrs = driver.find_elements(
            By.CSS_SELECTOR,
            'div[data-qa="calendar-timeline-header"]'
        )

        print("User name: ", calendar_timeline_headelrs[1].text)

        return calendar_timeline_headelrs[1].text.strip()
    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def get_all_blocked_hrs2():
    try:

        blocked_hrs = []

        xpath = "//*[contains(@class, 'eventsWrapperDiv')]"

        elements = driver.find_elements(By.XPATH, xpath)

        print("Events wrapper divs: ", len(elements))

        main_div = elements[1].find_elements(
            By.XPATH, "//div[contains(@id, 'calendar-event-blocked-time')]"
        )

        print("Blocked hrs list: ", len(main_div))

        for div in main_div:

            time_element = div.find_element(
                By.CSS_SELECTOR, ".time-enZrtm"
            )
            title_element = div.find_element(
                By.CSS_SELECTOR, ".title-P0TT6G")

            event_time = time_element.text.strip() if time_element else "N/A"
            event_title = title_element.text.strip() if title_element else "N/A"

            print(f"Event Time: {event_time}")
            print(f"Appointment Title: {event_title}")
            print("-" * 50)

            blocked_hrs.append([event_time, event_title])

        return blocked_hrs
    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def get_all_blocked_hrs3():
    try:

        blocked_hrs = {}

        xpath = "//*[contains(@class, 'eventsWrapperDiv')]"

        elements = driver.find_elements(By.XPATH, xpath)

        print("Events wrapper divs: ", len(elements))

        main_div = elements[1].find_elements(
            By.XPATH, "//div[contains(@id, 'calendar-event-blocked-time')]"
        )

        print("Blocked hrs list: ", len(main_div))

        for div in main_div:

            time_element = div.find_element(
                By.CSS_SELECTOR, ".time-enZrtm"
            )
            title_element = div.find_element(
                By.CSS_SELECTOR, ".title-P0TT6G")

            event_time = time_element.text.strip() if time_element else "N/A"
            event_title = title_element.text.strip() if title_element else "N/A"

            print(f"Event Time: {event_time}")
            print(f"Appointment Title: {event_title}")
            print("-" * 50)

            blocked_hrs[event_time] = event_title

        return blocked_hrs
    except Exception as e:
        print(f"Error closing offcanvas: {e}")


try:
    login()
    print("Logged in successfully...\n")
    time.sleep(5)
    # remove_banner()

    click_calendar_link()
    print("Clicked on calendar link...")
    time.sleep(2)
    accept_cookie()

    while 1:
        on_date = get_current_date()
        time.sleep(1)
        user_name = get_user_name()
        time.sleep(1)
        blocked_hrs = get_all_blocked_hrs3()
        time.sleep(1)

        tmp = {
            on_date: {
                user_name: blocked_hrs
            }
        }

        print("\nBlocked hrs: ", blocked_hrs)

        with open(out_json_file_path, 'r') as file:
            data = json.load(file)

        data.update(tmp)

        with open(out_json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        get_to_next_page()
        print("Clicked on next page button...\n")
        time.sleep(2)

except Exception as e:
    print(e)
