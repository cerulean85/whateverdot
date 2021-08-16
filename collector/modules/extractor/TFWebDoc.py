import collections
import re
from modules.extractor.TFBase import TFBase
from modules.extractor.TFPreProc import TFPreProc
from modules.extractor.TFTextBlock import TFTextBlock
import copy
import pandas as pd
from konlpy.tag import Okt
import config as cfg


class TFWebDoc(TFBase):
    def __init__(self):
        super().__init__()
        self.__org_src = ''
        self.__tb_arr = []
        self.line = 0
        self.__pproc = TFPreProc()
        self.__file_name = ''
        self.okt = Okt()
        self.ENABLED_TEXT_COUNT = 3

    def __explore_node(self, depth, parent_path_tags, prev_node_name, current_node, keyword):
        def get_tag_name(__node):
            tag = str(__node.tag).replace('{http://www.w3.org/1999/xhtml}', '')
            tag = tag.replace('{http://www.w3.org/2000/xhtml}', '')
            tag = tag.replace('{http://www.w3.org/2000/svg}', '')
            return tag

        depth = depth + 1
        pts = parent_path_tags
        pts.append(prev_node_name)

        for i in range(0, len(current_node)):
            node = current_node[i]
            tagname = get_tag_name(node)
            self.line = self.line + 1
            # if len(node) > 0 and node.text is not None:
            # txt = str(node.text).replace(' ', '')

            if len(node) == 0:
                tail_text = str(node.text)
                # print(tail_text)
                tail_text = self.__pproc.replace_words_prev(tail_text)
                tail_text = self.__pproc.clean_stopwords(tail_text)
                tail_text = self.__pproc.replace_words_post(tail_text)
                # m1 = re.compile('^\n$').match(tail_text)
                # m2 = re.compile('^[\s]+$').match(tail_text)
                eq_keyword = False
                keywords = keyword.split('_')
                for k in keywords:

                    if tail_text == k:
                        eq_keyword = True
                        break

                if tail_text != 'None' and len(tail_text) > self.ENABLED_TEXT_COUNT and not eq_keyword:
                    tail_text = re.sub('\n', '', tail_text, 0)
                    word_density = self.get_word_density(tail_text)
                    tb = TFTextBlock(self.line, tail_text, copy.deepcopy(pts), word_density, 0)
                    # print(tail_text)
                    self.__tb_arr.append(tb)

                # print("__explore_node {}, {} / {} ".format(depth, i, len(current_node)))
                continue

            # print("CHECK {} {}".format(len(current_node), i))
            self.__explore_node(depth, copy.deepcopy(pts), tagname, node, keyword)

        # print("exit __explore_node {}".format(depth))

    def get_tb_data(self, line, text, parent_tags, word_density, label):
        tags = ''
        for i in range(0, len(parent_tags)):
            tags += parent_tags[i] + ('' if i == (len(parent_tags) - 1) else '/')

        return str(line) + ',' + text + ',' + tags + ',' + str(word_density) + ',' + str(label) + '\n'

    def load_text_blocks(self, target_path, filename):
        self.__file_name = filename
        save_path = target_path + filename
        data = pd.read_csv(save_path)
        for i in range(0, len(data)):
            line = data['line'][i]
            text = data['text'][i]
            lb = data['lb'][i]
            word_density = data["word_density"][i]
            parent_tags_arr = (data['tags'][i]).split('/')
            tags_list = [tag for tag in parent_tags_arr]
            tb = TFTextBlock(line, text, tags_list, word_density, lb)
            self.__tb_arr.append(tb)

    def create_text_blocks(self, channel, target_path, filename, keyword):

        dom, s_text = self.__pproc.create_dom(target_path + filename)
        self.__explore_node(0, [], 'html', list(dom), keyword)

        last_line = 0
        txt_check_list = {}
        # tb_data = ["line,text,tags,word_density,lb\n"]
        tb_data = []
        for tb in self.__tb_arr:
            text = tb.get_text()
            # text = re.sub("^[\s]+", '', text, 0)
            # text = re.sub("^[0-9]+([\s]*[0-9]+)+", '', text, 0)
            if text != '':
                tb_data.append({
                    "text": text,
                    "ptp": tb.get_parent_tags_pattern(),
                    "label": 1
                })
                # tb_data.append(self.get_tb_data(tb.get_line(), text, tb.get_parent_tags(), tb.get_word_density(), 1))

                last_line = tb.get_line()
                if txt_check_list.get(text) is None:
                    txt_check_list[text] = 1
                else:
                    txt_check_list[text] += 1

        if channel == "jna" or channel == "dna":
            tb_data = self.append_no_explorable_text(s_text, txt_check_list, last_line, tb_data, keyword)

        return tb_data
        # filename = filename.split('.')[0] + '.csv'
        # self.tff.write_web_doc(target_path + "predict/", filename, tb_data)

    def append_no_explorable_text(self, s_text, txt_check_list, last_line, tb_data, keyword):
        s_text = s_text.split('\n')
        s_text = [text for text in s_text if text != '']
        n_text = []
        for text in s_text:
            text = self.__pproc.replace_words_prev(text)
            text = self.__pproc.clean_stopwords(text)
            text = self.__pproc.replace_words_post(text)

            eq_keyword = False
            keywords = keyword.split('_')
            for k in keywords:
                if text == k:
                    eq_keyword = True
                    break

            if len(text) > self.ENABLED_TEXT_COUNT and not eq_keyword:
                n_text.append(text)

        # 중앙일보에만...
        for text in n_text:
            if txt_check_list.get(text) is None:
                # print(text)
                last_line += 1
                word_density = self.get_word_density(text)
                tb = TFTextBlock(last_line, text, ["undefined"], word_density, 1)
                self.__tb_arr.append(tb)
                tb_data.append({
                    "text": text,
                    "ptp": tb.get_parent_tags_pattern(),
                    "label": 1
                })

                # tb_data.append(self.get_tb_data(last_line, text, ["undefined"], word_density, 1,))
                txt_check_list[text] = 1

        return tb_data

    def get_tb_arr(self):
        return self.__tb_arr

    def get_filename(self):
        return self.__file_name

    def get_word_density(self, txt):
        okt = Okt()
        mean_sentence_line_length = 40 #27  # 27.914828804678933
        unit_text_length = len(txt)
        line_count = int(unit_text_length / mean_sentence_line_length)
        line_count = line_count if line_count >= 1 else 0

        word_count = 0
        try:
            nouns = okt.nouns(txt)
            collection = collections.Counter(nouns)

            for value in collection.values():
                word_count += value
        except Exception as e:
            print(e)

        word_density = (word_count / line_count) if line_count >= 1 else 0.0001
        return word_density
