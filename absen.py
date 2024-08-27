import time
import requests
import csv
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
    config_list = []
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            config_list.append(row)
    return config_list

config_list = read_config('config.csv')

# Function to send Telegram notification
def send_telegram_message(telegram_bot_token, telegram_chat_id, message):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {"chat_id": telegram_chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()

# Function to set geolocation
def set_geolocation(driver, latitude, longitude):
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": 100
    })

# Function to wait until the page is fully loaded
def wait_for_full_load(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="theForm"]/div/p[1]/input'))
        )
    except Exception as e:
        print(f"Page not fully loaded, refreshing...")
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="theForm"]/div/p[1]/input'))
        )

# Function perjalanan
def wait_for_perjalanan(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr/td[2]/input[6]'))
        )
    except Exception as e:
        print(f"Page not fully loaded, refreshing...")
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr/td[2]/input[6]'))
        )

# Function kesehatan
def wait_for_kesehatan(driver, timeout=3):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[2]/input'))
        )
    except Exception as e:
        print(f"Page not fully loaded, refreshing...")
        driver.refresh()
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/form/div/div[2]/div/div/table/tbody/tr[1]/td[2]/input'))
        )        

# Function to wait until the next page is fully loaded
def wait_for_next_page_load(driver, timeout=3):
   try:
       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-primary.btn-block'))
       )
   except Exception as e:
       print(f"Next page not fully loaded, refreshing...")
       driver.refresh()
       WebDriverWait(driver, timeout).until(
           EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-primary.btn-block'))
       )

# Function to set browser zoom level
def set_browser_zoom(driver, zoom_level):
    driver.execute_script(f"document.body.style.zoom='{zoom_level}%'")

# Function to scroll down the page
def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Function to scroll down the page
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # wait for the page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to perform the attendance submission
def submit_attendance(entry):
    NIP = entry['NIP']
    password = entry['password']
    name = entry['name']
    telegram_chat_id = entry['telegram_chat_id']

    # Hardcoded values
    wfh_status = "Work From Office"
    telegram_bot_token = "7482058034:AAGnXDqvNVOZ5gle4Jw0YOMjG6JD4KnP1KI"  # Replace with your actual Telegram bot token
    latitude = -6.975933  # Example latitude, replace with the actual value
    longitude = 107.646185  # Example longitude, replace with the actual value
    suhu = "36"  # Example temperature, replace with the actual value

    max_retries = 3
    retry_delay = 3  # seconds

    for attempt in range(max_retries):
        driver = None
        try:
            # Setup Chrome driver with custom geolocation
            chrome_options = Options()
            chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})
            service = Service(executable_path="C:\chromedriver.exe")  # Ensure this path is correct
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
            status_dropdown.select_by_visible_text(wfh_status)

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
            send_telegram_message(telegram_bot_token, telegram_chat_id, f"Absen bos {name} telah dilaksanakan.")
            print(f"Absen bos {name} telah dilaksanakan.")

            # Open Skemaraja login page again
            driver.get("https://skemaraja.dephub.go.id/")
            break  # Exit the loop if submission is successful
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed for {name}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                error_message = f"Attendance submission failed for {name} after {max_retries}"
                send_telegram_message(telegram_bot_token, telegram_chat_id, f"Absen bos {name} Gagal dilaksanakan.")
                print(error_message)
        finally:
            if driver:
                driver.quit()

# Function to process all entries
def process_all_entries():
    global config_list  # Use the global config_list to update it
    delay_between_entries = 5  # seconds
    
    # Reload the config list
    config_list = read_config('config.csv')
    
    for entry in config_list:
        print(f"Processing entry for {entry['name']}")
        submit_attendance(entry)
        time.sleep(delay_between_entries)  # Delay between each submission

# Function to check if the current time is within the specified range
def is_time_in_range(start_time, end_time):
    now = datetime.now().strftime("%H:%M")
    return start_time <= now <= end_time

# Function to check if today is one of the specified days to run
def is_allowed_day(allowed_days):
    now = datetime.now()
    return now.weekday() in allowed_days

# Function to get the next scheduled run time, adjusted for allowed days
def get_next_run_time(start_time, allowed_days):
    now = datetime.now()
    start_time_time = datetime.strptime(start_time, "%H:%M").time()

    today_start = datetime.combine(now.date(), start_time_time)
    
    # Find the next allowed day
    days_ahead = 0
    while (now + timedelta(days=days_ahead)).weekday() not in allowed_days:
        days_ahead += 1
    
    next_start = today_start + timedelta(days=days_ahead)
    
    if now > today_start and days_ahead == 0:
        days_ahead = 1
        while (now + timedelta(days=days_ahead)).weekday() not in allowed_days:
            days_ahead += 1
        next_start = today_start + timedelta(days=days_ahead)

    return next_start

# Function to print and update the countdown
def print_countdown(start_times, allowed_days):
    next_run_times = [get_next_run_time(start_time, allowed_days) for start_time in start_times]
    while True:
        now = datetime.now()
        # Cari waktu berikutnya yang paling dekat
        next_run_time = min(next_run_times)
        time_remaining = next_run_time - now
        if time_remaining.total_seconds() <= 0:
            print(f"Proses Absen BOS at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            process_all_entries()
            # Perbarui waktu berikutnya setelah proses berjalan
            next_run_times = [get_next_run_time(start_time, allowed_days) for start_time in start_times]
        else:
            countdown_str = f"Absen Selanjutnya pada {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}, Countdown: {str(time_remaining).split('.')[0]}"
            print(f"\r{countdown_str}", end="")
        time.sleep(1)  # Update every second

# Function to run the scheduling and processing
def run_scheduling():
    start_times = ['07:00', '12:00', '16:30']  # Daftar waktu mulai
    allowed_days = [0, 1, 2, 3, 4]  # Misalnya: Senin, Rabu, Jumat (0 = Senin, 6 = Minggu)
    print_countdown(start_times, allowed_days)

if __name__ == "__main__":
    # Read initial configuration
    config_list = read_config('config.csv')
    run_scheduling()
