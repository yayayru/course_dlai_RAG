# Applications of RAG

## Источники

- Основной источник: `theory\Module_1_RAG_Overview\04_lec_Applications_of_RAG_.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_1_RAG_Overview\slides_M1.pdf`

## Общая идея применений RAG

RAG соединяет off-the-shelf `LLM` с `knowledge base`, содержащей информацию, к которой модель могла не иметь доступа во время training. Многие `LLM`-powered systems используют такую модель.

Общий принцип: если есть набор информации, который, вероятно, не входил в training data модели, его можно использовать как `knowledge base` для улучшения ответов.

## Code generation

Одно важное применение RAG - code generation.

Хотя языковые модели обучались на большом количестве кода, возможно на множестве public Git repositories, корректная генерация кода для конкретного проекта требует specialized information.

`LLM` нужно знать:

- classes в проекте;
- functions;
- definitions;
- общую coding style, используемую в проекте.

Если построить RAG-систему, в которой собственная codebase используется как `knowledge base`, эта информация становится доступной модели. `retriever` может извлекать релевантные classes, definitions и files из repository, а `LLM` после этого лучше генерирует код или отвечает на вопросы, относящиеся к проекту.

> Важный вывод: для code generation RAG помогает не потому, что модель вообще не знает языки программирования, а потому, что ей нужен контекст конкретного проекта.

## Company chatbots

Другое крупное применение - кастомизация chatbots под отдельную компанию.

У каждой компании есть собственные:

- products;
- policies;
- communication guidelines.

Enterprise documents можно рассматривать как `knowledge base`. Это позволяет развернуть `LLM` в нескольких полезных сценариях.

Customer service chatbot может знать:

- информацию о продуктах компании;
- current inventory;
- common troubleshooting steps.

Internal chatbot может:

- accurately отвечать на вопросы о company policies;
- направлять пользователя к useful documentation.

В обоих случаях `knowledge base` помогает ground responses модели в конкретных продуктах или политиках компании. Это снижает вероятность generic или misleading responses.

## Healthcare и legal domains

RAG имеет значимые применения в healthcare и legal domains.

В этих случаях `knowledge base` может содержать:

- legal documents from a particular case;
- тексты недавно опубликованных medical journals;
- другие специализированные и потенциально private documents.

В таких областях precision is imperative, а объем niche и potentially private information велик. Поэтому RAG-based approach может быть единственным способом развернуть достаточно accurate `LLM`-based product, который использует private information.

## AI-assisted web search

Еще одно применение - AI-assisted web search.

Исторически search engines работали похоже на `retriever`: по search query они возвращали relevant websites.

Современные search engines могут предоставлять AI summaries of search results, чтобы быстро представить пользователю наиболее полезную информацию в skimmable format.

Такие AI web summaries можно рассматривать как RAG-систему, где `knowledge base` - весь интернет.

## Personalized assistants

RAG может быть не только large-scale, но и highly personalized.

Персональные assistants в:

- text messages;
- email client;
- word processor;
- calendar;
- других инструментах

могут помогать отправлять сообщения, организовывать расписание, писать документы и завершать проекты.

В этих случаях чем больше context у `LLM` о проекте пользователя, тем лучше она может поддерживать работу. `knowledge base` может быть относительно небольшой:

- text messages;
- contact lists;
- emails;
- folder of documents.

Такие документы могут быть небольшими по масштабу, но плотными по важному context. Поэтому RAG-система с доступом к small-scale personal information может выполнять задачи значительно релевантнее текущей ситуации пользователя.

## Когда появляется возможность для RAG

Лекция формулирует общий критерий: если у компании, организации или отдельного пользователя есть коллекция информации, которая может улучшить качество текста, генерируемого `LLM`, то есть потенциальная возможность для RAG.

Особенно это относится к информации, которая likely wasn't used to train a large-language model.

## Выводы лекции

RAG применим в разных контекстах: code generation, company chatbots, healthcare, legal, web search и personalized assistants. Объединяет эти сценарии то, что `LLM` получает доступ к private, recent, project-specific или otherwise unavailable information и использует ее для более релевантных ответов.

