from Config import TFHUB_HANDLE_PREPROCESS, TFHUB_HANDLE_ENCODER
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow_text as text
from tqdm.notebook import tqdm


class Transfomer:
    model = None
    def fit(self, text_series):
        raise NotImplementedError
    def transform(self, text_series):
        raise NotImplementedError
    def fit_transform(self, text_series):
        self.fit(text_series)
        return self.transform(text_series)

class TFIDF_Transfomer(Transfomer):
    def __init__(self):
        self.model = TfidfVectorizer(min_df= 3, max_df=0.5, analyzer = 'char_wb', ngram_range = (3,5))
    def fit(self, text_series):
        self.model = self.model.fit(text_series)
    def transform(self, text_series):
        return self.model.transform(text_series)

class BERT_Transfomer(Transfomer):
    def __init__(self):
        self.model = BERT_transformer()
    def fit(self, text_series):
        pass
    def transform(self, text_series):
        return self.model(text_series)


def BERT_transformer(tfhub_handle_encoder = TFHUB_HANDLE_ENCODER,
                    tfhub_handle_preprocess = TFHUB_HANDLE_PREPROCESS):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
    preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
    encoder_inputs = preprocessing_layer(text_input)
    encoder = hub.KerasLayer(tfhub_handle_encoder, name='BERT_encoder')
    outputs = encoder(encoder_inputs)['pooled_output']
    return tf.keras.Model(text_input, outputs)


TRANSFORMER_DICT = {
    "TFIDF":TFIDF_Transfomer,
    "BERT":BERT_Transfomer
}


class Embedding:
    def __init__(self):
        self.__transformer_dict = {key:obj() for key, obj in TRANSFORMER_DICT.items()}
        self.__fit_dict = {key:False for key in TRANSFORMER_DICT.keys()}
    def fit(self, text_series):
        self.text_series = text_series
        self.__fit_dict = {key:False for key in self.__fit_dict.keys()}
        self.__fit_dict['BERT'] = True
    def isFit(self, method):
        return self.__fit_dict.get(method)
    def transform(self, method, text_series, batch_size = None):
        if batch_size == None:
            if method == 'BERT':
                return self.__batch_transform(method, text_series, 100)
            else:
                return self.__transform(method, text_series)
        else:
            assert isinstance(batch_size, int)
            return self.__batch_transform(method, text_series, batch_size)
    def __batch_transform(self, method, text_series, batch_size):
        result_list = []
        for i in tqdm(range(0, len(text_series)//batch_size+1)):
            batch_text = text_series.iloc[i*batch_size:(i+1)*batch_size]
            result_list.extend(self.__transform(method, batch_text))
        return result_list
    def __transform(self, method, text_series):
        if method not in self.__transformer_dict:
            raise ValueError("Method is not defined.")
        if not self.isFit(method):
            self.__transformer_dict.get(method).fit(self.text_series)
        return self.__transformer_dict.get(method).transform(text_series)