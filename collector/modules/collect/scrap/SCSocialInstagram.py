import datetime as dt

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import hashlib

from selenium.webdriver.common.keys import Keys
import config as cfg
import modules.collect.dir as dir
from modules.collect.scrap.SCScrapper import SCScrapper
from modules.dbconn import DBHandler
from abc import ABC


class SCSocialInstagram(SCScrapper, ABC):

    def __init__(self, work):
        super().__init__(work)
        self.chromeDriver = cfg.get_chrome_driver(config_path=dir.config_path)

    def collect_probed_urls(self):
        self.login()
        self._collect_urls()
        self.chromeDriver.quit()

    def _get_url(self, keyword):
        return 'https://www.instagram.com/explore/tags/' + keyword

    def login(self):

        conf = cfg.get_config(path="../../")
        self.chromeDriver.get(conf[self.channel]["domain"])
        time.sleep(3)
        elem = self.chromeDriver.find_element_by_name("username")
        elem.send_keys(conf[self.channel]["account"]["id"])

        elem = self.chromeDriver.find_element_by_name("password")
        elem.send_keys(conf[self.channel]["account"]["pass"])
        elem.send_keys(Keys.RETURN)

        time.sleep(5)
        elem = self.chromeDriver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        self.chromeDriver.execute_script("arguments[0].click();", elem)

        time.sleep(2)
        elem = self.chromeDriver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
        self.chromeDriver.execute_script("arguments[0].click();", elem)

    def _collect_urls(self):

        keyword = self.keyword.replace('_', '')
        url = self._get_url(keyword)
        self.chromeDriver.get(url)
        time.sleep(3)

        file_no = 1
        while True:
            a_list = self.chromeDriver.find_elements_by_tag_name('a')

            url_list = []
            for a in a_list:
                try:
                    url = a.get_attribute("href")
                    if not str(url).find("https://www.instagram.com/p/"):
                        url_list.append(url)
                        self.print_url(url)
                except:
                    continue

            if len(url_list) == 0:
                continue

            DBHandler().insert_urls(url_list, self.work)

            self.chromeDriver.execute_script("window.scrollTo(0, window.scrollY - 50);")
            time.sleep(0.5)
            self.chromeDriver.execute_script("window.scrollTo(0, window.scrollY + 800);")

            file_no += 1

            f = open("../config.txt", 'r')
            delay_time = float(f.read())
            f.close()

            time.sleep(delay_time)

# if __name__ == "__main__":
#     scf = SCSocialInstagram()
#     scf.login()
#     scf.get_web_urls(scc.KEYWORD)
