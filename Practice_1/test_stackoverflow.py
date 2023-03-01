from loguru import logger

import undetected_chromedriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote
import time

class Stackoverflow_tester():
    def __init__(self) -> None:
        self.driver = undetected_chromedriver.Chrome()
        logger.info('[+] Driver is ready')

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


if '__main__' == __name__:
    stackoverflow_tester = Stackoverflow_tester()
    stackoverflow_tester._open_stackoverflow_page()
    stackoverflow_tester._press_login_button()
    time.sleep(5)