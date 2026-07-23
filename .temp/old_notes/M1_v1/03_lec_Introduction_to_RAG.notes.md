# Introduction to RAG

## Источники

- Транскрипция: `03_lec_Introduction_to_RAG.trans.txt`
- Дополнительная сверка: `slides_M1.pdf`

## Что уже умеют LLMs

LLMs described as remarkable tools. Они могут:

- answer questions;
- summarize and rewrite text;
- provide feedback on documents;
- generate code;
- выполнять many other tasks.

Такие задачи еще несколько лет назад seemed out of reach for computers. Взаимодействие с LLM can feel a lot like working with another person.

## Как RAG улучшает LLM

RAG is an approach that further improves the performance of large language models by giving them access to information that they don’t know from their training.

Слайды формулируют это как:

- LLMs are already powerful;
- RAG further improves them;
- LLM + new information.

## Пример с ценами на отели

Лекция использует серию вопросов про отели, чтобы показать, когда требуется retrieval.

### Вопрос 1: почему отели дорогие на выходных

Вопрос:

> Why are hotels expensive on the weekend?

На него обычно можно ответить без дополнительного поиска: больше людей путешествует по выходным, поэтому выше competition for rooms.

Здесь достаточно general knowledge.

### Вопрос 2: почему отели в Vancouver дорогие в ближайшие выходные

Вопрос:

> Why are hotels in Vancouver super expensive this coming weekend?

Для ответа уже нужна дополнительная информация. Если searched online, можно найти, что Taylor Swift is in town this weekend. В транскрипции это названо two-night residency.

На слайде этот пример уточняется: Taylor Swift is performing her Eras Tour in Vancouver at BC Place Stadium on December 6-8, 2024.

С дополнительной информацией снова можно ответить на вопрос.

### Вопрос 3: почему в Vancouver нет большего hotel capacity close to downtown

Вопрос:

> Why doesn’t Vancouver have more hotel capacity close to downtown?

Для ответа потребовался бы deep research into:

- history of Vancouver’s development;
- urban planning in general;
- other specialized information.

На слайдах среди релевантного материала указан пример: zoning laws and city planning since the early 1900s limited hotel growth downtown.

## Две фазы ответа на вопрос

Ответ на вопросы можно представить как two phases:

1. collect any necessary information;
2. reason over that information to develop your response.

Иногда information collection не нужна: general world knowledge достаточно, чтобы respond right away.

В других случаях нужно collect a little bit or even a lot of information.

## Retrieval и Generation

В RAG:

- retrieval is the process of collecting useful information;
- generation is the process of reasoning over that information and responding.

Название Retrieval Augmented Generation становится понятным именно из этой связки: сначала retrieval relevant information, затем augmented generation ответа.

## Почему LLMs выигрывают от retrieval stage

LLMs benefit from the retrieval stage for basically the same reasons people do.

Для текущего объяснения LLM можно представить как систему, которая имеет a wide variety of general knowledge from reading huge chunks of the Internet. Когда пользователь prompt an LLM, модель relies on this knowledge to generate a response.

Для many prompts это works great.

Но в других случаях LLM doesn’t know the information it needs to respond accurately:

- prompt может быть about a very recent event;
- prompt может требовать specialized information;
- нужная информация могла never appear in training data.

Как и от человека, unreasonable to expect LLMs to be experts on every topic. Они provide much better responses when they have access to better information.

## Что LLMs знают после обучения

LLMs are not people who spend time on Wikipedia. Они mathematical models, trained on massive data sets taken from all over the open Internet.

During training process модель learns information contained in the training data.

Когда prompt отправляется в LLM, пользователь надеется, что relevant information была included in the training data, ideally many times.

## Какие данные могут отсутствовать

Lots of information won’t be included in training data.

В лекции и слайдах названы несколько причин:

- companies keep private databases;
- some information is hidden or hard to access;
- news is published every minute of the day;
- LLMs are trained on past data and don’t update automatically.

Из-за этого always be information out there that an LLM wasn’t trained on.

## Основной прием: put it in the prompt

Ключевой вопрос:

> How do you make sure the LLM knows this useful information?

Short answer:

> Just put it in the prompt.

Key idea of a RAG system: modify a prompt before sending it to the large language model.

Помимо original question пользователя можно add in information that helps the LLM respond.

## Augmented prompt

Если пользователь спрашивает RAG system:

> Why are hotels in Vancouver super expensive this weekend?

Система сначала performs a retrieval step to gather relevant information.

Затем language model receives an augmented prompt that includes:

- original question;
- retrieved information.

После этого LLM has the information it needs to respond accurately.

На слайдах augmented prompt показан как original user prompt плюс retrieved articles.

## Retriever

Information needs to be retrieved from somewhere. Component of a RAG system that handles this process is called a retriever.

Retriever:

- manages a knowledge base of trusted, relevant, and possibly private information;
- when RAG system receives a prompt, finds and retrieves the most relevant information from the knowledge base;
- shares that retrieved information with the LLM;
- improves generation by giving the model information it did not have.

На слайде это сведено к схеме:

- Retriever;
- Knowledge Base;
- LLM receives useful retrieved information.

## Полная формулировка Retrieval Augmented Generation

Retrieval Augmented Generation means improving or augmenting the way an LLM generates text by first retrieving relevant information from a knowledge base.

В лекции это пока high-level description of how RAG works. Следующая лекция обещает перейти к example applications.
