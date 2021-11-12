import pickle
from typing import Dict

from transformers import pipeline

from QA import QA_PATH

ROBERT_PATH = QA_PATH / 'roberta.pkl'


def dump_roberta():
    classifier = pipeline("zero-shot-classification", )
    with open(ROBERT_PATH, 'wb') as f:
        pickle.dump(classifier, f)


class RoBertaAns:
    _classifier = None

    @property
    def classifier(self):
        if self._classifier is None:
            with open(ROBERT_PATH, 'rb') as f:
                unpickler = pickle.Unpickler(f)
                self._classifier = unpickler.load()
        return self._classifier

    def get_p_ans(self,
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
            'answer_1': 0,
            'answer_2': 0,
            'answer_3': 0,
            'answer_4': 0,
            }
        dict_ans = {v: k for k, v in ans.items()}
        print(dict_ans)
        cl_ans = self.classifier(q, list(ans.values()))
        print(cl_ans)
        cl_ans = {dict_ans[k]: v
                  for k, v in zip(cl_ans['labels'],cl_ans['scores'])}
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
    print(RoBertaAns().get_p_ans(question, answers))
