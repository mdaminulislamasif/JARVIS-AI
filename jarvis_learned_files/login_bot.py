import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ফাইল পাথ
PHONE_PATH = r"C:\Users\PHP\Desktop\PHONENUMBER.TEXT"
OLD_PASS_PATH = r"C:\Users\PHP\Desktop\NUMBER.TEXT"
NEW_PASS_PATH = r"C:\Users\PHP\Desktop\PASS.TEXT"

def start_bot():
    try:
        with open(PHONE_PATH, "r") as f: phones = [l.strip() for l in f if l.strip()]
        with open(OLD_PASS_PATH, "r") as f: old_pwds = [l.strip() for l in f if l.strip()]
        with open(NEW_PASS_PATH, "r") as f: new_pwds = [l.strip() for l in f if l.strip()]
    except Exception as e:
        print(f"File Error: {e}"); return

    chrome_options = Options()
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 5) 

    for i in range(min(len(phones), len(old_pwds), len(new_pwds))):
        phone, old_pass, new_pass = phones[i], old_pwds[i], new_pwds[i]

        try:
            print(f"Target: {phone}")
            
            # ১. লগইন লিঙ্ক
            driver.get("https://accounts.google.com/v3/signin/identifier?dsh=S-32557173%3A1670678350345454&continue=https%3A%2F%2Faccounts.google.com%2F&followup=https%3A%2F%2Faccounts.google.com%2F&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AeAAQh7WM12s-KKXnMinlFoUqKIyvTLfyeaMxCw85c6WC2nWTXK7za_7s4z00LuPJzTrKZRXvWiR2g")

            # ফোন ও পাসওয়ার্ড ইনপুট
            wait.until(EC.visibility_of_element_located((By.ID, "identifierId"))).send_keys(phone + Keys.ENTER)
            wait.until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(old_pass + Keys.ENTER)
            
            # ২. সরাসরি পাসওয়ার্ড চেঞ্জ পেজে জাম্প
            time.sleep(1.5) 
            driver.get("https://myaccount.google.com/signinoptions/password")

            # পেজ চেক: যদি ফালতু সিকিউরিটি পেজে যায় তবে সাথে সাথে এক্সিট (Skip)
            current_url = driver.current_url
            if "intro/security" in current_url or "security-checkup" in current_url:
                print(f"Faltu Site Detected! Exiting {phone}...")
                driver.delete_all_cookies()
                continue # এই আইডি ছেড়ে পরেরটাতে চলে যাবে

            # ৩. পাসওয়ার্ড চেঞ্জ প্রসেস
            try:
                re_auth = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
                re_auth.send_keys(old_pass + Keys.ENTER)
            except Exception as e:
                print(f"⚠️ Error: {e}")

            pwd_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='password']")))
            if len(pwd_fields) >= 2:
                pwd_fields[0].send_keys(new_pass)
                pwd_fields[1].send_keys(new_pass + Keys.ENTER)
                
                print(f"Success: {phone}")
                with open("success_log.txt", "a") as log:
                    log.write(f"{datetime.now().strftime('%H:%M:%S')} | {phone} | Done\n")
            
            driver.delete_all_cookies()

        except Exception:
            print(f"Error/Skip: {phone}")
            continue

    driver.quit()

# ১২ ঘণ্টা রান
start_time = time.time()
while (time.time() - start_time) < 43200:
    start_bot()
    time.sleep(1)
