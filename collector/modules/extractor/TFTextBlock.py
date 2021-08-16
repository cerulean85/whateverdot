import collections
from konlpy.tag import Okt

class TFTextBlock:

    def __init__(self, line, text, parent_tags, word_density, lb):
        super().__init__()
        self.__line = line
        self.__text = text
        self.__parent_tags = parent_tags

        self.__parent_tags_pattern = ''
        for i in range(len(parent_tags)):
            tag = parent_tags[i]
            self.__parent_tags_pattern += tag + ('' if i == ( len(parent_tags) - 1) else '/')

        self.__tag_features = {}
        self.__word_features = {}
        self.__merged_features = []
        self.__raw_sparse_features = []
        self.__nouns = []
        self.__label = lb
        self.__word_density = word_density
        self.__prev_word_density = 0.0
        self.__next_word_density = 0.0

    def set_nouns(self, nouns):
        self.__nouns = nouns

    def get_nouns(self):
        return self.__nouns

    def get_line(self):
        return self.__line

    def get_label(self):
        return self.__label

    def get_word_density(self):
        return self.__word_density

    def get_text(self):
        return self.__text

    def append_parent_tag(self, tag):
        self.__parent_tags.append(tag)

    def get_parent_tags(self):
        return self.__parent_tags

    def get_parent_tags_pattern(self):
        return self.__parent_tags_pattern

    def get_parent_tags_freq(self):
        return collections.Counter(self.__parent_tags)

    def get_words_freq(self):
        okt = Okt()
        nouns = okt.nouns(self.__text)
        count = collections.Counter(nouns)
        return count.most_common(100)

    def set_features(self, word_features, tag_features):
        self.__tag_features = tag_features
        self.__word_features = word_features

    def get_features(self):
        return self.__word_features, self.__tag_features

    def init_features(self, tag_features_list, word_features_list):
        for tag in tag_features_list:
            self.__tag_features[tag] = 0
        for word in word_features_list:
            self.__word_features[word] = 0

    def set_tag_feature(self, tag, count):
        if self.__tag_features.get(tag) is not None:
            self.__tag_features[tag] = count

    def set_word_feature(self, word, count):
        if self.__word_features.get(word) is not None:
            self.__word_features[word] = count

    def get_tag_features(self):
        return self.__tag_features

    def get_word_features(self):
        return self.__word_features

    def merge_features(self):

        for item in self.__tag_features.items():
            tag, count = item[0], item[1]
            self.__merged_features.append((tag, count))

        for item in self.__word_features.items():
            word, count = item[0], item[1]
            self.__merged_features.append((word, count))

        for feature in self.__merged_features:
            self.__raw_sparse_features.append(feature[1])

    def get_merged_features(self):
        return self.__merged_features

    def get_raw_sparse_features(self):
        return self.__raw_sparse_features

    def set_word_density(self, density):
        self.__word_density = density

    def get_word_density(self):
        return self.__word_density

    def set_prev_word_density(self, density):
        self.__prev_word_density = density

    def get_prev_word_density(self):
        return self.__prev_word_density

    def set_next_word_density(self, density):
        self.__next_word_density = density

    def get_next_word_density(self):
        return self.__next_word_density

    # def __repr__(self):
    #     print("Created TextBlock...")
