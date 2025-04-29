import os
import time
# import pwinput  # For masked password input
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import json
import glob

def delete_latest_files(download_dir, num_files=2):
    list_of_files = glob.glob(os.path.join(download_dir, '*'))
    if list_of_files:
        latest_files = sorted(list_of_files, key=os.path.getctime, reverse=True)[:num_files]
        for file in latest_files:
            try:
                os.remove(file)
                print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file: {file}, {e}")


def downloading(folder_path):
    """Check if the folder contains any downloading temporary files."""
    temp_extensions = ['.crdownload', '.part', '.tmp']
    for file_name in os.listdir(folder_path):
        if any(file_name.endswith(ext) for ext in temp_extensions):
            return True
    return False


login = json.load(open('login.json'))
# ✅ Prompt user for login credentials
email = login['email']
password = login['password']  # Shows **** while typing
download_dir = input("Enter the         `directory to save downloads (default: downloads/test): ") or "downloads/test"
download_number = int(input("Enter the number of files to download (default: 5): ") or "5")

# Ensure the directory exists
os.makedirs(download_dir, exist_ok=True)

# ✅ Setup Firefox WebDriver with download directory
firefox_options = Options()
firefox_options.set_preference("browser.download.folderList", 2)  # Use custom directory
firefox_options.set_preference("browser.download.dir", os.path.abspath(download_dir))
firefox_options.set_preference("browser.download.useDownloadDir", True)

firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                               "application/pdf, application/octet-stream, application/vnd.ms-excel, text/csv")  
firefox_options.set_preference("pdfjs.disabled", True)  # Disable built-in PDF viewer

# ✅ Launch Firefox
driver = webdriver.Firefox(options=firefox_options)

# ✅ Open login page
driver.get("https://access.ambrahealth.com/")

# ✅ Find and fill login fields
email_field = driver.find_element(By.NAME, 'login')
password_field = driver.find_element(By.ID, 'password')
submit_button = driver.find_element(By.ID, "submit")

email_field.send_keys(email)
password_field.send_keys(password)
submit_button.click()

# ✅ Wait for login to complete
time.sleep(30)  # Adjust timing if needed


timeout = 500  # Set your timeout duration in seconds
current_download = 0
page_max = 100
while current_download < download_number:

    checkboxes = driver.find_elements(By.TAG_NAME, "tbody")
    for cb in checkboxes:
        
        download_button = cb.find_elements(By.TAG_NAME, "button")
        if len(download_button) > 1:  # Ensure there is a second button
            print("Downloading file...--->",current_download + 1, 'of', download_number)
            download_button[1].click()
            start_time = time.time()
            time.sleep(15)
            while downloading(download_dir):
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    print(f"Download timed out after {timeout} seconds.")
                    delete_latest_files(download_dir)
                    break
                print('Waiting for download to complete...--->', current_download + 1, 'of', download_number)
                time.sleep(2)
            current_download += 1
            if current_download >= download_number:
                print('Downloaded all files requested.')
                driver.quit()
                exit()
    if current_download % page_max == 0:
        nav = driver.find_elements(By.CLASS_NAME, 'pagination-controls')
        next_page = nav[0].find_elements(By.TAG_NAME, 'span')
        next_page[-1].click()
        time.sleep(5)




driver.quit()
