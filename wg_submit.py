from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By

from loguru import logger
import socket
import time


XPATH_SEND_MESSAGE_BTN = "//div[contains(@class, 'panel')]//a[@class='btn btn-block btn-md wgg_orange'][contains(., 'Send Message')]"
XPATH_VIEW_CONVERSATION_BTN = "//div[contains(@class, 'panel')]//a[@class='btn btn-md btn-block wgg_blue'][contains(., 'View conversation')]"
XPATH_SUBMIT_BTN = "//form[@id='messenger_form']//button[@type='submit' and contains(.,'Send message')]"
XPATH_INPUT_TXT = "//div[@id='start_new_conversation']//textarea[@id='message_input']"
XPATH_COOKIES_ACCEPT = "/html/body/div[@id='cmpbox']/div[@class='cmpboxinner']/div[@class='cmpboxbtns']/span[@id='cmpwelcomebtnyes']/a[@class='cmpboxbtn cmpboxbtnyes cmptxt_btn_yes']"
XPATH_LOGIN_NAV = '//*[@id="main-nav-wrapper"]/nav[1]/div[3]/div/a[@onclick="{}"]'.format("fireLoginOrRegisterModalRequest('sign_in');ga('send', 'event', 'main_navigation', 'login', '1st_level');")
XPATH_LANG_BTN = "//span[@class='text-uppercase cursor-pointer dropdown-toggle footer_selected_language'][contains(., 'de')]"
XPATH_LANG_ENG_BTN = "//div[@class='footer_language_selection language_wrapper mt5']//div[@class='dropup noprint display-inline open']//a[normalize-space()='English']"
MAX_TRIES = 3


def submit_app(config, offer) -> bool:
    url = 'https://www.wg-gesucht.de' + offer
    logger.debug("Opening the website: {url}", url=url)

    driver = driver_connect(url)
    if driver is None:
        logger.warning("Unable to start drivers")
        return False

    set_lang(driver)
    accept_cookies(driver)
    try_to_login(driver, config)

    try:
        send_message_buttons = driver.find_element(By.XPATH, XPATH_SEND_MESSAGE_BTN)
        send_message_buttons.click()
        logger.debug("Opening new conversation...")
    except NoSuchElementException as err:
        try:
            driver.find_element(By.XPATH, XPATH_VIEW_CONVERSATION_BTN)
            logger.debug("Already sent message to this offer, closing the browser...")
            driver.quit()
            return True
        except NoSuchElementException as err:
            logger.debug("Unable to identify the conversation with the landlord")
            driver.quit()
            return False
        except (TimeoutException, WebDriverException) as err:
            logger.exception("Unexpected driver problem")
            return False
    except (TimeoutException, WebDriverException) as err:
        logger.exception("Unexpected driver problem")
        return False

    close_security_advice_alert(driver)

    submit_button = find_submit_btn(driver)
    text_area = find_input_txt(driver)

    if not text_area and not submit_button:
        logger.debug("Already sent message to this offer, closing the browser...")
        driver.quit()
        return True
    elif not text_area or not submit_button:
        driver.quit()
        return False

    logger.debug("Writing message...")
    text_area.clear()
    text_area.send_keys(config['message'])
    logger.debug("Sending message...")
    submit_button.click()
    
    time.sleep(1)

    driver.quit()
    logger.debug("Sent")
    return True


def driver_connect(url):
    for tries in range(0, MAX_TRIES):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1600,900")
            options.add_argument("user-data-dir=selenium")
            # options.headless = True

            logger.debug("Opening the browser")
            driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        except (TimeoutException, WebDriverException) as err:
            if tries + 1 == MAX_TRIES:
                return None
            if not check_connection():
                time.sleep(30)
            logger.info("Retrying...")

        try:
            driver.get(url)
            return driver
        except (TimeoutException, WebDriverException) as err:
            if tries + 1 == MAX_TRIES:
                return None
            if not check_connection():
                time.sleep(30)
            logger.info("Retrying...")
        driver.quit()

    return None


def find_submit_btn(driver):
    try:
        return driver.find_element(By.XPATH, XPATH_SUBMIT_BTN)
    except NoSuchElementException:
        logger.debug("Cannot find 'submit' button")
        return None


def find_input_txt(driver):
    try:
        return driver.find_element(By.XPATH, XPATH_INPUT_TXT)
    except NoSuchElementException:
        logger.debug("Cannot find 'start new conversation' textarea")
        driver.quit()
        return False


def set_lang(driver):
    try:
        lang_button = driver.find_element(By.XPATH, XPATH_LANG_BTN)
        logger.debug("Setting lang to EN...")
        lang_button.click()

        lang_en_button = driver.find_element(By.XPATH, XPATH_LANG_ENG_BTN)
        lang_en_button.click()
        time.sleep(5)
    except NoSuchElementException:
        pass


def close_security_advice_alert(driver):
    try:
        agree_button = driver.find_element(By.ID, "sicherheit_bestaetigung")
        logger.debug("Closing security advice alert...")
        agree_button.click()
    except NoSuchElementException:
        pass


def accept_cookies(driver):
    try:
        accept_button = driver.find_element(By.XPATH, XPATH_COOKIES_ACCEPT)
        logger.debug("Closing cookies alert...")
        accept_button.click()
    except NoSuchElementException:
        pass


def try_to_login(driver, config):
    try:
        login_dialog_button = driver.find_element(By.XPATH, XPATH_LOGIN_NAV)
        logger.debug("Login...")
        login_dialog_button.click()

        driver.implicitly_wait(1)
        email = driver.find_element(By.ID, 'login_email_username')
        email.send_keys(config['username'])
        passwd = driver.find_element(By.ID, 'login_password')
        passwd.send_keys(config['password'])
        # Enabled by default
        # remember_button = driver.find_element(By.ID, 'auto_login')
        # remember_button.click()

        login_button = driver.find_element(By.ID, 'login_submit')
        login_button.click()
        # TODO Check that it is logged in correctly without errors
        logger.debug("Logged")
    except:
        pass


def check_connection():
    try:
        hostname = "one.one.one.one"
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    
    except Exception:
        return False
