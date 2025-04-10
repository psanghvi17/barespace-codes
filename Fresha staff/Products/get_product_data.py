from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium import webdriver
import csv
import time

# service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()

out_csv_file_path = 'product_list.csv'
out_csv_file = open(out_csv_file_path, mode='a', newline='', encoding='utf-8')
out_csv_file_writer = csv.writer(out_csv_file)
out_csv_file_writer.writerow(
    ["Product Name", "Barcode", "Brand", "Category", "Supplier", "RetailPrice", "SupplyPrice"])


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


def click_products_link():
    try:
        products_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'a[data-qa="navtabs-item-products"]'))
        )
        products_link.click()
    except Exception as e:
        print(f"Error clicking products link: {e}")


def remove_banner():
    # Locate the element using XPath
    remind_me_later = driver.find_element(
        By.XPATH, "//span[text()='Remind me later']")

    if remind_me_later:
        remind_me_later.click()

    time.sleep(2)


def accept_cookie():
    # Wait for the button to be clickable
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bXwggy")))

    # Click the button
    accept_button.click()


def get_no_stock():

    # Find the span element and get its text
    span_element = driver.find_element(By.XPATH, "//span[@data-qa='in-stock']")
    inner_content = span_element.text

    # Print the extracted text
    return inner_content


def get_data(qa):
    try:
        span_element = driver.find_element(
            By.XPATH, f"//span[@data-qa='{qa}']")
        inner_content = span_element.text
        return inner_content
    except Exception as e:
        print(f"❌ Error getting product name: {e}")


def get_bar_code():
    span_element = driver.find_element(By.XPATH, "//span[@data-qa='barcode']")
    inner_content = span_element.text
    # Print the extracted text
    return inner_content


def get_product_name():
    try:
        offcanvas = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div[data-qa="drawer-header-title"]')))
        product_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//p[@data-qa="drawer-header-title"]')))
        inner_content = product_title.text
        return inner_content
    except Exception as e:
        print(f"❌ Error getting product name: {e}")


def get_product_name2():
    try:
        product_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//p[@data-qa="drawer-header-title"]')))
        product_name = product_title.text
        print(f"✅ Product Name Found: {product_name}")
        driver.switch_to.default_content()
        return product_name
    except Exception as e:
        print(f"❌ Error getting product name: {e}")
        # Ensure switching back even if there's an error
        driver.switch_to.default_content()
        return None


def click_each_product():
    print('click_each_product')
    try:
        time.sleep(50)
        products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'tr[data-qa^="inventory-list-item"]')))
        print(len(products), ' Products Found')
        for product in products:
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(product)).click()
                retail_price = get_retail_price()
                bar_code = get_bar_code()
                product_name = get_product_name()
                print(f"{retail_price}, {bar_code}, {product_name}")
                close_button = driver.find_element(
                    By.XPATH, "//span[@id='label-close-button']")
                close_button.click()

            except Exception as e:
                print(f"Error clicking product: {product.text}, Error: {e}")

    except Exception as e:
        print(f"Error finding products: {e}")


def get_inventory_rows():
    print("get_inventory_rows")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Give time for elements to load
    print("JS exce")

    inventory_rows = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//tr[starts-with(@data-qa, "inventory-list-item-")]')))

    print(f"Found {len(inventory_rows)} inventory rows.")
    driver.switch_to.default_content()
    return inventory_rows


def close_offcanvas():
    try:
        close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-qa="close-button"]')))
        close_button.click()
        print("🔒 Offcanvas closed")
    except Exception as e:
        print(f"Error closing offcanvas: {e}")


def click_anywhere_in_row(row):
    try:
        # Click anywhere in the row instead of the product name
        WebDriverWait(row, 5).until(
            EC.element_to_be_clickable((By.XPATH, '.'))
        ).click()

        print(f"✅ Clicked anywhere in row: {row.get_attribute('data-qa')}")

    except Exception as e:
        print(f"❌ Error clicking row {row.get_attribute('data-qa')}: {e}")


def get_product_name_js():
    try:
        # JavaScript to extract text content from the element
        product_name = driver.execute_script(
            'return document.querySelector("p[data-qa=\'drawer-header-title\']").textContent;'
        )

        print(f"✅ Product Name Found (JS): {product_name.strip()}")
        return product_name.strip()

    except Exception as e:
        print(f"❌ Error getting product name via JS: {e}")
        return None


def click_next_page():
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@data-qa="next-page"]')))
    next_button.click()
    print("✅ Clicked 'Next Page' button.")


try:
    login()
    time.sleep(10)
    # remove_banner()
    click_catalogue_link()
    click_products_link()
    accept_cookie()
    while 1:
        rows = get_inventory_rows()
        for row in rows:
            click_anywhere_in_row(row)
            time.sleep(10)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe")))

            iframe = driver.find_element(By.TAG_NAME, "iframe")
            product_name = get_product_name_js()
            print("product_name : ", product_name)
            driver.switch_to.default_content()
            barcode = get_data('barcode')
            print("barcode :", barcode)
            brand = get_data('brand')
            print("brand :", brand)
            category = get_data('category')
            print("category :", category)
            supplier = get_data('supplier')
            print("supplier :", supplier)
            retail = get_data('retail-price')
            print("retail :", retail)
            supply = get_data('supply-price')
            print("supply :", supply)
            out_csv_file_writer.writerow(
                [product_name, barcode, brand, category, supplier, retail, supply])
            close_offcanvas()
        click_next_page()
        time.sleep(2)


except Exception as e:
    print(e)
