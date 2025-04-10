from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
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


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def login():
    driver.get("https://barespace.app/login/")
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email = "setup+obsessedhairsalon@barespace.io"
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password")
    password = "obsessedhairsalon123"
    password_field.send_keys(password)
    login_button = driver.find_element(
        By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']")
    time.sleep(2)
    login_button.click()


try:
    login()
    system_definitions_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]")))
    system_definitions_link.click()

    products_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/products')]//div[text()='Products']")))

    products_link.click()

    while 1:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'desktop-table'))
        )

        rows = driver.find_elements(
            By.XPATH, '//table[@id="desktop-table"]//tbody//tr')

        for row in rows:
            columns = row.find_elements(By.TAG_NAME, 'td')
            for column in columns:
                print(column.text)

            print("\n")

            # delete_button = row.find_element(
            #     By.XPATH, "//button[contains(@class, 'bg-danger') and text()='Delete']")

            delete_button = driver.find_element(
                By.XPATH, "//button[contains(@class, 'bg-danger') and contains(., 'Delete')]")
            delete_button.click()
            time.sleep(1)

            confirm_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'btn-primary') and text()='Confirm']")))
            confirm_button.click()
            time.sleep(1)

        time.sleep(1)
        # wait = WebDriverWait(driver, 10)
        # next_button = wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//button//span[text()='Next']/parent::button")))
        # next_button.click()

        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button//span[text()='Next']/parent::button")))
        print(f"Button Found: {next_page_button.get_attribute('outerHTML')}")
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", next_page_button)
        driver.execute_script("arguments[0].click();", next_page_button)
        print("Next page button clicked successfully using JavaScript.")


except Exception as e:
    print(e)
    time.sleep(10)
finally:
    driver.quit()
