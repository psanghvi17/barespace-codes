import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

csv_file_path = "clients_info.csv"
csv_file = open(csv_file_path, mode="a", newline="", encoding="utf-8")
csv_file_writer = csv.writer(csv_file)
csv_file_writer.writerow(
    [
        "index",
        "firstName",
        "lastName",
        "phone",
        "email",
        "address_line_1",
        "address_line_2",
        "town",
        "region",
        "postcode",
        "notes",
    ]
)


def login():
    driver.get("https://my.phorest.com")
    time.sleep(5)
    username_field = driver.find_element(By.NAME, "email")
    username_field.send_keys("aoifebsp+bombshell@gmail.com")
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("Password1")
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)


def click_link_by_id(id):
    print("Clicking using id " + id)
    manager_link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, id))
    )
    manager_link.click()


def get_all_rows(driver):
    try:
        rows = driver.find_elements(
            By.XPATH, "//td[@data-column-name='First Name']//a")
        print("Found " + str(len(rows)) + " Rows")
        return rows
    except Exception as e:
        print(f"Error finding brand elements: {e}")
        return []


def click_back_button():
    try:
        retries = 3  # Number of retries for stale element
        for attempt in range(retries):
            try:
                back_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@aria-label="Back"]')
                    )
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", back_button
                )
                back_button.click()
                print("Back button clicked successfully.")
                return
            except StaleElementReferenceException:
                print(
                    f"Stale element exception on attempt {
                        attempt + 1}. Retrying..."
                )
                continue  # Retry locating the element
        print("Failed to click the back button after retries.")
    except Exception as e:
        print(f"Error clicking the back button: {e}")


def click_next_page_button(driver):
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "next-page"))
        )
        print(f"Button Found: {next_page_button.get_attribute('outerHTML')}")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", next_page_button
        )
        driver.execute_script("arguments[0].click();", next_page_button)
        print("Next page button clicked successfully using JavaScript.")
        return 0
    except Exception as e:
        print(f"Error clicking the next page button: {e}")


def get_value(field, driver):
    print("field: ", field)
    input_field = driver.find_element(
        By.XPATH, f"//input[starts-with(@name, '{field}')]"
    )

    print(input_field.get_attribute("value"))
    return input_field.get_attribute("value")


def get_notes(field, driver):
    print("field", field)
    textarea = driver.find_element(By.ID, "notes")
    textarea_value = textarea.get_attribute("value")
    return textarea_value


def safe_click(element, driver):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)  # Give time for any overlay to disappear
    driver.execute_script("arguments[0].click();", element)


while True:

    # service = Service()
    service = Service(ChromeDriverManager().install())

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Prevents memory overflow
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    login()
    click_link_by_id("main-nav-clients-link")
    time.sleep(5)
    x = 0
    z = 0
    skip = 0  # skip the row number
    try:
        while True:
            rows = get_all_rows(driver)

            for i in range(len(rows)):
                if z < skip:
                    z += 1
                    print(f"Skiping........{z}")
                    continue
                time.sleep(3)
                rows = get_all_rows(driver)
                time.sleep(2)
                row = rows[i]
                safe_click(row, driver)
                time.sleep(3)
                firstName = get_value("first-name-", driver)
                lastName = get_value("last-name-", driver)
                phone = get_value("phone-number-", driver)
                email = get_value("email-", driver)
                address_line_1 = get_value("address-line-1-", driver)
                address_line_2 = get_value("address-line-2-", driver)
                town = get_value("town-city-", driver)
                region = get_value("region-", driver)
                postcode = get_value("postcode-", driver)
                notes = get_notes("notes", driver)
                reader = [
                    [
                        str(z + 1),
                        firstName,
                        lastName,
                        phone,
                        email,
                        address_line_1,
                        address_line_2,
                        town,
                        region,
                        postcode,
                        notes,
                    ]
                ]
                cleaned_data = [[element.strip() for element in row]
                                for row in reader]
                result = ",".join(str(item) for item in cleaned_data)
                converted_list = eval(result)
                csv_file_writer.writerow(converted_list)

                print(
                    str(z + 1),
                    firstName,
                    lastName,
                    phone,
                    email,
                    address_line_1,
                    address_line_2,
                    town,
                    region,
                    postcode,
                    notes,
                )
                click_back_button()
                z += 1
                time.sleep(2)
                print("\n\n")
            x = click_next_page_button(driver)

    except Exception as e:
        print(f"Exception occured: {e}")
        print("Restarting driver!!")
        driver.quit()
