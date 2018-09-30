class Model:

    def __init__(self):
        self.if_rnn = True
        self.rnn_units = 200
        self.model = None
        self.max_len = 100
        self.num_words = 20000
        self.embedding_matrix = None
        self.embedding_trainable = False
        self.EMBEDDING_DIM = 200
        self.class_num = 2

    def build_model(self):
        pass

    def train_model(self):
        pass

    def predict(self):
        pass
