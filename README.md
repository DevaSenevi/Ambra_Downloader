# AmbraBot - Automated File Downloader

AmbraBot is a **Selenium-based script** that logs into the Ambra Health platform and automates the **download of files** across multiple pages. It prompts the user for login credentials and allows manual navigation between pages for a more stable and flexible experience.

---

## 🚀 Features
✅ **Automated Login** – Securely enter your email & password at runtime  
✅ **File Downloads** – Automatically selects and downloads available files  
✅ **Manual Pagination** – The user manually switches pages to avoid detection issues  
✅ **Custom Download Directory** – Choose where to save files  

---

## 📌 Prerequisites

Ensure you have:
- **Python 3.9+**
- **Mozilla Firefox** installed
- **Geckodriver** (Firefox WebDriver) installed  
  - You can install it via Conda:  
    ```sh
    conda install -c conda-forge geckodriver
    ```
  - Or download manually from: [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)

---

## ⚙️ Setup

### 1️⃣ **Create the Conda Environment**
To set up a dedicated environment, run:

```sh
conda env create -f environment.yml
conda activate ambra_downloader
```

### 2️⃣ **Install Dependencies**
If using `pip` instead of Conda:

```sh
pip install -r requirements.txt
```

---

## 🛠️ Usage

### **Run the script:**
```sh
python ambra_downloader.py
```

### **Enter your credentials when prompted:**
```
Enter your email: your@email.com
Enter your password: ******
Enter the directory to save downloads (default: downloads/test):
```

### **How to navigate pages:**
1️⃣ The script downloads **all files on the current page**  
2️⃣ It then **asks you to manually change pages in the browser**  
3️⃣ Once you've navigated to the next page, press **Enter** to continue downloading  

### **Exit the script**
- Type **`exit`** instead of pressing Enter when asked to move to the next page.

---

## 🔧 Troubleshooting

### **Firefox or Geckodriver Not Found?**
Ensure that:
- **Firefox** is installed  
- **Geckodriver** is installed & available in PATH  
  ```sh
  which geckodriver  # Linux/macOS
  where geckodriver  # Windows
  ```

### **Script closes too fast?**
- If files are missing, check the **download directory** for partial files.
- Increase `time.sleep(5)` to allow more time for downloads.

---

## 📝 License
This project is for **personal use only**. Please check Ambra Health’s **terms of service** before automating downloads.

---

## Credits
Developed by **Yuanhan**,**Deva**.
