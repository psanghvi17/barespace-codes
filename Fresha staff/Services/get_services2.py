import time
import json
import ast
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

wait = WebDriverWait(driver, 10)

out_csv_file_path = 'product_list.csv'
out_csv_file = open(out_csv_file_path, mode='a', newline='', encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(
    ["Service Name", "Barcode", "Brand", "Category", "Supplier", "RetailPrice", "SupplyPrice"])


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


def click_catalogue_link():
    try:
        catalogue_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[data-qa="nav-d-catalog"]'))
        )
        catalogue_link.click()
    except Exception as e:
        print(f"Error clicking catalogue link: {e}")


def click_services_link():
    try:
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[data-qa="navtabs-item-service-menu"]'))
        )
        products_link.click()
    except Exception as e:
        print(f"Error clicking products link: {e}")


def click_on_filter():
    try:
        filters_button = driver.find_element(
            By.XPATH, "//button[normalize-space(text())='Filters']")
        filters_button.click()
    except Exception as e:
        print(f"Error clicking products link: {e}")


def get_data(qa):
    try:
        span_element = driver.find_element(
            By.XPATH, f"//span[@data-qa='{qa}']")
        inner_content = span_element.text
        return inner_content
    except Exception as e:
        print(f"❌ Error getting product name: {e}")


def accept_cookie():
    # Wait for the button to be clickable
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bXwggy")))

    # Click the button
    accept_button.click()


def click_on_item(element):
    try:
        ActionChains(driver).move_to_element(element).perform()
        element.click()
        # time.sleep(2)
    except Exception as e:
        print(f"An error occurred while clicking on element: {e}")


def click_close_button():
    close_button = driver.find_element(
        By.XPATH, '//button[@data-qa="close-modal-close-service-form"]')
    ActionChains(driver).move_to_element(close_button).perform()
    close_button.click()
    print("Cilcked on close button......\n")


def get_service_name():

    service_name = ""
    try:
        service_name = driver.find_element(
            By.CSS_SELECTOR, 'input[name="name"]').get_attribute('value')
    except Exception as e:
        print("Get name error: ", e)
    return service_name


def get_service_type():
    service_type = ""
    try:
        service_type_element = driver.find_element(
            By.XPATH, '//input[@data-qa="input-input-structure-service-type"]')
        service_type = service_type_element.get_attribute('value')
    except Exception as e:
        print("Get service type error: ", e)
    return service_type


def get_category():
    menu_category = ""
    try:
        menu_category_element = driver.find_element(
            By.XPATH, '//div[@data-qa="select-structure-value-menu-category"]/span')
        menu_category = menu_category_element.text
    except Exception as e:
        print("Get category error: ", e)
    return menu_category


def get_description():
    description = ""
    try:
        description_element = driver.find_element(
            By.XPATH, "//div[@data-qa='input-structure-description']/textarea")
        description = description_element.get_attribute('value')

    except Exception as e:
        print("Get description error: ", e)
    return description


def get_price():
    price = ""
    try:
        price = driver.find_element(
            By.CSS_SELECTOR, 'input[name="servicePricingLevels[0].price"]').get_attribute('value')
    except Exception as e:
        print("Get description error: ", e)
    return price


def get_price_type():
    price_type = ""
    try:
        # Extract 'Price type'
        price_type_element = driver.find_element(
            By.XPATH, "//div[@data-qa='select-structure-priceType']/div/span")
        price_type = price_type_element.text
    except Exception as e:
        print("Get price type error: ", e)
    return price_type


def get_duration():
    duration = ""
    try:
        duration_element = driver.find_element(
            By.XPATH, "//div[@data-qa='select-structure-duration']/div/span")
        duration = duration_element.text
    except Exception as e:
        print("Get price type error: ", e)
    return duration


def click_on_team_members():
    try:
        team_members_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@aria-labelledby="Team members"]')))
        team_members_button.click()
        print("Cilcked on team memebers button...")
    except Exception as e:
        print("Cilcked on team memebers button error: ", e)


def get_selected_team_member():
    try:
        team_member_divs = driver.find_elements(
            By.CSS_SELECTOR, "div[data-qa^='select-service']")
        for div in team_member_divs:
            checkbox = div.find_element(
                By.CSS_SELECTOR, "input[type='checkbox']")
            if checkbox.get_attribute("checked"):
                return checkbox.get_attribute("aria-label")
        return None  # No team member is selected
    except WebDriverException as e:
        print(f"Error locating selected team member: {e}")
        return None


def click_online():
    online_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@data-qa='online-booking']")))
    online_button.click()


def check_online():
    checkbox = driver.find_element(By.ID, "input-onlineBookingEnabled")
    return checkbox.get_attribute("aria-checked") == "true"


try:
    time.sleep(2)
    login()
    time.sleep(1)
    click_catalogue_link()
    time.sleep(2)
    accept_cookie()
    time.sleep(1)
    click_services_link()

    divs = driver.find_elements(
        By.XPATH, "//div[@data-qa='services-list-category-header']")

    for div in divs:
        # print(div)
        elements = div.find_elements(
            By.XPATH, "//div[contains(@data-qa, 'service-list-item-')]")

        for element in elements:
            print(element.get_attribute("data-qa"))
            click_on_item(element)
            time.sleep(2)

            service_name = driver.find_element(
                By.CSS_SELECTOR, 'input[name="name"]').get_attribute('value')
            print(f"Service Name: {service_name}")

            name = get_service_name()
            price = get_price()
            description = get_description()
            price_type = get_price_type()
            duration = get_duration()

            service_type = get_service_type()
            menu_category = get_category()

            time.sleep(1)
            click_on_team_members()
            time.sleep(1)
            get_team_members = get_selected_team_member()

            click_online()
            time.sleep(1)
            data = check_online()

            print(f"{name}, {service_type}, {price}, {
                  menu_category}, {description}, {
                  price_type}, {duration}, {get_team_members}, {data}\n")

            click_close_button()
            time.sleep(2)

    time.sleep(10)
except Exception as e:
    print("Error: ", e)
finally:
    driver.quit()  # Ensure the browser closes
    print()
