# Retriever Architecture Overview

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\02_lec_Retriever_architecture_overview.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Зачем нужен общий mental model

В модуле подробно рассматриваются разные search techniques, но перед этим полезно иметь общий mental model всей системы: как устроена architecture `retriever` и как его компоненты работают вместе.

## Общий поток retrieval

Когда RAG-система получает prompt, он сначала отправляется в `retriever`.

`retriever` имеет доступ к `knowledge base`. В лекции ее предлагают представлять как набор text files, лежащих в database.

Задача `retriever`:

1. быстро решить, какие documents наиболее relevant to the prompt;
2. вернуть эти documents;
3. передать их дальше, чтобы они попали в `augmented prompt` для `LLM`.

## Две основные search techniques

Большинство современных `retriever` используют две search techniques.

### Keyword search

`keyword search` ищет документы, которые содержат exact words из prompt.

Этот подход:

- traditional;
- time-tested;
- decades used in information retrieval systems.

Он делает систему чувствительной к точным словам пользователя.

### Semantic search

`semantic search` ищет документы, whose meaning similar to the prompt.

Этот подход делает `retriever` more flexible, потому что позволяет находить документы, релевантные по смыслу, даже если они не содержат exact words из prompt.

## Первичные результаты поиска

Каждая search technique возвращает collection of documents. В лекции приведен примерный масштаб:

- 20 to 50 documents from keyword search;
- 20 to 50 documents from semantic search.

Многие документы могут появиться в обоих списках, но из-за разного стиля поиска их rank может отличаться.

## Metadata filtering

После получения двух списков каждый из них фильтруется по metadata.

Пример из лекции:

- часть документов relevant to engineering team;
- часть документов relevant to HR;
- система знает, к какой team относится пользователь;
- metadata filter пропускает дальше только документы, relevant to that department.

`metadata filtering` применяется уже после получения ranked lists и отсекает документы по rigid criteria.

## Объединение списков

После metadata filtering у `retriever` есть два filtered lists:

- список, сгенерированный keyword search;
- список, сгенерированный semantic search.

Эти списки combined to create a final ranking of the most relevant documents.

Затем `retriever`:

1. берет top ranked documents из final list;
2. завершает retrieval;
3. отправляет documents дальше, чтобы они были добавлены в `augmented prompt`.

## Hybrid search

Такой стиль поиска называется `hybrid search`, потому что он uses multiple techniques to produce final document ranking.

> Важный процесс: hybrid search объединяет keyword search, semantic search и metadata filtering, чтобы получить итоговый ranked list документов.

## Роль каждой техники

Каждая техника дает свой вклад в overall performance of the retriever.

`keyword search`:

- чувствителен к exact words in the prompt;
- полезен, когда важны точные термины или названия.

`semantic search`:

- дает flexibility;
- находит documents whose meaning is similar to the prompt;
- работает даже без совпадения exact words.

`metadata filtering`:

- позволяет exclude documents based on rigid criteria;
- делает то, чего не дают keyword search и semantic search.

## Дизайн high performing retriever

Designing a high performing `retriever` означает:

1. понимать relative strengths каждой техники;
2. понимать limitations каждой техники;
3. tune balance between techniques;
4. align retrieval pipeline with project needs.

Лекция завершает переходом к metadata filtering как к simplest of the three techniques.
