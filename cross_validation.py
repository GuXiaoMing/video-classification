##
# @file cross_validation.py
# @Synopsis  parition the input(labeled data) into training set and validation
# set, train model with training part and test with validation part
# @author Ming Gu(guming02@baidu.com))
# @version 1.0
# @date 2015-12-05
import numpy
from conf.env_config import EnvConfig
from dataset import Dataset
from train import Trainer
from predict import Predictor

class CrossValidation(object):
    @staticmethod
    def crossValidate(train_ratio, test_ratio):
        data_train, target_train, data_test, target_test = \
                Dataset.getTrainTestData(EnvConfig.TRAIN_DATA_PATH,
                        train_ratio=train_ratio, test_ratio=test_ratio)

        Trainer.train(data_train, target_train)

        predictor = Predictor()
        predictor.loadModel()
        predicted = predictor.predict(data_test)

        precision = numpy.mean(predicted == target_test)
        return precision

if __name__ == '__main__':
    precision = CrossValidation.crossValidate(0.7, 0.3)
    print precision
