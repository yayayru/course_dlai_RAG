# RAG Architecture Overview

## Источники

- Основной источник: `theory\Module_1_RAG_Overview\05_lec_RAG_architecture_overview.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_1_RAG_Overview\slides_M1.pdf`

## Основные компоненты RAG

К этому моменту в курсе уже названы ключевые компоненты RAG-системы:

- `LLM`;
- `knowledge base` relevant information;
- `retriever`, который может искать в `knowledge base`.

Лекция объясняет, как эти компоненты работают вместе в общей архитектуре.

## Обычное использование LLM

Обычная схема работы с `LLM` проста:

1. пользователь пишет prompt;
2. prompt отправляется в `LLM`;
3. `LLM` обрабатывает prompt;
4. модель генерирует response.

С точки зрения user experience RAG-система выглядит так же: пользователь отправляет prompt и получает response.

## Что меняется внутри RAG-системы

Внутри RAG-системы появляется несколько дополнительных шагов.

Когда система получает prompt:

1. prompt сначала направляется в `retriever`;
2. `retriever` имеет доступ к `knowledge base`;
3. practically speaking, `knowledge base` - это database of useful documents;
4. `retriever` queries the database;
5. `retriever` возвращает documents, которые считает наиболее relevant to the prompt;
6. система создает `augmented prompt`, включая information from relevant documents в original prompt;
7. `augmented prompt` отправляется в `LLM`;
8. `LLM` генерирует response.

Пример `augmented prompt` из лекции:

- инструкция ответить на вопрос;
- вопрос о том, почему hotels in Vancouver expensive this coming weekend;
- пять relevant articles, которые могут помочь ответить;
- текст этих articles.

После этого система снова работает как обычная `LLM`: модель получает prompt и генерирует ответ.

## Как LLM использует два источника знания

При генерации ответа `LLM` может опираться на:

- knowledge learned from training data;
- additional context, provided by retrieved documents.

Пользовательский опыт остается почти тем же, возможно с небольшой added latency. Пользователь вводит prompt и получает response, но благодаря side route through the retriever вероятность accurate, up to date и context aware ответа становится выше.

> Важный процесс: RAG добавляет маршрут через `retriever` до вызова `LLM`, чтобы original prompt был дополнен релевантными документами из `knowledge base`.

## Главное отличие от прямого LLM-вызова

Главное отличие между direct `LLM` usage и RAG system - добавление `retriever`.

Это простое на вид дополнение дает несколько преимуществ.

## Преимущество 1: доступ к недоступной информации

RAG делает доступной для `LLM` информацию, которой у модели иначе могло не быть.

Примеры:

- company policies;
- personal information;
- this morning's headlines.

В таких случаях RAG часто является единственным способом сделать некоторые виды информации доступными модели.

## Преимущество 2: снижение hallucinations

RAG снижает вероятность hallucinations или misleading responses.

Такие ответы часто возникают, когда `LLM` генерирует текст о темах, которые:

- были исключены из training data;
- упоминались в training data редко.

Добавление релевантной информации прямо в prompt grounds responses модели и делает generic или misleading text менее вероятным.

## Преимущество 3: обновляемость информации

RAG упрощает поддержание `LLM` в актуальном состоянии.

Retraining language model обычно costly и time-consuming. Поэтому `LLM` трудно успевать за very new information.

В RAG-системе можно просто обновить информацию в `knowledge base`, как обновляют entries в любой другой database. Как только изменения indexed, `LLM` сможет отвечать на основе новой информации.

## Преимущество 4: source citation

RAG улучшает способность `LLM` cite sources.

Система может добавить citation information в `augmented prompt`, а модель затем может включить эту информацию в final response. Это:

- grounds response;
- дает human readers возможность углубиться и validate generated text.

## Преимущество 5: разделение работы между компонентами

RAG позволяет `LLM` focus on text generation.

`retriever` фильтрует большой объем информации, находит наиболее важное и relevant, а затем представляет это succinctly. `LLM` по-прежнему должна написать хороший ответ, но от нее не требуют выполнять fact-finding или filtering steps.

Каждый компонент делает то, в чем он силен:

- `retriever` ищет факты и релевантные документы;
- `LLM` пишет response.

## Простая code demo архитектуры

В лекции показана очень простая code demo, где большинство деталей abstracted away.

Используются две функции:

- `retrieve`: wrapper around a retriever, принимает text query и возвращает relevant documents из `knowledge base`;
- `generate`: wrapper around a large language model, принимает text prompt и возвращает response `LLM`.

Последовательность demo:

1. prompt сохраняется в переменной `prompt`;
2. prompt спрашивает, почему hotel prices in Vancouver super expensive this weekend;
3. prompt сначала отправляется directly to `LLM`;
4. затем вызывается `retriever`, чтобы посмотреть, какая additional information есть о prompt;
5. строится `augmented prompt`, содержащий original user question и retrieved information;
6. `augmented prompt` отправляется в `LLM`;
7. модель дает accurate response, integrating retrieved information.

## Выводы лекции

Архитектура RAG сводится к добавлению релевантного context в prompt перед вызовом `LLM`. Это повышает вероятность accurate, up to date и context aware ответов, уменьшает hallucinations, упрощает обновление знаний и позволяет отделить retrieval facts от generation response.

