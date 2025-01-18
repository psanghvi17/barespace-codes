from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time 


service = Service(executable_path='chromedriver/chromedriver/chromedriver.exe')
chrome_profile_path = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"

chrome_options = Options()

# chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
# chrome_options.add_argument("--profile-directory=Profile 1") 
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.headless = False
# chrome_options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=service,options=chrome_options)
# Open Gmail
driver.get("https://www.zurichlife.ie/bgsi/log_on/login.jsp")

# Wait for the user to log in manually
print("Please log in to your Gmail account...")

# Waiting for the Gmail inbox page to load
# This is a generic waiting, can be adjusted according to your network speed
try:
    WebDriverWait(driver, 600).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.T-I.T-I-KE.L3"))
    )
    print("Login successful!")
except Exception as e:
    print("Timed out waiting for login. Exiting...")
    driver.quit()
    exit()

# Click on the 'Compose' button to create a new email
try:
    compose_button = driver.find_element(By.CSS_SELECTOR, "div.T-I.T-I-KE.L3")
    compose_button.click()
    print("Compose button clicked!")
except Exception as e:
    print(f"Error: {e}")
    driver.quit()

# Optional: Keep the browser open for a while
time.sleep(10)

# Close the browser
driver.quit()
