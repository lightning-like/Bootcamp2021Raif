from typing import Dict

from flask import Flask
from flask import request

from millionaire.QA.roberta import RoBertaAns

app = Flask(__name__)

ASW_50 = {
    'help': "fifty fifty",
    }


@app.route("/predict", methods=['POST'])
def predict():
    roberta = RoBertaAns()
    data: Dict[str, str] = request.form.get('data')

    if (data['question money'] == 100
            and "fifty fifty" in data['available help']):
        return {
            'help': "fifty fifty",
            }

    answers = {ans_n: ans_test
               for ans_n, ans_test in data
               if ans_n.startwith('answer')
               }

    ans = roberta(data['question'], answers)

    if "can mistake" in data['available help']:
        return {
            'help':   "can mistake",
            'answer': max(ans.items(), key=lambda x: x[1]),

            }

    all_p = sorted(list(ans.values()))

    if (all_p[-1] - all_p[-2]) / all_p[-1] < 1.1:
        if "new question" in data['available help']:
            return {
                'help': "new question",
                }
        if data['question money'] not in (1_000, 32_000):
            return {
                'end game': "take money",
                }

    return {
        'answer': max(ans.items(), key=lambda x: x[1]),
        }

    #  data:
    #  {   
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer_1': "Усы",
    #    'answer_2': "Борода",
    #    'answer_3': "Лысина",
    #    'answer_4': "Третья нога",
    #
    #    'question money': 4000,
    #    'saved money': 1000,
    #    'available help': ["fifty fifty", "can mistake", "take money",
    #    'new question' ]
    #
    #  }

    #  resp:
    #  {   
    #
    #    'help': "fifty fifty",
    #
    #  }

    #  resp:
    #  {   
    #
    #    'help': "can mistake",
    #    'answer': 1,
    #
    #  }

    #  resp:
    #  {   
    #
    #    'end game': "take money",
    #
    #  }


@app.route("/result_question", methods=['POST'])
def result_question():
    data = request.form.get('data')

    #  data:
    #  {   
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer': 1,
    #
    #    'bank': 4000,
    #    'saved money': 1000,
    #    'response type': "good"
    #
    #  }

    #  data:
    #  {   
    #
    #    'number of game': 5,
    #
    #    'question': "Что есть у Пескова?",
    #    'answer': 4,
    #
    #    'bank': 1000,
    #    'saved money': 1000,
    #    'response type': "bad"
    #
    #  }

    return {
        'data': 'ok'
        }


app.run(host='127.0.0.1', port=12301)

# команда-1: port=12301
# команда-2: port=12302
# команда-3: port=12303
# команда-4: port=12304
# команда-5: port=12305
# команда-6: port=12306
# команда-7: port=12307
