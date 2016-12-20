from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from tokenizer import Tokenizer
import numpy
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
import random
import datetime
from sklearn.externals import joblib
import pickle
import json

class Test(object):
    pass



if __name__ == '__main__':
    time_start = datetime.datetime.now()

    input_obj = open('./data/derivants/filtered_videos.txt')
    docs_train = []
    docs_predict = []
    y_train = []
    y_test = []
    lines = input_obj.readlines()
    random.shuffle(lines)
    line_cnt = len(lines)
    train_ratio = 0.8
    train_line_cnt = int(line_cnt * train_ratio)

    line_index = 0
    for line in lines:
        line = line.decode('utf8')
        fields = line.strip('\n').split('\t')
        tag = fields[0]
        title = fields[1]
        if line_index < train_line_cnt:
            y_train.append(tag)
            docs_train.append(title)
        else:
            y_test.append(tag)
            docs_predict.append(title)
        line_index += 1

    tokenizer = Tokenizer()
    algorithms_dict = {
            # 'NB': MultinomialNB(),
            'SVM_linear': SVC(kernel='linear'),
            'SVM_poly': SVC(kernel='poly'),
            'SVM_rbf': SVC(kernel='rbf'),
            'SVM_sigmoid': SVC(kernel='sigmoid'),
            # 'LR': LogisticRegression(penalty='l1', n_jobs=-1),
            }

    for algorithm_name, classifier in algorithms_dict.iteritems():
        text_clf = Pipeline([
            ('vect', CountVectorizer(tokenizer=tokenizer.tokenizeAndFilter)),
            ('tfidf', TfidfTransformer(use_idf=True)),
            ('clf', classifier),
            ])
        text_clf.fit(docs_train, y_train)

        predicted = text_clf.predict(docs_predict)
        precision = numpy.mean(predicted == y_test)
        print '{0}\t{1}'.format(algorithm_name, precision)

    # text_clf = Pipeline([
    #     ('vect', CountVectorizer(tokenizer=tokenizer.tokenizeAndFilter)),
    #     ('tfidf', TfidfTransformer(use_idf=True)),
    #     ('clf', SGDClassifier(n_jobs=-1)),
    #     ])

    # parameters = {
    #         'clf__penalty': ('l1', 'l2'),
    #         # 'clf__loss': ('hinge', 'log', 'squared_hinge')
    #         }

    # gs_clf = GridSearchCV(text_clf, parameters, n_jobs=-1)
    # gs_clf = gs_clf.fit(docs_train, y_train)
