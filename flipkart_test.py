import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

class FlipkartAutomation(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Set up driver with ChromeService
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Apply stealth mode
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

        self.driver.get("https://www.flipkart.com/")
        time.sleep(random.uniform(3, 7))

    def test_flipkart_login_and_checkout(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)

        # Click on login
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Login']")))
        login_button.click()
        time.sleep(2)

        # Enter mobile number
        phone_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#container > div > div.VCR99n > div > div.Sm1-5F.col.col-3-5 > div > form > div.I-qZ4M.vLRlQb > input")))
        phone_input.send_keys("YOUR_PHONE_NUMBER")

        # Click on Request OTP
        request_otp_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#container > div > div.VCR99n > div > div.Sm1-5F.col.col-3-5 > div > form > div.LSOAQH > button")))
        request_otp_button.click()

        # Wait for manual OTP entry
        print("Waiting 45 seconds for manual OTP entry...")
        time.sleep(20)  # You manually enter the OTP during this time

        # Click submit OTP (if required)
        try:
            submit_otp_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[3]/div/div[2]/div/div/form/button")))
            submit_otp_button.click()
        except:
            print("OTP submitted manually or auto-detected by Flipkart.")

        time.sleep(5)  

        # Go to product page
        driver.get("""https://www.flipkart.com/shozie-women-flats/p/itm1eb628058e1f5?pid=SNDGZBZQZGZSZYRG&lid=LSTSNDGZBZQZGZSZYRGFHCTA0&marketplace=FLIPKART&store=osp%2Fiko&srno=b_1_14&otracker=browse&fm=organic&iid=c37699a1-6dcf-4aa7-9f5e-d2daeddc9f02.SNDGZBZQZGZSZYRG.SEARCH&ppt=browse&ppn=browse""")
        time.sleep(5)

        time.sleep(3)

        # Click on Add to Cart
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li[1]/button")))
        add_to_cart_button.click()
        time.sleep(5)

        try:
            place_order_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#container > div > div.z1ALT8 > div > div > div:nth-child(1) > div > div.cPHDOP.col-12-12.MfqIAz > div > form > button")))
            place_order_button.click()
            print("Order process started.")
        except:
            print("No Place Order button found, possibly out of stock.")

        time.sleep(5)

        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div/div/div[3]/span[2]/button")))
        continue_button.click()

        time.sleep(5)

        credit_card_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]")))
        credit_card_button.click()

        # Enter credit card details
        card_number_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[1]/div/div/input")))
        card_number_input.send_keys("4111111111111111")

        # Enter expiry date 
        month_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[2]/span[2]/div[1]/select")))
        Select(month_dropdown).select_by_value("05") 

        # Wait for the year dropdown and select a value
        year_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[2]/span[2]/div[2]/select"))
        )
        Select(year_dropdown).select_by_value("29")  # e.g., '29' for 2029

        # Fill the CVV (usually an input field, so send_keys should work)
        cvv_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[3]/div/div/input"))
        )
        cvv_field.send_keys("999")

        zip_code_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[4]/div[1]/div/input")))
        zip_code_input.send_keys("560066")

        city_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[4]/div[3]/div/input")))
        city_input.send_keys("Bangalore")

        state_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[4]/div[4]/div/input")))
        state_input.send_keys("Karnataka")

        country_dropdown = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[4]/div[2]/div/select")))
        Select(country_dropdown).select_by_value("India") 

        address_input = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[4]/div[5]/textarea")))
        address_input.send_keys("123, Main St, Anytown, India Flat placeholder building placeholder")

        time.sleep(3)

        # Click on the PAY button
        pay_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div/label[3]/div[2]/div/div/div[3]/form/div[5]/button")))
        pay_button.click()

        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()