import random

import pandas as pd
import requests

from millionaire import DATA_PATH

money = [(100, False),
         (200, False),
         (300, False),
         (500, False),
         (1000, True),
         (2000, False),
         (4000, False),
         (8000, False),
         (16000, False),
         (32000, True),
         (64000, False),
         (125000, False),
         (250000, False),
         (500000, False),
         (1000000, False)]

number_of_game = 1
_available_help = ["fifty fifty", "can mistake", "new question"]
available_help = ["fifty fifty", "can mistake", "new question"]
bank = 0
saved_money = 0

server_host = 'http://127.0.0.1:12301'


def ask(number_of_game,
        row,
        i,
        saved_money,
        available_help,
        ff=False,
        after_cm=0):
    request_data = {
        'number of game': number_of_game,
        'question':       row['Вопрос'],
        'question money': money[i][0],
        'saved money':    saved_money,
        'available help': available_help,
        'answer_1':       row['1'],
        'answer_2':       row['2'],
        'answer_3':       row['3'],
        'answer_4':       row['4']
        }

    if ff:
        # упрощение. оставляем правильный и случайный вариант
        correct = [1, 2, 3, 4]
        correct.remove(row['Правильный ответ'])
        i1 = random.choice(correct)
        correct.remove(i1)
        i2 = random.choice(correct)
        request_data[f'answer_{i1}'] = None
        request_data[f'answer_{i2}'] = None

    if after_cm != 0:
        request_data[f'answer_{after_cm}'] = None

    print(request_data)
    return requests.post(
        f'{server_host}/predict',
        data=request_data).json()


def check_answer(answer, row, i, saved_money, cm=False):
    global bank
    new_saved_money = saved_money
    request_data = {
        'number of game': number_of_game,
        'question':       row['Вопрос'],
        'answer':         None if cm else int(row['Правильный ответ']),
        }

    if answer == int(row['Правильный ответ']):
        bank = money[i][0]
        if money[i][1]:
            new_saved_money = money[i][0]
        request_data['response type'] = 'good'
    elif cm:
        request_data['response type'] = 'try again'
    else:
        bank = saved_money
        request_data['response type'] = 'bad'

    request_data['bank'] = bank
    request_data['saved money'] = new_saved_money

    requests.post(
        f'{server_host}/result_question',
        data=request_data).json()
    return bank, new_saved_money, answer == int(row['Правильный ответ'])


if __name__ == '__main__':
    total_bank = 0
    dataset = pd.read_csv(DATA_PATH / "boot_camp_train.csv", ).sample(frac=1)
    # dataset1 = pd.read_csv(DATA_PATH / "part_test.csv", ).sample(frac=1)
    # dataset1['Правильный ответ'] += 1
    # dataset = pd.concat([dataset, dataset1], ignore_index=True)
    print(dataset)
    last_i = 0
    print(len(dataset))
    for i, row in enumerate(dataset.iterrows()):
        print(f"---------{i}------------")
        i -= last_i
        resp = ask(number_of_game, row[1], i, saved_money, available_help)
        print(resp, int(row[1]['Правильный ответ']))
        if 'end game' in resp:
            last_i += i
            number_of_game += 1
            total_bank += bank
            print("Total:", total_bank, "in this time", bank)
            bank = 0
            saved_money = 0
            available_help = _available_help[:]
            continue
        elif 'answer' in resp:
            if 'help' in resp:
                assert resp.get('help') == "can mistake"
                assert "can mistake" in available_help
                available_help.remove("can mistake")
                bank, saved_money, status = check_answer(
                    int(resp.get('answer')), row[1], i, saved_money, cm=True)
                if not status:
                    resp2 = ask(number_of_game, row[1], i, saved_money,
                                available_help,
                                after_cm=int(resp.get('answer')))
                    print(resp2, int(row[1]['Правильный ответ']))
                    bank, saved_money, _ = check_answer(
                        int(resp2.get('answer')), row[1], i, saved_money)
            else:
                bank, saved_money, status = check_answer(
                    int(resp.get('answer')),
                    row[1], i, saved_money)
        else:
            if resp.get('help') == "fifty fifty":
                assert "fifty fifty" in available_help
                available_help.remove('fifty fifty')
                resp2 = ask(number_of_game, row[1], i, saved_money,
                            available_help, ff=True)
                print(resp2, int(row[1]['Правильный ответ']))
                bank, saved_money, status = check_answer(
                    int(resp2.get('answer')),
                    row[1], i, saved_money)
            elif resp.get('help') == "new question":
                assert "new question" in available_help
                available_help.remove('new question')
                resp2 = ask(number_of_game, row[1], i, saved_money,
                            available_help)
                print(resp2, int(row[1]['Правильный ответ']))
                bank, saved_money, status = check_answer(
                    int(resp2.get('answer')),
                    row[1], i,
                    saved_money)
        print(bank, saved_money, status)

        if not status:
            last_i += i
            number_of_game += 1
            total_bank += bank
            print("Total:", total_bank, "in this time", bank)
            bank = 0
            saved_money = 0
            available_help = _available_help[:]
