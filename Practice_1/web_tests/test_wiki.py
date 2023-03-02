from loguru import logger

import undetected_chromedriver
from selenium.webdriver.common.by import By
from urllib.parse import unquote


class Wiki_tester():
    def __init__(self) -> None:
        self.driver = undetected_chromedriver.Chrome()
        logger.info('[+] Driver is ready')

    def _open_wiki_page(self) -> None:
        try:
            self.driver.get('https://ru.wikipedia.org')
            logger.info('[+] Wikipedia page is opened')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _input_search_query(self, search_query: str) -> None:
        try:
            search_field = self.driver.find_element(
                By.CLASS_NAME, 'vector-search-box-input')
            search_field.send_keys(search_query)
            logger.info(f'[+] Search query "{search_query}" is entered')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def _press_search_button(self):
        try:
            search_button = self.driver.find_element(By.ID, 'searchButton')
            search_button.click()
            logger.info('[+] Search button is pressed')

        except Exception as e:
            logger.error(f'[!] Error: {e}')

    def check_wiki_search_result(self, final_link: str) -> None:
        """check if search result contains link to page

        Args:
            link (str): final link to page
        """
        try:
            # find link in rel = "canonical" tag and catch href attribute
            link = self.driver.find_element(
                By.XPATH, '/html/head/link[11]').get_attribute('href')
            # decode '/%D0%A0%D0%BE%D1%81%D1%81%D1%83%D0%BC' to 'Россум'
            link = unquote(link)
            assert link == final_link
            logger.success(
                f'[+] Link "{link}" is found for search query "{final_link}" on Wikipedia; test passed')
        except Exception as e:
            logger.error(f'[!] Error while trying to find link "{link}": {e}')

    def search_on_wiki(self, search_query: str, final_link: str = None):
        """search on wikipedia and log result

        Args:
            search_query (str): search query for wikipedia
            final_link (str, optional): estimated final link to page. Defaults to None.
        """
        if not final_link:
            logger.warning(
                f'[!] Final link is not provided for search query "{search_query}"')
        self._open_wiki_page()
        self._input_search_query(search_query)
        self._press_search_button()

        if final_link:
            self.check_wiki_search_result(final_link)
        else:  # if final link is not provided, log link from search result
            try:
                # find link in rel = "canonical" tag and catch href attribute
                link = self.driver.find_element(
                    By.XPATH, '/html/head/link[11]').get_attribute('href')
                assert link

                # decode '/%D0%A0%D0%BE%D1%81%D1%81%D1%83%D0%BC' to 'Россум'
                link = unquote(link)
                logger.success(
                    f'[+] Link "{link}" is found for search query "{search_query}" on Wikipedia; test passed')
            except Exception as e:
                logger.error(
                    f'[!] Error while trying to find link for search query "{search_query}" on Wikipedia: {e}')

    def __del__(self):
        self.driver.quit()
        logger.info('[+] Driver is closed')


if __name__ == '__main__':

    # create instance of Tester class
    tester = Wiki_tester()
    tester.search_on_wiki('heap sort')
    tester.search_on_wiki('Guido van Rossum')
    tester.search_on_wiki('Python', 'https://ru.wikipedia.org/wiki/Python')
