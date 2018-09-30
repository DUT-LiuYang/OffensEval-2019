from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


class data2input(object):

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"
