import csv
import math
import pickle
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
import re
import html5lib
import os
import pandas as pd
from pandas import DataFrame

# from text_extraction.Aggregator import Aggregator
# from text_extraction.DataProcessor import DataProcessor
from modules.extractor.WebDoc import WebDoc
import collections
from konlpy.tag import Okt
import sklearn.metrics as metrics
# import sklearn.metrics as confusion_matrix
from sklearn.metrics import confusion_matrix
import numpy as np
from multiprocessing import Process, Queue, Semaphore, Value
from konlpy.tag import Okt
from matplotlib import pyplot as plt
from scipy.stats import mode
from sklearn.metrics import confusion_matrix


class Corpus:
    limit_count = 2000

    f_limit_count = 616

    channel_folder = 'D:/__programming/data2/test/'

    def __init__(self):
        self.okt = Okt()

    def reduce(self, text_histogram):
        reduce_dict = {}
        for i in range(0, len(text_histogram)):
            text = text_histogram.loc[i]["text"]
            count = text_histogram.loc[i]["count"]
            if reduce_dict.get(text) is None:
                reduce_dict[text] = count
            else:
                reduce_dict[text] = reduce_dict[text] + count

        result = []
        for item in reduce_dict.items():
            result.append({"text": item[0], "count": item[1]})
        return pd.DataFrame(result).sort_values(["count"], ascending=False)

    def create_word_features(self):

        text = ''
        ir_count = 0
        file_list = os.listdir(self.channel_folder)
        for file in file_list:

            # 디렉토리 내 html의 DOM tree 분석
            wd = WebDoc()
            wd.load_text_blocks(self.channel_folder + file)

            wb_tb_arr = wd.get_tb_arr()
            for tb in wb_tb_arr:
                text += tb.get_text() + '\n'

            ir_count = ir_count + 1
            if ir_count == self.f_limit_count:
                break

        okt = Okt()
        nouns = okt.nouns(text)
        words_collection = collections.Counter(nouns)
        # print(words_collection)
        features = ''
        for item in words_collection.items():
            features += item[0] + ',' + str(item[1]) + '\n'
        with open('feature_word_count.csv', "w", encoding="utf-8") as f:
            f.write(features)

    def create_tag_features(self):
        pass

    def get_features(self, n):
        f = pd.read_csv('feature_word_count.csv')
        words_arr = f.head(n)

        with open('feature_tag.csv', "r", encoding="utf-8") as tags:
            arr = str(tags.read()).split('\n')
            tag_arr = [tag for tag in arr if tag != '']

        return tag_arr, words_arr["text"]

    def get_feature_list(self):

        feature_tag_list = []
        feature_word_list = []
        tag_features, word_features = self.get_features(300)
        for tag in tag_features:
            feature_tag_list.append(tag)

        for word in word_features:
            feature_word_list.append(word)

        return feature_tag_list, feature_word_list

    def iter_predict_docs(self, target_path, limit_count=2000):

        ir_count = 0
        df_arr = []
        file_list = []
        for i in range(1, limit_count + 1):
            file_list.append('wdoc_' + str(i) + '.csv')

        # with tqdm(total=limit_count) as pup:
            # print('Creating freq table...')
        for file in file_list:
            wd = WebDoc()
            wd.set_tb_arr(target_path + 'predict/', file)
            text_dict = wd.reduce()
            df = pd.DataFrame(text_dict)
            df_arr.append(df)

            ir_count = ir_count + 1
            if ir_count == limit_count:
                break

        result = pd.concat(df_arr)
        result = result.sort_values(["count"], ascending=False)
        result = result.reset_index(drop=True)
        result = self.reduce(result)
        result.describe()

        return result

    def take_resourece_from_origin(self):
        return ['wdoc_' + str(i) + '.html' for i in range(1, self.limit_count + 1)]

    def take_resources_from_predcit(self, target_path):
        return os.listdir(target_path)

    def create_doc_text_blocks(self, target_path, limit_count=10):
        ir_count = 0
        file_list = self.take_resourece_from_origin()
        docs = []
        for file in file_list:
            wd = WebDoc()
            wd.create_text_blocks(target_path, file, save_path=target_path + 'predict/')

            docs.append(wd)
            ir_count = ir_count + 1
            if ir_count == limit_count:
                break

        return docs

    def iter_docs(self, file_list, target_path_list):

        docs = []
        for i in range(0, len(file_list)):
            file = file_list[i]
            target_path = target_path_list[i]
            wd = WebDoc()
            # print(target_path + file)
            wd.load_text_blocks(target_path + file)
            docs.append(wd)

        return docs

    def count_freq(self, target_list, target_dict):
        for key in target_list:
            if target_dict.get(key) is None:
                target_dict[key] = 1
            else:
                target_dict[key] += 1

    def sort_dict(self, target_dict, reverse=True):
        # 내림차순 정렬. 빈도수가 큰 순서대로 정렬.
        return sorted(target_dict.items(), key=lambda x: x[1], reverse=reverse)

    # 텍스트는 1~1,000부터
    # 태그 정보는 10,000부터
    def create_word_to_index(self, start_index, target_dict, feature_type):
        index = start_index
        result_dict = {}
        for item in target_dict:
            result_dict[index] = item[0]
            index += 1

        content = ''
        for item in result_dict.items():
            content += str(item[0]) + ',' + item[1] + '\n'
        with open(feature_type + '_to_index.csv', "w", encoding="utf-8") as f:
            f.write(content)

        return result_dict

    def create_index_to_word(self, target_dict, feature_type):
        result_dict = {}
        for item in target_dict.items():
            index, word = item[0], item[1]
            result_dict[word] = index

        content = ''
        for item in result_dict.items():
            content += item[0] + ',' + str(item[1]) + '\n'
        with open('index_to_' + feature_type + '.csv', "w", encoding="utf-8") as f:
            f.write(content)

        return result_dict

    def __load_feature_list(self, path, feature_type):
        result_dict = {}
        with open(path, "r", encoding="utf-8") as f:
            rdr = csv.reader(f)
            for line in rdr:
                key, value = line[0], line[1]
                if result_dict.get(key) is None:
                    result_dict[key] = value
        return result_dict

    def load_word_to_index(self, feature_type):
        return self.__load_feature_list(feature_type + '_to_index.csv', feature_type)

    def load_index_to_word(self, feature_type):
        return self.__load_feature_list('index_to_' + feature_type + '.csv', feature_type)

    def set_nouns(self, docs):
        okt = Okt()
        for doc in docs:
            tb_arr = doc.get_tb_arr()
            for tb in tb_arr:
                try:
                    nouns = okt.nouns(tb.get_text())
                except:
                    nouns = []
                _nouns = []
                for noun in nouns:
                    if len(noun) > 1:
                        _nouns.append(noun)
                nouns = _nouns
                tb.set_nouns(nouns)

    def set_nouns_width_blocks(self, text_block_list):
        okt = Okt()
        # for doc in docs:
        #     tb_arr = doc.get_tb_arr()
        for tb in text_block_list:
            try:
                nouns = okt.nouns(tb.get_text())
            except:
                nouns = []
            _nouns = []
            for noun in nouns:
                if len(noun) > 1:
                    _nouns.append(noun)
            nouns = _nouns
            tb.set_nouns(nouns)

    def count_features_freq_with_blocks(self, text_block_list):
        tag_dict = {}
        noun_dict = {}
        okt = Okt()

        # docs 특징 추출
        # for doc in docs:
        for tb in text_block_list:
            try:
                nouns = okt.nouns(tb.get_text())
            except:
                nouns = []

            _nouns = []
            for noun in nouns:
                if len(noun) > 1:
                    _nouns.append(noun)
            nouns = _nouns
            tb.set_nouns(nouns)

            tags = tb.get_parent_tags()

            self.count_freq(nouns, noun_dict)
            self.count_freq(tags, tag_dict)

        noun_freq_list = self.sort_dict(noun_dict)
        tag_freq_list = self.sort_dict(tag_dict)

        self.write_freq_list(noun_freq_list, tag_freq_list)

        return noun_freq_list, tag_freq_list

    def count_features_freq(self, docs):
        tag_dict = {}
        noun_dict = {}
        okt = Okt()

        # docs 특징 추출
        for doc in docs:
            tb_arr = doc.get_tb_arr()
            for tb in tb_arr:
                try:
                    nouns = okt.nouns(tb.get_text())
                except:
                    nouns = []

                _nouns = []
                for noun in nouns:
                    if len(noun) > 1:
                        _nouns.append(noun)
                nouns = _nouns
                tb.set_nouns(nouns)

                tags = tb.get_parent_tags()

                self.count_freq(nouns, noun_dict)
                self.count_freq(tags, tag_dict)

        noun_freq_list = self.sort_dict(noun_dict)
        tag_freq_list = self.sort_dict(tag_dict)

        self.write_freq_list(noun_freq_list, tag_freq_list)

        return noun_freq_list, tag_freq_list

    def write_freq_list(self, noun_freq_list, tag_freq_list):
        with open('noun_freq_list.csv', 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            for item in noun_freq_list:
                writer.writerow(item)

        with open('tag_freq_list.csv', 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            for item in tag_freq_list:
                writer.writerow(item)

    def read_freq_list(self):
        noun_freq_list = []
        tag_freq_list = []

        with open('noun_freq_list.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            for line in rdr:
                noun_freq_list = line

        with open('tag_freq_list.csv', 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            for line in rdr:
                tag_freq_list = line

        return noun_freq_list, tag_freq_list

    def load_docs_features(self, filename):
        feature_result = []
        with open(filename, 'r', encoding='utf-8') as f:
            rdr = csv.reader(f)
            for line in rdr:
                # print(len(line))
                line = np.array(list(map(int, line)))
                feature_result.append(line)
                # print(line)
        return feature_result

    def get_docs_features(self, docs, filename, index_to_noun_dict, index_to_tag_dict, pred=False):

        nouns_length = 84
        tags_length = 62
        result_list = []
        for doc in docs:
            self.__get_doc_features(doc, index_to_noun_dict, index_to_tag_dict, nouns_length, tags_length)
            tb_arr = doc.get_tb_arr()
            for tb in tb_arr:
                words, tags = tb.get_features()
                lb = tb.get_label() if pred else 0
                result = words + tags + [lb]
                result_list.append(result)
                # print(len(result))

        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            for item in result_list:
                writer.writerow(item)

        return result_list

    def get_text_block_features(self, text_block, filename, index_to_noun_dict, index_to_tag_dict, pred=False):

        nouns_length = 84
        tags_length = 62
        result_list = []
        for doc in docs:
            self.__get_doc_features(doc, index_to_noun_dict, index_to_tag_dict, nouns_length, tags_length)
            tb_arr = doc.get_tb_arr()
            for tb in tb_arr:
                words, tags = tb.get_features()
                lb = tb.get_label() if pred else 0
                result = words + tags + [lb]
                result_list.append(result)
                # print(len(result))

        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            for item in result_list:
                writer.writerow(item)

        return result_list

    def __get_doc_features(self, doc, index_to_noun_dict, index_to_tag_dict, nouns_length, tags_length):

        tb_arr = doc.get_tb_arr()
        for tb in tb_arr:

            nouns = tb.get_nouns()
            tags = tb.get_parent_tags()
            # print(nouns)
            noun_feature_to_index = []
            tag_feature_to_index = []
            # if len(nouns) < nouns_length:

            ir_count = 0
            for noun in nouns:

                index = 0 if index_to_noun_dict.get(noun) is None else index_to_noun_dict.get(noun)
                noun_feature_to_index.append(index)

                ir_count += 1
                if ir_count == nouns_length:
                    break

            if ir_count < nouns_length:
                for _ in range(len(noun_feature_to_index), nouns_length):
                    noun_feature_to_index.append(0)

            ir_count = 0
            for tag in tags:

                index = 0 if index_to_tag_dict.get(tag) is None else index_to_tag_dict.get(tag)
                tag_feature_to_index.append(index)

                ir_count += 1
                if ir_count == tags_length:
                    break

            if ir_count < tags_length:
                for _ in range(len(tag_feature_to_index), tags_length):
                    tag_feature_to_index.append(0)

            tb.set_features(noun_feature_to_index, tag_feature_to_index)

        return doc

        # n_lengths.append(len(nouns))
        # t_lengths.append(len(tb.get_parent_tags()))
        # print(len(nouns), len(tb.get_parent_tags()))

        # print(max(n_lengths), max(t_lengths))

        # print('최빈값:', mode(n_lengths), mode(t_lengths))
        # n_lengths = np.array(n_lengths)
        # t_lengths = np.array(t_lengths)
        # print(n_lengths.mean(), t_lengths.mean())

        # words_collection = collections.Counter(nouns)
        # print(words_collection)
        # features = ''
        # for item in words_collection.items():
        #     features += item[0] + ',' + str(item[1]) + '\n'
        # with open('feature_word_count.csv', "w", encoding="utf-8") as f:
        #     f.write(features)
        # tb.init_features(tag_features_list, word_features_list)
        #
        #     wb_tb_arr = wd.get_tb_arr()
        #     for tb in wb_tb_arr:
        #         tb.init_features(tag_features_list, word_features_list)
        #
        #         for item in tb.get_path_tags_freq().items():
        #             tag, count = item[0], item[1]
        #             tb.set_tag_feature(tag, count)
        #
        #         for item in tb.get_words_freq():
        #             word, count = item[0], item[1]
        #             tb.set_word_feature(word, count)
        #
        #         tb.merge_features()
        #
        #     ir_count = ir_count + 1
        #     if ir_count == self.limit_count:
        #         break
        #
        # # print(text_dict)
        #
        # result = pd.concat(df_arr)
        # result = result.sort_values(["count"], ascending=False)
        # result = result.reset_index(drop=True)
        # result = self.reduce(result)
        # result.describe()
        #
        # return result

    ####################

    ###########

    ######################

    ################
    def predict_proposed(self, target_path, o_count, f_table, limit_count):
        ir_count = 0
        texts = f_table['text'][f_table['count'] > o_count]
        # print('text count:', len(texts))
        result = {}
        file_list = os.listdir(target_path + 'predict/')
        # print('Predicting Propsed...')
        with tqdm(total=limit_count) as pbar:
            for file in file_list:
                file_path = target_path + 'predict/' + file

                f = pd.read_csv(file_path)
                for text in texts:
                    f.loc[f['text'] == text, 'lb'] = 0
                result[file] = f[['line', 'text', 'lb']]
                pbar.update(1)
                ir_count = ir_count + 1
                if ir_count == limit_count:
                    break
            return result


    def insertion_sort(self, x, align_type='desc'):
        for size in range(1, len(x)):
            val = x[size]
            i = size
            if align_type == 'desc':
                while i > 0 and x[i - 1] < val:
                    x[i] = x[i - 1]
                    i -= 1
            else:
                while i > 0 and x[i - 1] > val:
                    x[i] = x[i - 1]
                    i -= 1
            x[i] = val

        return x

    def get_predict_keyword_score_table(self):
        ir_count = 0
        result = {}
        keyword_count = {}
        file_list = os.listdir(self.channel_folder + 'predict_zero/')
        for file in file_list:
            if file == 'keyword_score_list.csv':
                continue

            file_path = self.channel_folder + 'predict_zero/' + file
            # if not os.path.isfile(file_path) :
            # print('[Predicting By Keyword...] {}'.format(file))
            f = pd.read_csv(file_path)
            text_total_count = len(f['text'])
            for i in range(0, text_total_count):
                text = f['text'][i]

                # sentence_count = (len(text) / 80) + (1 if len(text) % 80 > 0 else 0)
                word_tokens = self.okt.nouns(text)
                for word in word_tokens:
                    if keyword_count.get(word) is None:
                        keyword_count[word] = 1
                    else:
                        keyword_count[word] += 1

            ir_count = ir_count + 1
            if ir_count == self.limit_count:
                break

            if ir_count % 100 == 0:
                print('[Creating Predicting File By Keyword...] {}%'.format((ir_count / self.limit_count) * 100))

        print('[Finshed Predicting File By Keyword...]')
        # count_values = [ count for count in keyword_count.values() ]
        # count_values = self.insertion_sort(count_values, align_type='asc')

        # print(keyword_count)
        # print(len(count_values))
        # for item in keyword_count.items():
        #     key, value = item[0], item[1]
        #     for i in range(0, len(count_values)):
        #         count = count_values[i]
        #         if value == count:
        #             keyword_count[key] = i + 1
        #             break
        #             # value = (i + 1) * 5
        #
        # print(keyword_count)

        # Score 표 만들기
        score_list = []
        ir_count = 0
        for file in file_list:
            if file == 'keyword_score_list.csv':
                continue

            file_path = self.channel_folder + 'predict_zero/' + file
            f = pd.read_csv(file_path)
            f['score'] = 0

            text_total_count = len(f['text'])
            for i in range(0, text_total_count):
                text = f['text'][i]
                word_tokens = self.okt.nouns(text)
                score = 0
                for word in word_tokens:
                    if keyword_count.get(word) is not None:
                        score += keyword_count[word]
                f.at[i, 'score'] = score
                score_list.append(score)
            result[file] = f[['line', 'score', 'lb']]

            ir_count = ir_count + 1
            if ir_count == self.limit_count:
                break

            if ir_count % 100 == 0:
                print('[Creating Score Table By Keyword...] {}%'.format((ir_count / self.limit_count) * 100))
        print('[Finshed Score Table By Keyword...]')
        # 기준 Score 결정
        score_list = self.insertion_sort(score_list)
        csvfile = open(self.channel_folder + 'predict_zero/keyword_score_list.csv', 'w', newline='')
        csvwriter = csv.writer(csvfile)
        print(score_list)
        for row in [score_list]:
            csvwriter.writerow(row)

        # save data
        with open(self.channel_folder + 'predict_zero/web_dictionary.pickle', 'wb') as fw:
            pickle.dump(result, fw)

        return score_list, result

    def read_predict_keyword_src(self):
        score_list = list()
        f = open(self.channel_folder + 'predict_zero/keyword_score_list.csv', 'r', encoding='utf-8')
        rea = csv.reader(f)
        for row in rea:
            score_list.append(row)

        # load data
        with open(self.channel_folder + 'predict_zero/web_dictionary.pickle', 'rb') as fr:
            user_loaded = pickle.load(fr)

        return score_list[0], user_loaded

    def predict_keyword(self, score_list, result, alpha=0.01):

        # print('Get Top Score By Keyword...')
        n_score_set = set({})
        for score in score_list:
            n_score_set.add(int(score))

        top_score_count = int(len(n_score_set) * (alpha))
        if top_score_count < 1:
            top_score_count = 10
        # print(len(n_score_set), 'top_score_count', top_score_count)
        top_score_set = set([])
        n_score_list = list(n_score_set)
        n_score_list.sort(reverse=True)
        # print(n_score_list)
        for score in n_score_list:
            if len(top_score_set) == top_score_count:
                break
            top_score_set.add(score)

        top_score_list = list(top_score_set)
        max_score = max(top_score_list)
        min_score = min(top_score_list)
        # print(max_score, min_score)
        # print(top_score_list[min_score: max_score])
        min_score = min(top_score_list)
        print(alpha, min_score)
        # print('Finished To Get Top Score By Keyword...')

        # 인접한 텍스트 블록 선택
        # print('Selecting Label By Keyword...')
        ir_count = 0
        for item in result.items():
            df = item[1]
            row_total_count = len(df['score'])
            for i in range(0, row_total_count):
                score = df['score'][i]
                # df.at[i, 'lb'] = 1
                if score >= min_score:
                    # print(score, min_score)
                    prev_idx = (i - 1) if (i - 1) >= 0 else 0
                    next_idx = (i + 1) if (i + 1) < len(df['lb']) else (len(df['lb']) - 1)
                    # df.at[prev_idx, 'lb'] = 1
                    df.at[i, 'lb'] = 1
                    # df.at[next_idx, 'lb'] = 1
                    # print(prev_idx, i, next_idx)

            ir_count = ir_count + 1
            if ir_count == self.limit_count:
                break

            # print('Selecting Label By Keyword... {}%'.format((ir_count / self.limit_count) * 100))

        return result

    density_count_group = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def predict_density(self):
        result = {}
        file_list = os.listdir(self.channel_folder + 'predict/')
        for file in file_list:
            file_path = self.channel_folder + 'predict/' + file
            print('[Predicting By Density...] {}'.format(file))
            f = pd.read_csv(file_path)

            text_total_count = len(f['text'])
            for i in range(0, text_total_count):
                text = f['text'][i]
                # print(f['text'][i])

                sentence_count = (len(text) / 80) + (1 if len(text) % 80 > 0 else 0)
                word_tokens = self.okt.nouns(text)
                word_density = len(word_tokens) / sentence_count
                # group_index = int(math.floor(word_density))
                # if group_index > 9:
                #     group_index = 9

                if word_density < 2.5:
                    f.at[i, 'lb'] = 0

            result[file] = f[['line', 'lb']]

        return result
        # self.density_count_group[group_index] += 1
        # print(text, word_density)
        # density_arr.append(word_density)
        # print(txt[0:], ':', word_density,len(word_tokens), sentence_count)
        # if word_density > 2.5:

        # for text in tex/ts:
        #     f.loc[f['text'] == text, 'lb'] = 0
        # result[file] = f[['line', 'lb']]

        # print(self.density_count_group)

    def answer_ratio(self):
        folder = '../a_lb_n_example_case_1/'
        file_list = os.listdir(folder)
        for filename in file_list:
            f = pd.read_csv(folder + filename)
            # print(f)
            answers = f['text'][f['lb'] == 1]
            print('total:{}, answers:{}, answers_ratio:{}'.format(len(f), len(answers),
                                                                  '%0.2f' % (len(answers) / len(f))))

    def answer_label(self, answer_path):

        a_lbss = np.array([], dtype=np.int64)  # 실제치
        folder = answer_path + 'labels/'
        file_list = os.listdir(folder)
        for filename in file_list:
            f = pd.read_csv(folder + filename)
            a_lbs = f['lb'].to_numpy()
            a_lbss = np.concatenate([a_lbss, a_lbs])

        return a_lbss

    def predicted_label(self):
        pass

    def f_measure(self, a_lbss, p_lbss):
        """
        :param a_lbss: NUMPY Arr Type
        :param p_lbss: NUMPY Arr Type
        :return:
        """
        # sklearn 을 이용하면 전부 계산해준다.  실제치, 예측치
        print('accuracy', metrics.accuracy_score(a_lbss, p_lbss))
        print('precision', metrics.precision_score(a_lbss, p_lbss, average='micro'))
        print('recall', metrics.recall_score(a_lbss, p_lbss, average='micro'))
        print('f1', metrics.f1_score(a_lbss, p_lbss, average='micro'))

        with open('p_lbss.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(p_lbss.tolist())

        with open('a_lbss.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(a_lbss.tolist())

        y_true = pd.Series(p_lbss.tolist())
        y_pred = pd.Series(a_lbss.tolist())
        print(pd.crosstab(y_true, y_pred, rownames=['True'], colnames=['Predicted'], margins=True))


    def confusion_matrix2(self, a_lbss, p_lbss):
        a_lbss = np.array(a_lbss, dtype=np.int64)  # 실제치
        p_lbss = np.array(p_lbss, dtype=np.int64)  # 예측치

        print(a_lbss)

        true_negative = 0
        true_positive = 0
        false_negative = 0
        false_positive = 0

        for i in range(0, len(a_lbss)):

            # TRUE POSITIVE
            if a_lbss[i] == 1 and p_lbss[i] == 1:
                true_positive += 1

            # TRUE NEGATIVE
            if a_lbss[i] == 0 and p_lbss[i] == 0:
                true_negative += 1

            # FALSE POSITIVE
            if a_lbss[i] == 0 and p_lbss[i] == 1:
                false_positive += 1

            # FALSE NEGATIVE
            if a_lbss[i] == 1 and p_lbss[i] == 0:
                false_negative += 1

                # pup.update(1)

        recall = true_positive / (true_positive + false_negative)
        precision = true_positive / (true_positive + false_positive)
        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        fscore =  2*recall*precision / (recall + precision)

        return true_positive, false_positive, false_negative, true_negative, recall, precision, accuracy, fscore


    def confusion_matrix(self, answer_path, p_result):
        p_lbss = np.array([], dtype=np.int64)  # 예측치
        a_lbss = np.array([], dtype=np.int64)  # 실제치

        folder = answer_path + 'labels/'
        # with tqdm(total=len(p_result)) as pbar:
        for item in p_result.items():
            key, value = item[0], item[1]
            p_lbs = value['lb'].to_numpy()
            p_lbss = np.concatenate([p_lbss, p_lbs])
            f = pd.read_csv(folder + key)
            a_lbs = f['lb'].to_numpy()
            a_lbss = np.concatenate([a_lbss, a_lbs])

            # pbar.update(1)

        true_negative = 0
        true_positive = 0
        false_negative = 0
        false_positive = 0

        for i in range(0, len(a_lbss)):

            # TRUE POSITIVE
            if a_lbss[i] == 1 and p_lbss[i] == 1:
                true_positive += 1

            # TRUE NEGATIVE
            if a_lbss[i] == 0 and p_lbss[i] == 0:
                true_negative += 1

            # FALSE POSITIVE
            if a_lbss[i] == 0 and p_lbss[i] == 1:
                false_positive += 1

            # FALSE NEGATIVE
            if a_lbss[i] == 1 and p_lbss[i] == 0:
                false_negative += 1

                # pup.update(1)

        recall = true_positive / (true_positive + false_negative)
        precision = true_positive / (true_positive + false_positive)
        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        fscore =  2*recall*precision / (recall + precision)

        return true_positive, false_positive, false_negative, true_negative, recall, precision, accuracy, fscore

        # Predicted    0     1    All
        # True
        # 0         1525    43   1568
        # 1           58  1820   1878
        # All       1583  1863   3446

    # y = np.array([1,1,1,1,0,0])   # 실제치

# p = np.array([1,1,0,0,0,0])   # 예측치
#
# # sklearn 을 이용하면 전부 계산해준다.
# print('accuracy', metrics.accuracy_score(y,p) )
# print('precision', metrics.precision_score(y,p) )
# print('recall', metrics.recall_score(y,p) )
# print('f1', metrics.f1_score(y,p) )
#
# print(metrics.classification_report(y,p))
# print(metrics.confusion_matrix(y,p))
#
# # exit()
# corpus = Corpus()
# # # corpus.answer_ratio()
# # # freq_table = corpus.iter_docs(init=True)
# # freq_table = corpus.iter_predict_docs()
# # result = corpus.predict_proposed(2, freq_table)
# result = corpus.predict_keyword()
# # result = corpus.predict_density()
# corpus._confusion_matrix(result)
# exit()
#
# cnt = {
#     3: 7372, 12: 644, 5: 5917, 18: 180, 13: 444,
#     11: 842, 8: 2271, 14: 377, 4: 7478, 23: 66,
#     7: 3004, 19: 141, 2: 5223, 9: 1611, 15: 307,
#     6: 4139, 1: 2002, 10: 1223, 0: 695, 21: 93,
#     36: 13, 17: 192, 28: 39, 16: 246, 25: 62,
#     26: 58, 22: 80, 32: 23, 24: 68, 20: 108,
#     35: 14, 29: 38, 27: 45, 55: 1, 39: 14,
#     30: 27, 38: 12, 42: 8, 31: 31, 50: 2,
#     33: 14, 54: 1, 34: 17, 45: 2, 37: 9,
#     44: 1, 315: 1, 94: 1, 40: 7, 59: 2,
#     46: 2, 53: 2, 41: 8, 66: 1, 52: 1,
#     49: 1, 138: 1, 43: 5, 48: 2, 61: 1,
#     60: 1, 100: 1, 2177: 1, 57: 1}
#
#
# def insertionSort(x):
#     for size in range(1, len(x)):
#         val = x[size]
#         i = size
#         while i > 0 and x[i-1] > val:
#             x[i] = x[i-1]
#             i -= 1
#         x[i] = val
#
#     return x
#
#
# x_values = [key for key in cnt.keys()]
#
# # print(x_values)
# # y_values = [value for value in cnt.values()]
# # sorted_x_values = []
# # sorted_y_values = []
# x_values = insertionSort(x_values)
# # print(insertionSort(x_values))
# y_values = [cnt[score] for score in x_values ]
# print(x_values, y_values)
# # print(min(x_values), max(x_values))
#
# plt.plot(x_values, y_values)
# plt.xlabel('Keyword Score')
# plt.ylabel('Text Count')
# # plt.axis()
# plt.axis([min(x_values), max(x_values), min(y_values), max(y_values)])
# plt.show()
#
# df = DataFrame({
#
#         'Keyword Score': x_values,
#         'Text Count': y_values,
#
# })
#
# pd.set_option('display.max_columns', None) ## 모든 열을 출력한다.
# pd.set_option('display.max_rows', None) ## 모든 열을 출력한다.
# print(df.head(65))
#
#
#


# corpus._confusion_matrix(result)

# u_count = len(freq_table) / 4
# print(len(freq_table))

# ps = []
# for i in range(0, 4):
#     start_index = u_count * i
#     ps.append(Process(target=corpus.predict, args=(2, freq_table[start_index : start_index + u_count],)))
#
# for i in range(0, len(ps)):
#     p = ps[i]
#     p.start()
#
#
# while True:
#
#     time.sleep(3)
#     alive_count = 0
#     for i in range(0, len(ps)):
#         p = ps[i]
#         if not p.is_alive():
#             alive_count += 1
#
#
#     if alive_count == len(ps):
#         corpus._confusion_matrix(result)
#         exit()


# print(result)

# p_lbss = np.array([], dtype=np.int64)   #예측치
# a_lbss = np.array([], dtype=np.int64)   #실제치
# folder = '../a_lb_n_example_case_1/'
# for item in result.items():
#     key, value = item[0], item[1]
#     p_lbs = value['lb'].to_numpy()
#     # print(p_lbs)
#     p_lbss = np.concatenate([p_lbss, p_lbs])
#
#     f = pd.read_csv(folder + key)
#     a_lbs = f['lb'].to_numpy()
#     a_lbss = np.concatenate([a_lbss, a_lbs])
#     # print(key,'--------------')
#     # print(p_lbs)
#     # print(a_lbs)
#
# print(p_lbss.shape)
# print(a_lbss.shape)
#
# # sklearn 을 이용하면 전부 계산해준다.  실제치, 예측치
# print('accuracy', metrics.accuracy_score(a_lbss,p_lbss))
# print('precision', metrics.precision_score(a_lbss,p_lbss))
# print('recall', metrics.recall_score(a_lbss,p_lbss))
# print('f1', metrics.f1_score(a_lbss,p_lbss))
#
# print(metrics.classification_report(a_lbss,p_lbss))
# print(metrics.confusion_matrix(a_lbss,p_lbss))


# file_list = os.listdir(folder)
# for filename in file_list:
#     f = pd.read_csv(folder + filename)
#     lbs = f['lb'].to_numpy()
#     print(lbs)
# tag_features_list, word_features_list = corpus.get_feature_list()
# print(tag_features)
# print(word_features)
# tag_features, word_features = corpus.get_features(300)
# print(tag_features, word_features)
# print(len(word_features))


# print(corpus.create_tags_feature())
# print(corpus.get_top_word_req(300))

# corpus.save_word_freq_map()


# corpus.iter_docs()
