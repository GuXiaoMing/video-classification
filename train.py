from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from tokenizer import Tokenizer
import numpy
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import datetime
from sklearn.externals import joblib
from conf.env_config import EnvConfig
from util import Util

from dataset import Dataset
class Trainer(object):

    @staticmethod
    def train(data_train, target_train):
        tokenizer = Tokenizer()
        count_vect = CountVectorizer(encoding='unicode',
                tokenizer=tokenizer.tokenizeAndFilter)

        X_train_counts = count_vect.fit_transform(data_train)
        target_list = Trainer.getAndSaveTargetList(target_train,
                EnvConfig.TARGET_LIST_PATH)
        Util.saveVocabulary(count_vect.vocabulary_,
                EnvConfig.VOCABULARY_READABLE_PATH)
        joblib.dump(count_vect.vocabulary_, EnvConfig.VOCABULARY_PATH)
        vocabulary = dict([(key, value) for (value, key) in
            count_vect.vocabulary_.iteritems()])

        tfidf_transformer = TfidfTransformer(use_idf=False)
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        joblib.dump(tfidf_transformer, EnvConfig.TFIDF_TRANSFORMER_PATH)
        Trainer.saveCsrMatrix(X_train_tfidf, vocabulary,
                EnvConfig.X_TRAIN_TFIDF_READABLE_PATH)

        lr_model = LogisticRegression(penalty='l1', n_jobs=-1)
        lr_model.fit(X_train_tfidf, target_train)
        joblib.dump(lr_model, EnvConfig.LR_MODEL_PATH)
        lr_model.sparsify()
        Trainer.saveCsrMatrix(lr_model.coef_, vocabulary,
                EnvConfig.LR_MODEL_COEF_PATH, target_list)
        Trainer.saveNdArray(lr_model.intercept_,
                EnvConfig.LR_MODEL_INTERCEPT_PATH, target_list)

    @staticmethod
    def getAndSaveTargetList(target_train, file_path):
        output_obj = open(file_path, 'w')
        target_list = list(set(target_train))
        target_list.sort()
        for target in target_list:
            output_obj.write(u'{0}\n'.format(target).encode('utf8'))
        return target_list

    @staticmethod
    def saveCsrMatrix(matrix, vocabulary, file_path, row_labels=None):
        line_cnt = matrix.shape[0]
        if row_labels is not None  and line_cnt != len(row_labels):
            raise Exception('Value Error',
                    'Matrix row count inequal to row lable count')
        output_obj = open(file_path, 'w')
        with output_obj:
            for i in xrange(0, matrix.shape[0]):
                begin_index = matrix.indptr[i]
                next_begin_index = matrix.indptr[i + 1]
                column_id_values = []
                if row_labels is not None:
                    output_obj.write(u'{0}\t'.format(row_labels[i])\
                            .encode('utf8'))
                for index in xrange(begin_index, next_begin_index):
                    column_id_values.append((matrix.indices[index],
                        matrix.data[index]))
                column_id_values.sort(key=lambda x: x[1], reverse=True)
                for column_id, value in column_id_values:
                    token = vocabulary[column_id]
                    output_obj.write(u'({0},{1}) '.format(token, value)\
                            .encode('utf8'))
                output_obj.write('\n')

    @staticmethod
    def saveNdArray(array, file_path, row_labels=None):
        output_obj = open(file_path, 'w')
        with output_obj:
            for i in xrange(0, array.shape[0]):
                if row_labels is not None:
                    output_obj.write(u'{0}\t'.format(row_labels[i])\
                            .encode('utf8'))
                if len(array.shape) == 2:
                    for j in xrange(0, array.shape[1]):
                        output_obj.write('{0}\t'.format(array.item(i, j)))

                elif len(array.shape) == 1:
                    output_obj.write('{0}'.format(array.item(i)))
                output_obj.write('\n')




if __name__ == '__main__':
    data_train, target_train, data_test, target_test = \
            Dataset.getTrainTestData(EnvConfig.TRAIN_DATA_PATH,
                    train_ratio=1, test_ratio=0, sample_cnt=-1)
    Trainer.train(data_train, target_train)
