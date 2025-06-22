import os
import time
import re
import requests
from datetime import datetime
from PIL import Image
import pytesseract
import difflib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

def similar(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.8

try:
    driver.get("https://patinformed.wipo.int/")
    search_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='searchField']")))
    search_input.clear()
    search_input.send_keys("Paracetamol")
    search_input.send_keys(Keys.ENTER)

    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/dialog/modal-acceptance/div[2]/button[1]")))
    accept_button.click()

    inn_item = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/page-search/div[2]/div/table/tbody/tr/td[3]/ul/li/div")))
    inn_item.click()

    time.sleep(3)
    screenshot_path = "screenshot_after_inn.png"
    driver.save_screenshot(screenshot_path)

    x1, y1 = 1363, 568
    x2, y2 = 1865, 743
    image = Image.open(screenshot_path)
    cropped = image.crop((x1, y1, x2, y2))
    cropped_path = "cropped_region.png"
    cropped.save(cropped_path)

    extracted_text = pytesseract.image_to_string(cropped)

    publication_date_str = None
    filing_date_str = None
    lines = extracted_text.splitlines()

    for i, line in enumerate(lines):
        clean_line = line.replace(" ", "").lower()
        if similar(clean_line, "publicationdate") or "publicationdate" in clean_line:
            match = re.search(r"\d{4}-\d{2}-\d{2}", line)
            if match:
                publication_date_str = match.group()
            elif i + 1 < len(lines):
                match = re.search(r"\d{4}-\d{2}-\d{2}", lines[i + 1])
                if match:
                    publication_date_str = match.group()
        elif similar(clean_line, "filingdate") or "filingdate" in clean_line:
            match = re.search(r"\d{4}-\d{2}-\d{2}", line)
            if match:
                filing_date_str = match.group()
            elif i + 1 < len(lines):
                match = re.search(r"\d{4}-\d{2}-\d{2}", lines[i + 1])
                if match:
                    filing_date_str = match.group()

    if publication_date_str and filing_date_str:
        pub_date = datetime.strptime(publication_date_str, "%Y-%m-%d").date()
        fil_date = datetime.strptime(filing_date_str, "%Y-%m-%d").date()
        diff_days = (pub_date - fil_date).days
        print(f"Filing Date: {fil_date}")
        print(f"Publication Date: {pub_date}")
        print(f"Days Between: {diff_days}")
    else:
        print("Could not extract both dates.")

except Exception as e:
    print("Error:", e)

finally:
    input("Press Enter to close the browser...")
    driver.quit()
