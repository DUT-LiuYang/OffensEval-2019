from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


class data2input(object):

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"

    @staticmethod
    def read_sentences(file=""):
        sentences = []
        rf = open(file, 'w', encoding='utf-8')
        while True:
            line = rf.readline()
            if line == "":
                break
            sentences.append(line)
        rf.close()
        return sentences

    @staticmethod
    def read_label(file=""):
        labels = []
        rf = open(file, 'w', encoding='utf-8')
        while True:
            line = rf.readline()
            if line == "":
                break
            labels.append(int(line))
        rf.close()
        return labels

    @staticmethod
    def label2onehot(labels=[], task=1):
        onehot_label = []
        for index, label in enumerate(labels):
            onehot_label.append([0] * (task + 1))
            onehot_label[index][label] = 1
        return  onehot_label
