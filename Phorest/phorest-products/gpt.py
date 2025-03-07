from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)  # Set default wait time

def login():
    """Log in to the application."""
    driver.get("https://barespace.app/login/")
    wait.until(EC.presence_of_element_located((By.ID, "email"))).send_keys("setup+dollhousehair&beauty@barespace.io")
    driver.find_element(By.ID, "password").send_keys("dollhousehair&beauty123")
    driver.find_element(By.XPATH, "//button[contains(@class, 'btn-next') and text()='Login']").click()

def select_dropdown_option(option_text):
    """Select an option from a dropdown."""
    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".multiselect__tags")))
        ActionChains(driver).move_to_element(dropdown).click().perform()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'multiselect__content')]//span[text()='{option_text}']")))
        ActionChains(driver).move_to_element(option).click().perform()
    except Exception as e:
        print(f"Error selecting dropdown option: {e}")

def process_product(row):
    """Process each product and add it to the system."""
    try:
        print(f"Processing: {row['Name']}")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Add Product']]"))).click()

        # Fill product details
        wait.until(EC.element_to_be_clickable((By.NAME, "product_name"))).send_keys(row["Name"].title())
        driver.find_element(By.NAME, "price").send_keys(row["SalePrice"])
        
        if row["CostPrice"]:
            driver.find_element(By.NAME, "cost_price").send_keys(row["CostPrice"])

        select_dropdown_option(row["Category"].title() if row["Category"] else 'Uncategorized')
        if row["Brand"]:
            select_dropdown_option(row["Brand"].title())

        # Location
        select_dropdown_option("Dollhouse Hair & Beauty")

        # Barcode
        if row["Barcode"]:
            driver.find_element(By.NAME, "barcode").send_keys(row["Barcode"])

        # Usage dropdown
        usage_dropdown = Select(driver.find_element(By.ID, "usage"))
        usage_dropdown.select_by_value("retail" if row["SalePrice"] != '0.00' else "professional")

        # Save product
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.flex-1.order-1.lg\\:order-2").click()
        print(f"Product {row['Name']} added successfully.")
    except Exception as e:
        print(f"Error processing product {row['Name']}: {e}")

try:
    login()
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/system-definitions')]"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/products')]//div[text()='Products']"))).click()

    # Read products from CSV
    file_path = 'product_info.csv'
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            process_product(row)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
