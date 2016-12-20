##
# @file predict.py
# @Synopsis  predict category
# @author Ming Gu(guming02@baidu.com))
# @version 1.0
# @date 2015-12-04


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from tokenizer import Tokenizer
import numpy
from sklearn.linear_model import LogisticRegression
import datetime
from sklearn.externals import joblib
from conf.env_config import EnvConfig
from dataset import Dataset

class Predictor(object):
    def __init__(self):
        self.__tokenizer = Tokenizer()
        self.__count_vect = CountVectorizer(
                tokenizer=self.__tokenizer.tokenizeAndFilter)
        self.__tfidf_transformer = None
        self.__classifier = None

    def loadModel(self):
        vocabulary = joblib.load(EnvConfig.VOCABULARY_PATH)
        self.__count_vect.vocabulary_ = vocabulary

        self.__tfidf_transformer = joblib.load(
                EnvConfig.TFIDF_TRANSFORMER_PATH)
        self.__classifier = joblib.load(EnvConfig.LR_MODEL_PATH)

    def predict(self, data_test):
        X_test_counts = self.__count_vect.transform(data_test)
        X_test_tfidf = self.__tfidf_transformer.transform(X_test_counts)
        predicted = self.__classifier.predict_proba(X_test_tfidf)
        return predicted, self.__classifier.classes_

if __name__ == '__main__':
    # data_train, target_train, data_test, target_test = \
    #         Dataset.getTrainTestData(EnvConfig.TRAIN_DATA_PATH, train_ratio=0,
    #                 test_ratio=1e-5)
    predictor = Predictor()
    predictor.loadModel()
    input_obj = open('./data/source/querys')
    uids = []
    queries = []
    for line in input_obj:
        line = line.decode('gbk')
        fields = line.strip('\n').split('\t')
        uids.append(fields[0])
        queries.append(fields[1])

    tag_map_obj = open('./data/output_tag_mapping')
    tag_map_dict = dict()
    for line in tag_map_obj:
        line = line.decode('utf8')
        fields = line.strip('\n').split('\t')
        tag_map_dict[fields[0]] = fields[1]

    predicted, classes = predictor.predict(queries)
    THRESHOLD = 7e-2
    output_obj = open('./data/derivants/reclist.txt', 'w')
    for rownum, row in enumerate(predicted):
        rec_list = []
        for colnum, prob in enumerate(row):
            if prob >= THRESHOLD:
                rec_list.append((colnum, prob))
        rec_list = map(lambda x: classes[x[0]], rec_list)
        rec_list = map(lambda x: tag_map_dict[x], rec_list)
        rec_set = set(rec_list)
        for tag in rec_set:
            output_obj.write(u'{0}\t{1}\n'.format(uids[rownum],
                tag).encode('utf8'))



    # for title, prediction in zip(queries, predicted):
    #     print(u'{0} => {1}'.format(title, prediction).encode('utf8'))
    # for uid, prediction in zip(uids, predicted):
    #     output_obj.write(u'{0}\t{1}\n'.format(uid, prediction).encode('utf8'))




