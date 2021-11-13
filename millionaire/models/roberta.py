import pickle
from typing import Dict

from transformers import pipeline

from millionaire import DATA_PATH

ROBERT_PATH = DATA_PATH / 'roberta.pkl'


def dump_roberta():
    classifier = pipeline("zero-shot-classification", )
    with open(ROBERT_PATH, 'wb') as f:
        pickle.dump(classifier, f)


class RoBertaAns:
    _classifier = None

    def test(self):
        return True

    @property
    def classifier(self):
        if self._classifier is None:
            with open(ROBERT_PATH, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                self._classifier = unpickler.load()
        return self._classifier

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
        default_ans = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            }
        dict_ans = {v: int(k[-1]) for k, v in ans.items()}
        cl_ans = self.classifier(q, list(ans.values()))
        cl_ans = {dict_ans[k]: v
                  for k, v in zip(cl_ans['labels'], cl_ans['scores'])}
        return {**default_ans, **cl_ans}


if __name__ == '__main__':
    # dump_roberta()
    question = "Что есть у Пескова?"
    answers = {
        'answer_1': "Усы",
        'answer_2': "Борода",
        'answer_3': "Лысина",
        'answer_4': "Третья нога",
        }
    print(RoBertaAns()(question, answers))
