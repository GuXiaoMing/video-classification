#encoding: utf-8

import os, sys
import traceback
import wordseg
import postag

SEG_WPCOMP = wordseg.SCW_WPCOMP
SEG_BASIC  = wordseg.SCW_BASIC

SEG_DEFAULT   = SEG_WPCOMP

class Tokenizer():
    def __init__(self):
        print >> sys.stderr, 'WordSegUtil constructed'
        self.MAX_TERM_CNT = 2048
        DICT_PATH = '/home/video/guming02/tools/dict'
        self.scw_worddict = wordseg.scw_load_worddict(
                os.path.join(DICT_PATH, 'wordseg/chinese_gbk'))
        self.scw_tagdict = postag.tag_create(
                os.path.join(DICT_PATH, 'postag'))
        self.scw_out = wordseg.scw_create_out(self.MAX_TERM_CNT * 10)

        # token
        self.tokens = wordseg.create_tokens(self.MAX_TERM_CNT)
        self.tokens = wordseg.init_tokens(self.tokens, self.MAX_TERM_CNT)

    def __del__(self):
        wordseg.destroy_tokens(self.tokens)
        wordseg.scw_destroy_out(self.scw_out)
        wordseg.scw_destroy_worddict(self.scw_worddict)
        print 'Tokenize destroied'

    def tokenizeString(self, text, encoding='utf8', seg_type=SEG_DEFAULT):
        ret={
            'errno' : 0,
            'data' : [],
            }
        try:
            if encoding == 'utf8':
                text = text.decode('utf8', errors='ignore').encode('gbk')
            elif encoding == 'unicode':
                text = text.encode('gbk')
            data = []
            # 切词
            if len(text) == 0 or not isinstance(text, str):
                return ret
            wordseg.scw_segment_words(self.scw_worddict, self.scw_out, text,
                    len(text), 1)

            token_cnt = wordseg.scw_get_token_1(self.scw_out, seg_type,
                    self.tokens, self.MAX_TERM_CNT)
            tokens = wordseg.tokens_to_list(self.tokens, token_cnt)

            token_cnt = postag.tag_postag(self.scw_tagdict, self.tokens,
                    token_cnt)
            postag_ret = postag.print_tags(self.tokens, token_cnt)

            for token, pos in postag_ret:
                token = token.decode('gbk', 'ignore')
                data.append([token, pos])
            ret['data'] = data
            return ret

        except Exception as e:
            print e.message
            if encoding == 'unicode':
                print text.encode('utf8')
            else:
                print text.decode(encoding).encode('utf8')
            ret['errno'] = 1
            return ret

    def tokenizeAndFilter(self, text, encoding='unicode', seg_type=SEG_DEFAULT):
        POS_BLACK_LIST = ['w']
        ret = self.tokenizeString(text, encoding)
        if ret['errno'] != 0:
            return []
        else:
            data = ret['data']
            data_filtered = filter(lambda x: x[1] not in POS_BLACK_LIST, data)
            tokens = map(lambda x: x[0], data_filtered)
            return tokens


if __name__=="__main__":
    test_str = 'CCTV5在直播中国队比赛, 赵丽颖出演花千骨, 达芬奇密码'
    tokenizer = Tokenizer()
    r = tokenizer.tokenizeString(test_str)
    for e in r['data']:
        print '%s\t%s' % (e[0].encode('utf8'), e[1])
