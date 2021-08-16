import time

from modules.collect.CollectorStrategy import CollectorStrategy
from modules.collect.scrap.SCSocialInstagram import SCSocialInstagram


class CollectorInstagram(CollectorStrategy):

    def collect_docs(self, work):
        self.docs_batch_collection(work)

    def collect_urls(self, work):
        scp = SCSocialInstagram(work)
        scp.collect_probed_urls()