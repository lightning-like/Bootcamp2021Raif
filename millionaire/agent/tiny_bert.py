import pickle
from typing import Dict

import numpy as np
import torch
from transformers import AutoModel
from transformers import AutoTokenizer

from millionaire import DATA_PATH

TINY_PATH = DATA_PATH / 'tiny.pkl'


def distance(v1, v2):
    return np.sqrt(np.sum((v1 - v2)**2))


def dump_tiny():
    tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny")
    model = AutoModel.from_pretrained("cointegrated/rubert-tiny")

    with open(TINY_PATH, 'wb') as f:
        pickle.dump((model, tokenizer), f)


class TinyAns:
    _model = None
    _tokenizer = None

    @property
    def model(self):
        if self._model is None:
            with open(TINY_PATH, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                self._model, self._tokenizer = unpickler.load()
        return self._model, self._tokenizer

    def __call__(self,
                 q: str,
                 ans: Dict[str, str]
                 ):
        """

        :param q:
        :param ans:
        :return: ['answer_1',
                 'answer_2',
                 'answer_3',
                 'answer_4',]
        """

        q = embed_bert_cls(question, *self.model)
        cl_ans = {a: - abs(distance(q, embed_bert_cls(a, *self.model)))
                  for a in ans.values()}

        default_ans = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            }
        dict_ans = {v: int(k[-1]) for k, v in ans.items()}

        cl_ans = {dict_ans[k]: v
                  for k, v in cl_ans.items()}
        return {**default_ans, **cl_ans}


def embed_bert_cls(text, model, tokenizer):
    t = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**{k: v.to(model.device) for k, v in t.items()})
    embeddings = model_output.last_hidden_state[:, 0, :]
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].cpu().numpy()


if __name__ == '__main__':
    question = "Что есть у Пескова?"
    answers = {
        'answer_1': "Усы",
        'answer_2': "Борода",
        'answer_3': "Лысина",
        'answer_4': "Третья нога",
        }
    dump_tiny()
    print(TinyAns()(question,answers))