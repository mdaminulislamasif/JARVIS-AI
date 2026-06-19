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

# ফাইল পাথ (আপনার পাথ অনুযায়ী)
PHONE_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\1PHONENUMBER.TEXT"
OLD_PASS_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\1NUMBER.TEXT"
NEW_PASS_PATH = r"C:\Users\PHP\Desktop\New folder\New folder\1PASS.TEXT"

def start_bot():
    try:
        # ফাইল রিড করা
        with open(PHONE_PATH, "r", encoding='utf-8') as f: phones = [l.strip() for l in f if l.strip()]
        with open(OLD_PASS_PATH, "r", encoding='utf-8') as f: old_pwds = [l.strip() for l in f if l.strip()]
        with open(NEW_PASS_PATH, "r", encoding='utf-8') as f: new_pwds = [l.strip() for l in f if l.strip()]
    except Exception as e:
        print(f"File Error: {e}")
        return

    chrome_options = Options()
    # ইমেজ লোড বন্ধ করে স্পিড বাড়ানো হয়েছে
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--window-size=1280,800")
    
    try:
        # স্বয়ংক্রিয়ভাবে ড্রাইভার ইনস্টল এবং স্টার্ট
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 6) # আল্ট্রা ফাস্ট নেটের জন্য ৬ সেকেন্ড ওয়েট
    except Exception as e:
        print(f"Chrome Error: {e}")
        return

    for i in range(min(len(phones), len(old_pwds), len(new_pwds))):
        phone, old_pass, new_pass = phones[i], old_pwds[i], new_pwds[i]

        try:
            print(f"Running: {phone}")
            
            # ১. আপনার দেওয়া প্রথম লিঙ্ক: লগইন পেজ
            driver.get("https://accounts.google.com/v3/signin/identifier?dsh=S-32557173%3A1670678350345454&continue=https%3A%2F%2Faccounts.google.com%2F&followup=https%3A%2F%2Faccounts.google.com%2F&passive=1209600&flowName=GlifWebSignIn&flowEntry=ServiceLogin&ifkv=AeAAQh7WM12s-KKXnMinlFoUqKIyvTLfyeaMxCw85c6WC2nWTXK7za_7s4z00LuPJzTrKZRXvWiR2g")

            # ফোন ইনপুট
            wait.until(EC.element_to_be_clickable((By.ID, "identifierId"))).send_keys(phone + Keys.ENTER)

            # পাসওয়ার্ড ইনপুট
            wait.until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(old_pass + Keys.ENTER)
            
            # ২. আপনার দেওয়া দ্বিতীয় লিঙ্ক: সরাসরি পাসওয়ার্ড চেঞ্জ পেজ (জাম্প)
            time.sleep(2) 
            driver.get("https://myaccount.google.com/signinoptions/password")

            # ফালতু সিকিউরিটি পেজ ফিল্টার
            if "intro/security" in driver.current_url:
                print(f"Security wall on {phone}, skipping...")
                driver.delete_all_cookies()
                continue

            # ৩. পাসওয়ার্ড চেঞ্জ প্রসেস
            try:
                # Re-auth (যদি আবার পাসওয়ার্ড চায়)
                re_auth = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
                re_auth.send_keys(old_pass + Keys.ENTER)
            except Exception as e:

                print(f"⚠️ Error: {e}")
                pass

            # ৪. নতুন পাসওয়ার্ড সেট
            pwd_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@type='password']")))
            if len(pwd_fields) >= 2:
                pwd_fields[0].send_keys(new_pass)
                pwd_fields[1].send_keys(new_pass + Keys.ENTER)
                
                # সাকসেস রিপোর্ট সেভ (success_log.txt ফাইলে)
                now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                with open("success_log.txt", "a", encoding='utf-8') as log:
                    log.write(f"Time: {now} | {phone} | {new_pass} | Success\n")
                print(f"Done: {phone}")
            
            driver.delete_all_cookies()

        except Exception:
            print(f"Skip: {phone}")
            continue

    driver.quit()

# ১২ ঘণ্টার কন্টিনিউয়াস রান
start_time = time.time()
while (time.time() - start_time) < 43200:
    start_bot()
    time.sleep(2)
