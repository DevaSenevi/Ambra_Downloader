import os
import time
import pwinput  # For masked password input
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def is_download_complete(file_path):
    """Check if the file has finished downloading."""
    temp_extensions = ['.crdownload', '.part', '.tmp']
    return not any(os.path.exists(file_path + ext) for ext in temp_extensions)

# ✅ Prompt user for login credentials
email = input("Enter your email: ")
password = pwinput.pwinput("Enter your password: ", mask="*")  # Shows **** while typing
download_dir = input("Enter the directory to save downloads (default: downloads/test): ") or "downloads/test"



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
time.sleep(10)  # Adjust timing if needed

page = 1
while True:
    print(f"📄 Downloading files from Page {page}...")

    # ✅ Find files to download
    checkboxes = driver.find_elements(By.TAG_NAME, "tbody")
    print(f"🔍 Found {len(checkboxes)} checkboxes.")

    # ✅ Download files
    for cb in checkboxes:
        download_button = cb.find_elements(By.TAG_NAME, "button")
        if len(download_button) > 1:  # Ensure there is a second button
            print("📥 Downloading file...")
            download_button[1].click()
            time.sleep(5)  # Adjust based on download speed

    print(f"✅ Page {page} downloads complete.")

    # ✅ Ask user to manually change pages
    print("\n🔄 Please manually navigate to the next page in the browser.")
    next_page = input("➡️ Once done, press Enter to continue, or type 'exit' to quit: ").strip().lower()
    
    if next_page == "exit":
        print("🚪 Exiting...")
        break

    page += 1  # Increment page number

print("✅ All downloads complete. Browser will remain open.")
input("Press Enter to close the browser...")  # Keeps browser open until user presses Enter
driver.quit()
