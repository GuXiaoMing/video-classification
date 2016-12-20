# -*- coding:utf-8 -*-
import re
from tokenizer import Tokenizer
def filterData():
    input_obj = open('./data/source/tag_shortvideos.txt')
    output_obj = open('./data/derivants/filtered_videos.txt', 'w')
    tag_map_obj = open('./data/source/tag_mapping.txt')

    new_input_obj = open('./data/source/new_tag_video.txt')
    TAG_TRANSLATE_DICT = {
            'news': u'新闻',
            'funny': u'搞笑',
            'girl': u'美女',
            'sports': u'体育',
            'entertainment': u'娱乐',
            'game': u'游戏',
            '95meng': u'二次元',
            }

    tag_map_obj.readline()
    tag_map_dict = dict()
    for line in tag_map_obj:
        line = line.decode('utf8')
        fields = line.strip().split('\t')
        origin_tag = fields[0]
        target_tag = fields[1]
        tag_map_dict[origin_tag] = target_tag

    for line in input_obj:
        line = line.decode('utf8')
        fields = line.strip('\n').split('\t')
        if len(fields) == 4:
            title = fields[0]
            tag = fields[1]
            sub_tag = fields[2]
            intro = fields[3]
            if tag in tag_map_dict:
                tag = tag_map_dict[tag]
                output_obj.write('\t'.join([tag, title, sub_tag, intro])\
                        .encode('utf8') + '\n')
    for line in new_input_obj:
        line = line.decode('utf8')
        fields = line.strip('\n').split('\t')
        if len(fields) == 2:
            tag = fields[0]
            title = fields[1]
            if tag in TAG_TRANSLATE_DICT.keys():
                tag = TAG_TRANSLATE_DICT[tag]
            output_obj.write(u'{0}\t{1}\t\t\n'.format(tag, title).encode('utf8'))




def prepareTrainFile(strategy = 'mixed'):
    input_obj = open('./data/derivants/filtered_videos.txt')
    output_obj = open('./data/derivants/train_{0}.txt'.format(strategy), 'w')
    tokenizer = Tokenizer()
    POS_BLACK_LIST = ['w']
    for line in input_obj:
        line = line.decode('utf8')
        fields = line.strip('\n').split('\t')
        if len(fields) >= 2:
            title = fields[1]
            tag = fields[0]
            if strategy == 'titleOnly':

                ret = tokenizer.tokenizeString(title, 'unicode')['data']
                ret = filter(lambda x: x[1] not in POS_BLACK_LIST, ret)
                tokens = map(lambda x: x[0], ret)
                if len(tokens) > 0:
                    tokens_str = '$$$$'.join(tokens)
                    output_obj.write(u'{0}\t{1}\n'.format(tag, tokens_str)\
                            .encode('utf8'))

# def preparePredictFile():
#     input_obj = open('./search_reason')
#     output_obj = open('./predict', 'w')
#     for line in input_obj:
#         line = line.decode('gbk')
#         fields = line.strip().split('\t')
#         uid = fields[0]
#         tmp = fields[1].strip('[').strip(']')
#         titles = tmp.split(',')
#         titles = map(lambda x: x.strip().strip('"'), titles)
#         single_title = ' '.join(titles)
#         output_obj.write('{0}\t{1}\t\t\n'.format(uid.encode('gbk'),
#             single_title.encode('gbk')))

def preparePredictFile():
    input_obj = open('./data/source/predict.txt')
    output_obj = open('./data/derivants/predict', 'w')
    tokenizer = Tokenizer()
    for line in input_obj:
        line = line.decode('utf8')
        text = line.strip('\n')
        tokens_str = str2TokenStr(text, tokenizer)
        output_obj.write(u'{0}\n'.format(tokens_str).encode('utf8'))



if __name__ == '__main__':
    # filterData()
    # tagMapping()
    # prepareTrainFile('titleOnly')
    # prepareTrainFile('mixed')
    preparePredictFile()
