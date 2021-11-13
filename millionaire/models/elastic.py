from typing import Dict

from elasticsearch import Elasticsearch


class Elastic:

    def test(self):
        try:
            self._get_score('test', self.index)
        except:
            return False

        return True

    def __init__(self, what_index="all"):
        """

        :param what_index: all / quotes
        """
        self.es = Elasticsearch([{
            'host': 'localhost',
            'port': 9200
            }], timeout=60)
        if what_index == 'all':
            self.index = 'ruwiki'
        else:
            self.index = 'ruwikiq'

    def _get_score(self, text, index):
        res = self.es.search(index=index,
                             body={
                                 "query": {
                                     "match":
                                         {
                                             "text": text
                                             }
                                     }
                                 }
                             )

        return sum(x['_score'] for x in res['hits']['hits'])

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
        cl_ans = self._get_score([q + a for a in ans.values()], self.index)
        cl_ans = {dict_ans[k]: v
                  for k, v in zip(list(ans.values()), cl_ans['scores'])}
        return {**default_ans, **cl_ans}

def test():
    question = "Что есть у Пескова?"
    answers = {
        'answer_1': "Усы",
        'answer_2': "Борода",
        'answer_3': "Лысина",
        'answer_4': "Третья нога",
        }
    print(Elastic()(question,answers))


if __name__ == '__main__':
    test()