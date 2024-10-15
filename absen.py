import time
import requests
import csv
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Read the configuration file
def read_config(file_path):
    with open(file_path, mode='r') as infile:
        config = json.load(infile)
    return config

# Function to send Telegram notification
def send_telegram_message(telegram_bot_token, telegram_chat_id, message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# Fungsi cek waktu
def get_part_of_day():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Pagi"
    elif 12 <= current_hour < 15:
        return "Siang"
    else:
        return "Sore"

# Function to set geolocation
def set_geolocation(driver, latitude, longitude):
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })

# Function to wait until the page is fully loaded
def wait_for_full_load(driver, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="theForm"]/div/p[1]/input'))
        )
    except Exception as e:
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="theForm"]/div/p[1]/input'))
        )

# Function perjalanan
def wait_for_perjalanan(driver, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr/td[2]/input[6]'))
        )
    except Exception as e:
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr/td[2]/input[6]'))
        )

# Function kesehatan
def wait_for_kesehatan(driver, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[2]/input'))
        )
    except Exception as e:
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[2]/input'))
        )        

# Function to wait until the next page is fully loaded
def wait_for_next_page_load(driver, timeout=2):
   try:
       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-warning.btn-block'))
       )
   except Exception as e:
       driver.refresh()
       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-warning.btn-block'))
       )

# Function to scroll down the page
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # wait for the page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to check if today is a national holiday using DayOffAPI
def is_national_holiday():
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://dayoffapi.vercel.app/api"
    response = requests.get(url)
    
    if response.status_code == 200:
        holidays = response.json()
        for holiday in holidays:
            if holiday['tanggal'] == today and holiday['keterangan']:
                return True
    return False

# Function to perform the attendance submission
def submit_attendance(entry):
    NIP = entry['NIP']
    password = entry['password']
    name = entry['name']
    telegram_chat_id = entry['telegram_chat_id']

    # Baca konfigurasi dari file JSON
    config = read_config('config.json')
    telegram_bot_token = config['telegram_bot_token']
    latitude = config['latitude']
    longitude = config['longitude']
    suhu = config['suhu']

    max_retries = 3
    retry_delay = 2  # seconds

    if is_national_holiday():
        print(f"Today is a national holiday. Skipping attendance for {name}.")
        return

    for attempt in range(max_retries):
        driver = None
        try:
            # Setup Chrome driver with custom geolocation
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
            service = Service(executable_path="/root/absen/chromedriver")  # Ensure this path is correct
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.maximize_window()  # Maximize the browser window

            # Open the Skemaraja login page
            set_geolocation(driver, latitude, longitude)
            driver.get("https://skemaraja.dephub.go.id/")
            wait_for_full_load(driver)

            # Input NIP
            nip_field = driver.find_element(By.XPATH, '//*[@id="theForm"]/div/p[1]/input')
            nip_field.send_keys(NIP)

            time.sleep(1)

            # Input Password
            password_field = driver.find_element(By.XPATH, '//*[@id="theForm"]/div/p[2]/input[4]')
            password_field.send_keys(password)

            time.sleep(1)

            # Select WFH/WFO status
            status_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="theForm"]/div/p[3]/select'))
            status_dropdown.select_by_visible_text("Work From Office")

            time.sleep(1)

            # Select Shift
            shift_button = driver.find_element(By.XPATH, '//*[@id="shift_1"]')  # Replace with the actual XPath of the shift dropdown
            shift_button.click()

            # Wait for the page to load (you might need to add explicit waits here)
            time.sleep(1)

            # Submit the attendance form
            submit_button = driver.find_element(By.XPATH, '//*[@id="btnSubmit"]')
            submit_button.click()

            time.sleep(1)

            # Wait for the next page to be fully loaded after form submission
            driver.get("https://skemaraja.dephub.go.id/")
            time.sleep(1)

            scroll_to_bottom(driver)

            try:
                # Attempt to submit form perjalanan
                wait_for_perjalanan(driver)
                time.sleep(1)
                jalan_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary')
                jalan_button.click()
                time.sleep(1)
                scroll_down(driver)

            except Exception as e:
                print(f"Form perjalanan tidak ditemukan. Melanjutkan ke langkah berikutnya...")

            try:
                # Attempt to fill additional form inputs
                wait_for_kesehatan(driver)
                time.sleep(1)
                suhu_field = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[2]/input')
                suhu_field.send_keys(suhu)

                scroll_down(driver)

                health_conditions_buttons = [
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[2]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[3]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[4]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[5]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[6]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[7]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[8]/td[4]/input',
                    '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[9]/td[4]/input'
                ]

                for button_xpath in health_conditions_buttons:
                    button = driver.find_element(By.XPATH, button_xpath)
                    driver.execute_script("arguments[0].click();", button)  # Click the button using JavaScript

                scroll_to_bottom(driver)
                time.sleep(1)

                # Attempt to submit additional health info
                additional_submit_button = driver.find_element(By.CLASS_NAME, 'btn.btn-primary')
                additional_submit_button.click()

            except Exception as e:
                print(f"Input tambahan tidak ditemukan. Melanjutkan ke langkah berikutnya...")

            time.sleep(1)

            # Wait for the next page to be fully loaded after form submission
            wait_for_next_page_load(driver)
            time.sleep(1)

            # Send Telegram notification without current time
            part_of_day = get_part_of_day()
            message = f"Absen {part_of_day} {name} telah dilaksanakan."
            send_telegram_message(telegram_bot_token, telegram_chat_id, message)
            print(message)

            # Open Skemaraja login page again
            driver.get("https://skemaraja.dephub.go.id/")
            time.sleep(1)
            break  # Exit the loop if submission is successful
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {name}. Retrying in {retry_delay} seconds...: {e}")
                time.sleep(retry_delay)
            else:
                error_message = f"Attendance submission failed for {name} after {max_retries}"
                send_telegram_message(telegram_bot_token, telegram_chat_id, f"Absen {name} Gagal dilaksanakan.")
                print(error_message)
        finally:
            if driver:
                driver.quit()

# Main program loop
if __name__ == "__main__":
    with open('data.csv', mode='r') as infile:
        reader = csv.DictReader(infile)
        for entry in reader:
            submit_attendance(entry)
