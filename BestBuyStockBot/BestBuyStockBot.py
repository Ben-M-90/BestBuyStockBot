from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import localtime, strftime, sleep
import hashlib
import random
import os
from discord import Webhook, RequestsWebhookAdapter
import requests
import sys
from re import sub
from decimal import Decimal
from dotenv import load_dotenv
from urllib.request import urlopen
from fake_useragent import UserAgent

load_dotenv()

#BestBuy Login Info
loginURL = "https://www.bestbuy.com/identity/global/signin"
cartURL = "https://bestbuy.com/cart"
checkoutURL = "https://www.bestbuy.com/checkout/r/fast-track"
loginEmail = os.getenv('LOGIN_EMAIL')
loginPass = os.getenv('LOGIN_PASSWORD')
cvv = os.getenv('CVV')
mentionID = os.getenv('MENTION_ID')
webhookURL = os.getenv('WEBHOOK_URL')

urlList = os.getenv('URL_LIST').split(", \n")

###Nvidia RTX 3080 FE Best Buy Page URL
targetURL = "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440"
###Test Page = Mouse Pad
#targetURLTest = "https://www.bestbuy.com/site/insignia-mouse-pad-black/7536185.p?skuId=7536185"
targetURLTest = "https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000"

#Common XPaths and CSS Selectors
cssDisabledButton = "c-button-disabled"
cssAvailableButton = "button.btn-primary:nth-child(1)"

#Control Variables
discordPrinting = False
minWait = 20 #Note that time will be allowed for the page to fully load or time out
maxWait = 40
sleepTime = 5
timeOutLim = 10
testThreshold = 0 #Set to 0 to run program normally. Set between 1-20 to change frequency of test page loading. Higher = More Likely.

###Create webhook for posting updates to Discord.
webhook = Webhook.from_url(webhookURL, adapter=RequestsWebhookAdapter())

#Set browser as the driver. Configure some settings to help hide the bot from detection and hide driver messages from cluttering terminal.
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.delete_all_cookies()

#Function for printing the same message to discord and terminal. Can be toggled to only print with terminal by setting variable discordPrint = False.
def TerminalAndDiscordMsg(discordPrint, message, mention=False):
    print(message)
    if mention: mentionPre = "<@&" + mentionID + "> "
    else: mentionPre = ""
    if discordPrint: webhook.send(mentionPre + message)

######Function to login. Goes to login page, enters e-mail/password and hits Sign In button. Gives time for login redirect to finish before continuing (may not complete login otherwise).
def loginSeq():
    while True:
        driver.get(loginURL)
        try:
                WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "fld-e"))).send_keys(loginEmail)
                WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "fld-p1"))).send_keys(loginPass)
                WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cia-form__controls"))).click()
                #WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-secondary"))).click()
                sleep(timeOutLim)
                print("Logged in successfully.\n\n")
                break            
        except:
            print("Login fields not detected, retrying.\n")

######Continuous loop to refresh, check stock, and refresh (or exit loop and continue to purchase if stock is detected).
def reCheck():
    stock = False
    while stock == False:
        for url in urlList:
            if random.randint(0, 20) >= testThreshold: #Random chance of loading the test page.
                while True:
                    try:
                        driver.get(url)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(sleepTime)
                    else: break
            else:
                while True:
                    try:
                        driver.get(targetURLTest)
                    except:
                        print("Failed to load page, retrying.")
                        sleep(sleepTime)
                    else: break
            stock = stockCheck() #Check stock after loading/refreshing page. Will return False if stock is found, True if not found. TRUE = CONTINUE LOOP, FALSE = STOP LOOP
            if stock == True: break # Break out of for loop if stockCheck() returns True (in stock).
        print("---\n")
        if stock == True: break # Break out of while loop is stockCheck() returns True (in stock). Bypass random sleep period, goes straight to adding to cart process.
        sleep(random.randint(minWait, maxWait)) #Sleep a random interval before refreshing tabs. Attempt to make refreshes less robotic.

######Function to determine if there is stock by checking text of button.
def stockCheck():
    curTime = strftime("%Y/%m/%d - %I:%M:%S %p", localtime())
    try: #Try finding the disabled button. If found, print timestamp and out of stock.
        driver.find_element_by_css_selector(cssDisabledButton).text
        #TerminalAndDiscordMsg(discordPrinting, "Stock check: " + driver.find_element_by_css_selector(".sku-title").text + "\n~~~ " + curTime + ": Out of Stock\n\n")
        print("Stock check: " + driver.find_element_by_css_selector(".sku-title").text + "\n~~~ " + curTime + ": Out of Stock\n\n")
        return False #Returning False will trigger parent loop (reCheck) to continue.
    except:
        try: #If disabled button was unable to be located, try finding available button. If found, print "timestamp - in stock" and proceed.
            driver.find_element_by_css_selector(cssAvailableButton).text
            TerminalAndDiscordMsg(discordPrinting, "Stock check: " + driver.find_element_by_css_selector(".sku-title").text + "\n~~~ " + curTime + ": IN STOCK\n\n", True)
            return True #Returning True will break out of parent loop (reCheck).
        except: 
            print("Failed to find button.\n") #If not able to find the disabled button OR available button, print that it failed to find any button
            return False #Returning False will trigger parent loop (reCheck) to continue.
        else: 
            print("ERROR!\n")
            return False #Returning False will trigger parent loop (reCheck) to continue.

######Functions for performing a purchase once in stock.
def addToCartProcess():
    buttonElement = driver.find_element_by_css_selector(cssAvailableButton)
    TerminalAndDiscordMsg(discordPrinting, "=== RUNNING PROCESS: ADD TO CART", True)
    print("Button says:" + buttonElement.text)

    buttonElement.click()
    TerminalAndDiscordMsg(discordPrinting, "***Clicked Add to Cart!")

    afterClickTxt = buttonElement.text
    print("***Button changed text to: " + afterClickTxt)

    while True:
        try:
            #Check if the item has been Added to Cart. Time allowed for this to be displayed is controlled by sleepTime variable. If it is not displayed, keep trying. If it is displayed, proceed with normal buy process.
            WebDriverWait(driver, sleepTime).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".continue-shopping")))
            TerminalAndDiscordMsg(discordPrinting, "***Detected as added to cart.\n\n", True)
            #sleep(sleepTime)
            break
        except: 
            print("Not detected as added to cart. Retrying.")
            try: buttonElement.click()
            except: pass
            print("***Button clicked.\n")
        else: break

######Normal purchasing process.
def purchProcess():
    TerminalAndDiscordMsg(discordPrinting, "=== RUNNING PROCESS: PURCHASE")
    try: #Ignore survey popup to prevent it from interrupting
                driver.find_element_by_xpath('//*[@id="survey_invite_no"]').click()
    except: pass

    while True:
        try:
            driver.get(cartURL)
            print("***Changed page to Cart\n\n")
            False
        except: 
            print("Couldn't load cart, retrying.")
            sleep(sleepTime)
            True
        else: break

    driver.find_element_by_css_selector('.checkout-buttons__checkout').click() #Click checkout button.
    TerminalAndDiscordMsg(discordPrinting, "***Clicked Checkout!")

    while True:
        try:
            TerminalAndDiscordMsg(discordPrinting, "WAITING TO CHECKOUT")
            #WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "credit-card-cvv"))).send_keys(cvv)
            #############WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg"))).click()
            #print("**************Just need to click " + driver.find_element_by_css_selector('.btn-lg').text)
            #TerminalAndDiscordMsg(discordPrinting, "**************Just need to click " + driver.find_element_by_css_selector('.btn-lg').text)
            wait = input("Press any key to exit!")
            system.exit()
        except: pass
        else: break

######Process to skip going to the cart and go straight to checkout page.
def checkoutProcess():
    TerminalAndDiscordMsg(discordPrinting, "=== RUNNING PROCESS: CHECKOUT (CART BYPASS)!", True)

    while True:
        try:
            driver.get(checkoutURL)
            print("***Changed page to Checkout\n")
            break
        except:
            print("Couldn't load checkout, retrying.")
            sleep(sleepTime)
            True
        else: break
    
    try: #Try switching to shipping instead of pickup. Checkout
        driver.find_element_by_link_text("Switch to Shipping").click()
        #sleep(sleepTime)
    except: pass

    try: WebDriverWait(driver, sleepTime).under(EC.presence_of_element_located((By.XPATH, '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'))).click()
    except: pass
    sleep(sleepTime)
    try: WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "cvv"))).send_keys(cvv) # Attempt to enter CVV
    except: pass
    try: WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.ID, "credit-card-cvv"))).send_keys(cvv) # Attempt to enter CVV on alternative element ID
    except: pass
    TerminalAndDiscordMsg(discordPrinting, "!!! WAITING TO CHECKOUT", True)
    
    #############WebDriverWait(driver, sleepTime).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-lg"))).click()
    #TerminalAndDiscordMsg(discordPrinting, "**************Just need to click " + driver.find_element_by_css_selector('.btn-lg').text)

    wait = input("Press any key to EXIT!")
    system.exit()

############Initialize program
TerminalAndDiscordMsg(discordPrinting, "### INITIALIZED: " + strftime("%Y/%m/%d - %I:%M:%S %p", localtime()), True)

loginSeq()
reCheck()
addToCartProcess()
checkoutProcess()
