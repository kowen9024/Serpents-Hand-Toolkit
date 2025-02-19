import os
import re
import csv
import pytesseract
from PIL import Image
import cv2
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import platform

def check_and_install_tesseract():
    """
    Check if Tesseract is installed and install it if not.
    """
    try:
        # Check if Tesseract is installed
        pytesseract.get_tesseract_version()
        logging.info("Tesseract is already installed.")
    except pytesseract.pytesseract.TesseractNotFoundError:
        logging.info("Tesseract is not installed. Attempting to install it.")
        system_platform = platform.system()
        
        if system_platform == "Windows":
            subprocess.run(["choco", "install", "tesseract"], check=True)
        elif system_platform == "Darwin":  # macOS
            subprocess.run(["brew", "install", "tesseract"], check=True)
        elif system_platform == "Linux":
            subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True)
        else:
            raise EnvironmentError("Unsupported platform: " + system_platform)

        logging.info("Tesseract installed successfully.")
        # Verify installation
        pytesseract.get_tesseract_version()

def extract_seagate_serials(image_path):
    """
    Extract Seagate serial numbers from an image using OCR.
    """
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            logging.error(f"[OCR] Could not read image => {image_path}")
            return []

        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        config = "--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        pil_im = Image.fromarray(morph)
        text = pytesseract.image_to_string(pil_im, config=config)
        pat = r"[A-Z0-9]{8,12}"
        found = re.findall(pat, text.upper())
        logging.info(f"Extracted serials from {image_path}: {found}")
        return found
    except Exception as e:
        logging.error(f"[extract_seagate_serials] => {e}")
        return []

def perform_ocr_on_directory(folder_path, output_csv, progress_callback=None):
    """
    Perform OCR on all images in a directory and save results to a CSV file.
    """
    check_and_install_tesseract()
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    total = len(files)
    results = []
    done = 0

    for i, fname in enumerate(files):
        path = os.path.join(folder_path, fname)
        found = extract_seagate_serials(path)
        for s in found:
            results.append({"filename": fname, "serial_number": s})
        done += 1
        if progress_callback:
            progress_callback(done, total)
    
    try:
        with open(output_csv, "w", newline="", encoding="utf-8") as cf:
            w = csv.DictWriter(cf, fieldnames=["filename", "serial_number"])
            w.writeheader()
            for r in results:
                w.writerow(r)
        logging.info(f"OCR results saved to {output_csv}")
    except Exception as e:
        logging.error(f"Error saving OCR results: {e}")

def perform_ocr_in_browser(search_term, search_url, listing_urls, screenshot_path="search_results.png", output_csv="item_details.csv"):
    """
    Perform OCR directly in the browser using Selenium and save item details to a CSV file.
    """
    check_and_install_tesseract()
    # Configure Selenium with headless option
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the e-commerce website and perform a search
    driver.get(f"{search_url}?q={search_term}")

    # Wait for the page to load
    time.sleep(5)

    # Capture a full-page screenshot of the search results
    driver.save_screenshot(screenshot_path)

    # Perform OCR on the screenshot
    try:
        image = Image.open(screenshot_path)
        text = pytesseract.image_to_string(image)
        logging.info(f"OCR Text: {text}")
    except pytesseract.pytesseract.TesseractNotFoundError:
        logging.error("Tesseract is not installed or it's not in your PATH. See README file for more information.")
        return

    # Function to gather item details from a listing link
    def gather_item_details(url):
        driver.get(url)
        time.sleep(5)
        
        # Extract item details
        item_name = driver.find_element(By.CLASS_NAME, "item-name").text
        price = driver.find_element(By.CLASS_NAME, "price").text
        seller = driver.find_element(By.CLASS_NAME, "seller").text
        reviews = driver.find_element(By.CLASS_NAME, "reviews").text
        description = driver.find_element(By.CLASS_NAME, "description").text
        
        # Return a dictionary of item details
        return {
            "Item Name": item_name,
            "Price": price,
            "Seller": seller,
            "Reviews": reviews,
            "Description": description
        }

    # Gather item details for each listing and save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Item Name", "Price", "Seller", "Reviews", "Description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for url in listing_urls:
            details = gather_item_details(url)
            writer.writerow(details)

    # Close the Selenium driver
    driver.quit()