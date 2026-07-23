# RAG Architecture Overview

## Источники

- Транскрипция: `05_lec_RAG_architecture_overview.trans.txt`
- Дополнительная сверка: `slides_M1.pdf`

## Состояние транскрипции

Файл транскрипции пуст. Поэтому содержательные заметки ниже составлены только по соответствующему разделу `slides_M1.pdf` с заголовком `RAG Architecture Overview`.

## Normal LLM Use

На слайдах normal LLM use показан как простая цепочка:

- Prompt;
- LLM;
- Response.

В этом варианте LLM отвечает без отдельного retrieval stage и без добавления relevant documents из knowledge base.

## Компоненты RAG System

Слайды показывают RAG System как связку:

- Prompt;
- Retriever;
- Knowledge Base;
- Relevant Documents;
- Augmented Prompt;
- LLM;
- Response.

Retriever обращается к Knowledge Base и возвращает Relevant Documents.

## Augmented Prompt

В RAG system исходный prompt дополняется retrieved documents.

Пример augmented prompt со слайда:

> Why are hotels in Vancouver so expensive this coming weekend? Here are the five relevant articles that may help you respond. \<retrieved articles\>

Этот пример показывает, что LLM получает не только вопрос пользователя, но и relevant articles, которые должны помочь ответить.

## Added latency и better responses

Слайды отмечают tradeoff:

- RAG adds latency;
- RAG can produce better responses.

В примере про Vancouver response grounding связан с retrieved information о том, что Taylor Swift is performing her Eras Tour in Vancouver at BC Place Stadium on December 6-8, 2024.

## Advantages of RAG

Слайды перечисляют advantages of RAG.

### Injects missing knowledge

RAG adds info not in the training data.

Примеры на слайде:

- policies;
- updates.

### Reduces hallucinations

RAG grounds answers with relevant context. Это reduces hallucinations because the model has specific context to use.

### Keeps models up to date

RAG reflects new info by updating the knowledge base.

Это позволяет не полагаться только на training data модели.

### Enables source citation

RAG includes sources for verifiable answers.

### Focuses model on generation

Retriever finds facts, and LLM writes responses.

На слайдах это подано как разделение ролей:

- Retriever работает с Knowledge Base и relevant facts;
- LLM формирует final response.
