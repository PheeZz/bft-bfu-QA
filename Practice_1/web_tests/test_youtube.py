from loguru import logger

import undetected_chromedriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class YouTube_tester():
    def __init__(self) -> None:
        self.driver = undetected_chromedriver.Chrome()
        logger.info('[+] Driver is ready')

    def _open_yt_page(self) -> None:
        try:
            self.driver.get('https://www.youtube.com')
            logger.info('[+] Youtube page is opened')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _input_search_query(self, search_query: str) -> None:
        try:
            # search field is <input id="search" ...>
            search_field = self.driver.find_element(
                By.XPATH, '//input[@id="search"]')
            assert search_field
            search_field.send_keys(search_query)
            logger.info(f'[+] Search query "{search_query}" is entered')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _press_search_button(self):
        try:
            search_button = self.driver.find_element(
                By.ID, 'search-icon-legacy')
            assert search_button.is_displayed()
            search_button.click()
            logger.info('[+] Search button is pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _open_first_video(self):
        """open first video in search results by clicking first video title"""
        try:
            # find first video title in <a id="video-title" ...> tag that
            first_video_title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="video-title"]')))
            assert first_video_title.is_displayed()
            first_video_title.click()
            logger.info('[+] First video is opened')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _check_video_title(self, sq_video_title: str) -> None:
        """check if video title contains search query

        Args:
            video_title (str): video title
        """
        try:
            # find video title in h1 tag that not hidden and has class "style-scope ytd-watch-metadata"
            # wait while page is loaded

            # WebDriverWait(self.driver, 15).until(
            #     EC.presence_of_element_located((By.XPATH, '//h1[@class="style-scope ytd-watch-metadata"]')))
            # i have no idea why this doesn't work, so i use time.sleep
            time.sleep(5)
            title = self.driver.find_element(
                By.XPATH, '//h1[@class="style-scope ytd-watch-metadata"]').text

            if sq_video_title in title:
                logger.success(
                    f'[+] Video title "{title}" contains search query "{sq_video_title}"; test passed')
            if sq_video_title not in title:
                logger.warning(
                    f'[!] Video title "{title}" does not equal search query "{sq_video_title}"; test failed')

            if 'Rick Astley' in title or 'Never Gonna Give You Up' in title:
                logger.warning(
                    f'[!] You are successfully Rickrolled!')
                time.sleep(5)

        except Exception as e:
            logger.error(
                f'[!] Error while trying to find video title "{title}": {e}')

    def search_on_yt(self, search_query: str, video_title: str = None):
        """search on youtube and log result

        Args:
            search_query (str): search query
            video_title (str, optional): video title. Defaults to None.
        """
        self._open_yt_page()
        self._input_search_query(search_query)
        self._press_search_button()
        self._open_first_video()

        if video_title:
            self._check_video_title(video_title)

        self.driver.quit()

    def __del__(self):
        self.driver.quit()
        logger.info('[+] Driver is closed')


if __name__ == '__main__':
    yt_tester = YouTube_tester()
    yt_tester.search_on_yt(
        search_query='Rick Astley',
        video_title='Rick Astley - Never Gonna Give You Up')
