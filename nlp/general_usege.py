from deeppavlov import configs, build_model

kbqa_model = build_model(configs.kbqa.kbqa_cq_rus, download=True)
kbqa_model(['Когда родился Пушкин?'])