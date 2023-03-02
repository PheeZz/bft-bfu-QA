from web_tests import Wiki_tester, Stackoverflow_tester, YouTube_tester
from utils import setup_logger

if __name__ == '__main__':
    setup_logger()
    wiki_tester = Wiki_tester()
    wiki_tester.search_on_wiki('heap sort')
    wiki_tester.search_on_wiki('Guido van Rossum')
    stackoverflow_tester = Stackoverflow_tester()
    stackoverflow_tester.login_site()
    stackoverflow_tester.logout_site()

    YouTube_tester().search_on_yt('Rick Astley')
