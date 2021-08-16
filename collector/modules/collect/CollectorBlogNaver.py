import time

from modules.collect.CollectorStrategy import CollectorStrategy
from modules.collect.scrap.SCBlogNaver import SCBlogNaver


class CollectorBlogNaver(CollectorStrategy):

    def collect_docs(self, work):
        self.docs_batch_collection(work)

    def collect_urls(self, work):
        scp = SCBlogNaver(work)
        scp.collect_probed_urls()
