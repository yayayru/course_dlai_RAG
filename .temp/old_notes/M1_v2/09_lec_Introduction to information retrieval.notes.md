# Introduction to information retrieval

## Источники

- Основной источник: `09_lec_Introduction to information retrieval.trans.txt`.
- Дополнительный источник для сверки терминов и структуры: `slides_M1.pdf`.

## Назначение retriever

К этому моменту курса purpose of the `retriever` уже сформулирован: он должен предоставлять `LLM` useful information, которая потенциально не была доступна модели во время training.

Лекция объясняет, как этот компонент работает.

> **Определение:** `retriever` — компонент `RAG`-системы, который ищет в `knowledge base` документы, релевантные prompt, и передает их дальше для использования `LLM`.

## Аналогия с библиотекой

Работа `retriever` объясняется через аналогию с библиотекой.

Представим, что нужно ответить на вопрос:

- how can I make New York-style pizza at home?

В библиотеке есть большая коллекция книг по многим темам. Чтобы упростить browsing, книги организованы:

- по sections;
- по shelves;
- по характеристикам topics;
- по genre;
- по authors;
- по другим признакам.

Если задать вопрос librarian, librarian может помочь найти:

- нужные sections of the library;
- возможно, exact books, наиболее relevant to the question.

## Компоненты retriever через аналогию

В `RAG`-системе есть похожие элементы.

Где в библиотеке есть collection of books, у `retriever` есть `knowledge base` of documents.

`retriever` также создает `index` документов в `knowledge base`.

> **Определение:** `index` — структура, которая организует документы в `knowledge base` и делает их easy to search.

Индекс выполняет роль организации коллекции, похожую на sections и shelves в библиотеке.

## Как retriever ищет релевантную информацию

Следующий шаг — само извлечение релевантной информации.

В библиотеке можно напрямую спросить librarian. Librarian понимает meaning of the question и знает, где искать: например, в sections про cooking, Italian cuisine или, возможно, New York.

Способность interpret the meaning of your question позволяет librarian:

- определить правильные shelves;
- найти relevant books.

Внутри `RAG`-системы `retriever` делает похожее:

1. Сначала process the prompt, чтобы понять его underlying meaning.
2. Затем использует это понимание, чтобы search the index of documents.
3. После поиска возвращает documents from the `knowledge base`, которые считает most relevant to the prompt.

## Ranking и similarity scores

Во время поиска `retriever` ranks documents in the `knowledge base` по релевантности к prompt.

Каждый document получает numerical score, который quantifies its relevance.

Обычно это означает некоторую меру similarity между:

- text of the prompt;
- text of the document.

Documents with the highest scores are returned.

В лекции отмечается, что есть разные approaches к вычислению similarity scores, и они будут изучаться позже в курсе.

## Баланс между relevant и irrelevant documents

Хорошо спроектированный `retriever` должен не только возвращать релевантные документы, но и отсеивать нерелевантные документы.

Если для вопроса о New York-style pizza `retriever` вернет все документы из `knowledge base`, технически среди них будут все relevant documents. Но они будут lost in a mountain of irrelevant information.

Такой вариант создает проблемы:

- prompts становятся costly;
- можно полностью use up `LLM` `context window`;
- модель получает слишком много нерелевантной информации.

С другой стороны, если извлекать только документы с самым высоким rank, можно пропустить ценную релевантную информацию, которая оказалась на 2-м, 3-м или 4-м месте.

## Идеальный и практический retriever

В perfect world `retriever`:

- perfectly ranks the documents;
- выбирает ровно нужное количество документов для возврата.

На практике `retriever` будет ошибаться:

- иногда relevant documents получают too low rank;
- иногда irrelevant documents получают too high rank.

Из-за этого трудно уверенно решить, сколько документов нужно вернуть.

> **Вывод:** чтобы оптимизировать performance `retriever`, нужно наблюдать за ним со временем и экспериментировать с разными settings.

Лекция подчеркивает, что monitoring и эксперименты с настройками будут подробно показаны в течение курса.

## Связь с familiar software

Многие знакомые виды software выполняют задачи, очень похожие на работу `retriever`.

Примеры:

- web search engine извлекает web pages, релевантные web search;
- relational database извлекает rows и tables, которые соответствуют SQL query.

Более широкая область `information retrieval` уже была зрелой, когда `LLM` только появились. Идеи из этой области лежат в основе проектирования `retriever` и `RAG` systems.

## Реализация retriever и vector database

Теоретически есть много способов реализовать `retriever` в `RAG`-системе.

Поскольку у большинства компаний данные уже находятся в реляционных databases, было бы удобно оставить данные там и найти способ извлекать их из такой database для `RAG`-системы.

В лекции уточняется, что `vector database` не strictly necessary. Но at scale большинство `retriever` будут построены поверх `vector database`.

> **Определение:** `vector database` — специализированная database, оптимизированная для быстрого поиска документов в `knowledge base`, которые наиболее близко соответствуют prompt.

В дальнейшем курсе будут изучаться:

- general principles of `information retrieval`, лежащие в основе разных search technologies;
- `vector database`, которые typically used as a `retriever` inside a production-scale `RAG` system.

## Итог лекции

`retriever` нужен, чтобы найти полезные документы в `knowledge base` и передать их `LLM`.

Ключевые элементы его работы:

- создание `index`;
- понимание prompt;
- поиск по индексу;
- ranking documents по relevance;
- выбор количества документов для возврата;
- оптимизация через monitoring и experiments.

Главная engineering problem состоит в балансе: вернуть достаточно relevant information, но не перегрузить `LLM` irrelevant documents, expensive prompts и ограничением `context window`.
