#coding: utf-8
# -N [花千骨] [0(花千骨)] [] -U 1000

input_obj = open('./data/source/new_words_gbk.txt')
output_obj = open('./worddict.man', 'w')

for line in input_obj:
    title = line.strip()
    if title != '':
        entry = '-N [{0}] [0({0})] [] -U 1000\n'.format(title)
        output_obj.write(entry)
