import jieba
import re


jieba.add_word("一型糖尿病")

def get_new_segment(segment): #  新增的方法 ####
    """
    输入一句话，返回一句经过处理的话: 为了支持中文全称mask，将被分开的词，将上特殊标记("#")，使得后续处理模块，能够知道哪些字是属于同一个词的。
    Args:
        segment(list): input_string list
    Returns:
        new_segment(list): string after process
    example:
        segment = ['一', '型', '糖', '尿', '病', '形', '成', '的', '原', '因', '是', '什', '么', '呢']
        new_segment = ['一', '##型', '##糖', '##尿', '##病', '形', '##成', '的', '原', '##因', '是', '什', '##么', '呢']
    """
    seq_cws = jieba.lcut("".join(segment))
    seq_cws_set = set(seq_cws)
    max_word_len = max([len(_) for _ in seq_cws_set])
    new_segment = []
    i = 0
    while i < len(segment):
        if len(re.findall('[\u4E00-\u9FA5]', segment[i]))==0: # 不是中文的，原文加进去。
            new_segment.append(segment[i])
            i += 1
            continue
        has_add = False
        for length in range(max_word_len,0,-1):
            if i+length>len(segment):
                continue
            if ''.join(segment[i:i+length]) in seq_cws_set:
                new_segment.append(segment[i])
                for l in range(1, length):
                    new_segment.append('##' + segment[i+l])
                i += length
                has_add = True
                break
        if not has_add:
            new_segment.append(segment[i])
            i += 1
    return new_segment


def get_raw_instance(document, max_sequence_length): # 新增的方法
    """
    获取初步的训练实例，将整段按照max_sequence_length切分成多个部分,并以多个处理好的实例的形式返回。
    Args:
        document(list): 一整段
        max_sequence_length(int):最大长度
    Returns:
        result_list(list): 相当于新的document,  安装max_sequence_length拆分的新document, each element is a sequence of text
    """
    max_sequence_length_allowed=max_sequence_length-2
    document = [seq for seq in document if len(seq)<max_sequence_length_allowed]
    sizes = [len(seq) for seq in document]
    result_list = []
    curr_seq = [] # 当前处理的序列
    sz_idx = 0
    while sz_idx < len(sizes):
        # 当前句子加上新的句子，如果长度小于最大限制，则合并当前句子和新句子；否则即超过了最大限制，那么做为一个新的序列加到目标列表中
        if len(curr_seq) + sizes[sz_idx] <= max_sequence_length_allowed: # or len(curr_seq)==0:
            curr_seq += document[sz_idx]
            sz_idx += 1
        else:
            result_list.append(curr_seq)
            curr_seq = []
    # 对最后一个序列进行处理，如果太短的话，丢弃掉。
    if len(curr_seq)>max_sequence_length_allowed/2: # /2
        result_list.append(curr_seq)
    return result_list


if __name__ == '__main__':
    # segment = list("一型糖尿病形成的原因是什么呢")
    # print(segment)
    # print(get_new_segment(segment))
    document = [ "一型糖尿病形成的原因是什么呢" ] * 10
    print(get_raw_instance(document=document, max_sequence_length=128))