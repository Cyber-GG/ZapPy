import zap_auth
import zap_config
import zap_blindxss
import os
import traceback
import logging
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
current_url = driver.current_url
logging.info(current_url)
#totp = pyotp.TOTP('XXUUNAVCYKI3UGHPCWUMVCUHZSYOLMTL')
#totp.now()

#element=driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/div[1]/div/input[1]")

# Check if the element is visible
#if element.is_displayed():
usernameid=driver.find_element(By.ID, "username")
passwordid=driver.find_element(By.ID, "password")
usernameid.send_keys(username)
passwordid.send_keys(password)
loginbutton = driver.find_element(By.ID, "Login")
loginbutton.click()
current_url = driver.current_url
logging.info(current_url)
time.sleep(10)
current_url = driver.current_url
logging.info(current_url)
verify = driver.page_source
#print(verify)
current_url = driver.current_url
logging.info(current_url)

logging.info("Hi Welcome")

config = zap_config.ZapConfig()

# Triggered when running a script directly (ex. python zap-baseline.py ...)
def start_docker_zap(docker_image, port, extra_zap_params, mount_dir):
    config.load_config(extra_zap_params)

# Triggered when running from the Docker image
def start_zap(port, extra_zap_params):
    config.load_config(extra_zap_params)

def zap_started(zap, target):
    try:
        # ZAP Docker scripts reset the target to the root URL
        if target.count('/') > 2:
            # The url can include a valid path, but always reset to spider the host
            target = target[0:target.index('/', 8)+1]

        scan_policy = 'Default Policy'
        zap.ascan.update_scan_policy(scanpolicyname=scan_policy , attackstrength="LOW")
        
        auth = zap_auth.ZapAuth(config)
        auth.authenticate(zap, target)

        zap_blindxss.load(config, zap)
    except Exception:
        logging.error("error in zap_started: %s", traceback.print_exc())
        os._exit(1)

    return zap, target

def zap_pre_shutdown(zap):
    logging.debug("Overview of spidered URL's:")
    for url in zap.spider.all_urls:
        logging.debug("found: %s", url)
    
    for result in zap.ajaxSpider.full_results['inScope']:
        logging.debug("found: %s", result['url'])
