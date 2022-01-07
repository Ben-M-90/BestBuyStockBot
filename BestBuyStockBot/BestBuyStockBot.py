from decimal import Decimal
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
from fake_useragent import UserAgent
import hashlib
import os
import random
from re import sub
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from time import localtime, strftime, sleep
from urllib.request import urlopen


load_dotenv()

#BestBuy Login Info
cart_url = "https://bestbuy.com/cart"
checkout_url = "https://www.bestbuy.com/checkout/r/fast-track"
cvv = os.getenv('CVV')
login_url = "https://www.bestbuy.com/identity/global/signin"
login_email = os.getenv('LOGIN_EMAIL')
login_password = os.getenv('LOGIN_PASSWORD')
mention_id = os.getenv('MENTION_ID')
webhook_url = os.getenv('WEBHOOK_URL')
url_list = os.getenv('URL_LIST').split(", \n")

#target_url_Test = "https://www.bestbuy.com/site/insignia-mouse-pad-black/7536185.p?skuId=7536185"
target_url_test = "https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000"

#Control Variables
discord_printing = False
minimum_wait = 20 #Note that time will be allowed for the page to fully load or time out
maximum_wait = 40
sleep_time = 5
time_out_limit = 10
test_threshold = 0 #Set to 0 to run program normally. Set between 1-20 to change frequency of test page loading. Higher = More Likely.

#Set browser as the driver. Configure settings to help hide the bot from detection and hide driver messages from cluttering terminal.
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()


if discord_printing:
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())


def terminal_and_discord_print(discord_printing, message, mention=False):
    print(message)
    if mention: 
        mention_prefix = "<@&" + mention_id + "> "
    else: 
        mention_prefix = ""
    if discord_printing: 
        webhook.send(mention_prefix + message)


def login():
    while True:
        driver.get(login_url)
        try:
                WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.ID, "fld-e"))).send_keys(login_email)
                WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.ID, "fld-p1"))).send_keys(login_password)
                WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cia-form__controls"))).click()
                sleep(time_out_limit)
                print("Logged in successfully.\n\n")
                break            
        except:
            print("Login fields not detected, retrying.\n")


def main_loop():
    stock = False
    while stock == False:
        for url in url_list:
            if random.randint(0, 20) >= test_threshold:
                while True:
                    try:
                        driver.get(url)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(sleep_time)
                    else: break
            else:
                while True:
                    try:
                        driver.get(target_url_test)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(sleep_time)
                    else: break
            stock = check_stock()
            if stock == True: break
        print("---\n")
        if stock == True: break
        sleep(random.randint(minimum_wait, maximum_wait))


def check_stock():
    current_time = strftime("%Y/%m/%d - %I:%M:%S %p", localtime())
    try:
        driver.find_element(By.CLASS_NAME, "c-button-disabled").text
        print("Stock check: " + driver.find_element(By.CSS_SELECTOR, ".sku-title").text + "\n~~~ " + current_time + ": Out of Stock\n\n")
        return False
    except:
        try:
            if driver.find_element(By.CLASS_NAME, "add-to-cart-button").text == "Add to Cart":
                terminal_and_discord_print(discord_printing, "Stock check: " + driver.find_element(By.CSS_SELECTOR, ".sku-title").text + "\n~~~ " + current_time + ": IN STOCK\n\n", True)
                return True
            else:
                print("Stock check: " + driver.find_element(By.CSS_SELECTOR, ".sku-title").text + "\n~~~ " + current_time + ": Potentially in stock, but not showing Add to Cart option\n\n")
                return False
        except: 
            print("Failed to find button.\n")
            return False
        else: 
            print("ERROR!\n")
            return False


def add_to_cart():
    button_element = driver.find_element(By.CLASS_NAME, "add-to-cart-button")
    terminal_and_discord_print(discord_printing, "=== RUNNING PROCESS: ADD TO CART", True)
    print("Button says:" + button_element.text)

    button_element.click()
    terminal_and_discord_print(discord_printing, "***Clicked Add to Cart!")

    after_click_text = button_element.text
    print("***Button changed text to: " + after_click_text)

    while True:
        try:
            WebDriverWait(driver, sleep_time).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".continue-shopping")))
            terminal_and_discord_print(discord_printing, "***Detected as added to cart.\n\n", True)
            break
        except: 
            print("Not detected as added to cart. Retrying.")
            try: button_element.click()
            except: pass
            print("***Button clicked.\n")
        else: break


def purchase():
    terminal_and_discord_print(discord_printing, "=== RUNNING PROCESS: PURCHASE")
    try:
                driver.find_element(By.XPATH, '//*[@id="survey_invite_no"]').click()
    except: pass

    while True:
        try:
            driver.get(cart_url)
            print("***Changed page to Cart\n\n")
            False
        except: 
            print("Couldn't load cart, retrying.")
            sleep(sleep_time)
            True
        else: break

    driver.find_element(By.CSS_SELECTOR, ".checkout-buttons__checkout").click()
    terminal_and_discord_print(discord_printing, "***Clicked Checkout!")

    while True:
        try:
            terminal_and_discord_print(discord_printing, "WAITING TO CHECKOUT")
            #WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "credit-card-cvv"))).send_keys(cvv)
            #############WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg"))).click()
            #print("**************Just need to click " + driver.find_element(By.CSS_SELECTOR, ".btn-lg").text)
            #TerminalAndDiscordMsg(discordPrinting, "**************Just need to click " + driver.find_element(By.CSS_SELECTOR, ".btn-lg").text)
            wait = input("Press any key to exit!")
            system.exit()
        except: pass
        else: break


def checkout():
    terminal_and_discord_print(discord_printing, "=== RUNNING PROCESS: CHECKOUT (CART BYPASS)!", True)

    while True:
        try:
            driver.get(checkout_url)
            print("***Changed page to Checkout\n")
            break
        except:
            print("Couldn't load checkout, retrying.")
            sleep(sleep_time)
            True
        else: break
    
    try:
        driver.find_element(By.LINK_TEXT, "Switch to Shipping").click()
    except: pass

    try: WebDriverWait(driver, sleep_time).under(EC.presence_of_element_located((By.XPATH, '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'))).click()
    except: pass
    sleep(sleep_time)
    try: WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.ID, "cvv"))).send_keys(cvv) # Attempt to enter CVV
    except: pass
    try: WebDriverWait(driver, sleep_time).until(EC.presence_of_element_located((By.ID, "credit-card-cvv"))).send_keys(cvv) # Attempt to enter CVV on alternative element ID
    except: pass
    terminal_and_discord_print(discord_printing, "!!! WAITING TO CHECKOUT", True)
    
    #############WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg"))).click()
    #TerminalAndDiscordMsg(discordPrinting, "**************Just need to click " + driver.find_element(By.CSS_SELECTOR, ".btn-lg").text)

    wait = input("Press any key to EXIT!")
    system.exit()




terminal_and_discord_print(discord_printing, "### INITIALIZED: " + strftime("%Y/%m/%d - %I:%M:%S %p", localtime()), True)

login()
main_loop()
add_to_cart()
checkout()
