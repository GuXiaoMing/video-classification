#encoding=utf8
def histogram(filtered=False):
    if filtered:
        input_obj = open('./derivants/filtered_videos.txt')
        output_obj = open('./filtered_tag_histogram', 'w')
    else:
        input_obj = open('./source/tag_shortvideos.txt')
        output_obj = open('./tag_histogram', 'w')
    tag_mapping_obj = open('./tag_mapping', 'w')
    tag_video_cnt_dict = dict()
    for line in input_obj:
        line = line.decode('utf8')
        fields = line.strip().split('\t')
        if len(fields) >= 2:
            if filtered:
                tag = fields[0]
            else:
                tag = fields[1]
            tag_video_cnt_dict[tag] = tag_video_cnt_dict.get(tag, 0) + 1
    hist = tag_video_cnt_dict.items()
    hist.sort(key=lambda x: x[1], reverse=True)

    for tag, video_cnt in hist:
        output_obj.write('{0}\t{1}\n'.format(tag.encode('utf8'), video_cnt))
        tag_mapping_obj.write('{0}\t{0}\n'.format(tag.encode('utf8')))

def countBrief():
    input_obj = open('./tag_shortvideos.txt')
    brief_cnt = 0
    tags_cnt = 0
    video_cnt = 0
    for line in input_obj:
        video_cnt += 1
        line = line.decode('utf8')
        fields = line.strip().split('\t')
        if len(fields) >= 3:
            tags = fields[2]
            if tags != '':
                tags_cnt += 1
        if len(fields) >= 4:
            brief = fields[3]
            if brief != '':
                brief_cnt += 1
    print 'brief count is {0}/{1}'.format(brief_cnt, video_cnt)
    print 'tags count is {0}/{1}'.format(tags_cnt, video_cnt)

if __name__ == '__main__':
    histogram(filtered=True)
    # countBrief()
