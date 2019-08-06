import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging
import time
from functools import wraps
import os
import re
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from opencc import OpenCC


def save_log():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler('word2vec.log', mode='w')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def is_chinese(word):
    for ch in list(word):
        if ch < u'\u4e00' or ch > u'\u9fff':
            return False
    return True


def decorator(func):
    @wraps(func)
    def wrap():
        start_time = time.time()
        logger.info('input {} function，start time：{}'.format(func.__name__, start_time))
        func()
        logger.info('{} function run end，running spends：{} second'.format(func.__name__, str(time.time() - start_time)))
        logger.info('*' * 50 + ' spilt line ' + '*' * 50)

    return wrap


@decorator
def cut_word():
    cc = OpenCC('t2s')
    for parent, dir_names, file_names in os.walk(DATA_PATH, followlinks=True):
        for filename in file_names:
            if re.match(r'^w', filename):
                file_path = os.path.join(parent, filename)
                output = open(CUT_WORDS_RESULT, 'w', encoding='utf-8')
                with open(file_path, 'r', encoding='utf-8') as content:
                    for text_num, line in enumerate(content):
                        line = line.strip('\n')
                        if not line.strip(): continue
                        if re.findall('<.*>', line): continue
                        words = jieba.cut(cc.convert(line), cut_all=False)
                        for word in words:
                            if is_chinese(word):
                                output.write(word + ' ')
                        output.write('\n')
                output.close()
                logger.info('file name：{} finished!'.format(filename))
                print('file name：{} finished!'.format(filename))


@decorator
def train_model():
    sentences = LineSentence(CUT_WORDS_RESULT)
    model = Word2Vec(sentences, size=300, min_count=100, window=7)
    model.save(MODEL_PATH)


@decorator
def predict_model():
    model = Word2Vec.load(MODEL_PATH)
    s_1, s_2 = '', ''
    try:
        # 查看两个词相似度
        s_1 = model.similarity('爱情', '友情')
        # 查看和 这个词最相关的几个词
        s_2 = model.most_similar('数学')
    except KeyError:
        pass
    print(s_1)
    print(s_2)
    # 查看这个词的 词向量
    print(model.wv['数学'])


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    for word in model.wv.vocab:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)
    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
    plt.figure(figsize=(8, 8))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


if __name__ == '__main__':
    logger = save_log()
    DATA_PATH = '../../zhwiki/'
    CUT_WORDS_RESULT = 'cut_words_result'
    MODEL_PATH = 'model.Word2Vec'
    cut_word()
    train_model()
    model = Word2Vec.load(MODEL_PATH)
    predict_model()
    tsne_plot(model)
