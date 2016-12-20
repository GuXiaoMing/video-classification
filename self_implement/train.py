from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
import numpy



class Train(object):
    @staticmethod
    def str2dict(feature_str):
        feature_value_dict = {}
        feature_values_strs = feature_str.split('$$$$')
        for feature_value_str in feature_values_strs:
            feature, value = feature_value_str.split('::::')
            feature_value_dict[feature] = float(value)
        return feature_value_dict

    @staticmethod
    def vectorizeSamples():
        input_obj = open('./data/derivants/video_feature.txt')

        output_obj = open('./data/derivants/vocabulary.txt', 'w')
        tag_list = []
        feature_dict_list = []
        video_cnt = 0
        train_sample_cnt = 0
        predict_sample_cnt = 0
        for line in input_obj:
            video_cnt += 1
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            tag = fields[0]
            feature_str = fields[1]
            feature_value_dict = Train.str2dict(feature_str)
            tag_list.append(tag)
            feature_dict_list.append(feature_value_dict)
            if video_cnt >= 100:
                break
        v = DictVectorizer(sparse=True)
        feature_value_matrix = v.fit_transform(feature_dict_list)
        print feature_value_matrix
        print type(feature_value_matrix)
        vocabulary_list = v.vocabulary_.items()
        vocabulary_list.sort(key=lambda x: x[1])
        for term, indice in vocabulary_list:
            output_obj.write(u'{0}\t{1}\n'.format(indice, term).encode('utf8'))
        return feature_value_matrix, v.vocabulary_, tag_list


if __name__ == '__main__':
    X, vocabulary, y = Train.vectorizeSamples()
    # print vocabulary
    lr = LogisticRegression(penalty='l1')
    lr.fit(X, y)
    numpy.savetxt('./data/derivants/coef.txt', lr.coef_)
    numpy.savetxt('./data/derivants/intercept.txt', lr.intercept_)
    classes_obj = open('./data/derivants/classes.txt', 'w')
    for class_ in lr.classes_:
        classes_obj.write(u'{0}\n'.format(class_).encode('utf8'))
    # y = [1,1,2,2,3,3,1,1,2,1]
    # logistic = LogisticRegression()
    # print logistic.fit(X, y).score(X, y)

