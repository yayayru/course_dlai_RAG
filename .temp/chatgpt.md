Ваш метод правильный: **одна корневая папка курса, один `AGENTS.md`, отдельные разделы `theory/` и `practice/`, внутри которых одинаково пронумерованы модули**.

Я бы внёс одно важное изменение: не помещать полный учебный план в `AGENTS.md`. Корневой `AGENTS.md` должен содержать правила работы и карту проекта, а названия всех модулей и лекций лучше хранить в `theory/COURSE_MAP.md`. OpenAI рекомендует сохранять `AGENTS.md` небольшим и использовать его как навигационную карту к более подробной документации. Корневой `AGENTS.md` будет действовать на весь проект, пока вы запускаете Codex внутри этого репозитория. ([OpenAI Developers][1])

Обязательно используйте точное имя **`AGENTS.md`**, заглавными буквами.

## Рекомендуемая структура

```text
rag/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .gitignore
│
├── theory/
│   ├── COURSE_MAP.md
│   │
│   ├── module_01_rag_overview/
│   │   ├── module_notes.md
│   │   │
│   │   ├── lec_01_conversation_with_andrew_ng/
│   │   │   ├── slides.pdf
│   │   │   ├── transcript.md
│   │   │   └── notes.md
│   │   │
│   │   ├── lec_02_module_introduction/
│   │   │   ├── slides.pdf
│   │   │   ├── transcript.md
│   │   │   └── notes.md
│   │   │
│   │   ├── lec_03_introduction_to_rag/
│   │   │   ├── slides.pdf
│   │   │   ├── transcript.md
│   │   │   └── notes.md
│   │   │
│   │   └── lec_04_applications_of_rag/
│   │       ├── slides.pdf
│   │       ├── transcript.md
│   │       └── notes.md
│   │
│   ├── module_02_information_retrieval_and_search_foundations/
│   │   ├── module_notes.md
│   │   ├── lec_01_module_introduction/
│   │   │   ├── slides.pdf
│   │   │   ├── transcript.md
│   │   │   └── notes.md
│   │   └── lec_02_retriever_architecture_overview/
│   │       ├── slides.pdf
│   │       ├── transcript.md
│   │       └── notes.md
│   │
│   ├── module_03_information_retrieval_with_vector_databases/
│   ├── module_04_llms_and_text_generation/
│   └── module_05_rag_systems_in_production/
│
├── practice/
│   ├── module_01_rag_overview/
│   │   ├── notebooks/
│   │   │   ├── lec_03_introduction_to_rag.ipynb
│   │   │   └── lec_04_applications_of_rag.ipynb
│   │   ├── src/
│   │   │   ├── retrieval.py
│   │   │   ├── generation.py
│   │   │   └── utils.py
│   │   ├── exercises/
│   │   ├── data/
│   │   └── outputs/
│   │
│   ├── module_02_information_retrieval_and_search_foundations/
│   ├── module_03_information_retrieval_with_vector_databases/
│   ├── module_04_llms_and_text_generation/
│   └── module_05_rag_systems_in_production/
│
└── tests/
    └── ...
```

### Почему `notes.md`, а не `trans_notes.md`

Внутри папки конкретной лекции контекст уже понятен:

```text
lec_03_introduction_to_rag/
├── transcript.md
└── notes.md
```

Поэтому префикс `trans_` избыточен. При этом:

* `transcript.md` — полная исходная транскрипция;
* `notes.md` — конспект транскрипции;
* `module_notes.md` — общий конспект всего модуля.

## Корневой `AGENTS.md`

# RAG Course Repository Instructions

## Project purpose

This repository contains theory materials and practical implementations for the course **RAG**.

The repository is divided into:

* `theory/` — lecture slides, transcripts, lecture notes, and module notes.
* `practice/` — Python scripts, Jupyter notebooks, exercises, data, and generated outputs.
* `tests/` — automated tests for reusable Python code.

Read `theory/COURSE_MAP.md` to identify the course modules, lectures, titles, and corresponding directories.

## Repository structure

Each module directory must use this naming convention:

```text
module_NN_short_descriptive_name
```

Each lecture directory must use this naming convention:

```text
lec_NN_short_descriptive_name
```

Use lowercase ASCII characters and underscores in directory and file names.

Examples:

```text
module_01_rag_overview
lec_01_conversation_with_andrew_ng
lec_03_introduction_to_rag
```

Do not rename module or lecture directories unless explicitly requested.

## Theory files

A lecture directory may contain:

* `slides.pdf` — original lecture slides.
* `transcript.md` — complete source transcript.
* `notes.md` — structured notes generated from the transcript and slides.

A module directory may contain:

* `module_notes.md` — consolidated notes covering all lectures in the module.

Treat `slides.pdf` and `transcript.md` as source files.

Do not modify, shorten, overwrite, or delete source files unless explicitly requested.

## Creating lecture notes

When creating or updating `notes.md`:

1. Use `transcript.md` as the primary source.
2. Use `slides.pdf` to verify terminology, headings, formulas, names, dates, numbers, and technical concepts.
3. Preserve all substantial information from the transcript.
4. Do not invent facts, interpretations, examples, or conclusions.
5. Remove only verbal fillers, accidental repetitions, and fragments without informational value.
6. Correct transcription errors only when the correction is supported by the slides or unambiguous context.
7. Mark uncertain content as `[unclear]`.
8. Organize the result with descriptive Markdown headings and lists.
9. Preserve formulas, code snippets, definitions, examples, warnings, and conclusions.
10. Write the finished result only to `notes.md`.

## Creating module notes

When creating or updating `module_notes.md`:

1. Read the `notes.md` files from all completed lectures in the module.
2. Preserve the logical order defined in `theory/COURSE_MAP.md`.
3. Combine overlapping explanations without deleting unique information.
4. Clearly separate concepts, definitions, architectures, examples, and practical recommendations.
5. Do not introduce information that is absent from the lecture materials.
6. Add references to the corresponding lecture directories when useful.

## Practice files

Use Jupyter notebooks for:

* guided demonstrations;
* experiments;
* visualizations;
* step-by-step explanations;
* temporary exploration.

Use Python modules for:

* reusable functions;
* classes;
* data-loading logic;
* retrieval components;
* generation components;
* evaluation utilities;
* production-oriented implementations.

Reusable logic must be moved from notebooks into the relevant `src/` Python modules.

Notebooks should import reusable functions from `src/` rather than duplicate their implementations.

## Practice directory roles

Within each practice module:

* `notebooks/` — lecture demonstrations and experiments in `.ipynb` format.
* `src/` — reusable Python code in `.py` format.
* `exercises/` — tasks and learner solutions.
* `data/` — local input data used by examples.
* `outputs/` — generated indexes, reports, images, and experiment results.

Do not place generated files beside source code when they belong in `outputs/`.

## Code requirements

When modifying Python code:

1. Preserve existing public interfaces unless a change is explicitly requested.
2. Prefer small, reusable functions with clear names.
3. Add type hints to reusable Python functions.
4. Add docstrings where behavior is not self-evident.
5. Avoid duplicating code between notebooks and Python modules.
6. Do not hard-code API keys, tokens, passwords, or machine-specific absolute paths.
7. Read secrets from environment variables.
8. Update `.env.example` when introducing a new required environment variable.
9. Add or update tests when reusable behavior changes.
10. Run the relevant tests or validation commands before finishing.

## Notebook requirements

When modifying a notebook:

1. Keep cells in an executable top-to-bottom order.
2. Remove obsolete debugging cells and accidental duplicate outputs.
3. Do not embed credentials.
4. Use relative project paths.
5. Keep explanatory Markdown cells close to the code they describe.
6. Avoid placing essential reusable logic only inside a notebook.
7. Do not overwrite original data files.

## Source integrity

Never claim that a statement came from a lecture unless it is supported by its transcript or slides.

When sources conflict:

1. Preserve both versions.
2. Identify the conflict explicitly.
3. Do not silently choose one version unless the correct version is unambiguous.

When a required source file is missing, report the missing file instead of reconstructing its contents from assumptions.

## Scope control

Modify only the files required for the current task.

Do not reorganize unrelated modules.

Do not rename files or directories merely for stylistic consistency unless explicitly requested.

At the end of a task, summarize:

* files created;
* files modified;
* validations performed;
* unresolved uncertainties.

## `theory/COURSE_MAP.md`

# RAG Course Map

## Course

**RAG**

## Module 1: RAG Overview

Directory:

```text
theory/module_01_rag_overview/
```

Lectures:

1. **A Conversation with Andrew Ng**

   * Directory: `lec_01_conversation_with_andrew_ng/`
2. **Module 1 Introduction**

   * Directory: `lec_02_module_introduction/`
3. **Introduction to RAG**

   * Directory: `lec_03_introduction_to_rag/`
4. **Applications of RAG**

   * Directory: `lec_04_applications_of_rag/`

## Module 2: Information Retrieval and Search Foundations

Directory:

```text
theory/module_02_information_retrieval_and_search_foundations/
```

Lectures:

1. **Module 2 Introduction**

   * Directory: `lec_01_module_introduction/`
2. **Retriever Architecture Overview**

   * Directory: `lec_02_retriever_architecture_overview/`

Add the remaining Module 2 lectures here in their original course order.

## Module 3: Information Retrieval with Vector Databases

Directory:

```text
theory/module_03_information_retrieval_with_vector_databases/
```

Add the Module 3 lectures here in their original course order.

## Module 4: LLMs and Text Generation

Directory:

```text
theory/module_04_llms_and_text_generation/
```

Add the Module 4 lectures here in their original course order.

## Module 5: RAG Systems in Production

Directory:

```text
theory/module_05_rag_systems_in_production/
```

Add the Module 5 lectures here in their original course order.

Итоговая логика получается чистой:

```text
AGENTS.md          → как Codex должен работать
COURSE_MAP.md      → какие модули и лекции существуют
theory/            → исходные материалы и конспекты
practice/          → notebooks, Python-код и упражнения
```

Это лучше, чем помещать весь учебный контент в один большой `AGENTS.md`: агент получает короткие постоянные правила, а подробную структуру курса читает только тогда, когда она нужна.

[1]: https://developers.openai.com/codex/agent-configuration/agents-md "
  Custom instructions with AGENTS.md | ChatGPT Learn
"


№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

На русском:

№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

Ваш метод **правильный**: один курс `RAG`, одна корневая инструкция `AGENTS.md`, отдельно теория и практика, а внутри — одинаковые папки пяти модулей.

Я бы внёс три уточнения:

1. Использовать точное имя **`AGENTS.md`** с заглавными буквами. Codex автоматически ищет именно это имя, если другие варианты отдельно не настроены. ([OpenAI Developers][1])
2. Для всех модулей использовать одинаковые английские имена папок.
3. Для лекций указывать номер и короткое название в имени файла, поскольку в одном модуле будет несколько транскрипций и конспектов.

Один корневой `AGENTS.md` подходит для такого проекта: Codex читает инструкции от корня проекта до текущей рабочей папки. Дополнительные `AGENTS.md` внутри модулей нужны только тогда, когда у отдельных папок появятся особые правила. ([OpenAI Developers][1])

## Рекомендуемая структура

```text
RAG/
├── AGENTS.md
├── README.md
│
├── theory/
│   ├── module_01_rag_overview/
│   │   ├── slides.pdf
│   │   ├── lec_01_a_conversation_with_andrew_ng_transcript.md
│   │   ├── lec_01_a_conversation_with_andrew_ng_notes.md
│   │   ├── lec_02_module_1_introduction_transcript.md
│   │   ├── lec_02_module_1_introduction_notes.md
│   │   ├── lec_03_introduction_to_rag_transcript.md
│   │   ├── lec_03_introduction_to_rag_notes.md
│   │   ├── lec_04_applications_of_rag_transcript.md
│   │   └── lec_04_applications_of_rag_notes.md
│   │
│   ├── module_02_information_retrieval_and_search_foundations/
│   │   ├── slides.pdf
│   │   ├── lec_01_module_2_introduction_transcript.md
│   │   ├── lec_01_module_2_introduction_notes.md
│   │   ├── lec_02_retriever_architecture_overview_transcript.md
│   │   └── lec_02_retriever_architecture_overview_notes.md
│   │
│   ├── module_03_information_retrieval_with_vector_databases/
│   │   ├── slides.pdf
│   │   └── ...
│   │
│   ├── module_04_llms_and_text_generation/
│   │   ├── slides.pdf
│   │   └── ...
│   │
│   └── module_05_rag_systems_in_production/
│       ├── slides.pdf
│       └── ...
│
└── practice/
    ├── module_01_rag_overview/
    │   ├── notebooks/
    │   │   └── rag_overview.ipynb
    │   ├── src/
    │   │   └── rag_overview.py
    │   └── README.md
    │
    ├── module_02_information_retrieval_and_search_foundations/
    │   ├── notebooks/
    │   │   └── retriever_basics.ipynb
    │   ├── src/
    │   │   └── retriever.py
    │   └── README.md
    │
    ├── module_03_information_retrieval_with_vector_databases/
    │   ├── notebooks/
    │   ├── src/
    │   └── README.md
    │
    ├── module_04_llms_and_text_generation/
    │   ├── notebooks/
    │   ├── src/
    │   └── README.md
    │
    └── module_05_rag_systems_in_production/
        ├── notebooks/
        ├── src/
        └── README.md
```

## Почему лучше не использовать `trans_notes.md`

Название `trans_notes.md` подходит, когда транскрипция в папке только одна. При нескольких лекциях появится конфликт: будет непонятно, к какой лекции относится файл.

Лучше использовать парные названия:

```text
lec_03_introduction_to_rag_transcript.md
lec_03_introduction_to_rag_notes.md
```

Так Codex сразу видит:

* номер лекции;
* тему лекции;
* исходный файл;
* результирующий конспект.

## Язык файлов

Оптимальная схема:

* `AGENTS.md` — на русском;
* названия папок и файлов — на английском;
* Python-функции, переменные и классы — на английском;
* конспекты — на русском;
* исходные названия курса, модулей и лекций — сохранять на английском;
* специальные термины вроде `retriever`, `embedding`, `reranker`, `chunking` можно не переводить либо давать русский перевод при первом упоминании.

## Готовый корневой `AGENTS.md`

Файл лучше держать кратким и практическим: официальный подход рекомендует использовать его как карту проекта и набор рабочих правил, а не как огромную энциклопедию. ([OpenAI Developers][2])

# RAG Course Project Instructions

## Назначение проекта

Этот репозиторий содержит теоретические материалы, конспекты и практический код курса **RAG**.

Основные разделы:

* `theory/` — презентации, транскрипции и конспекты лекций.
* `practice/` — практические примеры в форматах Python и Jupyter Notebook.

## Структура курса

Курс состоит из пяти модулей:

1. `module_01_rag_overview` — RAG Overview
2. `module_02_information_retrieval_and_search_foundations` — Information Retrieval and Search Foundations
3. `module_03_information_retrieval_with_vector_databases` — Information Retrieval with Vector Databases
4. `module_04_llms_and_text_generation` — LLMs and Text Generation
5. `module_05_rag_systems_in_production` — RAG Systems in Production

Папки модулей в `theory/` и `practice/` должны иметь одинаковые названия.

## Язык

* Инструкции и конспекты пиши на русском языке.
* Названия курса, модулей и лекций сохраняй на английском языке.
* Названия файлов, папок, функций, классов и переменных пиши на английском языке.
* Общепринятые технические термины можно сохранять на английском.
* При первом использовании сложного термина при необходимости добавляй краткое объяснение на русском.

## Теоретические материалы

Каждая папка `theory/module_*` содержит:

* одну презентацию `slides.pdf`;
* транскрипции лекций `lec_NN_<lecture_name>_transcript.md`;
* конспекты лекций `lec_NN_<lecture_name>_notes.md`.

Пример:

```text
lec_03_introduction_to_rag_transcript.md
lec_03_introduction_to_rag_notes.md
```

Файл с суффиксом `_transcript.md` является исходным материалом.

Файл с суффиксом `_notes.md` является структурированным конспектом соответствующей транскрипции.

Не записывай конспект в файл транскрипции и не изменяй исходную транскрипцию без прямого указания пользователя.

## Создание конспектов

При создании или обновлении файла `_notes.md`:

1. Используй соответствующий файл `_transcript.md` как основной источник.
2. Используй `slides.pdf` того же модуля как дополнительный источник для проверки структуры, терминов, формул, имён, дат и чисел.
3. Не добавляй факты, которых нет в транскрипции или презентации.
4. Не придумывай объяснения, примеры, выводы или связи от себя.
5. Не теряй существенную информацию.
6. Сохраняй определения, аргументы, этапы процессов, ограничения, примеры, имена, даты, числа и выводы.
7. Удаляй только слова-паразиты, технические реплики, бессодержательные фрагменты и явные повторы.
8. Исправляй ошибки распознавания речи только тогда, когда исправление подтверждается контекстом или презентацией.
9. Неуверенные или неразборчивые места помечай как `[неясно]`.
10. Не объединяй информацию из разных лекций без прямого указания.
11. Оформляй результат в Markdown.
12. Используй содержательные заголовки и подзаголовки.
13. Не сокращай текст до краткого `summary`, если пользователь просит полный конспект.

## Формат конспекта

Рекомендуемая структура файла `_notes.md`:

```markdown
# Lecture title

## Основная тема

## Ключевые понятия

## Подробный конспект

### Подтема 1

### Подтема 2

## Примеры

## Ограничения и важные замечания

## Итоги лекции
```

Добавляй только те разделы, для которых есть информация в исходных материалах.

Не создавай пустые разделы.

## Презентации

В каждой папке теоретического модуля должна находиться одна презентация:

```text
slides.pdf
```

Презентация относится ко всему модулю, а не к одной конкретной лекции.

При работе с отдельной лекцией используй только те слайды, которые относятся к её теме.

Не извлекай из презентации утверждения, не связанные с текущей лекцией, если пользователь отдельно не просит объединить материалы модуля.

## Практические материалы

Папка `practice/` содержит практический код по соответствующим модулям.

В каждой папке практического модуля могут находиться:

* `notebooks/` — исследовательские и учебные Jupyter Notebook;
* `src/` — повторно используемый Python-код;
* `README.md` — описание практического задания и порядок запуска.

Используй `.ipynb` для:

* пошаговых демонстраций;
* экспериментов;
* визуализаций;
* учебных пояснений;
* исследования данных и моделей.

Используй `.py` для:

* повторно используемых функций;
* классов;
* загрузчиков данных;
* компонентов retriever и generator;
* конфигурации пайплайнов;
* тестируемой бизнес-логики.

Не дублируй большие фрагменты логики одновременно в `.ipynb` и `.py`.

Выноси повторно используемую реализацию в `src/*.py`, а в notebook импортируй её.

## Требования к Python-коду

* Используй понятные английские имена.
* Добавляй type hints к новым функциям.
* Добавляй docstring к публичным функциям и классам.
* Не добавляй зависимости без необходимости.
* Не помещай секретные ключи и токены в код.
* Используй переменные окружения для секретных данных.
* Не изменяй рабочий код, не относящийся к текущей задаче.
* После изменений проверяй импорты и запускай доступные тесты или соответствующие ячейки notebook.
* Не утверждай, что код работает, если он не был запущен или проверен.

## Работа с Jupyter Notebook

* Располагай ячейки в логическом порядке выполнения.
* Notebook должен запускаться сверху вниз.
* Перед использованием переменная должна быть создана или импортирована.
* Удаляй ненужные отладочные ячейки.
* Не сохраняй секретные ключи в выводе ячеек.
* Сохраняй важные Markdown-пояснения рядом с соответствующим кодом.
* Не заменяй рабочий `.py`-модуль копией его полного содержимого в notebook.

## Изменение файлов

Перед выполнением задачи:

1. Определи, относится ли задача к `theory/`, `practice/` или обоим разделам.
2. Найди соответствующий модуль.
3. Прочитай связанные исходные материалы.
4. Изменяй только файлы, необходимые для задачи.
5. Сохраняй существующую структуру и схему именования.

После выполнения задачи сообщи:

* какие файлы были созданы или изменены;
* какие источники использовались;
* какие проверки были выполнены;
* какие места остались неясными или непроверенными.

Такая структура остаётся простой, но уже чётко разделяет **источники**, **конспекты**, **ноутбуки** и **переиспользуемый Python-код**.

[1]: https://developers.openai.com/codex/agent-configuration/agents-md "
  Custom instructions with AGENTS.md | ChatGPT Learn
"
[2]: https://developers.openai.com/codex/learn/best-practices "
  Best practices | ChatGPT Learn
"

№№№№№№№№№№№№№№№№№№

Отлично, спасибо. Но есть замечание папке Практика, лучше в одной папке каждой модули разные файлы без папки, как думаешь7

№№№№№№№№№№№№№№№№№№

Да, для вашего проекта **плоская структура практики будет лучше**, если в каждом модуле немного файлов. Папки `src/` и `notebooks/` здесь могут только усложнять навигацию.

Рекомендую так:

```text
RAG/
├── AGENTS.md
├── README.md
│
├── theory/
│   ├── module_01_rag_overview/
│   ├── module_02_information_retrieval_and_search_foundations/
│   ├── module_03_information_retrieval_with_vector_databases/
│   ├── module_04_llms_and_text_generation/
│   └── module_05_rag_systems_in_production/
│
└── practice/
    ├── module_01_rag_overview/
    │   ├── README.md
    │   ├── lec_03_introduction_to_rag.ipynb
    │   ├── rag_pipeline.py
    │   └── utils.py
    │
    ├── module_02_information_retrieval_and_search_foundations/
    │   ├── README.md
    │   ├── retriever_architecture.ipynb
    │   ├── keyword_search.py
    │   └── retriever.py
    │
    ├── module_03_information_retrieval_with_vector_databases/
    │   ├── README.md
    │   ├── vector_search.ipynb
    │   ├── embeddings.py
    │   └── vector_store.py
    │
    ├── module_04_llms_and_text_generation/
    │   ├── README.md
    │   ├── text_generation.ipynb
    │   ├── generator.py
    │   └── prompts.py
    │
    └── module_05_rag_systems_in_production/
        ├── README.md
        ├── production_rag.ipynb
        ├── rag_service.py
        └── evaluation.py
```

## Когда плоская структура удобнее

Она хорошо подходит, если в модуле примерно:

* 1–5 ноутбуков;
* несколько `.py`-файлов;
* один `README.md`;
* нет отдельного Python-пакета;
* нет большого количества тестов и конфигураций.

Codex также будет проще видеть все практические файлы модуля в одном месте.

## Главное правило именования

Поскольку `.py` и `.ipynb` лежат рядом, имена должны ясно показывать назначение:

```text
basic_rag.ipynb
vector_search.ipynb
rag_evaluation.ipynb

retriever.py
generator.py
embeddings.py
evaluation.py
utils.py
```

Не стоит делать слишком общие имена:

```text
code.py
main2.py
test.ipynb
notebook.ipynb
practice.py
```

## Нужно ли добавлять номер лекции

Для ноутбука, напрямую связанного с конкретной лекцией, можно использовать:

```text
lec_03_introduction_to_rag.ipynb
```

Для практики по всему модулю лучше использовать тему задания:

```text
basic_rag_pipeline.ipynb
retriever_comparison.ipynb
vector_database_search.ipynb
```

То есть номер лекции не обязателен для каждого практического файла.

## Что изменить в `AGENTS.md`

Раздел практики лучше сформулировать так:

````markdown
## Практические материалы

Каждая папка `practice/module_*` содержит практические материалы соответствующего модуля.

Все файлы модуля располагаются непосредственно в папке модуля без дополнительных папок `src/` и `notebooks/`.

В папке могут находиться:

- `.ipynb` — пошаговые демонстрации, эксперименты и учебные задания;
- `.py` — повторно используемые функции, классы и компоненты;
- `README.md` — описание практических материалов и инструкции по запуску;
- конфигурационные файлы, если они необходимы для конкретного модуля.

Используй содержательные английские имена файлов.

Примеры:

```text
basic_rag_pipeline.ipynb
retriever_comparison.ipynb
retriever.py
embeddings.py
evaluation.py
utils.py
````

Не создавай дополнительные папки внутри практического модуля, если количество файлов остаётся небольшим.

Не дублируй большие фрагменты логики в `.ipynb` и `.py`.

Если код используется в нескольких ячейках или ноутбуках, вынеси его в отдельный `.py`-файл и импортируй в notebook.

```

Итог: **для текущего курса плоская структура внутри каждого практического модуля предпочтительнее**. Разделение на `src/` и `notebooks/` стоит вводить только позже, если один модуль разрастётся примерно до 10–15 файлов или превратится в самостоятельный Python-пакет.
```
