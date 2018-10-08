from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


class data2input(object):

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"

    def read_sentences(self, file=""):
        sentences = []
        rf = open(self.data_dir + file, 'w', encoding='utf-8')
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

    def convert_text_to_input(self, sentences=[], max_len=100):
        tk = Tokenizer(num_words=10000, filters="", split=" ")
        tk.fit_on_texts(sentences)
        inputs = tk.texts_to_sequences(sentences)
        inputs = pad_sequences(inputs, maxlen=max_len, padding='post')
        self.write_word_index(tk.word_index)
        self.save_inputs(inputs, self.dir + "train_inputs")
        return inputs, tk

    def write_word_index(self, word_index={}):
        word_index_file = self.dir + "word_index.txt"
        wf = open(word_index_file, 'w', encoding='utf-8')
        for word, index in word_index.items():
            wf.write(word + " " + str(index) + "\n")
        wf.close()

    def save_inputs(self, inputs=[], file=""):
        wf = open(file, 'w', encoding='utf-8')
        for line in inputs:
            for index in line:
                wf.write(str(index) + " ")
            wf.write("\n")
        wf.close()


if __name__ == '__main__':
    x = data2input()
    print("========== reading text from file. ============")
    train_sentence_file = "sentences-sub-task1.txt"
    sentences = x.read_sentences(train_sentence_file)
    x.convert_text_to_input(sentences, max_len=100)
