import time
from abc import *
import config as cfg
import modules.collect.dir as dir
from selenium import webdriver

from modules.dbconn import DBHandler


class CollectorStrategy(metaclass=ABCMeta):

    @abstractmethod
    def collect_urls(self, work):
        pass

    @abstractmethod
    def collect_docs(self, work):
        pass

    def write_file(self, file_info):

        with open(file_info["filepath"] + '/' + file_info["filename"], "w", encoding="utf-8") as f:
            f.write(str(file_info["source"]))
        print('Written {}...'.format(file_info["filename"]))

    def docs_batch_collection(self, work):
        # print("collect docs")

        channel = work["channel"]
        work_group_no = work["work_group_no"]
        work_no = work["work_no"]

        print(channel, work_group_no)

        dbh = DBHandler()
        url_objs = dbh.find_item({"work.work_group_no": work_group_no, "work.work_no": work_no},
                              db_name="whateverdot", collection_name="urls")

        conf = cfg.get_config(path=dir.config_path)
        file_path = conf["storage"]["save_dir"] + channel
        index = 0
        chromeDriver = cfg.get_chrome_driver(dir.config_path)
        for item in url_objs:
            url = item["url"]
            chromeDriver.get(url)
            file_info = {
                "channel": channel,
                "source": chromeDriver.page_source,
                "filepath": file_path,
                "filename": channel + "_web_doc_" + str(work_group_no) + '_' + str(work_no) +
                             '_' + str(index+1) + ".html"
            }

            self.write_file(file_info)
            time.sleep(conf[channel]["delay_time"])
            index += 1

        chromeDriver.quit()

        dbh.update_item_many(
            condition={"work.work_group_no": work_group_no, "work.work_no": work_no},
            update_value={"$set": {"save_path": file_path}},
            db_name="whateverdot", collection_name="urls")

