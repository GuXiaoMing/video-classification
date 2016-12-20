from sklearn.linear_model import LogisticRegression
import numpy

class Predict(object):
    @staticmethod
    def loadCoef():
        coef = numpy.loadtxt('./data/derivants/coef.txt')
        print coef

if __name__ == '__main__':
    Predict.loadCoef()
