##
# @file env_config.py
# @Synopsis  environment configure
# @author Ming Gu(guming02@baidu.com))
# @version 1.0
# @date 2015-12-04
import os


class EnvConfig(object):
    CONF_PATH = os.path.split(os.path.realpath(__file__))[0]
    PROJECT_PATH = os.path.join(CONF_PATH, '..')
    DATA_PATH = os.path.join(PROJECT_PATH, 'data')
    SOURCE_DATA_PATH = os.path.join(DATA_PATH, 'source')
    DERIVANT_DATA_PATH = os.path.join(DATA_PATH, 'derivants')
    MODEL_DATA_PATH = os.path.join(DERIVANT_DATA_PATH, 'model')

    TRAIN_DATA_PATH = os.path.join(DERIVANT_DATA_PATH, 'filtered_videos.txt')


    VOCABULARY_PATH = os.path.join(MODEL_DATA_PATH, 'vocabulary.pkl')
    TFIDF_TRANSFORMER_PATH = os.path.join(MODEL_DATA_PATH, 'tfidf_transformer.pkl')
    LR_MODEL_PATH = os.path.join(MODEL_DATA_PATH, 'lr.pkl')

    VOCABULARY_READABLE_PATH = os.path.join(MODEL_DATA_PATH, 'vocabulary.txt')
    TARGET_LIST_PATH = os.path.join(MODEL_DATA_PATH, 'target_list.txt')
    X_TRAIN_TFIDF_READABLE_PATH = os.path.join(MODEL_DATA_PATH, 'x_train_tfidf.txt')
    LR_MODEL_COEF_PATH = os.path.join(MODEL_DATA_PATH, 'lr_coef.txt')
    LR_MODEL_INTERCEPT_PATH = os.path.join(MODEL_DATA_PATH, 'lr_intercept.txt')

