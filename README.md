# Millionaire

Agent for wint game

Rules:

1) Q&A
2) Choose answer
3) use tips

We have separated task on 2 part

## NLP

Try to get probability of all answers.

##### Literature
1. [All state-of-arts](https://paperswithcode.com/task/answer-selection)
2. [Context Question Answering](http://docs.deeppavlov.ai/en/master/features/skills/odqa.html?highlight=Answer%20Selection)
   * ODQA dataset tries to find open answers => then we can find which answer is the most similar to the predicted one
3. [Ranking and paraphrase identification](http://docs.deeppavlov.ai/en/master/features/models/neural_ranking.html)
4. [Datasets for similar tasks](https://russiansuperglue.com/ru/tasks/)
5. [BERT для классификации русскоязычных текстов](https://habr.com/ru/post/567028/)
6. [Sber approach to NLP](https://habr.com/ru/company/sberbank/blog/567776/)

## Game

RL - task setup:

#### State:
1. Probability answer 1
2. Probability answer 2
3. Probability answer 3
4. Probability answer 4
5. Number of question ( Safety amount, next price )
6. Used or not tips 1
7. Used or not tips 2
8. Used or not tips 3
9. Used or not tips 4

#### Actions:
1. Take price
2. Choose the best answer
3. Take tips 1
3. Take tips 2
3. Take tips 3
3. Take tips 4
