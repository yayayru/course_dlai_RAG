# RAG — конспекты курса Coursera / DeepLearning.AI

Конспекты курса **Retrieval Augmented Generation (RAG)** от DeepLearning.AI на платформе [Coursera](https://www.coursera.org/learn/retrieval-augmented-generation-rag) или [DeepLearning.ai](https://www.deeplearning.ai/courses/retrieval-augmented-generation) : подробные заметки по каждой лекции (на основе транскрипций) и разбор кода из ungraded-лабораторных и graded-заданий.

## Источник

- 5 pdf-файлов слайдов взяты из обсуждения на форуме: https://community.deeplearning.ai/t/rag-lecture-notes/852809
- Форум курса: https://community.deeplearning.ai/t/rag-lecture-notes/852809
- Референсные задания и решения: https://github.com/singh-krishan/coursera_rag и https://github.com/muhammad-faizan-122/rag-course

## Структура репозитория

```
theory/     — конспекты лекций (*.notes.md) и разбор кода (*_code_*.md) по модулям
practice/   — исходные материалы курса: notebooks, вспомогательные .py-файлы, датасеты
docs/       — шаблоны промптов, которыми конспекты создавались (docs/prompt)
images/     — иллюстрации
```

Внутри каждой `theory/Module_N_*/` папки:

- `NN_lec_Name.trans.txt` — исходная транскрипция лекции (первичный источник);
- `NN_lec_Name.notes.md` — конспект по этой лекции;
- `NN_code_Name.md` / `NN_code_assig(n)ment_Name.md` — ссылка на соответствующий notebook из `practice/` плюс раздел `## Конспект по коду`;
- `RAG_MN.pdf` / `slides_MN.pdf` — слайды модуля (дополнительный источник для сверки терминов, схем и чисел).

Конспекты лекций строго следуют транскрипции (без пересказа своими словами и без добавления фактов из слайдов, которых нет в аудио); слайды используются только для сверки терминологии, схем, формул и чисел. Пустые транскрипции пропускались — конспект по ним не создавался. Полные формулировки промптов, по которым собирались конспекты каждого модуля, сохранены в [`docs/prompt/`](docs/prompt/).

## Содержание

### [Module 1 — RAG Overview](theory/Module_1_RAG_Overview) · [слайды 📑](theory/Module_1_RAG_Overview/slides_M1.pdf)

| # | Лекция / код |
|---|---|
| 01 | [Разговор с Andrew Ng](theory/Module_1_RAG_Overview/01_lec_A_conversation_with_andrew_ng.notes.md) |
| 02 | [Введение в Модуль 1](theory/Module_1_RAG_Overview/02_lec_Module_1_introduction.notes.md) |
| 03 | [Введение в RAG](theory/Module_1_RAG_Overview/03_lec_Introduction_to_RAG.notes.md) |
| 04 | [Применения RAG](theory/Module_1_RAG_Overview/04_lec_Applications_of_RAG_.notes.md) |
| 05 | [Обзор архитектуры RAG](theory/Module_1_RAG_Overview/05_lec_RAG_architecture_overview.notes.md) |
| 06 | [Введение в LLM](theory/Module_1_RAG_Overview/06_lec_Introduction_to_LLMs.notes.md) |
| 07 | [код: A brief Python refresher](theory/Module_1_RAG_Overview/07_code_A_brief_Python_refresher.md) |
| 08 | [код: LLM Calls and Crafting Simple Augmented Prompts](theory/Module_1_RAG_Overview/08_code_LLM_Calls_and_Crafting_Simple_Augmented_Prompts.md) |
| 09 | [Введение в information retrieval](<theory/Module_1_RAG_Overview/09_lec_Introduction to information retrieval.notes.md>) |
| 10 | [код (assignment): Introduction to RAG systems](theory/Module_1_RAG_Overview/10_code_assignment_Introduction_to_RAG_systems.md) |

### [Module 2 — Information Retrieval and Search Foundations](theory/Module_2_Information_Retrieval_and_Search_Foundations) · [слайды 📑](theory/Module_2_Information_Retrieval_and_Search_Foundations/RAG_M2.pdf)

| # | Лекция / код |
|---|---|
| 01 | [Введение в Модуль 2. Information Retrieval Foundations](theory/Module_2_Information_Retrieval_and_Search_Foundations/01_lec_Module_2_introduction.notes.md) |
| 02 | [Обзор архитектуры retriever](theory/Module_2_Information_Retrieval_and_Search_Foundations/02_lec_Retriever_architecture_overview.notes.md) |
| 03 | [Metadata filtering](theory/Module_2_Information_Retrieval_and_Search_Foundations/03_lec_Metadata_filtering.notes.md) |
| 04 | [Keyword search — TF-IDF](theory/Module_2_Information_Retrieval_and_Search_Foundations/04_lec_Keyword_search-TF-IDF.notes.md) |
| 05 | [Keyword search — BM25](theory/Module_2_Information_Retrieval_and_Search_Foundations/05_lec_Keyword_search-BM25.notes.md) |
| 06 | [Semantic search — введение](theory/Module_2_Information_Retrieval_and_Search_Foundations/06_lec_Semantic_search-introduction.notes.md) |
| 07 | [код: Vector embeddings in RAG](theory/Module_2_Information_Retrieval_and_Search_Foundations/07_code_Vector_embeddings_in_RAG.md) |
| 08 | [Hybrid search](theory/Module_2_Information_Retrieval_and_Search_Foundations/08_lec_Hybrid_search.notes.md) |
| 09 | [Оценка retrieval](theory/Module_2_Information_Retrieval_and_Search_Foundations/09_lec_Evaluating_retrieval.notes.md) |
| 10 | [код: Retrieval metrics](theory/Module_2_Information_Retrieval_and_Search_Foundations/10_code_Retrieval_metrics.md) |
| 11 | [код (assignment): Implementing retriever functions in a RAG system](theory/Module_2_Information_Retrieval_and_Search_Foundations/11_code_assignment_Implementing_retriever_functions_in_a_RAG_system.md) |

### [Module 3 — Information Retrieval with Vector Databases](theory/Module_3_Information_Retrieval_with_Vector_Databases) · [слайды 📑](theory/Module_3_Information_Retrieval_with_Vector_Databases/RAG_M3.pdf)

| # | Лекция / код |
|---|---|
| 01 | [Введение в Модуль 3](theory/Module_3_Information_Retrieval_with_Vector_Databases/01_lec_Module_3_introduction.notes.md) |
| 02 | [Approximate nearest neighbors algorithms (ANN)](<theory/Module_3_Information_Retrieval_with_Vector_Databases/02_lec_Approximate_nearest_neighbors_algorithms(ANN).notes.md>) |
| 03 | [Vector databases](theory/Module_3_Information_Retrieval_with_Vector_Databases/03_lec_Vector_databases.notes.md) |
| 04 | [код: Introduction to the Weaviate API](theory/Module_3_Information_Retrieval_with_Vector_Databases/04_code_Introduction_to_the_Weaviate_API.md) |
| 05 | [Chunking](theory/Module_3_Information_Retrieval_with_Vector_Databases/05_lec_Chunking.notes.md) |
| 06 | [код: Chunking](theory/Module_3_Information_Retrieval_with_Vector_Databases/06_code_Chunking.md) |
| 07 | [Продвинутые техники chunking](theory/Module_3_Information_Retrieval_with_Vector_Databases/07_lec_Advanced_chunking_techniques.notes.md) |
| 08 | [Query parsing](theory/Module_3_Information_Retrieval_with_Vector_Databases/08_lec_Query_parsing.notes.md) |
| 09 | [Cross-encoders и ColBERT](theory/Module_3_Information_Retrieval_with_Vector_Databases/09_lec_Cross-encoders_and_ColBERT.notes.md) |
| 10 | [Reranking](theory/Module_3_Information_Retrieval_with_Vector_Databases/10_lec_Reranking.notes.md) |
| 11 | [код (assignment): Building RAG Systems with a Vector Database](theory/Module_3_Information_Retrieval_with_Vector_Databases/11_code_assignment_Building_RAG_Systems_with_a_Vector_Database.md) |

### [Module 4 — LLMs and Text Generation](theory/Module_4_LLMs_and_Text_Generation) · [слайды 📑](theory/Module_4_LLMs_and_Text_Generation/RAG_M4.pdf)

| # | Лекция / код |
|---|---|
| 01 | [Module 4 introduction](theory/Module_4_LLMs_and_Text_Generation/01_lec_Module_4_introduction.notes.md) |
| 02 | [Transformer architecture](theory/Module_4_LLMs_and_Text_Generation/02_lec_Transformer_architecture.notes.md) |
| 03 | [LLM sampling strategies](theory/Module_4_LLMs_and_Text_Generation/03_lec_LLM_sampling_strategies.notes.md) |
| 04 | [код: Exploring LLM capabilities](theory/Module_4_LLMs_and_Text_Generation/04_code_Exploring_LLM_capabilities.md) |
| 05 | [Choosing your LLM](theory/Module_4_LLMs_and_Text_Generation/05_lec_Choosing_your_LLM.notes.md) |
| 06 | [Prompt engineering: building your augmented prompt](theory/Module_4_LLMs_and_Text_Generation/06_lec_Prompt_engineering_building_your_augmented_prompt.notes.md) |
| 07 | [Prompt engineering: advanced techniques](theory/Module_4_LLMs_and_Text_Generation/07_lec_Prompt_engineering_advanced_techniques.notes.md) |
| 08 | [код: Prompt engineering](theory/Module_4_LLMs_and_Text_Generation/08_code_Prompt_engineering.md) |
| 09 | [Handling hallucinations](theory/Module_4_LLMs_and_Text_Generation/09_lec_Handling_hallucinations.notes.md) |
| 10 | [Evaluating your LLM's performance](theory/Module_4_LLMs_and_Text_Generation/10_lec_Evaluating_your_LLMs_performance.notes.md) |
| 11 | [Agentic RAG](theory/Module_4_LLMs_and_Text_Generation/11_lec_Agentic_RAG.notes.md) |
| 12 | [RAG vs. Fine-Tuning](theory/Module_4_LLMs_and_Text_Generation/12_lec_RAG_vs_Fine-Tuning.notes.md) |
| 13 | [код (assignment): Developing a RAG-based Chatbot](theory/Module_4_LLMs_and_Text_Generation/13_code_assigment_Developing_a_RAG-based_Chatbot.md) |

### [Module 5 — RAG Systems in Production](theory/Module_5_RAG_Systems_in_Production) · [слайды 📑](theory/Module_5_RAG_Systems_in_Production/RAG_M5.pdf)

| # | Лекция / код |
|---|---|
| 01 | [Module 5 introduction](theory/Module_5_RAG_Systems_in_Production/01_lec_Module_5_introduction.notes.md) |
| 02 | [What makes production challenging](theory/Module_5_RAG_Systems_in_Production/02_lec_What_makes_production_challenging.notes.md) |
| 03 | [Implementing RAG evaluation strategies](theory/Module_5_RAG_Systems_in_Production/03_lec_Implementing_RAG_evaluation_strategies.notes.md) |
| 04 | [Logging, monitoring, and observability](<theory/Module_5_RAG_Systems_in_Production/04_lec_Logging, monitoring, and observability.notes.md>) |
| 05 | [код: Tracing a RAG system](theory/Module_5_RAG_Systems_in_Production/05_code_Tracing_a_RAG_system.md) |
| 06 | [Customized evaluation](<theory/Module_5_RAG_Systems_in_Production/06_lec_Customized evaluation.notes.md>) |
| 07 | [Quantization](theory/Module_5_RAG_Systems_in_Production/07_lec_Quantization.notes.md) |
| 08 | [Cost vs. Response Quality](theory/Module_5_RAG_Systems_in_Production/08_lec_Cost_vs_Response_Quality.notes.md) |
| 09 | [Latency vs. Response Quality](theory/Module_5_RAG_Systems_in_Production/09_lec_Latency_vs_Response_Quality.notes.md) |
| 10 | [Security](theory/Module_5_RAG_Systems_in_Production/10_lec_Security.notes.md) |
| 11 | [Multimodal RAG](theory/Module_5_RAG_Systems_in_Production/11_lec_Multimodal_RAG.notes.md) |
| 12 | [код (assignment): Improving the ChatBot](theory/Module_5_RAG_Systems_in_Production/12_code_assigment_Improving_the_ChatBot.md) |

## Сквозные темы курса

- **Retrieval**: keyword search (TF-IDF, BM25), semantic search, hybrid search, metadata filtering, метрики оценки retrieval.
- **Vector databases**: ANN (HNSW), Weaviate API, chunking-стратегии, query parsing, cross-encoders/ColBERT, reranking.
- **LLM**: архитектура transformer, стратегии сэмплирования, выбор модели, prompt engineering, борьба с галлюцинациями, оценка качества LLM, agentic RAG, RAG vs fine-tuning.
- **Production**: наблюдаемость и логирование (Phoenix/OpenTelemetry), кастомные датасеты для оценки, квантизация, компромиссы cost/latency/quality, безопасность knowledge base, multimodal RAG.
