import time

from modules.collect.CollectorStrategy import CollectorStrategy
from modules.collect.scrap.SCSocialTweeter import SCSocialTweeter


class CollectorTweeter(CollectorStrategy):

    def collect_docs(self, work):
        # scp = SCSocialTweeter()
        # scp.get_web_doc(work)
        while True:
            print("collect docs 트위터 test")
            time.sleep(1)

    def probe(self, work):
        pass

    def collect_urls(self, work):
        pass

# if __name__ == "__main__":
#
#     work = WorkProtocolService_pb2.Work
#     work.keyword = "ㅋㅋㅋ"
#     work.start_dt = "2021-01-01"
#     work.end_dt = "2021-01-03"
#     CollectorTweeter().collect_docs(work)
