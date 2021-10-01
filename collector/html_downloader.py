import json
import os

import config as cfg
import kkconn
import modules.collect.dir as dir
import time
import pandas as pd
from collections import Counter
import sys


def work():
    conf = cfg.get_config(path=dir.config_path)
    consumer = kkconn.kafka_consumer("urls")
    chromeDriver = cfg.get_chrome_driver(dir.config_path)

    while True:
        print("Waiting...")
        # time.sleep(60)
        records = consumer.poll(3000)
        for tp, record in records.items():

            url_counter_dict = {}
            for item in record:
                url_info = json.loads(str(item.value.decode('utf-8')))

                channel = url_info["channel"]
                work_no = url_info["work_no"]
                work_group_no = url_info["work_group_no"]
                date = url_info["date"]
                keyword = url_info["keyword"].replace("'", "")

                if url_counter_dict.get(channel) is None:
                    url_counter_dict[channel] = {
                        "counter": Counter(),
                        "work_group_no": work_group_no,
                        "work_no": work_no,
                        "keyword": keyword,
                        "date": date
                    }

                url_counter_dict[channel]["counter"].update(url_info["urls"])

            for channel, value in url_counter_dict.items():
                work_no = value["work_no"]
                work_group_no = value["work_group_no"]
                keyword = value["keyword"]
                date = value["date"]
                for url_count in value["counter"].items():
                    url = url_count[0]
                    dup_count = url_count[1]

                    if dup_count > 3:
                        print("Dup File Info: {}, {}, {}, {}, {}, {}".
                              format(url, dup_count, work_no, work_group_no, keyword, date))
                        continue

                    file_path = conf["storage"]["save_dir"] + channel
                    switch_to_iframe = conf[channel]["switch_to_iframe"]
                    try:
                        chromeDriver.get(url)
                    except:
                        print("Can't collect {}".format(url))
                        continue

                    if switch_to_iframe:
                        try:
                            iframe = chromeDriver.find_element_by_tag_name('iframe')
                            chromeDriver.switch_to.frame(iframe)
                            time.sleep(1)
                        except Exception as e:
                            print(e)
                            continue

                    index = len(os.listdir(file_path)) - 1
                    file_info = {
                        "channel": channel,
                        "source": chromeDriver.page_source,
                        "filepath": file_path,
                        "filename": "{}_{}_{}_{}_{}_{}.html".
                            format(channel, str(work_group_no), str(work_no), keyword, date.replace('-', ''),
                                   str(index + 1))
                    }

                    filename = file_info["filepath"] + '/' + file_info["filename"]
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(str(file_info["source"]))

                    time.sleep(3)
                    print('Written {}...'.format(file_info["filename"]))

    # for record in records:
    #     print(record.value)
    # url_info = json.loads(str(message.value.decode('utf-8')))
    # url_counter.update(url_info["urls"])
    # for item in url_counter.items():
    #     print(item[0], item[1], count)
    # channels = []
    # for message in consumer:
    #     url_info = json.loads(str(message.value.decode('utf-8')))
    #     url_counter.update(url_info["urls"])
    #     for item in url_counter.items():
    #         print(item[0], item[1], count)

    # channels.append(url_info["channel"])
    # print(url_info)
    # url_info = zhp.create_data_frame_to_dict(url_info)
    # print(url_info, count)
    # print( url_info["channel"] + str(count))
    # print(count)
    # print(len(channels))
    # channel = ""
    # work_group_no, work_no = 0, 0
    # url_objs = []
    #
    # conf = cfg.get_config(path=dir.config_path)
    # file_path = conf["storage"]["save_dir"] + channel
    # switch_to_iframe = conf[channel]["switch_to_iframe"]
    # index = 0
    # chromeDriver = cfg.get_chrome_driver(dir.config_path)
    #
    # for item in url_objs:
    #     url = item["url"]
    #     chromeDriver.get(url)
    #
    #     if switch_to_iframe:
    #         try:
    #             iframe = chromeDriver.find_element_by_tag_name('iframe')
    #             chromeDriver.switch_to.frame(iframe)
    #             time.sleep(1)
    #         except Exception as e:
    #             print(e)
    #             continue
    #
    #     file_info = {
    #         "channel": channel,
    #         "source": chromeDriver.page_source,
    #         "filepath": file_path,
    #         "filename": channel + "_web_doc_" + str(work_group_no) + '_' + str(work_no) + '_' + str(index + 1)
    #     }
    #
    #     with open(file_info["filepath"] + '/' + file_info["filename"], "w", encoding="utf-8") as f:
    #         f.write(str(file_info["source"]) + ".html")
    #     print('Written {}...'.format(file_info["filename"]))
    #
    #     time.sleep(conf[channel]["delay_time"])
    #     index += 1
    #
    # chromeDriver.quit()


work()
