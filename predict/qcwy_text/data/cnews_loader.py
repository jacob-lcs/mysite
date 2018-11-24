# coding: utf-8

import sys
from collections import Counter
import imp


import numpy as np
import tensorflow.contrib.keras as kr

if sys.version_info[0] > 2:
    is_py3 = True
else:
    imp.reload(sys)
    # sys.setdefaultencoding("utf-8")
    is_py3 = False


def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):  # 转换字符编码
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    """
    常用文件操作
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []  # 存储内容和标签
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')  #分离标签和内容
                if content:
                    contents.append(list(native_content(content)))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels


def build_vocab(train_dir, vocab_dir, vocab_size=5567):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file(train_dir)

    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category():
    """读取分类目录，固定"""
    categories = ['软件工程师', 'ERP实施顾问', '标准化工程师', 'ERP技术开发', '电脑维修', '测试员', '高级软件工程师', '仿真应用工程师', '计量工程师', 
    '高级硬件工程师', '技术文员', '计算机辅助设计工程师', '配置管理工程师', '软件UI设计师', '品质经理', '技术总监', '软件测试', '数据库工程师',
     '手机维修', '首席技术执行官', '网络维修', '算法工程师', '维护工程师', '网络管理', '维护经理', '系统分析员', '系统测试',
      '文档工程师', '系统集成工程师', '系统架构工程师', '系统工程师', '项目经理', '信息技术经理', '项目总监', '项目执行', '项目主管',
       '信息技术专员', '需求工程师', '硬件测试', '硬件工程师', 'flash设计', 'web前端开发', 'UI设计师', '电子商务经理', '大数据开发',
        '脚本开发工程师', '视觉设计师', '电子商务总监','网络信息安全工程师', '网络推广专员', '特效设计师', '网络工程师', '网页设计', '网站编辑', 
        '网站策划', '网站架构设计师', '网站维护工程师', '系统管理员', '音效设计师', '游戏策划师', '用户体验设计师','游戏界面设计师', 'SEO',
         '语音视频图形开发工程师', '手机应用开发工程师','多媒体游戏开发工程师', '互联网软件开发工程师', '产品经理', '产品专员', '产品总监']

    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id


def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=600):
    """将文件转换为id表示"""
    contents, labels = read_file(filename)

    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]
