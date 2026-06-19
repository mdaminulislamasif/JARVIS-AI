import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Path for Bot 4
PHONE_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\3PHONENUMBER.TEXT"
OLD_PASS_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\3NUMBER.TEXT"
NEW_PASS_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\3PASS.TEXT"
# ...বাকি কোড আগের মতোই থাকবে...

def start_bot():
    try:
        with open(PHONE_PATH, "r") as f: phones = [l.strip() for l in f if l.strip()]
        with open(OLD_PASS_PATH, "r") as f: old_pwds = [l.strip() for l in f if l.strip()]
        with open(NEW_PASS_PATH, "r") as f: new_pwds = [l.strip() for l in f if l.strip()]
    except Exception as e:
        print(f"File Error: {e}")
        return

    chrome_options = Options()
    # Speed optimization: images load bondho kore deya hoyeche
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.implicitly_wait(5) # Element paoya matroi kaj shuru korbe
    except Exception as e:
        print(f"Chrome Error: {e}")
        return

    for i in range(min(len(phones), len(old_pwds), len(new_pwds))):
        phone, old_pass, new_pass = phones[i], old_pwds[i], new_pwds[i]

        try:
            print(f"Running: {phone}")
            
            # 1. Login Page
            driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2F&dsh=S234921485%3A1776791576532117&ec=futura_exp_og_so_72776762_e&hl=bn&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AT1y2_XYibKnOpDIUi22gLHAeLEsUdFzFSTXUnFyU-3n5tkv9iGCznJ2mYsZGJjlTy2tvv3im-RCxw")

            # 2. Phone Input
            email_box = driver.find_element(By.ID, "identifierId")
            email_box.send_keys(phone + Keys.ENTER)
            time.sleep(2.5) # Fast transition

            # 3. Password Input
            pass_box = driver.find_element(By.NAME, "Passwd")
            pass_box.send_keys(old_pass + Keys.ENTER)
            time.sleep(4)

            # 4. Password Change Page
            driver.get("https://myaccount.google.com/signinoptions/password")

            # Re-auth (if needed)
            re_auth = driver.find_elements(By.NAME, "Passwd")
            if re_auth:
                re_auth[0].send_keys(old_pass + Keys.ENTER)
                time.sleep(4)

            # 5. Set New Password
            pwd_fields = driver.find_elements(By.XPATH, "//input[@type='password']")
            if len(pwd_fields) >= 2:
                pwd_fields[0].send_keys(new_pass)
                pwd_fields[1].send_keys(new_pass + Keys.ENTER)
                time.sleep(3)
                
                now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                with open("success_log.txt", "a") as log:
                    log.write(f"Time: {now} | {phone} | {new_pass} | Success\n")
                print(f"Done: {phone}")
            
            driver.delete_all_cookies()

        except Exception:
            print(f"Skip: {phone}")
            continue

    driver.quit()

# 12 hours run
start_time = time.time()
while (time.time() - start_time) < 43200:
    start_bot()
    time.sleep(10) # Cycle break komano hoyeche
