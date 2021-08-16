import time

import config as conf
import requests
from bs4 import BeautifulSoup
import math


class SCNewsDonga:

    def __init__(self):
        self.url_list = []
        self.pred_total_article_count = 0
        self.pred_total_page_count = 0
        self.keyword = ''
        self.start_date = ''
        self.end_date = ''

    def start(self, keyword, start_date, end_date):

        self.keyword = keyword
        self.start_date = start_date
        self.end_date = end_date

        self.probe()
        self.collect_url()
        self.get_web_doc()

    def __get_url(self, target_page_no):
        url_set = set([])
        if int(self.pred_total_page_count) > 0:
            url = conf.get_collect_url('donga', target_page_no, self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
            # print(url)
            try:
                result = requests.get(url=url)
                bsObj = BeautifulSoup(result.content, "html.parser")
                time.sleep(0.5)
                items = bsObj.findAll("div", {"class": "searchList"})

                tags = [
                    [{'tag': 'p', 'class': 'txt'}],
                    [{'tag': 'div', 'class': 'p'}],
                    [{'tag': 'div', 'class': 't'}, {'tag': 'p', 'class': 'txt'}]
                ]

                for item in items:
                    __p = ''
                    for i in range(0, len(tags)):
                        tarr = tags[i]
                        for j in range(0, len(tarr)):
                            t = tarr[j]
                            try:
                                if j == 0:
                                    __p = item.find(t['tag'], {"class": t['class']})
                                else:
                                    __p = __p.find(t['tag'], {"class": t['class']})
                            except:
                                continue

                    if __p != '':
                        try:
                            addr = __p.find("a").attrs['href']
                        except:
                            addr = ''

                    url_set.add(addr)
            except Exception as e:
                print(e)

        return url_set

    def write_file(self, file_count, soup):
        filename = "dna_web_doc_" + str(file_count) + '.html'
        with open("D:/__programming/__data2/dna/" + filename, "w", encoding="utf-8") as f:
            f.write(str(soup))
        print('Written {}...'.format(filename))
        return file_count + 1

    def get_web_doc(self):
        file_count = 1
        for url in self.url_list:
            try:
                result = requests.get(url=url)
                soup = BeautifulSoup(result.content, "html.parser")
                file_count = self.write_file(file_count, soup)
            except Exception as e:
                print(e)

    def collect_url(self):
        self.start_date = self.start_date.replace('-', '')
        self.end_date = self.end_date.replace('-', '')
        for target_page_no in range(1, self.pred_total_page_count + 1):

            try:
                url_set = self.__get_url(target_page_no)
                self.url_list = self.url_list + list(url_set)
                time.sleep(0.5)
                print(target_page_no,':', len(url_set))
            except Exception as e:
                print(e)

    def probe(self):
        url = conf.get_probe_url('donga', self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
        result = requests.get(url=url)
        bsObj = BeautifulSoup(result.content, "html.parser")
        items = bsObj.findAll("h2")

        try:
            _totalCountStr = str(items[0].findAll("span")[0])
            _totalCountStr = _totalCountStr.replace('총 ', '')
            _totalCountStr = _totalCountStr.replace(' 건 검색', '')
            _totalCountStr = _totalCountStr.replace('<span>(', '')
            _totalCountStr = _totalCountStr.replace(')</span>', '')

            self.pred_total_article_count = int(_totalCountStr)
            self.pred_total_page_count = int(math.ceil(self.pred_total_article_count / 15))

            print(url, self.pred_total_article_count, self.pred_total_page_count)

        except Exception as err:
            print(err)


if __name__ == "__main__":
    scj = SCNewsDonga()
    scj.start("코로나_백신", "2021-02-26", "2021-06-30")

