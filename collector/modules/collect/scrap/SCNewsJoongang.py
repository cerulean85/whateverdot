import time
from abc import ABC

import requests
from bs4 import BeautifulSoup
import math
import config as cfg
import modules.collect.dir as dir
from modules.collect.scrap.SCScrapper import SCScrapper
from modules.dbconn import DBHandler


class SCNewsJoongang(SCScrapper, ABC):

    def __init__(self, work):
        super().__init__(work)

    def collect_probed_urls(self):
        self._probe()
        self._collect_urls()


    def _probe(self):
        url = cfg.get_probe_url(self.channel, self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
        result = requests.get(url=url)
        bsObj = BeautifulSoup(result.content, "html.parser")
        items = bsObj.findAll("span", {"class": "total_number"})

        try:
            _totalCountStr = str(items[0])
            _totalCountStrArr = _totalCountStr.split('/')
            _totalCountStr = _totalCountStrArr[1]
            _totalCountStr = _totalCountStr.replace(' ', '')
            _totalCountStr = _totalCountStr.replace('건<', '')
            _totalCountStr = _totalCountStr.replace(',', '')

            self.pred_total_article_count = int(_totalCountStr)
            self.pred_total_page_count = int(math.ceil(self.pred_total_article_count / 10))

            print(url, self.pred_total_article_count, self.pred_total_page_count)

        except Exception as err:
            print(err)

    def _collect_urls(self):
        self.start_date = self.start_date.replace('-', '')
        self.end_date = self.end_date.replace('-', '')
        for target_page_no in range(1, self.pred_total_page_count + 1):

            try:
                url_set = self._get_url(target_page_no)
                url_list = list(url_set)

                if len(url_list) > 0:
                    DBHandler().insert_urls(url_list, self.work)
                    print("Inserted {} URLS: {}".format(self.channel, len(url_list)))

                time.sleep(0.5)
            except Exception as e:
                print(e)



    def _get_url(self, target_page_no):
        url_set = set([])
        if int(self.pred_total_page_count) > 0:
            url = cfg.get_collect_url(self.channel, target_page_no, self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
            try:
                result = requests.get(url=url)
                bsObj = BeautifulSoup(result.content, "html.parser")
                items = bsObj.findAll("ul", {"class": "list_default"})
                for item in items:
                    __headline = item.findAll("h2", {"class": "headline"})
                    for _h in __headline:
                        addr = _h.find("a").attrs['href']
                        url_set.add(addr)
            except Exception as e:
                print(e)

        return url_set