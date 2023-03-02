from loguru import logger
import time
from os import getenv
from dotenv import load_dotenv

import undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Stackoverflow_tester():
    def __init__(self) -> None:
        self.driver = undetected_chromedriver.Chrome()
        logger.info('[+] Driver is ready')

        load_dotenv(override=True)
        self.LOGIN = getenv('STACKOVERFLOW_LOGIN')
        self.PASSWORD = getenv('STACKOVERFLOW_PASSWORD')
        logger.info('[+] Login and password for stackoverflow are loaded')

    def _open_stackoverflow_page(self) -> None:
        try:
            self.driver.get('https://stackoverflow.com')
            logger.info('[+] Stackoverflow page is opened')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _press_login_button(self) -> None:
        try:
            login_button = self.driver.find_element(
                By.LINK_TEXT, 'Log in')
            login_button.click()
            logger.info('[+] Login button is pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _input_login(self) -> None:
        try:
            # sleep driver for 2 seconds
            time.sleep(2)

            login_field = self.driver.find_element(
                By.ID, 'email')
            login_field.send_keys(self.LOGIN)
            logger.info(f'[+] Login "{self.LOGIN}" is entered')
        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _input_password(self) -> None:
        try:
            password_field = self.driver.find_element(
                By.ID, 'password')
            password_field.send_keys(self.PASSWORD)
            logger.info(f'[+] Password "{self.PASSWORD}" is entered')
        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _press_submit_button(self) -> None:
        try:
            submit_button = self.driver.find_element(
                By.ID, 'submit-button')
            submit_button.click()
            logger.info('[+] Submit button is pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def login_site(self):
        self._open_stackoverflow_page()
        self._press_login_button()
        self._input_login()
        self._input_password()
        self._press_submit_button()

    def _check_is_logged(self) -> None:

        try:
            # find a tag with href ending with 'inbox'
            assert self.driver.find_element(
                By.XPATH, '//a[contains(@href, "inbox")]')
            # find a tag with href ending with 'users/logout'
            assert self.driver.find_element(
                By.XPATH, '//a[contains(@href, "users/logout")]')

            logger.success('[+] User is logged in')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _find_logout_link(self) -> None:
        try:
            logout_link = self.driver.find_element(
                By.XPATH, '//a[contains(@href, "users/logout")]')
            assert logout_link
            self.driver.get(logout_link.get_attribute('href'))
            logger.info('[+] Logout link is found and pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _approve_logout(self) -> None:
        try:
            time.sleep(2)
            # find a button with text inside 'Log out', element <button>
            logout_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log out")]')))
            assert logout_button
            logout_button.click()
            logger.info('[+] Logout button is pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _check_logout(self) -> None:
        try:
            assert self.driver.find_element(
                By.LINK_TEXT, 'Log in')
            logger.success('[+] User is logged out')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def logout_site(self):
        self._check_is_logged()
        self._find_logout_link()
        self._approve_logout()
        self._check_logout()


if '__main__' == __name__:
    stackoverflow_tester = Stackoverflow_tester()
    stackoverflow_tester.login_site()
    time.sleep(2)
    stackoverflow_tester.logout_site()
