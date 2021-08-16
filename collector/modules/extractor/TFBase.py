from modules.extractor import TFExtractorConfig
from modules.extractor.TFFile import TFFile


class TFBase:
    def __init__(self):
        self.tfg = TFExtractorConfig
        self.tff = TFFile()
        self.target_path = {

            "naver_blog": {
                "prefix": self.tfg.TARGET_DIR_PATH + "nav5/",
                "predict": self.tfg.TARGET_DIR_PATH + "nav5/" + self.tfg.TARGET_DIR_PATH_PRED,
                "label": self.tfg.TARGET_DIR_PATH + "nav5/" + self.tfg.TARGET_DIR_PATH_LBEL
            },

            "tweeter": {
                "prefix": self.tfg.TARGET_DIR_PATH + "twt/",
                "predict": self.tfg.TARGET_DIR_PATH + "twt/" + self.tfg.TARGET_DIR_PATH_PRED,
                "label": self.tfg.TARGET_DIR_PATH + "twt/" + self.tfg.TARGET_DIR_PATH_LBEL
            },

            "joongang": {
                "prefix": self.tfg.TARGET_DIR_PATH + "jna/",
                "predict": self.tfg.TARGET_DIR_PATH + "jna/" + self.tfg.TARGET_DIR_PATH_PRED,
                "label": self.tfg.TARGET_DIR_PATH + "jna/" + self.tfg.TARGET_DIR_PATH_LBEL
            },

            "instagram": {
                "prefix": self.tfg.TARGET_DIR_PATH + "ins/",
                "predict": self.tfg.TARGET_DIR_PATH + "ins/" + self.tfg.TARGET_DIR_PATH_PRED,
                "label": self.tfg.TARGET_DIR_PATH + "ins/" + self.tfg.TARGET_DIR_PATH_LBEL
            },

            "donga": {
                "prefix": self.tfg.TARGET_DIR_PATH + "dna/",
                "predict": self.tfg.TARGET_DIR_PATH + "dna/" + self.tfg.TARGET_DIR_PATH_PRED,
                "label": self.tfg.TARGET_DIR_PATH + "dna/" + self.tfg.TARGET_DIR_PATH_LBEL
            },
        }

    def get_target_prefix_path(self, target_channel_type):
        t = self.target_path[target_channel_type]
        return t["prefix"]

    def get_target_path(self, target_channel_type, target_ext_type):
        t = self.target_path[target_channel_type]
        return t[target_ext_type]

