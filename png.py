from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set up the Chrome driver with options
options = webdriver.ChromeOptions()
# Uncomment the line below to run Chrome in headless mode
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("prefs", {
    "download.default_directory": "/path/to/download/directory",  # Change to your desired download directory
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(options=options)

# Navigate to Google Drive
driver.get("https://drive.google.com/drive/folders/13B1n68ef0hbfDMd7lX0I6fUKf86lCeJk")

# Wait for the user to log in manually
print("Please log in to your Google account and press Enter")
input()

# Wait for the page to load completely
time.sleep(10)

# Function to download folder by number
def download_folder(folder_number):
    try:
        # Locate the folder element by its number
        folder_xpath = f"//div[@class='Q5txwe' and text()='{folder_number}']"
        folder_element = driver.find_element(By.XPATH, folder_xpath)
        folder_element.click()

        # Wait for the folder to open
        time.sleep(2)

        # Click on the specific element to bring up the dropdown menu
        menu_icon_xpath = "//path[@d='M0 0h20v20H0V0z']"
        menu_icon_element = driver.find_element(By.XPATH, menu_icon_xpath)
        menu_icon_element.click()

        # Wait for the dropdown menu to appear
        time.sleep(1)

        # Click on the three dots icon in the dropdown menu
        three_dots_xpath = "//svg[contains(@class, 'c-qd a-s-fa-Ha-pa')]"
        three_dots_element = driver.find_element(By.XPATH, three_dots_xpath)
        three_dots_element.click()

        # Wait for the context menu to appear and click the download option
        time.sleep(1)  # Small delay to allow the context menu to appear
        download_xpath = "//div[contains(text(), 'Download')]"
        download_element = driver.find_element(By.XPATH, download_xpath)
        download_element.click()

        # Wait for the download to start
        time.sleep(5)
        print(f"Download started for folder {folder_number}")
    except Exception as e:
        print(f"Could not download folder {folder_number}: {e}")

# Download folders from 183 to 250
for i in range(183, 251):
    download_folder(i)

# Close the driver
driver.quit()
