import numpy as np

from modules.extractor.TFAnaly import TFAnaly
from modules.zhbase.ZHPandas import ZHPandas
from modules.extractor.Corpus import Corpus
from modules.extractor.WebDoc import WebDoc


class TFGeneratorDataSet:

    def get_dataset_file_freq(self,
                              file_list,
                              train_file_count=100,
                              valid_data_rate=0.5,
                              return_padnas=False,
                              focus_columns=["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"],
                              validation=False
                              ):

        zhp = ZHPandas()
        tfa = TFAnaly()

        train_file_list = file_list[0:train_file_count]
        train_block_df = None
        for filename in train_file_list:
            if ".csv" not in filename:
                continue

            if train_block_df is None:
                train_block_df = zhp.read_csv(filename)
            else:
                df = zhp.read_csv(filename)
                train_block_df = zhp.concat_row(train_block_df, df)

        df_dict = tfa.get_context_feature(train_block_df, is_train=True)
        train_df = zhp.create_data_frame_to_dict(df_dict)

        test_file_list = file_list[train_file_count:len(file_list)]
        test_block_df = None
        for filename in test_file_list:
            if ".csv" not in filename:
                continue

            if test_block_df is None:
                test_block_df = zhp.read_csv(filename)
            else:
                df = zhp.read_csv(filename)
                test_block_df = zhp.concat_row(test_block_df, df)

        df_dict = tfa.get_context_feature(test_block_df)
        test_df = zhp.create_data_frame_to_dict(df_dict)


        column_list = []
        for column in train_df.columns:
            if column != "y":
                column_list.append(column)

        train_X = train_df.loc[:, column_list]
        train_y = train_df.loc[:, "y"]
        test_X = test_df.loc[:, column_list]
        test_y = test_df.loc[:, "y"]

        column_list = []
        for column in test_X.columns:
            for fc in focus_columns:
                if column == fc:
                    column_list.append(column)

        last_index = len(test_X)
        test_split_index = int(last_index * valid_data_rate)
        # print("{} {} {}".format(last_index, test_split_index, valid_data_rate))

        val_X, val_y = None, None
        if validation:
            val_X, val_y = test_X[0:test_split_index], test_y[0:test_split_index]
            test_X, test_y = test_X[test_split_index:last_index], test_y[test_split_index:last_index]

        if return_padnas:
            val_X = None if val_X is None else val_X.loc[:, column_list]
            val_y = None if val_y is None else val_y

            return \
                train_X.loc[:, column_list], train_y, \
                test_X.loc[:, column_list], test_y, \
                val_X, val_y

        return self.__to_float_numpy(train_X, train_y, test_X, test_y, val_X, val_y)



    def get_dataset_freq(self,
                         file_list,
                         train_data_rate=0.6,
                         valid_data_rate=0.5,
                         return_padnas=False,
                         focus_columns=["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"],
                         validation=False):

        zhp = ZHPandas()
        tfa = TFAnaly()

        block_df = None
        for filename in file_list:
            if ".csv" not in filename:
                continue

            if block_df is None:
                block_df = zhp.read_csv(filename)
            else:
                df = zhp.read_csv(filename)
                block_df = zhp.concat_row(block_df, df)

        train_last_df_index = int(len(block_df) * train_data_rate)
        test_last_df_index = len(block_df)

        train_df_list = block_df[0:train_last_df_index]
        test_df_list = block_df[train_last_df_index:test_last_df_index]

        ### 훈련 데이터 생성 ###
        # df_dict = {}
        df_dict = tfa.get_context_feature(train_df_list, is_train=True)
        train_df = zhp.create_data_frame_to_dict(df_dict)
        ##########################

        ### 시험 데이터 생성 ###
        # df_dict = {}
        df_dict = tfa.get_context_feature(test_df_list)
        test_df = zhp.create_data_frame_to_dict(df_dict)
        ##########################

        ### 레이블 데이터 분리 ###
        column_list = []
        for column in train_df.columns:
            if column != "y":
                column_list.append(column)

        train_X = train_df.loc[:, column_list]
        train_y = train_df.loc[:, "y"]
        test_X = test_df.loc[:, column_list]
        test_y = test_df.loc[:, "y"]
        ##########################

        column_list = []
        for column in test_X.columns:
            for fc in focus_columns:
                if column == fc:
                    column_list.append(column)

        last_index = len(test_X)
        test_split_index = int(last_index * valid_data_rate)
        # print("{} {} {}".format(last_index, test_split_index, valid_data_rate))

        val_X, val_y = None, None
        if validation:
            val_X, val_y = test_X[0:test_split_index], test_y[0:test_split_index]
            test_X, test_y = test_X[test_split_index:last_index], test_y[test_split_index:last_index]

        if return_padnas:
            val_X = None if val_X is None else val_X.loc[:, column_list]
            val_y = None if val_y is None else val_y

            return \
                train_X.loc[:, column_list], train_y, \
                test_X.loc[:, column_list], test_y, \
                val_X, val_y

        return self.__to_float_numpy(train_X, train_y, test_X, test_y, val_X, val_y)

    def __to_float_numpy(self, train_X, train_y, test_X, test_y, val_X, val_y):
        train_X = train_X.to_numpy().astype(float)
        train_y = train_y.to_numpy().astype(float)
        test_X = test_X.to_numpy().astype(float)
        test_y = test_y.to_numpy().astype(float)
        val_X = None if val_X is None else val_X.to_numpy().astype(float)
        val_y = None if val_y is None else val_y.to_numpy().astype(float)
        return train_X, train_y, test_X, test_y, val_X, val_y
    #
    # def get_test_data(self, file_list):
    #
    #     zhp = ZHPandas()
    #     tfa = TFAnaly()
    #
    #     df_freq_dict = tfa.__get_basic_context_feature(file_list)
    #     df_tag_pattern_dict = tfa.__get_tags_pattern_feature(file_list)
    #
    #     df_dict = {}
    #     for item in df_freq_dict.items():
    #         df_dict[item[0]] = item[1]
    #
    #     for item in df_tag_pattern_dict.items():
    #         df_dict[item[0]] = item[1]
    #
    #     test_df = zhp.create_data_frame_to_dict(df_dict)
    #
    #     column_list = []
    #     for column in test_df.columns:
    #         if column != "y":
    #             column_list.append(column)
    #
    #     test_X = test_df.loc[:, column_list]
    #     test_y = test_df.loc[:, "y"]
    #
    #     return test_X, test_y

    def get_dataset_boilernet(self,
                              file_list,
                              file_target_path_list,
                              train_data_rate=0.6,
                              valid_data_rate=0.5,
                              features_train_file="./features/features_train.csv",
                              features_test_file="./features/features_test.csv",
                              create_file=False):

        FEATURES_TRAIN_FILE = features_train_file
        FEATURES_TEST_FILE = features_test_file

        corpus = Corpus()
        if create_file:

            text_block_list = []
            docs = corpus.iter_docs(file_list, file_target_path_list)
            for doc in docs:
                for tb in doc.get_tb_arr():
                    text_block_list.append(tb)

            train_last_block_index = int(len(text_block_list) * train_data_rate)
            test_last_block_index = len(text_block_list)

            train_text_block_list = text_block_list[0:train_last_block_index]
            test_text_block_list = text_block_list[train_last_block_index:test_last_block_index]
            print(len(text_block_list), len(train_text_block_list), len(test_text_block_list))

            print("Count Feature Frequency...")
            noun_freq_list, tag_freq_list = corpus.count_features_freq_with_blocks(train_text_block_list)

            print("Create Features List...")
            noun_word_to_index_dict = corpus.create_word_to_index(1, noun_freq_list, feature_type='noun')
            noun_index_to_word_dict = corpus.create_index_to_word(noun_word_to_index_dict, feature_type='noun')
            tag_word_to_index_dict = corpus.create_word_to_index(len(noun_word_to_index_dict) + 1, tag_freq_list,
                                                                 feature_type='tag')
            tag_index_to_word_dict = corpus.create_index_to_word(tag_word_to_index_dict, feature_type='tag')

            print("Bring Document Features...")
            train_doc = WebDoc()
            train_doc.set_tb(train_text_block_list)
            result = corpus.get_docs_features([train_doc], FEATURES_TRAIN_FILE, noun_index_to_word_dict,
                                              tag_index_to_word_dict, pred=True)

            print(len(result))

            test_doc = WebDoc()
            test_doc.set_tb(test_text_block_list)
            corpus.set_nouns([test_doc])

            print("Bring Document Features...")
            result = corpus.get_docs_features([test_doc], FEATURES_TEST_FILE, noun_index_to_word_dict,
                                              tag_index_to_word_dict, pred=True)
            print(len(result))

        train_data = corpus.load_docs_features(FEATURES_TRAIN_FILE)
        train_data = np.array(train_data)

        train_X = train_data[:, 0: (train_data.shape[1] - 1)]
        train_y = train_data[:, -1]

        test_data = corpus.load_docs_features(FEATURES_TEST_FILE)
        test_data = np.array(test_data)

        test_X = test_data[:, 0:(test_data.shape[1] - 1)]
        test_y = test_data[:, -1]

        last_index = len(test_X)
        test_split_index = int(last_index * valid_data_rate)
        val_X, val_y = test_X[0:test_split_index], test_y[0:test_split_index]
        test_X, test_y = test_X[test_split_index:last_index], test_y[test_split_index:last_index]

        print('훈련용 데이터 SHAPE:', train_X.shape, train_y.shape)
        print('검증용 데이터 SHAPE:', val_X.shape, val_y.shape)
        print('예측용 데이터 SHAPE:', test_X.shape, test_y.shape)

        return train_X, train_y, test_X, test_y, val_X, val_y

