from lib.Model import Model as BaseModel
from keras.layers import Dense, Embedding, Bidirectional, GRU, TimeDistributed, Input, Dropout
from keras.models import Model


class PlayModel(BaseModel):

    def __init__(self, rnn_units, max_len, num_words, embedding_matrix, embedding_trainable,
                 EMBEDDING_DIM, class_num):
        super(PlayModel, self).__init__()
        self.rnn_units = rnn_units
        self.max_len = max_len
        self.num_words = num_words
        self.embedding_matrix = embedding_matrix
        self.embedding_trainable = embedding_trainable
        self.EMBEDDING_DIM = EMBEDDING_DIM
        self.class_num = class_num

    def build_model(self):

        sentences = Input(shape=(self.max_len,), dtype='int32', name='sentence_input')

        sentence_embedding_layer = Embedding(self.num_words + 1,
                                             self.EMBEDDING_DIM,
                                             weights=[self.embedding_matrix],
                                             input_length=self.max_len,
                                             trainable=False,
                                             mask_zero=True)

        sentence_embedding = sentence_embedding_layer(sentences)

        sentence_embedding = Bidirectional(GRU(300,
                                               activation="relu",
                                               return_sequences=False,
                                               recurrent_dropout=0.5,
                                               dropout=0.5))(sentence_embedding)

        x = TimeDistributed(Dense(200, activation='tanh'))(sentence_embedding)
        x = Dropout(rate=0.5)(x)
        predictions = Dense(self.class_num, activation='softmax')(x)

        self.model = Model(inputs=[sentences], outputs=predictions).compile(loss=['categorical_crossentropy'],
                                                                            optimizer='rmsprop',
                                                                            metrics=['accuracy'])

        return self.model
