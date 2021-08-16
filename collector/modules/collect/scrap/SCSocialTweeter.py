import datetime as dt

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import hashlib
import config as cfg

class SCSocialTweeter:

    channel = "twt"

    def __init__(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('--no-sandbox')
        # options.add_argument('disable-gpu')
        options.set_capability('unhandledPromptBehavior', 'accept')
        self.chromeDriver = cfg.get_chrome_driver("../../")

    def __get_scrap_url(self, keyword, start_date, end_date):
        return 'https://twitter.com/search?q=' + keyword + '%20since%3A' + str(start_date) + '%20until%3A' + str(
            end_date)

    def write_file(self, file_count, file_no, soup):
        filename = self.channel + "_web_doc_" + str(file_count) + '_' + str(file_no) + '.html'
        with open(cfg.SAVE_DIR + self.channel + "/" + filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print('Written {}...'.format(filename))
        return file_no + 1

    def get_web_doc(self, work):

        file_count = 1
        keyword = work["keyword"].replace('_', ' ')

        start_date = work["start_dt"].replace('-', '')
        start_date = dt.date(year=int(start_date[0:4]), month=int(start_date[4:6]), day=int(start_date[6:8]))

        end_date = work["end_dt"].replace('-', '')
        end_date = dt.date(year=int(end_date[0:4]), month=int(end_date[4:6]), day=int(end_date[6:8]))

        until_date = start_date + dt.timedelta(days=1)

        while not end_date == start_date:
            url = self.__get_scrap_url(keyword, start_date, until_date)
            self.chromeDriver.get(url)
            lastHeight = self.chromeDriver.execute_script("return document.body.scrollHeight")

            file_no = 1
            while True:

                self.chromeDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(cfg.DELAY_SECONDS if file_no == 1 else 5)

                newHeight = self.chromeDriver.execute_script("return document.body.scrollHeight")
                soup = BeautifulSoup(self.chromeDriver.page_source, "html.parser")
                file_no = self.write_file(file_count, file_no, soup)
                if newHeight == lastHeight:
                    print("{} - {}, {}".format(file_count, start_date, until_date))
                    start_date = until_date
                    until_date += dt.timedelta(days=1)
                    self.write_file(file_count, file_no, soup)
                    file_count = file_count + 1
                    break

                lastHeight = newHeight

# if __name__ == "__main__":
#     sct = SCSocialTweeter()
#     sct.get_web_doc(scc.KEYWORD, scc.START_DATE, scc.END_DATE)
