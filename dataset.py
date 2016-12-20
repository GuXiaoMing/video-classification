##
# @file dataset.py
# @Synopsis  load data from file, and partition into training and test set
# @author Ming Gu(guming02@baidu.com))
# @version 1.0
# @date 2015-12-04
import random

class Dataset(object):
    def __init__(self):
        pass

    @staticmethod
    def getTrainTestData(data_path, train_ratio=0.7, test_ratio=0.3,
            sample_cnt=-1):
        data_train = []
        target_train = []
        data_test = []
        target_test = []
        lines = []
        input_obj = open(data_path)
        if sample_cnt == -1:
            lines = input_obj.readlines()
        else:
            line_index = 0
            for line in input_obj:
                if line_index >= sample_cnt:
                    break
                else:
                    lines.append(line.strip('\n'))
                line_index += 1

        random.shuffle(lines)

        line_cnt = len(lines)
        train_cnt = int(train_ratio * line_cnt)
        test_cnt = int(test_ratio * line_cnt)

        line_index = 0
        for line in lines:
            line = line.decode('utf8')
            fields = line.strip('\n').split('\t')
            tag = fields[0]
            title = fields[1]
            if line_index < train_cnt:
                target_train.append(tag)
                data_train.append(title)
            elif line_index < train_cnt + test_cnt:
                target_test.append(tag)
                data_test.append(title)
            line_index += 1
        return data_train, target_train, data_test, target_test

    @staticmethod
    def getPredictData(data_path):
        input_obj = open(data_path)
        data_predict = []
        for line in input_obj:
            line = line.decode('utf8')
            title = line.strip('\n')
            data_predict.append(title)
        return data_predict


