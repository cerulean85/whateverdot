import os

import pandas as pd
from bs4 import BeautifulSoup
import re
import html5lib
import numpy as np
from modules.extractor.TFTextBlock import TFTextBlock
import copy

from modules.extractor.TextBlock import TextBlock


class WebDoc:
    def __init__(self):
        self.__org_src = ''
        self.__tb_arr = []
        self.line = 0

    def create_dom(self, filename):
        f = open(filename, 'rb')
        html = f.read()
        f.close()

        html = re.sub('<', '\n<', html.decode('utf-8'))
        html = re.sub('(<!--)[\sa-zA-Z0-9-{>}]+', '', html)
        d_list = ["head", "footer", "header", "script", "style", "link", "iframe", "a", "em", "svg", "g", "strike",
                  "filter", "symbol", "defs", "feMerge", "button", "fieldset", "caption", "colgroup"]
        soup = BeautifulSoup(html, "html.parser")
        for script in soup(d_list):
            script.decompose()

        return html5lib.parse(str(soup))

    def clean_stopwords(self, text):
        text = re.sub("​", '', text, 0)
        text = re.sub(".*[퀵에디터].*", '', text, 0)
        text = re.sub(".*[빈프레임].*", '', text, 0)
        text = re.sub('[\d]{4}[.] [\d]{1,2}[.] [\d]{1,2}[.]', '', text, 0)
        # text = re.sub('[(a-zA-Z0-9)]', '', text, 0)
        text = re.sub('[a-zA-Z]+[a-zA-Z0-9]', '', text, 0)

        text = re.sub('[\s]+', ' ', text, 0)
        text = re.sub('[\s]$', '', text, 0)
        # text = re.sub('^[\s]', '', text, 0)
        # text = re.sub(",", '', text, 0)
        # text = re.sub("\[ \]> </> <!\[\]", '', text, 0)
        text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》{}“”]', '', text, 0)
        return text

    def __explore_node(self, depth, parent_path_tags, prev_node_name, current_node):

        def get_tag_name(__node):
            tag = str(__node.tag).replace('{http://www.w3.org/1999/xhtml}', '')
            tag = tag.replace('{http://www.w3.org/2000/xhtml}', '')
            return tag

        depth = depth + 1
        pts = parent_path_tags
        pts.append(prev_node_name)

        for i in range(0, len(current_node)):
            node = current_node[i]
            self.line = self.line + 1

            # print("{}[{}] {} [hasNode: {}, parentCount: {}]".format('-' * depth, self.line, get_tag_name(node), len(node), len(pts)))
            if len(node) == 0:
                # v = 'X'
                tail_text = str(node.text)
                tail_text = self.clean_stopwords(tail_text)
                m1 = re.compile('^\n$').match(tail_text)
                m2 = re.compile('^[\s]+$').match(tail_text)
                if tail_text != 'None' and len(tail_text) > 10 and tail_text and not m1 and not m2:
                    tail_text = re.sub('\n', '', tail_text, 0)
                    tb = TFTextBlock(self.line, tail_text, copy.deepcopy(pts), 0)
                    self.__tb_arr.append(tb)
                continue

            self.__explore_node(depth, copy.deepcopy(pts), get_tag_name(node), node)

    def load_text_blocks(self, save_path):
        """
        :param save_path:
        """
        # print(save_path)
        data = pd.read_csv(save_path)
        for i in range(0, len(data)):
            line = data['line'][i]
            text = data['text'][i]
            lb = data['lb'][i]
            parent_tags_arr = (data['tags'][i]).split('/')
            tags_list = [tag for tag in parent_tags_arr]
            tb = TextBlock(line, text, tags_list, lb)
            self.__tb_arr.append(tb)

    def __get_tb_data(self, line, text, parent_tags, label):
        tags = ''
        for i in range(0, len(parent_tags)):
            tags += parent_tags[i] + ('' if i == (len(parent_tags) - 1) else '/')
        return str(line) + ',' + text + ',' + tags + ',' + str(label) + '\n'

    def create_text_blocks(self, folder, filename, save_path='../lb_n_example_case_1/', w_type='label'):
        # print("[Creating Text Blocks] ... {}".format(filename))

        # print('creating.. {}'.format(filename))
        dom = self.create_dom(folder + filename)
        children = list(dom)
        self.__explore_node(0, [], 'html', children)

        def file_write(f, data):
            # print(data)
            f.write(data)

        filename = filename.split('.')[0] + '.csv'

        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        with open(save_path + filename, "w", encoding="utf-8") as f:
            f.write('line,text,tags,lb\n')
            is_lb = False
            for tb in self.__tb_arr:

                line = tb.get_line()

                text = tb.get_text()
                text = re.sub('^[\s]+', '', text, 0)
                text = re.sub('^[0-9]+([\s]*[0-9]+)+', '', text, 0)

                if w_type == 'label':
                    data = self.__get_tb_data(tb.get_line(), text, tb.get_parent_tags(), 0)
                    if line == 89 and text == '나만의 즐겨찾기를 추가해 보세요':
                        file_write(f, data)
                        is_lb = True

                    elif text == '이 블로그 카테고리 글':
                        file_write(f, data)
                        is_lb = False
                    else:
                        if text != '':
                            data = self.__get_tb_data(tb.get_line(), text, tb.get_parent_tags(), 1 if is_lb else 0)
                            file_write(f, data)
                else:
                    if text != '':
                        data = self.__get_tb_data(tb.get_line(), text, tb.get_parent_tags(), 1)
                        file_write(f, data)

        # else:
        #     data = pd.read_csv(save_path + filename)
        #     for i in range(0, len(data)):
        #         line = data['line'][i]
        #         text = data['text'][i]
        #         tb = TextBlock(line, text, '')
        #         self.__tb_arr.append(tb)

    def set_tb_arr(self, dir_path, filename):
        data = pd.read_csv(dir_path + filename)
        for i in range(0, len(data)):
            line = data['line'][i]
            text = data['text'][i]
            tb = TFTextBlock(line, text, '', 0)
            self.__tb_arr.append(tb)

    def get_tb_arr(self):
        return self.__tb_arr

    def set_tb(self, tb):
        self.__tb_arr = tb

    def reduce(self):
        text_list = np.array([tb.get_text() for tb in self.__tb_arr if tb.get_line() != 2])
        # print(text_list)
        u, c = np.unique(text_list, return_counts=True)
        uniq_cnt_list = [{"text": u[i], "count": c[i]} for i in range(0, len(u))]
        return uniq_cnt_list
