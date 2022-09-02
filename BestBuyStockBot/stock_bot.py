'''Bot to check stock for list of items at Best Buy, add to cart, and purchase'''
import os
import random
import sys
from time import localtime, strftime, sleep
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


load_dotenv()
CART_URL = "https://bestbuy.com/cart"
CHECKOUT_URL = "https://www.bestbuy.com/checkout/r/fast-track"
LOGIN_URL = "https://www.bestbuy.com/identity/global/signin"
login_email = os.getenv('LOGIN_EMAIL')
login_password = os.getenv('LOGIN_PASSWORD')
cvv = os.getenv('CVV')
mention_id = os.getenv('MENTION_ID')
webhook_url = os.getenv('WEBHOOK_URL')
url_list = os.getenv('URL_LIST').split(",\n")

#TARGET_URL_TEST = "https://www.bestbuy.com/site/insignia-mouse-pad-black/7536185.p?skuId=7536185"
TARGET_URL_TEST = "https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000"

#Control Variables
PRINT_TO_DISCORD = False
MINIMUM_WAIT = 20 #Note that time will be allowed for the page to fully load or time out
MAXIMUM_WAIT = 40
SLEEP_TIME = 5
TIME_OUT_LIMIT = 10
#0 <= TEST_THRESHOLD <= 20. Higher = More likely test page will load.
TEST_THRESHOLD = 0

#Create webdriver. Configure settings to mask bot.
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options, service=service)
driver.delete_all_cookies()


if PRINT_TO_DISCORD:
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())


def terminal_and_discord_print(discord_print_bool, message, mention=False):
    '''Takes in a message and prints to Terminal & Discord (if configured)'''
    print(message)
    if discord_print_bool is True:
        if mention is True:
            mention_prefix = "<@&" + mention_id + "> "
        else:
            mention_prefix = ""
        webhook.send(mention_prefix + message)


def login():
    '''Login to BestBuy'''
    while True:
        try:
            driver.get(LOGIN_URL)
            WebDriverWait(driver, SLEEP_TIME).until(
                EC.presence_of_element_located(
                    (By.ID, "fld-e"))).send_keys(login_email)

            WebDriverWait(driver, SLEEP_TIME).until(
                EC.presence_of_element_located(
                    (By.ID, "fld-p1"))).send_keys(login_password)

            WebDriverWait(driver, SLEEP_TIME).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".cia-form__controls"))).click()

            sleep(TIME_OUT_LIMIT)
            print("Logged in successfully.\n\n")
            break
        except:
            print("Login fields not detected, retrying.\n")
            sleep(TIME_OUT_LIMIT)


def main_loop():
    '''Continuous loop to keep bot checking until stock is detected.'''
    stock = False
    while stock is False:
        for url in url_list:
            if random.randint(0, 20) >= TEST_THRESHOLD:
                while True:
                    try:
                        driver.get(url)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(SLEEP_TIME)
                    else:
                        break
            else:
                while True:
                    try:
                        driver.get(TARGET_URL_TEST)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(SLEEP_TIME)
                    else:
                        break
            stock = check_stock()
            if stock is True:
                break
        print("---\n")
        if stock is True:
            break
        sleep(random.randint(MINIMUM_WAIT, MAXIMUM_WAIT))


def check_stock():
    '''Check if product is available on currently loaded page.'''
    try:
        WebDriverWait(driver, SLEEP_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, "c-button-disabled")))
        print("Stock check: "
              + driver.find_element(By.CSS_SELECTOR, ".sku-title").text
              + "\n~~~ "
              + strftime("%Y/%m/%d - %I:%M:%S %p", localtime())
              + ": Out of Stock\n\n")
        return False
    except:
        try:
            if driver.find_element(By.CLASS_NAME, "add-to-cart-button").text == "Add to Cart":
                terminal_and_discord_print(PRINT_TO_DISCORD, "Stock check: "
                                           + driver.find_element(By.CSS_SELECTOR, ".sku-title").text
                                           + "\n~~~ "
                                           + strftime("%Y/%m/%d - %I:%M:%S %p", localtime())
                                           + ": IN STOCK\n\n", True)
                return True
            else:
                print("Stock check: " + driver.find_element(By.CSS_SELECTOR, ".sku-title").text
                      + "\n~~~ "
                      + strftime("%Y/%m/%d - %I:%M:%S %p", localtime())
                      + ": Potentially in stock, but not showing Add to Cart option\n\n")
                return False
        except:
            print("Failed to find button.\n")
            return False


def add_to_cart():
    '''Add product on currently loaded page to cart.'''
    button_element = driver.find_element(By.CLASS_NAME, "add-to-cart-button")
    terminal_and_discord_print(PRINT_TO_DISCORD, "=== RUNNING PROCESS: ADD TO CART", True)
    print("Button says:" + button_element.text)

    button_element.click()
    terminal_and_discord_print(PRINT_TO_DISCORD, "***Clicked Add to Cart!")

    after_click_text = button_element.text
    print("***Button changed text to: " + after_click_text)

    while True:
        try:
            WebDriverWait(driver, SLEEP_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".continue-shopping")))
            terminal_and_discord_print(PRINT_TO_DISCORD, "***Detected as added to cart.\n\n", True)
            break
        except:
            print("Not detected as added to cart. Retrying.")
            try:
                button_element.click()
            except:
                pass
            print("***Button clicked.\n")


def purchase():
    '''Purchase product(s) currently in cart.'''
    terminal_and_discord_print(PRINT_TO_DISCORD, "=== RUNNING PROCESS: PURCHASE")
    try:
        driver.find_element(By.XPATH, '//*[@id="survey_invite_no"]').click()
    except:
        pass

    while True:
        try:
            driver.get(CART_URL)
            print("***Changed page to Cart\n\n")
            break
        except:
            print("Couldn't load cart, retrying.")
            sleep(SLEEP_TIME)
        else:
            break

    driver.find_element(By.CSS_SELECTOR, ".checkout-buttons__checkout").click()
    terminal_and_discord_print(PRINT_TO_DISCORD, "***Clicked Checkout!")

    while True:
        try:
            terminal_and_discord_print(PRINT_TO_DISCORD, "WAITING TO CHECKOUT")
            input("Press any key to exit!")
            sys.exit()
        except:
            pass


def checkout():
    '''Run through checkout process, wait for user input before finalizing.'''
    terminal_and_discord_print(PRINT_TO_DISCORD,
                               "=== RUNNING PROCESS: CHECKOUT (CART BYPASS)!",
                              True)

    while True:
        try:
            driver.get(CHECKOUT_URL)
            print("***Changed page to Checkout\n")
            break
        except:
            print("Couldn't load checkout, retrying.")
            sleep(SLEEP_TIME)

    try:
        driver.find_element(By.LINK_TEXT, "Switch to Shipping").click()
    except:
        pass

    try:
        WebDriverWait(driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH, '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'))).click()
    except:
        pass
    sleep(SLEEP_TIME)
    try:
        WebDriverWait(driver, SLEEP_TIME).until(
            EC.presence_of_element_located((By.ID, "cvv"))).send_keys(cvv)
    except:
        pass
    try:
        WebDriverWait(driver, SLEEP_TIME).until(
            EC.presence_of_element_located(
                (By.ID, "credit-card-cvv"))).send_keys(cvv)
    except:
        pass
    terminal_and_discord_print(PRINT_TO_DISCORD, "!!! WAITING TO CHECKOUT", True)

    input("Press any key to EXIT!")
    sys.exit()




terminal_and_discord_print(
    PRINT_TO_DISCORD,
    "### INITIALIZED: " + strftime("%Y/%m/%d - %I:%M:%S %p", localtime()),
    True)

login()
main_loop()
add_to_cart()
checkout()
