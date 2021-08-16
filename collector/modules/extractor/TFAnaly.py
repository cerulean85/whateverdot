import pandas as pd
import numpy as np
from modules.extractor.TFFile import TFFile
from modules.zhbase.ZHPandas import ZHPandas

pd.set_option('display.max_columns', None)  ## 모든 열을 출력한다.
pd.set_option('display.max_rows', None)  ## 모든 열을 출력한다.
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


class TFAnaly:

    def __init__(self):
        self.__txt_freq_table = {}
        self.__txt_index_table = {}
        self.__tags_freq_table = {}
        self.__tags_index_dict = {}
        self.__freq_count_table = {}
        self.__zhp = ZHPandas()

    def __agg_text_freq(self, txt):
        if self.__txt_freq_table.get(txt) is None:
            self.__txt_freq_table[txt] = 1
        else:
            self.__txt_freq_table[txt] += 1

    def __agg_tag_freq(self, txt):
        if self.__tags_freq_table.get(txt) is None:
            self.__tags_freq_table[txt] = 1
        else:
            self.__tags_freq_table[txt] += 1

    # def __agg_freq_count(self, freq):
    #     if self.__freq_count_table.get(freq) is None:
    #         self.__freq_count_table[freq] = 1
    #     else:
    #         self.__freq_count_table[freq] += 1
    #
    # def __read_file(self, filename):
    #     pass

    def __aggregate_freq(self, df):
        agg_txt_freq = self.__aggregate_text_freq(df)
        agg_tag_freq = self.__aggregate_tags_freq(df)
        return agg_txt_freq, agg_tag_freq

    def __aggregate_text_token(self):
        index = 1
        for txt in self.__txt_freq_table.keys():
            self.__txt_index_table[txt] = index
            index += 1

    def __aggregate_text_freq(self, df):
        # for filename in file_list:
        #     if ".csv" not in filename:
        #         continue

            # df = self.__zhp.read_csv(filename)
        txt_list = df.loc[:, ["text"]].values
        for txt_arr in txt_list:
            txt = txt_arr[0]
            self.__agg_text_freq(txt)
            continue

        sr_dict = {
            "text": self.__txt_freq_table.keys(),
            "freq": self.__txt_freq_table.values(), # 동일한 텍스트가 등장한 횟수
        }
        df = self.__zhp.create_data_frame_to_dict(sr_dict)
        df = self.__zhp.sort_df(df, ["freq"])
        return df.reset_index()

    def __aggregate_tags_freq(self, df):
        # for filename in file_list:

            # if ".csv" not in filename:
            #     continue

        # df = self.__zhp.read_csv(filename)
        tags_list = df.loc[:, ["tags"]].values
        for tags_arr in tags_list:
            tags = tags_arr[0]
            self.__agg_tag_freq(tags)
            continue

        sr_dict = {
            "tags": self.__tags_freq_table.keys(),
            "freq": self.__tags_freq_table.values()
        }
        df = self.__zhp.create_data_frame_to_dict(sr_dict)
        df = self.__zhp.sort_df(df, ["freq"])
        return df.reset_index()

    def __get_tags_pattern_feature(self, df):

        prev_step = 2
        next_step = 2
        prev_tags_pattern_token_1_list = []
        prev_tags_pattern_token_2_list = []
        current_tags_pattern_token_list = []
        next_tags_pattern_token_1_list = []
        next_tags_pattern_token_2_list = []

        tag_list = list(self.__tags_freq_table.keys())
        tag_id_list = {}
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            tag_id_list[tag] = i + 1

        # for filename in file_list:
        #
        #     if ".csv" not in filename:
        #         continue
        #
        #     df = self.__zhp.read_csv(filename)
        tags_list = df.loc[:, "tags"].values.tolist()

        for i in range(0, len(tags_list)):
            if i < prev_step:
                prev_tags_1 = 0
                prev_tags_2 = 0
            else:
                prev_tags_1 = tag_id_list[tags_list[i - prev_step]]
                prev_tags_2 = tag_id_list[tags_list[i - (prev_step + 1)]]

            if i > len(tags_list) - 1 - next_step:
                next_tags_1 = 0
                next_tags_2 = 0
            else:
                next_tags_1 = tag_id_list[tags_list[i + 1]]
                next_tags_2 = tag_id_list[tags_list[i + next_step]]

            prev_tags_pattern_token_1_list.append(prev_tags_1)
            prev_tags_pattern_token_2_list.append(prev_tags_2)
            current_tags_pattern_token_list.append(tag_id_list[tags_list[i]])
            next_tags_pattern_token_1_list.append(next_tags_1)
            next_tags_pattern_token_2_list.append(next_tags_2)

        # print(len(tags_list), len(current_tags_pattern_token_list))
        res_dict = {
            "Tag Path": tags_list,
            "Current Parent Tag Path Index": current_tags_pattern_token_list, # current_tags_pattern_token
            "Prev Parent Tag Path Index 1": prev_tags_pattern_token_1_list, # prev_tags_pattern_token_1
            "Prev Parent Tag Path Index 2": prev_tags_pattern_token_2_list, # prev_tags_pattern_token_2
            "Next Parent Tag Path Index 1": next_tags_pattern_token_1_list, # next_tags_pattern_token_1
            "Next Parent Tag Path Index 2": next_tags_pattern_token_2_list, # next_tags_pattern_token_2
        }

        return res_dict

    def __get_freq_list(self, t_list, txt_freq_table):
        freq_list = []
        # p_freq_list = []
        for i in range(0, len(t_list)):
            txt = t_list[i]
            freq = txt_freq_table[txt]
            freq_list.append(freq)
            # p_freq = p_freq_dict[freq]
            # p_freq_list.append(p_freq)

        return freq_list#, p_freq_list

    def __get_data_df(self, file_list):
        zhp = ZHPandas()
        df = None
        for filename in file_list:
            if ".csv" not in filename:
                continue

            if df is None:
                df = zhp.read_csv(filename)
            else:
                __df = zhp.read_csv(filename)
                df = pd.concat([df, __df])
        return df

    def __get_text_feature(self, df):
        txt_list = df["text"].values

        # 정수 인코딩
        txt_index_list = []
        for i in range(0, len(txt_list)):
            txt = txt_list[i]
            if self.__txt_index_table.get(txt) is None:
                """
                Out of Text의 경우에는 Index를 새로 추가할 것
                """
                txt_index = len(self.__txt_index_table) # Out of Text
            else:
                txt_index = self.__txt_index_table.get(txt)
            txt_index_list.append(txt_index)

        txt_freq_list = []
        for i in range(0, len(txt_list)):
            txt = txt_list[i]
            if self.__txt_freq_table.get(txt) is None:
                # Out of Text 빈도를 1로 측정
                freq = 1
            else:
                freq = self.__txt_freq_table[txt]
            txt_freq_list.append(freq)

        """
        example:
        - 나는 이번 주에는 운동을 3번 했어요. > freq = 3
        - 나처럼 운동을 3번 한 사람이 10명입니다. > freq_group_count = 10
        """
        txt_freq_group_count_list = []
        for freq in txt_freq_list:
            fg_count = list(self.__txt_freq_table.values()).count(freq)
            txt_freq_group_count_list.append(fg_count)

        return txt_list, txt_index_list, txt_freq_list, txt_freq_group_count_list

    def __get_tags_feature(self, df):
        tags_list = df["tags"].values
        tags_freq_list = []
        for i in range(0, len(tags_list)):
            tags = tags_list[i]
            if self.__tags_freq_table.get(tags) is None:
                # Out of Tags 빈도를 1로 측정
                freq = 1
            else:
                freq = self.__tags_freq_table[tags]
            tags_freq_list.append(freq)

        """
        example:
        - 나는 이번 주에는 운동을 3번 했어요. > freq = 3
        - 나처럼 운동을 3번 한 사람이 10명입니다. > freq_group_count = 10
        """
        tags_freq_group_count_list = []
        for freq in tags_freq_list:
            fg_count = list(self.__tags_freq_table.values()).count(freq)
            tags_freq_group_count_list.append(fg_count)

        return tags_list, tags_freq_list, tags_freq_group_count_list

    def get_context_feature(self, df, is_train=True):
        if is_train:
            # 훈련이 아닌 경우에는 freq 집계할 필요가 없음
            self.__aggregate_freq(df)
            self.__aggregate_text_token()

        basic_feature = self.__get_basic_context_feature(df)
        option_feature = self.__get_tags_pattern_feature(df)

        # "Text": txt_list,  # text
        # "Text Index": txt_token,  # text_token
        # "Text Frequency": txt_freq_list,  # text_freq
        # "Parent Tag Path Text": tag_list,  # tags
        # "Parent Tag Path Frequency": tag_freq_list,  # current_tags_freq
        # "word_density": word_density_list,  # word_density
        # "y": lb_list  # label
        # "Current Parent Tag Path Index": current_tags_pattern_token_list,  # current_tags_pattern_token
        # "Prev Parent Tag Path Index 1": prev_tags_pattern_token_1_list,  # prev_tags_pattern_token_1
        # "Prev Parent Tag Path Index 2": prev_tags_pattern_token_2_list,  # prev_tags_pattern_token_2
        # "Next Parent Tag Path Index 1": next_tags_pattern_token_1_list,  # next_tags_pattern_token_1
        # "Next Parent Tag Path Index 2": next_tags_pattern_token_2_list,  # next_tags_pattern_token_2
        feature = {
            "x1": basic_feature["Text Index"],
            "x2": basic_feature["Text Frequency"],
            "x3": option_feature["Current Parent Tag Path Index"],
            "x4": basic_feature["Parent Tag Path Frequency"],
            "x5": option_feature["Prev Parent Tag Path Index 1"],
            "x6": option_feature["Prev Parent Tag Path Index 2"],
            "x7": option_feature["Next Parent Tag Path Index 1"],
            "x8": option_feature["Next Parent Tag Path Index 2"],
            "x9": basic_feature["Text Frequency Group Count"],
            "x10": basic_feature["Parent Tag Path Frequency Group Count"],
            "x11": basic_feature["Text"],
            "x12": option_feature["Tag Path"],
            "y": basic_feature["y"],
        }

        return feature

    def __get_basic_context_feature(self, df):

        txt_list, txt_token, txt_freq_list, txt_freq_group_count_list = self.__get_text_feature(df)
        tag_list, tag_freq_list, tags_freq_group_count_list = self.__get_tags_feature(df)
        word_density_list = df["word_density"].values
        lb_list = df["lb"].values

        df_dict = {
            "Text": txt_list, # text
            "Text Index": txt_token, # text_token
            "Text Frequency": txt_freq_list, # text_freq
            "Text Frequency Group Count": txt_freq_group_count_list, # text_freq
            "Parent Tag Path Text": tag_list, # tags
            "Parent Tag Path Frequency": tag_freq_list, # current_tags_freq
            "Parent Tag Path Frequency Group Count": tags_freq_group_count_list, # current_tags_freq
            "word_density": word_density_list, # word_density
            "y": lb_list #label
        }

        return df_dict

    def get_txt_freq_tuple_table(self):
        return sorted(self.__txt_freq_table.items(), reverse=True, key=lambda item:item[1])

    def get_txt_freq_table(self):
        return self.__txt_freq_table

    def get_tag_freq_table(self):
        return self.__tags_freq_table

    def get_tag_freq_tuple_table(self):
        return sorted(self.__tags_freq_table.items(), reverse=True, key=lambda item:item[1])

    def tag_anal(self):
        ans_count = 100
        freq_type = "tag"

        tff = TFFile()
        prefix = "D:/__programming/__data2/twt/label/"
        file_list = tff.get_file_list(prefix)
        file_list = [(prefix + filename) for filename in file_list]

        tfa = TFAnaly()
        train_file_list = file_list[0:ans_count]
        tdf_txt, tdf_tag = tfa.__aggregate_freq(train_file_list)

        zhp = ZHPandas()
        df_dict = tfa.__get_basic_context_feature(tdf_txt, tdf_tag, train_file_list)
        # print(tdf_tag)
        # exit()
        tdf = zhp.create_data_frame_to_dict(df_dict)
        tag_freq_tuple = tfa.get_tag_freq_table()
        answer_tags = [tag_freq_tuple[0][0], tag_freq_tuple[3][0], tag_freq_tuple[10][0], tag_freq_tuple[14][0],
                       tag_freq_tuple[15][0], tag_freq_tuple[28][0], tag_freq_tuple[27][0]]
        # answer_tags = tag_freq_tuple[2][0]
        for i in range(0, len(tag_freq_tuple)):
            print(i, tag_freq_tuple[i])

        print(answer_tags)
        # exit()
        tfa = TFAnaly()
        pred_file_list = file_list[ans_count:len(file_list)]
        pdf_txt, pdf_tag = tfa.__aggregate_freq(pred_file_list)

        df_dict = tfa.__get_basic_context_feature(pdf_txt, pdf_tag, pred_file_list)
        pdf = zhp.create_data_frame_to_dict(df_dict)

        p_list = []
        ttl = []
        ttx = []
        p_tags_list = pdf["tags"].values
        p_txt_list = pdf["text"].values
        for i in range(0, len(p_tags_list)):
            tags = p_tags_list[i]
            txt = p_txt_list[i]
            p_answer = 0
            for atags in answer_tags:
                if tags == atags:
                    p_answer = 1
                    break

            ttl.append(tags)
            ttx.append(txt)
            p_list.append(p_answer)

        tfa = TFAnaly()
        train_file_list = file_list[ans_count:len(file_list)]
        tdf_txt, tdf_tag = tfa.__aggregate_freq(train_file_list)

        zhp = ZHPandas()
        df_dict = tfa.__get_basic_context_feature(tdf_txt, tdf_tag, train_file_list)
        tdf = zhp.create_data_frame_to_dict(df_dict)
        answer = tdf.lb
        a_list = answer.tolist()
        print(len(p_list), len(a_list))
        # exit()
        print(a_list[0:50])
        # p_list = [ 1 if p else 0 for p in y_pred.values.tolist() ]
        print(p_list[0:50])

        for i in range(0, 50):
            print(i, a_list[i], '-', p_list[i], ':', ttl[i], ttx[i])

        # print(p_list[0:50])

        TP, FP, TN, FN = 0, 0, 0, 0
        for i in range(0, len(answer)):
            a = a_list[i]
            p = p_list[i]

            if a == 1 and p == 1:
                TP += 1

            if a == 0 and p == 0:
                TN += 1

            if a == 1 and p == 0:
                FN += 1

            if a == 0 and p == 1:
                FP += 1

        RECALL = TP / (TP + FN)
        PRECISION = TP / (TP + FP)
        print(TP, FP, TN, FN, RECALL, PRECISION)


# '''
#     # ROC 곡선에 대해
#     # https://velog.io/@sset2323/03-05.-ROC-%EA%B3%A1%EC%84%A0%EA%B3%BC-AUC
#     # https://bskyvision.com/1165
#     # https://moons08.github.io/datascience/classification_score_roc_auc/
#     # 단어밀도 방식, 다른 머신러닝 방식들 비교.
#
#     사용 목적?
#     - RECALL, PRECISION, FALL-OUT 등의 값은 threshold 값을 조작함에 따라 얼마든지 왜곡이 가능
#     - threshold 값의 변화에 따라 변화하는 ROC 곡선의 면적을 계싼하여 모델의 전반적인 성능을 확인할 때 사용
#
#     로지스틱 회귀에서 임계값은 0.5로 설정되었던 그것이더라.
#     이 임계값에 따라 ROC 곡선이 그려지는 것.
# '''



    def logit_(self):

        ans_count = 600

        tff = TFFile()
        prefix = "D:/__programming/__data2/twt/label/"
        file_list = tff.get_file_list(prefix)
        file_list = [(prefix + filename) for filename in file_list]

        # tfa = TFAnaly()
        # train_file_list = file_list[0:ans_count]
        # tdf_txt, tdf_tag = tfa.agg_freq(train_file_list)
        #
        zhp = ZHPandas()
        # df_dict = tfa.get_label_freq_dict(tdf_txt, tdf_tag, train_file_list)
        # tdf = zhp.create_data_frame_to_dict(df_dict)
        # print(tdf[0:10])

        tfa = TFAnaly()
        pred_file_list = file_list[0:len(file_list)]
        pdf_txt, pdf_tag = tfa.__aggregate_freq(pred_file_list)

        df_dict = tfa.__get_basic_context_feature(pdf_txt, pdf_tag, pred_file_list)
        pdf = zhp.create_data_frame_to_dict(df_dict)
        ft = tfa.get_txt_freq_table()
        # print(ft.values())

        return pdf, file_list, max(ft.values())

        # print(ft)
        # exit()
        # p_list = []
        # for i in range(0, len(pdf)):
        #     p = pdf.loc[i, "text_freq"]
        #     p_list.append(1 if p <= ef else 0)
        #
        # # print(p_list)
        #
        #
        #
        #
        # # print(pdf[:, ["text_freq"]][0:50])
        # # exit()
        #
        # # formula = "lb ~ text_freq + tags_freq"
        # # model = sm.Logit.from_formula(formula, data=tdf)
        # # result = model.fit()
        # # print(result.summary())
        # # print(result.pvalues)
        # # # print(result.params)
        # # print(np.exp(result.params))
        # # exit()
        #
        # # y_pred = result.predict({'text_freq': pdf["text_freq"].values, "tags_freq": pdf["tags_freq"].values}) >= 0.5
        # # print(y_pred)
        # # exit()
        #
        # tfa = TFAnaly()
        # train_file_list = file_list[0:len(file_list)]
        # tdf_txt, tdf_tag = tfa.agg_freq(train_file_list)
        #
        # zhp = ZHPandas()
        # df_dict = tfa.get_label_freq_dict(tdf_txt, tdf_tag, train_file_list)
        # tdf = zhp.create_data_frame_to_dict(df_dict)
        # answer = tdf.lb
        #
        # # p_list = y_pred.values.tolist()
        # a_list = answer.tolist()
        # print(len(p_list), len(a_list))
        # # print(a_list[0:50])
        # # p_list = [1 if p else 0 for p in y_pred.values.tolist()]
        # print(a_list[0:50])
        # print(p_list[0:50])
        #
        # TP, FP, TN, FN = 0, 0, 0, 0
        # for i in range(0, len(answer)):
        #     a = a_list[i]
        #     p = p_list[i]
        #
        #     if a == 1 and p == 1:
        #         TP += 1
        #
        #     if a == 0 and p == 0:
        #         TN += 1
        #
        #     if a == 1 and p == 0:
        #         FN += 1
        #
        #     if a == 0 and p == 1:
        #         FP += 1
        #
        # RECALL = TP / (TP + FN)
        # PRECISION = TP / (TP + FP)
        # print(TP, FP, TN, FN, RECALL, PRECISION)
    def get_answer_label_list(self, file_list):
        train_file_list = file_list
        tdf_txt, tdf_tag = self.__aggregate_freq(train_file_list)
        df_dict = self.__get_basic_context_feature(tdf_txt, tdf_tag, train_file_list)
        tdf = self.__zhp.create_data_frame_to_dict(df_dict)
        a_list = tdf.lb.tolist()
        return a_list


# if __name__ == "__main__":
#
#     tff = TFFile()
#     prefix = "D:/__programming/__data2/twt/label/"
#     file_list = tff.get_file_list(prefix)
#     file_list = [(prefix + filename) for filename in file_list]
#
#     zhp = ZHPandas()
#     tfa = TFAnaly()
#     pred_file_list = file_list[0:len(file_list)]
#     pdf_txt, pdf_tag = tfa.agg_freq(pred_file_list)
#     df_dict = tfa.get_label_freq_dict(pdf_txt, pdf_tag, pred_file_list)
#     pdf = zhp.create_data_frame_to_dict(df_dict)
#     ft = tfa.get_txt_freq_table()
#     max_freq = max(ft.values())
#
#     a_list = tfa.get_answer_label_list(file_list[0:len(file_list)])
#
#     zhe = ZHEvalPerformance()
#     bin_c_measure_list = []
#     with tqdm(total=len(file_list)) as pbar:
#         for v in range(0, max_freq):
#
#             p_list = (pdf["text_freq"].to_numpy() <= v).tolist()
#             p_list = [1 if p else 0 for p in p_list]
#
#             bin_c_measure_list.append(zhe.get_binary_classification_measure(p_list, a_list))
#             pbar.update(1)
#
#     FPR = []
#     TPR = []
#     for vl in bin_c_measure_list:
#         FPR.append(vl["FPR"])
#         TPR.append(vl["TPR"])
#
#
#
#
#
#
#     # zhe.get_roc_auc(x_values, y_values)
#
#     exit()
#
#     # file_list = [
#     #     "D:/__programming/__data2/test/predict/twt_web_doc_1_1.csv",
#         # "D:/__programming/data/test/predict/wdoc_2.csv",
#         # "D:/__programming/data/test/predict/wdoc_3.csv",
#         # "D:/__programming/data/test/predict/wdoc_4.csv"
#     # ]
#
#
#     # df = tfa.agg_text_freq(file_list)
#     # print(df[0:10])
#     # df = tfa.agg_freq_count()
#     # print(df[0:10])
#     ans_count = 100
#     freq_type = "tag"
#
#     tff = TFFile()
#     prefix = "D:/__programming/__data2/twt/label/"
#     file_list = tff.get_file_list(prefix)
#     file_list = [(prefix + filename) for filename in file_list]
#
#     tfa = TFAnaly()
#     train_file_list = file_list[0:ans_count]
#     tdf_txt, tdf_tag = tfa.agg_freq(train_file_list)
#
#     zhp = ZHPandas()
#     df_dict = tfa.get_label_freq_dict(tdf_txt, tdf_tag, train_file_list)
#     # print(tdf_tag)
#     # exit()
#     tdf = zhp.create_data_frame_to_dict(df_dict)
#     tag_freq_tuple = tfa.get_tag_freq_table()
#     answer_tags = [tag_freq_tuple[0][0], tag_freq_tuple[3][0], tag_freq_tuple[10][0], tag_freq_tuple[14][0],
#                    tag_freq_tuple[15][0], tag_freq_tuple[28][0], tag_freq_tuple[27][0]]
#     # answer_tags = tag_freq_tuple[2][0]
#     for i in range(0, len(tag_freq_tuple)):
#         print(i, tag_freq_tuple[i])
#
#     print(answer_tags)
#     # exit()
#     tfa = TFAnaly()
#     pred_file_list = file_list[ans_count:len(file_list)]
#     pdf_txt, pdf_tag = tfa.agg_freq(pred_file_list)
#
#     df_dict = tfa.get_label_freq_dict(pdf_txt, pdf_tag, pred_file_list)
#     pdf = zhp.create_data_frame_to_dict(df_dict)
#
#     p_list = []
#     ttl = []
#     ttx = []
#     p_tags_list = pdf["tags"].values
#     p_txt_list = pdf["text"].values
#     for i in range(0, len(p_tags_list)):
#         tags = p_tags_list[i]
#         txt = p_txt_list[i]
#         p_answer = 0
#         for atags in answer_tags:
#             if tags == atags:
#                 p_answer = 1
#                 break
#
#         ttl.append(tags)
#         ttx.append(txt)
#         p_list.append(p_answer)
#
#     tfa = TFAnaly()
#     train_file_list = file_list[ans_count:len(file_list)]
#     tdf_txt, tdf_tag = tfa.agg_freq(train_file_list)
#
#     zhp = ZHPandas()
#     df_dict = tfa.get_label_freq_dict(tdf_txt, tdf_tag, train_file_list)
#     tdf = zhp.create_data_frame_to_dict(df_dict)
#     answer = tdf.lb
#     a_list = answer.tolist()
#     print(len(p_list), len(a_list))
#     # exit()
#     print(a_list[0:50])
#     # p_list = [ 1 if p else 0 for p in y_pred.values.tolist() ]
#     print(p_list[0:50])
#
#     for i in range(0, 50):
#         print(i,  a_list[i], '-', p_list[i], ':', ttl[i], ttx[i])
#
#     # print(p_list[0:50])
#
#
#     TP, FP, TN, FN = 0, 0, 0, 0
#     for i in range(0, len(answer)):
#         a = a_list[i]
#         p = p_list[i]
#
#         if a == 1 and p == 1:
#             TP += 1
#
#         if a == 0 and p == 0:
#             TN += 1
#
#         if a == 1 and p == 0:
#             FN += 1
#
#         if a == 0 and p == 1:
#             FP += 1
#
#     RECALL = TP / (TP + FN)
#     PRECISION = TP / (TP + FP)
#     print(TP, FP, TN, FN, RECALL, PRECISION)
#     #
#     #     if p_freq < p_max_freq and lb == 1:
#
#     # print(classification_report(tdf.lb, y_pred))
#     # print(y_pred)
#     # confusion_matrix(tdf.lb, y_pred)
#     # print("=============")
#     # print(result)
#     # fpr, tpr, thresholds = roc_curve(df.lb, result.predict(df.freq))
#     # plt.plot(fpr, tpr)
#     # plt.show()
#     #
#     # print(auc(fpr, tpr))
#
#     # df = df.loc[:, ["freq", "lb"]]
#     # print(df)
#
#     # TP, FP, TN, FN = 0, 0, 0, 0
#     # for i in range(0, len(df)):
#     #     txt = df.loc[i, "text"]
#     #     freq = txt_freq_table[txt]
#     #     p_freq = p_freq_dict[freq]
#     #     lb = df.loc[i, "lb"]
#     #
#     #     if p_freq == p_max_freq and lb == 1:
#     #         TP += 1
#     #
#     #     if p_freq < p_max_freq and lb == 1:
#
#
#
#         # print(txt, freq, p_freq, lb)
#
#
#
#
#         # print(df.loc[i, ["text", "lb"]])
#
#
#
#     exit()
#
#
#     # print(p_freq_list)
#     # print(max(sr_val_list))
#     # plt.plot(p_freq_list, sr_val_list)
#     # plt.scatter(p_freq_list, sr_val_list)
#     # plt.title('model accuracy')
#     # plt.ylabel('sr_val')
#     # plt.xlabel('p_freq')
#     # plt.xlim(0, 1)
#     # plt.ylim(0, 10)
#     # plt.show()
#
#
#     # print(df.loc[df["freq"] == 1])
#     # df = tfa.agg_freq_count()
    # print(df)
