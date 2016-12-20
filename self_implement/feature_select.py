import math
from feature_extract import FeatureExtraction

class FeatureSelection(object):

    @staticmethod
    def calEntropy(count_dict):
        entropy = 0
        if len(count_dict) > 0:
            cnt_values = count_dict.values()
            total_cnt = reduce(lambda a, b: a + b, cnt_values)
            if total_cnt >0:
                for count in cnt_values:
                        if count > 0:
                            entropy += count * (math.log(count) - math.log(total_cnt))
                entropy = -entropy / total_cnt
        return entropy

    @staticmethod
    def calInfoGain():
        input_obj = open('./data/derivants/train_titleOnly.txt')
        output_obj = open('./data/derivants/info_gain.txt', 'w')
        idf_dict = FeatureExtraction.loadIdf('./data/derivants/idf.txt')
        document_cnt = 0
        term_df_dict = {}
        tag_hist = {}
        pos_tag_hist_dict = {}
        neg_tag_hist_dict = {}
        for term in idf_dict:
            pos_tag_hist_dict[term] = {}
            neg_tag_hist_dict[term] = {}

        for line in input_obj:
                document_cnt += 1
                line = line.decode('utf8')
                fields = line.strip('\n').split('\t')
                tag = fields[0]
                terms_str = fields[1]
                terms = terms_str.split('$$$$')
                occur_term_set = set(terms)
                tag_hist[tag] = tag_hist.get(tag, 0) + 1
                for occur_term in occur_term_set:
                    term_df_dict[occur_term] = term_df_dict.get(
                            occur_term, 0) + 1
                    pos_tag_hist_dict[occur_term][tag] = pos_tag_hist_dict[occur_term]\
                            .get(tag, 0) + 1
        info_gain_dict = {}
        total_entropy = FeatureSelection.calEntropy(tag_hist)
        for term in idf_dict:
            p_pos = float(term_df_dict.get(term, 0)) / document_cnt
            p_neg = 1 - p_pos
            neg_tag_hist_dict.setdefault(term, {})
            for tag in tag_hist:
                if tag in pos_tag_hist_dict[term]:
                    neg_tag_hist_dict[term][tag] = tag_hist[tag] - \
                            pos_tag_hist_dict[term][tag]
                else:
                    neg_tag_hist_dict[term][tag] = tag_hist[tag]
            pos_entropy = FeatureSelection.calEntropy(pos_tag_hist_dict[term])
            neg_entropy = FeatureSelection.calEntropy(neg_tag_hist_dict[term])
            conditional_entropy = p_pos * pos_entropy + p_neg * neg_entropy
            info_gain = total_entropy - conditional_entropy
            # info_gain_dict[term] = [info_gain, p_pos, pos_entropy, p_neg, neg_entropy, total_entropy]
            info_gain_dict[term] = info_gain
        info_gain_list = info_gain_dict.items()
        info_gain_list.sort(key=lambda x: x[1], reverse=True)
        for term, info_gain in info_gain_list:
            output_obj.write(u'{0}\t{1}\n'.format(term, info_gain).encode('utf8'))



if __name__ == '__main__':
    FeatureSelection.calInfoGain()
