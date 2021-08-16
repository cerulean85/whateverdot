import time

from modules.collect.CollectorStrategy import CollectorStrategy
from modules.collect.scrap.SCNewsJoongang import SCNewsJoongang


class CollectorJoongang(CollectorStrategy):

    def collect_docs(self, work):
        self.docs_batch_collection(work)


    def collect_urls(self, work):
        # while True:
        #     print("collect url 중앙일보 test")
        #     time.sleep(1)

        scp = SCNewsJoongang(work)
        scp.collect_probed_urls()

# if __name__ == "__main__":
#
#     work = WorkProtocolService_pb2.Work
#     work.keyword = "ㅋㅋㅋ"
#     work.start_dt = "2021-01-01"
#     work.end_dt = "2021-01-03"
#     CollectorTweeter().collect_docs(work)
