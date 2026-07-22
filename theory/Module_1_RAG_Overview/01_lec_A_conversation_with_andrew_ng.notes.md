# A Conversation with Andrew Ng

## Источники

- Транскрипция: `01_lec_A_conversation_with_andrew_ng.trans.txt`
- Дополнительная сверка: `slides_M1.pdf`

## Главная идея RAG

Retrieval Augmented Generation (RAG) представляется как одна из самых широко используемых техник для повышения качества и точности ответов large language model (LLM).

Обычная LLM начинает с информации, которую получила при обучении, например из данных публичного интернета. Если нужно отвечать на вопросы на основе proprietary data, например собственных документов, RAG дает модели доступ к таким дополнительным данным. Благодаря этому LLM может отвечать фактами, на которых она не была заранее обучена.

В качестве знакомого примера упоминаются чат-боты вроде ChatGPT, Claude или Gemini, которые сообщают, что ищут в интернете, чтобы ответить на вопрос. В этом случае LLM обращается к дополнительной информации, чтобы сделать ответ более актуальным и точным.

## Инструктор курса

Andrew Ng представляет инструктора курса: Zain Hasan. В транскрипции имя местами распознано как `Zan`, но на слайдах указано `Zain Hasan`.

Zain Hasan описан как AI и machine learning engineer, researcher и educator. За последнее десятилетие он работал в нескольких AI-компаниях, включая:

- Weaviate, ведущую компанию в области vector database, одного из ключевых компонентов RAG;
- Together AI, поставщика LLM services.

## Почему RAG важен

Zain Hasan подчеркивает, что RAG дает простой и практичный способ сфокусировать мощность large language models. Основная идея состоит в сочетании classical search systems с reasoning abilities of large language models.

Курс построен как баланс между:

- foundational concepts, лежащими в основе search и LLMs;
- practical tips по архитектуре high-performing RAG system.

Хотя сама концепция RAG не сложная, существует много способов ее реализовать. Design choices сильно влияют на accuracy и speed системы.

## Практические навыки, которые дает курс

В курсе предполагается изучить, как:

- подготавливать данные для использования в RAG system;
- prompt language model так, чтобы получить максимум пользы от этих данных;
- evaluate actual user traffic, чтобы обеспечивать high-quality responses;
- понимать, почему применяемые техники работают.

Andrew Ng отмечает, что RAG может быть самым распространенным типом LLM-based application в мире на момент разговора.

## Примеры областей применения

Крупные компании используют RAG, чтобы:

- помогать клиентам получать ответы на вопросы о продуктах;
- помогать сотрудникам находить ответы по internal policies и другим внутренним вопросам.

Startups строят RAG applications в разных verticals, включая:

- healthcare, например для ответов на medical questions;
- education, например для tutoring students по разным предметам.

## Как развитие LLM влияет на RAG

По мере улучшения LLM technology RAG systems также быстро включают новые возможности.

Отмечаются несколько изменений:

- recent generation of models стали лучше, чем модели one or two years ago, в том, чтобы оставаться grounded in the documents or contexts, которые им дают;
- за последний год или около того hallucination rates of RAG systems steadily trending downwards;
- reasoning models позволяют решать более complex questions и reason on top of the provided context;
- рост input context window меняет best practices для RAG.

Andrew Ng отдельно говорит, что при большем context window меняется hyperparameter tuning: что именно вставлять в RAG, как cutting documents into pieces, как управлять context. Теперь не всегда нужно сжимать много информации в очень маленькое context window.

## Документы, PDF, слайды и agentic workflows

По мере развития agentic document extraction и связанных технологий становится проще строить RAG systems поверх:

- PDF files;
- slides;
- other types of documents.

Это позволяет RAG systems ingest, reason over и answer questions по более широким наборам материалов.

Также RAG часто становится одним компонентом complex multi-step agentic workflow. В примере Andrew Ng говорит, что на step five or step seven внутреннего enterprise workflow RAG может дать agent информацию, нужную для обработки документа или reasoning about a customer request.

## Advanced techniques в курсе

Zain Hasan отмечает, что курс дает strong foundation для работы с cutting edge advances. В курс включены advanced techniques, включая:

- multimodal models;
- reasoning models;
- balancing approaches like RAG, fine tuning, and newer long context models;
- agentic RAG.

## Agentic RAG

Agentic RAG описывается как системы, которые используют multiple large language models, где каждая модель отвечает за отдельную часть большого workflow и имеет agency decide what data to retrieve.

Andrew Ng противопоставляет это более раннему поколению RAG systems:

- human engineer писал code и rules;
- инженер решал, как по query взять long document;
- инженер решал, как cut it into pieces;
- инженер решал, how we retrieve it;
- затем, например, seven pieces помещались в LLM context.

В таком варианте именно human engineer решал, what to give as context for the LLM.

В agentic RAG AI agent получает tools для retrieval и сам решает:

- хочет ли он сделать web search next;
- какие keywords использовать для web search;
- нужно ли query a specific specialized database;
- достаточно ли first round of information;
- нужен ли second round of retrieval.

Такие highly agentic systems могут сами выбирать, what information to retrieve для specific information need. Это делает системы более flexible and powerful и дает способ работать с messiness of the real world. Если подход оказывается неудачным, система может route back and fix the approach.

## Диапазон курса: от basic RAG до agentic RAG

Курс покрывает диапазон техник from basic RAG to advanced agentic RAG:

- core principles;
- mental frameworks for building these systems;
- practicalities of tuning hyperparameters;
- choosing appropriate chunk size for a very long document;
- managing context.

Для тех, кто только начинает building GenAI applications, курс дает overview не только RAG, но и компонентов, которые входят в RAG и могут быть полезны в других будущих системах.

## Итог разговора и переход к следующей лекции

Andrew Ng формулирует цель следующего видео: Zain должен дать high-level overview of the most important components of RAG. Это нужно, чтобы у слушателя была mental map для построения:

- standalone RAG system;
- RAG как компонента более complex agentic system.

Следующее видео должно перейти от общей мотивации к деталям RAG.
