from deeppavlov import build_model, configs

ranker = build_model(configs.doc_retrieval.ru_ranker_tfidf_wiki, download=True)
question = "Что есть у Пескова?"
answers = {
    'answer_1': "Усы",
    'answer_2': "Борода",
    'answer_3': "Лысина",
    'answer_4': "Третья нога",
    }

print(ranker(question))
print(ranker("Усы"))
print(ranker("Борода"))
print(ranker("Лысина"))
print(ranker("Третья нога"))
