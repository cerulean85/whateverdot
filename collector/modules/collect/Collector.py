import copy
import os
import time
from multiprocessing import Process

import proto.WorkProtocolService_pb2 as WorkProtocol
from modules.collect.CollectorFactory import CollectorFactory
import modules.parallel as prl
from proto import WorkProtocolService_pb2
import multiprocessing as mp

class Collector:

    def test(self):
        print("ㅋㅋㅋ123123ㅋ")

    def collect_urls(self, works):
        work_type = "collect_url"
        print(work_type)
        for work in works:
            collector = CollectorFactory().create_instance(work["channel"])
            prl.add_proc(work, Process(target=collector.collect_urls, args=(work,)))
        prl.start_procs(work_type)

    # def start_collect_docs(self, works):
    #     collector.__collect_docs(works)

    def collect_docs(self, works):
        work_type = "collect_doc"
        print(work_type)

        for work in works:
            prl.stop_procs(work, "collect_url")

        for work in works:
            time.sleep(2)
            collector = CollectorFactory().create_instance(work["channel"])
            prl.add_proc(work, Process(target=collector.collect_docs, args=(work,)))

        prl.start_procs(work_type)


# if __name__ == "__main__":
#
#     collector = Collector()



    # time.sleep(30)
    #
    # work_list2 = []
    # work2 = {}
    # work2["channel"] = "nav"
    # work2["keyword"] = "코로나_백신"
    # work2["start_dt"] = "2021-01-01"
    # work2["end_dt"] = "2021-01-03"
    # work2["work_type"] = "collect_doc"
    # work2["work_group_no"] = "11"
    # work2["work_no"] = "100"
    # work_list2.append(work2)
    #
    # work3 = {}
    # work3["channel"] = "jna"
    # work3["keyword"] = "코로나_백신"
    # work3["start_dt"] = "2021-01-01"
    # work3["end_dt"] = "2021-01-03"
    # work3["work_type"] = "collect_doc"
    # work3["work_group_no"] = "12"
    # work3["work_no"] = "100"
    # work_list2.append(work3)
    #
    # collector.collect_docs(work_list2)