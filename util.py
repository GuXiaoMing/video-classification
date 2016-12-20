##
# @file util.py
# @Synopsis  utilility functions
# @author Ming Gu(guming02@baidu.com))
# @version 1.0
# @date 2015-12-06

class Util(object):
    @staticmethod
    def saveCsrMatrix(matrix, file_path):
        output_obj = open(file_path, 'w')
        with output_obj:
            for i in xrange(0, matrix.shape[0]):
                begin_index = matrix.indptr[i]
                next_begin_index = matrix.indptr[i + 1]
                column_id_values = []
                for index in xrange(begin_index, next_begin_index):
                    column_id_values.append((matrix.indices[index],
                        matrix.data[index]))
                column_id_values.sort(key=lambda x: x[1], reverse=True)
                for column_id, value in column_id_values:
                    output_obj.write('({0},{1})\t'.format(column_id, value))
                output_obj.write('\n')

    @staticmethod
    def saveNdArray(array, file_path):
        output_obj = open(file_path, 'w')
        with output_obj:
            if len(array.shape) == 2:
                for i in xrange(0, array.shape[0]):
                    for j in xrange(0, array.shape[1]):
                        output_obj.write('{0}\t'.format(array.item(i, j)))
                    output_obj.write('\n')
            elif len(array.shape) == 1:
                for i in xrange(0, array.shape[0]):
                    output_obj.write('{0}\n'.format(array.item(i)))

    @staticmethod
    def saveVocabulary(vocabulary, file_path):
        output_obj = open(file_path, 'w')
        vocabulary_list = vocabulary.items()
        vocabulary_list.sort(key=lambda x: x[1])
        with output_obj:
            for text, index in vocabulary_list:
                output_obj.write(u'{0}\t{1}\n'.format(index, text).encode(
                    'utf8'))



