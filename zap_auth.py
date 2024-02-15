from selenium import webdriver
import pyotp
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time


firefox_options = Options()
firefox_options.add_argument('--headless')
firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument("--no-sandbox");
firefox_options.add_argument("--disable-dev-shm-usage");

username = "gomathy.gopinath@qualitestgroup.com.perftestin"
password = "Password@3101"

driver = webdriver.Firefox(options = firefox_options)
driver.get('https://saint-gobain-uk--perftestin.sandbox.my.salesforce.com/')

totp = pyotp.TOTP('XXUUNAVCYKI3UGHPCWUMVCUHZSYOLMTL')
print(totp.now())

element=driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/div[1]/div/input[1]")

# Check if the element is visible
if element.is_displayed():
    print("Login Page visible")
    usernameid=driver.find_element(By.ID, "username")
    passwordid=driver.find_element(By.ID, "password")
    usernameid.send_keys(username)
    passwordid.send_keys(password)
    loginbutton = driver.find_element(By.ID, "Login")
    loginbutton.click()
    time.sleep(10)
    verify = driver.page_source
    if "Verify Your Identity" in verify:
        print("Now in OTP Page")
        print(verify)
        otpinput = driver.find_element(By.ID, "tc")
        totp = pyotp.TOTP('XXUUNAVCYKI3UGHPCWUMVCUHZSYOLMTL')
        print(totp.now())
        otpinput.send_keys(totp)
        verifybtn = driver.find_element(By.ID, "save")
        verifybtn.click()
        time.sleep(8)
        current_url = driver.current_url
        print(current_url)

    else: 
     print("Some other page")
     print(verify)
     current_url = driver.current_url
     print(current_url)
    

else:
    print("Login page not loaded")
