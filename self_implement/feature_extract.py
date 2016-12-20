import math
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from tokenizer import Tokenizer

class FeatureExtraction(object):

    def __init__():
        self.__tokenizer = Tokenizer()
        self.__idf_dict = {}

    def tokenizeAndFilter(line):
        POS_BLACK_LIST = ['w']
        ret = self.__tokenizer.tokenizeString(line, 'unicode')['data']
        ret = filter(lambda x: x[1] not in POS_BLACK_LIST, ret)
        tokens = map(lambda x: x[0], ret)
        return tokens

    def str2TokenStr(line, tokenizer):
        POS_BLACK_LIST = ['w']
        ret = tokenizer.tokenizeString(line, 'unicode')['data']
        ret = filter(lambda x: x[1] not in POS_BLACK_LIST, ret)
        tokens = map(lambda x: x[0], ret)
        tokens_str = '$$$$'.join(tokens)
        return tokens_str

    def tokenizeTrainFile(input_path, output_path, strategy = 'titleOnly'):
        input_obj = open(input_path)
        output_obj = open(output_path, 'w')
        for line in input_obj:
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            if len(fields) >= 2:
                title = fields[1]
                tag = fields[0]
                if strategy == 'titleOnly':
                    tokens = self.tokenizeAndFilter(title)
                    if len(tokens) > 0:
                        tokens_str = '$$$$'.join(tokens)
                        output_obj.write(u'{0}\t{1}\n'.format(tag, tokens_str)\
                                .encode('utf8'))

    def calIdf(train_data_path, idf_path):
        input_obj = open(train_data_path)
        output_obj = open(idf_path, 'w')
        document_cnt = 0
        df_dict = {}
        for line in input_obj:
            document_cnt += 1
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            tag = fields[0]
            terms_str = fields[1]
            terms = terms_str.split('$$$$')
            term_set = set(terms)
            for term in term_set:
                df_dict[term] = df_dict.get(term, 0) + 1

        idf_list = [(term, math.log(float(document_cnt)/df)) for term, df in
                df_dict.items()]
        idf_list.sort(key=lambda x: x[1])
        for term, idf in idf_list:
            output_obj.write(u'{0}\t{1}\n'.format(term, idf).encode('utf8'))

    def loadIdf(idf_path):
        input_obj = open(idf_path)
        for line in input_obj:
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            term = fields[0]
            idf = float(fields[1])
            self.__idf_dict[term] = idf
        return self.__idf_dict

    def getTfIdfFeature(tokenized_text):
            terms = tokenized_text.split('$$$$')
            tf_dict = Counter(terms)
            tfidf_list = [(term, tf * self.__idf_dict[term]) for term, tf in
                    tf_dict.items()]
            return dict(tfidf_list)

    def calTfIdfFeature(train_data_path, idf_path, feature_path):
        input_obj = open(train_data_path)
        output_obj = open(feature_path, 'w')
        for line in input_obj:
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            tag = fields[0]
            terms_str = fields[1]
            tfidf_dict = getTfIdfFeature(terms_str)
            tfidf_list = sorted(tfidf_dict.items(), key=lambda x: x[1],
                    reverse=True)
            tfidf_strs = map(lambda x: u'{0}::::{1}'.format(x[0], x[1]),
                    tfidf_list)
            total_tfidf_str = '$$$$'.join(tfidf_strs)
            output_obj.write(u'{0}\t{1}\n'.format(tag, total_tfidf_str)\
                    .encode('utf8'))

    @staticmethod
    def loadVocabulary(vocabulary_path):
        vocabulary_dict = {}
        input_obj = open(vocabulary_path)
        for line in output_obj:
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            index = int(fields[0])
            term = fields[1]
            vocabulary_dict[term] = index
        return vocabulary_dict

    def extractFeatureDict(text, idf_path, vocabulary_path):
        idf_dict = FeatureExtraction.loadIdf(idf_path)

        pass

    @staticmethod
    def str2dict(feature_str):
        feature_value_dict = {}
        feature_values_strs = feature_str.split('$$$$')
        for feature_value_str in feature_values_strs:
            feature, value = feature_value_str.split('::::')
            feature_value_dict[feature] = float(value)
        return feature_value_dict


if __name__ == '__main__':
    # FeatureExtraction.calIdf('./data/derivants/train_titleOnly.txt')
    FeatureExtraction.calTfIdf('./data/derivants/train_titleOnly.txt',
            './data/derivants/idf.txt', './data/derivants/video_feature.txt')

