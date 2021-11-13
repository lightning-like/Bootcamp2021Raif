import pickle
from typing import Dict

import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances

# from tiny_bert import embed_bert_cls
from millionaire import DATA_PATH
from millionaire.models import QA_PATH
from millionaire.models.tiny_bert import embed_bert_cls
from millionaire.models.tiny_bert import TinyAns


class Embedder():

    def __init__(self):
        self.embed_bert_cls = embed_bert_cls
        self.tiny = TinyAns()

    def embedding(self, text: str):
        return self.embed_bert_cls(text, *self.tiny.model)

    def transform(self, texts):
        return np.array([self.embedding(text) for text in texts])


class BaselineIndexer():
    def __init__(self, embedder: Embedder, metric='cosine'):
        """
          metric: as in sklearn.metrics
        """
        self.embedder = embedder
        self.metric = metric
        self._indexer = None
        self.df_umnik = pd.read_csv(QA_PATH / 'df_pandarina.csv',
                                    engine='python')

    def test(self):
        return True

    @property
    def indexer(self):
        if self._indexer is None:
            with open(QA_PATH / 'umnik.pkl', 'rb') as f:
                unpickler = pickle.Unpickler(f)
                self._indexer = unpickler.load()
        return self._indexer

    def build(self, texts: list):
        self._indexer = self.embedder.transform(texts)

    def get_nearest_k(self, text: str, k=3, isDistance=False):
        emb = self.embedder.embedding(text).reshape(1, -1)
        distances = pairwise_distances(emb, self.indexer, metric=self.metric)
        top_k_arguments = np.argsort(np.array(distances))[0][:k]
        if isDistance:
            return distances[:, top_k_arguments], top_k_arguments
        else:
            return top_k_arguments

    def __call__(self,
                 sequence: str,
                 candidate_labels: Dict[str, str],
                 treshhold=0.01
                 ):

        candidate_labels = list(candidate_labels.values())
        decode_answers = {
            candidate_labels[0]: 1,
            candidate_labels[1]: 2,
            candidate_labels[2]: 3,
            candidate_labels[3]: 4,
            }
        result = 0

        default_ans = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            }

        try:
            dist, idx = index_f.get_nearest_k(sequence, 1, True)
            if dist <= treshhold:
                umnik_str = self.df_umnik.iloc[idx[0]]['1']
                umnik = index_f.embedder.embedding(umnik_str).reshape(1, -1)
                cur_answers = [index_f.embedder.embedding(q) for q in
                               candidate_labels]
                distances = pairwise_distances(umnik, cur_answers,
                                               metric='cosine')
                result = (np.argsort(np.array(distances))[0] + 1)[0]
        finally:
            default_ans[result] = 1
            return default_ans


def store():
    # Загрузка Вопросов из умника
    df_umnik = pd.read_csv(DATA_PATH / 'df_pandarina.csv', engine='python')
    # Строим индексер
    index_f = BaselineIndexer(embedder=Embedder())
    index_f.build(df_umnik['Вопрос'])
    with open('../../image/umnik.pkl', 'wb') as f:
        pickle.dump(index_f.indexer, f)

    # Использование:
    idx = index_f.get_nearest_k("Что есть у Пескова?")

    # 3 ближайших ответа по бд:
    print(df_umnik.iloc[idx])


if __name__ == '__main__':
    index_f = BaselineIndexer(embedder=Embedder())
    idx = index_f.get_nearest_k("Что есть у Пескова?")
    print(idx)
