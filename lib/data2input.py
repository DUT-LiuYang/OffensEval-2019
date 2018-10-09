from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np


class data2input(object):

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"
        self.EMBEDDING_DIM = 200

    def read_sentences(self, file=""):
        sentences = []
        rf = open(self.dir + file, 'r', encoding='utf-8')
        while True:
            line = rf.readline()
            if line == "":
                break
            sentences.append(line.strip("\n"))
        rf.close()
        return sentences

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

    def convert_embedding_file(self,
                               origin_embedding_file="",
                               word_num=10000,
                               word_index={}):
        """
        extract word embeddings which would be looked up from the origin
        embedding file.
        """
        rf = open(self.data_dir + origin_embedding_file, 'r', encoding='utf-8')
        embeddings_index = {}
        print("reading embedding from " + origin_embedding_file)
        count = 0
        for line in rf:
            count += 1
            if count % 100000 == 0:
                print(str(count))
            values = line.split()
            index = len(values) - self.EMBEDDING_DIM
            if len(values) > (self.EMBEDDING_DIM + 1):
                word = ""
                for i in range(len(values) - self.EMBEDDING_DIM):
                    word += values[i] + " "
                word = word.strip()
            else:
                word = values[0]

            coefs = np.asarray(values[index:], dtype='float32')
            embeddings_index[word] = coefs
        rf.close()
        print("finish.")

        num_words = min(word_num, len(word_index))
        embedding_matrix = np.zeros((num_words + 1, self.EMBEDDING_DIM))
        for word, i in word_index.items():
            if i >= word_num:
                continue
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                # words not found in embedding index will be all-zeros.
                embedding_matrix[i] = embedding_vector
            else:
                print(word)

        embedding_matrix_file = self.dir + "embedding_matrix.txt"
        print("writing embedding matrix to " + embedding_matrix_file)
        wf = open(embedding_matrix_file, 'w', encoding='utf-8')
        for embedding in embedding_matrix:
            for num in embedding:
                wf.write(str(num) + " ")
            wf.write("\n")
        print("finish.")
        wf.close()


if __name__ == '__main__':
    x = data2input()
    print("========== reading text from file. ============")
    train_sentence_file = "sub1.txt"
    sentences = x.read_sentences(train_sentence_file)
    _, tk = x.convert_text_to_input(sentences, max_len=100)
    print("========== the word index and input sentences are generated. ============")

    origin_embedding_file = "glove.twitter.27B.200d.txt"
    x.convert_embedding_file(origin_embedding_file=origin_embedding_file, word_index=tk.word_index)
