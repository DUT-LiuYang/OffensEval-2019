import numpy as np


class ExampleReader(object):

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"

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
        return onehot_label

    def get_embedding_matrix(self, embedding_file=""):
        embedding_matrix_file = self.dir + embedding_file
        embedding_matrix = []
        rf = open(embedding_matrix_file, 'r', encoding='utf-8')
        while True:
            line = rf.readline()
            if line == "":
                break
            embedding_matrix.append([float(x) for x in line.split()])
        rf.close()
        return np.array(embedding_matrix)
