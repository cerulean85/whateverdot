import os

from modules.dbconn import DBHandler
from modules.extractor.TFBase import TFBase
from modules.extractor.TFWebDoc import TFWebDoc
import numpy as np
import pandas as pd
from multiprocessing import Value

from modules.zhbase.ZHPandas import ZHPandas
from modules.zhbase.ZHParallel import ZHParallel
import config as cfg

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
pd.set_option('display.max_columns', None)  ## 모든 열을 출력한다.
pd.set_option('display.max_rows', None)  ## 모든 열을 출력한다.


def create_doc_text_blocks(channel, target_path, file_list, finished_file_count, total_file_count, keyword, work_group_no, work_no):
# def create_doc_text_blocks(ext):
    target_file_list = []
    tfe = TFExtractor()
    for file in file_list:
        if "html" in file:
            target_file_list.append(file)

    dhb = DBHandler()
    for file in target_file_list:
        try:
            wd = TFWebDoc()
            filename = file
            tb_data = wd.create_text_blocks(channel, target_path, filename, keyword)
            for item in tb_data:
                item["work_group_no"] = work_group_no
                item["work_no"] = work_no
            dhb.insert_item_many(tb_data, db_name="whateverdot", collection_name="docs")
            # tfe.web_doc_list.append(wd)
            finished_file_count.value += 1
            print("Written [{}] - [{}/{}] ...".format(file, finished_file_count.value, total_file_count))
        except Exception as e:
            print(e)


def get_total_count(channel_type, target_path, file_list):
    total_block_count = 0

    zhp = ZHPandas()
    for filename in file_list:
        if ".csv" not in filename:
            continue

        df = zhp.read_csv(filename)
        total_block_count += len(df)

    print("Channel: {}".format(channel_type))
    print("Total File Count: {}".format(len(file_list)))
    print("Total Block Count: {}".format(total_block_count))
    print("Target Path: {}".format(target_path))

    return len(file_list), format(total_block_count)


class TFExtractor(TFBase):

    def __init__(self):
        super().__init__()
        self.web_doc_list = []

    def get_web_doc_list(self, file_list):
        total_block_count = 0

        zhp = ZHPandas()
        for filename in file_list:
            if ".csv" not in filename:
                continue

            df = zhp.read_csv(filename)
            total_block_count += len(df)

        print("Total File Count: {}, Total Block Count: {}".format(len(file_list), total_block_count))


if __name__ == '__main__':

    # tfb = TFBase()
    p_count = 4
    # channel_type = "tweeter"

    work_collect_doc_list = []
    work2 = {}
    work2["channel"] = "jna"
    work2["keyword"] = "코로나_백신"
    work2["start_dt"] = "2021-01-01"
    work2["end_dt"] = "2021-01-03"
    work2["work_type"] = "collect_doc"
    work2["work_group_no"] = "12"
    work2["work_no"] = "100"
    work_collect_doc_list.append(work2)

    channel = work2["channel"]
    keyword = work2["keyword"]
    work_group_no = work2["work_group_no"]
    work_no = work2["work_no"]
    target_path = cfg.SAVE_DIR + work2["channel"] + '/'
    file_list = [file for file in os.listdir(target_path) if ".html" in file]

    zhp = ZHParallel()
    total_file_count = len(file_list)
    finished_file_count = Value('i', 0)
    unit_count = int(len(file_list) / p_count)
    remain_count = len(file_list) % p_count

    ei = 0
    for i in range(0, p_count):
        si = unit_count * i
        ei = unit_count * (i + 1)
        zhp.add(create_doc_text_blocks,
                (channel, target_path, file_list[si:ei], finished_file_count, total_file_count, keyword, work_group_no, work_no))

    if remain_count > 0:
        si = ei
        ei = ei + remain_count
        zhp.add(create_doc_text_blocks,
                (channel, target_path, file_list[si:ei], finished_file_count, total_file_count, keyword, work_group_no, work_no))

    zhp.start()
