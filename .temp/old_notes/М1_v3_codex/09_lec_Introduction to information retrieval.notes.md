# Introduction to Information Retrieval

## Источники

- Основной источник: `theory\Module_1_RAG_Overview\09_lec_Introduction to information retrieval.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_1_RAG_Overview\slides_M1.pdf`

## Назначение retriever

К этому моменту назначение `retriever` уже ясно: он должен предоставлять `LLM` useful information, которая могла быть unavailable when the model was trained.

Лекция объясняет, как этот компонент работает внутри RAG-системы.

## Аналогия с библиотекой

Для объяснения используется аналогия с библиотекой.

Пользователь приходит в библиотеку с вопросом: как приготовить New York-style pizza at home?

Библиотека содержит большую collection of books по многим темам. Чтобы по ней можно было ориентироваться, книги organized in sections and shelves по характеристикам:

- topics;
- genre;
- authors;
- other characteristics.

Если задать вопрос librarian, librarian может помочь найти sections of the library или даже exact books, которые most relevant to the question.

## Соответствие между библиотекой и retriever

У `retriever` есть похожие компоненты.

Соответствия:

- library collection of books соответствует `knowledge base` of documents;
- sections and shelves соответствуют index of documents;
- librarian соответствует механизму search/retrieval;
- вопрос пользователя соответствует prompt/query.

`retriever` создает index документов в `knowledge base`. Index keeps documents organized and makes them easy to search.

> Важное определение: index - структура, которая организует документы `knowledge base` так, чтобы по ним можно было эффективно искать.

## Как выполняется retrieval

В библиотеке librarian понимает meaning of the question и знает, что нужно искать в разделах cooking, Italian cuisine или, возможно, New York.

В RAG-системе `retriever` делает похожее:

1. process the prompt, чтобы понять underlying meaning;
2. uses that understanding to search the index of documents;
3. returns documents from the `knowledge base`, которые считает most relevant to the prompt.

## Ranking и relevance score

Когда `retriever` выполняет search, он ranks documents in the `knowledge base` by relevance to the prompt.

Каждый документ получает numerical score, который quantifies its relevance. Обычно это мера similarity между:

- text of the prompt;
- text of the document.

Documents with the highest scores are returned.

Лекция отмечает, что существует variety of approaches to calculating similarity scores. Эти подходы будут изучаться позже в курсе.

## Retriever должен не только находить, но и отсеивать

Well-designed `retriever` должен возвращать relevant documents, но также withhold irrelevant documents.

Если на вопрос о New York-style pizza `retriever` вернет все документы в `knowledge base`, технически среди них будут все relevant documents. Но они потеряются в mountain of irrelevant information.

Такой подход также приводит к проблемам, уже обсуждавшимся в лекции про `LLM`:

- costly prompts;
- риск полностью use up the `context window`.

С другой стороны, если retrieving only the highest-ranked documents, можно пропустить valuable relevant information, которая находится на позициях 2nd, 3rd или 4th.

## Tradeoff в количестве возвращаемых документов

В идеальном случае `retriever` perfectly ranks documents и chooses the exact right number to return.

На практике `retriever` иногда:

- ranks some relevant documents too low;
- ranks irrelevant documents too high.

Из-за этого difficult to confidently decide how many documents to return.

Для оптимизации performance `retriever` нужно:

- monitor it over time;
- experiment with different settings.

Эти действия будут подробно рассматриваться в курсе.

> Важный вывод: retrieval - это не только поиск "самого похожего" документа, но и настройка баланса между полнотой релевантной информации и ограничением нерелевантного context.

## Information retrieval как зрелая область

Многие знакомые software systems выполняют задачи, похожие на работу `retriever`.

Примеры:

- web search engine retrieves web pages relevant to a web search;
- relational database retrieves rows and tables that match a SQL query.

Broader field of information retrieval был already mature, когда large language models только появились. Идеи этой области лежат в основе design of retrievers and RAG systems.

## Практическая реализация retriever

Теоретически `retriever` можно реализовать разными способами.

Поскольку у многих компаний данные уже лежат в traditional relational databases, было бы удобно оставить данные там и retrieve from that database to power a RAG system.

При этом на scale большинство retrievers обычно строятся поверх `vector database`.

`vector database`: specialized type of database, optimized for rapidly finding documents in a `knowledge base` that most closely match a prompt.

В курсе будут изучаться:

- general principles of information retrieval, которые используются в разных search technologies;
- `vector databases`, обычно используемые как `retriever` в production-scale RAG system.

## Выводы лекции

`retriever` ищет в `knowledge base` документы, релевантные prompt, организуя их через index, ranking и similarity scores. Его качество зависит не только от способности найти relevant documents, но и от способности не перегрузить `LLM` irrelevant information. Поэтому retrieval требует monitoring и experiment with settings.

