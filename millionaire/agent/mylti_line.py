import os
from typing import Dict

import numpy as np
from flask import Flask
from flask import request

from millionaire import DATA_PATH
from millionaire.log import configure_logger
from millionaire.log import get_logger
from millionaire.models.elastic import Elastic
from millionaire.models.roberta import RoBertaAns
from millionaire.models.tiny_bert import TinyAns

app = Flask(__name__)


nlp_models = [RoBertaAns(), Elastic(), Elastic('quests'), TinyAns()]

nlp_models = [i for i in nlp_models if i.test()]

configure_logger('predict', 'debug')
LOGGER = get_logger('predict')

LOGGER.info(DATA_PATH)

Train = os.environ.get('Train', False)
LOGGER.debug(Train)

configure_logger('result_question', 'debug')
LOGGER_R = get_logger('result_question')

DEFAULT_STATE = {
    'BANK':         0,
    'CURRENT_GAME': 0,
    'CAN_USE_CLUE': True,
    'USED_CLUE':    tuple()
    }

STATE = {
    'BANK':         0,
    'CURRENT_GAME': 0,
    'CAN_USE_CLUE': True,
    'USED_CLUE':    tuple()
    }

CLUE_55 = "fifty fifty"
CLUE_AGAIN = "can mistake"
CLUE_NEW = "new question"


@app.route("/predict", methods=['POST'])
def predict():
    LOGGER.debug(list(request.values.items()))
    # data: Dict[str, str] = request.form.get('data')
    data: Dict[str, str] = {k: v for k, v in request.values.items()}
    LOGGER.debug(data)
    if STATE['CURRENT_GAME'] != int(data.get('number of game')):
        STATE.update(DEFAULT_STATE)
        STATE['CURRENT_GAME'] = int(data.get('number of game'))

    used_clue = STATE['USED_CLUE'] if STATE['CAN_USE_CLUE'] else [CLUE_55,
                                                                  CLUE_AGAIN,
                                                                  CLUE_NEW]
    STATE["BANK"] = data['question money']
    LOGGER.debug(used_clue)
    answers = {ans_n: ans_test
               for ans_n, ans_test in data.items()
               if ans_n.startswith('answer') and ans_test is not None
               }

    LOGGER.debug(f'try predict {answers}')

    all_ans = [i(data['question'], answers) for i in nlp_models]
    all_ans = [{k: v / sum(one_ans.values()) for k, v in one_ans}
               for one_ans in all_ans]

    ans = {k: (np.mean([one_ans[k] for one_ans in all_ans]),
               np.min([one_ans[k] for one_ans in all_ans]),
               np.max([one_ans[k] for one_ans in all_ans]),
               )
           for k, v in all_ans[0]}
    ans = {k: v / sum(ans.values()) for k, v in ans}

    best_ans = max(ans.items(), key=lambda x: x[1])[0]
    all_p = sorted(list(ans.values()))
    all_p = all_p[-1] / all_p[-2]

    LOGGER.debug(f"get props: {ans}")
    LOGGER.debug(STATE)

    if STATE["BANK"] == 0 and CLUE_55 not in used_clue:
        resp = {
            'help': f"{CLUE_55}",
            }
        LOGGER.debug(f"send: {resp}")
        STATE['CAN_USE_CLUE'] = False
        STATE['USED_CLUE'] += (CLUE_55,)
        return resp

    if CLUE_AGAIN not in used_clue and all_p[-1] > 0.27:
        resp = {
            'help':   "can mistake",
            'answer': best_ans
            }
        STATE['CAN_USE_CLUE'] = False
        STATE['USED_CLUE'] += (CLUE_AGAIN,)
        LOGGER.debug(f"send: ")
        LOGGER.debug(resp)
        return resp

    if all_p < 1.3 and STATE["BANK"] not in (100, 1_000, 32_000):
        if CLUE_NEW not in used_clue:
            resp = {
                'help': "new question",
                }
            STATE['CAN_USE_CLUE'] = False
            STATE['USED_CLUE'] += (CLUE_NEW,)
            LOGGER.debug(f"send: ")
            LOGGER.debug(resp)
            return resp

    if (data['question money'] not in (100, 1_000, 32_000)
            and all_p < 1.3
            and STATE['CAN_USE_CLUE']):
        resp = {
            'end game': "take money",
            }
        LOGGER.debug(resp)

        return resp
    resp = {
        'answer': best_ans
        }
    LOGGER.debug(f"send: ")
    LOGGER.debug(resp)
    return resp

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
    data: Dict[str, str] = {k: v for k, v in request.values.items()}
    LOGGER_R.info(data)
    if data.get('response type') != 'try again':
        STATE['CAN_USE_CLUE'] = True
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


app.run(host='0.0.0.0', port=12301)

# команда-1: port=12301
# команда-2: port=12302
# команда-3: port=12303
# команда-4: port=12304
# команда-5: port=12305
# команда-6: port=12306
# команда-7: port=12307
