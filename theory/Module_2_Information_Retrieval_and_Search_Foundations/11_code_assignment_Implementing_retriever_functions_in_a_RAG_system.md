См. practice\Module2\Graded_Assignments\C1M2_Assignment.ipynb

## Конспект по коду

### Назначение assignment notebook

`C1M2_Assignment.ipynb` («Assignment 2: Implementing Retriever Functions in a RAG System») — второе графируемое задание курса. В нём слушатель дополняет RAG-систему, реализуя различные функции retrieval.

> Важно: изучен именно шаблон задания (`C1M2_Assignment.ipynb`), а не файл с готовым решением — в этой папке `Graded_Assignments` файла `..._Solution.ipynb` нет (в отличие от Module 1). Три `GRADED CELL`-ячейки (`bm25_retrieve`, `semantic_search_retrieve`, `reciprocal_rank_fusion`) в этом notebook оставлены как заготовки с плейсхолдерами `None` вместо реального кода, поэтому у соответствующих вызывающих ячеек нет фактического visible output — вместо него в markdown приведены ожидаемые (Expected output) значения, которые код должен вернуть после того, как слушатель допишет решение.

Согласно вводной ячейке, в задании нужно:

- использовать библиотеку для реализации BM25-поиска;
- реализовать semantic search с использованием vector embeddings;
- реализовать алгоритм Reciprocal Rank Fusion (RRF) для объединения BM25 и semantic search;
- проанализировать, как разные методы retrieval влияют на ответы, генерируемые LLM.

Оглавление notebook:

1. Importing the libraries.
2. Loading the Dataset.
3. Retrieve Functions — Query news by index, BM25 Retrieve (Exercise 1), Semantic Search, Embeddings (Exercise 2), RRF Retrieve (Exercise 3).
4. Completing the RAG System — Creating the final prompt, Experimenting with the RAG system, Ask yourself.

### Локальные источники кода

Помимо самого notebook изучены файлы из той же папки `practice\Module2\Graded_Assignments`:

- `utils.py`;
- `unittests.py`;
- данные: `news_data_dedup.csv`, `embeddings.joblib`.

### Импорты notebook

```python
import joblib
import numpy as np
import bm25s
import os
from sentence_transformers import SentenceTransformer

from utils import (
    read_dataframe,
    pprint,
    generate_with_single_input,
    cosine_similarity,
    display_widget
)
import unittests
```

Новым по сравнению с предыдущими notebook курса является импорт библиотеки [`bm25s`](https://bm25s.github.io/) для реализации BM25-поиска.

### Раздел 2: загрузка датасета

```python
NEWS_DATA = read_dataframe("news_data_dedup.csv")
```

В markdown отмечено, что используется тот же Kaggle-датасет [BBC News dataset](https://www.kaggle.com/datasets/gpreda/bbc-news), что и в Module 1, но теперь фокус — на части retrieval: реализация и эксперименты с тремя разными алгоритмами извлечения.

`pprint(NEWS_DATA[5])` — visible output: запись про туристический сбор в Венеции (`guid`, `title`, `description`, `venue: 'BBC'`, `url`, `published_at: '2024-04-25'`, `updated_at: '2024-04-26'`).

### Раздел 3: функции retrieval

Вводный markdown поясняет, что в этом задании даны все функции RAG-системы, кроме собственно retrieval-части, и приводится сравнение двух подходов:

- **Semantic Search** — использует продвинутые техники для понимания смысла запроса, вместо простого сопоставления ключевых слов смотрит на контекст и связи между словами.
- **BM25 Retrieve** — традиционный, но эффективный алгоритм, оценивающий документы по тому, насколько хорошо они соответствуют запросу, учитывая частоту термина, его уникальность и длину документа.

Иллюстрация `images/retriever_overview.png` показывает, какая часть общей RAG-архитектуры разбирается в задании.

#### 3.1 `query_news(indices)`

Дана готовой — идентична одноимённой функции из Module 1: возвращает список записей `NEWS_DATA` по списку индексов.

#### 3.2 BM25 Retrieve

**Пример использования библиотеки `bm25s`** (демонстрационная, не graded-ячейка):

```python
corpus = [x['title'] + " " + x['description'] for x in NEWS_DATA]
BM25_RETRIEVER = bm25s.BM25(corpus=corpus)
tokenized_data = bm25s.tokenize(corpus)
BM25_RETRIEVER.index(tokenized_data)

sample_query = "What are the recent news about GDP?"
tokenized_sample_query = bm25s.tokenize(sample_query)
results, scores = BM25_RETRIEVER.retrieve(tokenized_sample_query, k=3)
```

Корпус для BM25 составляется из конкатенации `title` и `description` каждой новости. Visible output этой демонстрационной ячейки (с прогресс-барами `Split strings`, `BM25S Count Tokens`, `BM25S Compute Scores`, `BM25S Retrieve` от библиотеки `bm25s`) показывает три документа по запросу про GDP, включая документ с индексом 752 (*«GDP and the Dow Are Up. But What About American Well-Being?»*), 673 (*«What the GDP Report Says About Inflation...»*) и 289 (*«A GDP Warning as Signs of Stagflation Appear»*).

Далее в отдельной (не graded) ячейке заново создаются глобальные объекты для использования в решении:

```python
corpus = [x['title'] + " " + x['description'] for x in NEWS_DATA]
BM25_RETRIEVER = bm25s.BM25(corpus=corpus)
TOKENIZED_DATA = bm25s.tokenize(corpus)
BM25_RETRIEVER.index(TOKENIZED_DATA)
```

**Exercise 1 — `bm25_retrieve(query, top_k=5)`** (GRADED CELL, оставлена как шаблон):

```python
def bm25_retrieve(query: str, top_k: int = 5):
    ### START CODE HERE ###
    tokenized_query = None
    BM25_RETRIEVER.index(None)
    results, scores = None
    results = None
    top_k_indices = None
    ### END CODE HERE ###
    return top_k_indices
```

По докстрингу и структуре ячейки, ожидаемое решение должно: токенизировать `query` через `bm25s.tokenize`, вызвать `.retrieve(...)` у `BM25_RETRIEVER` с параметром `k=top_k`, взять первый элемент `results` (список найденных документов для единственного запроса) и преобразовать найденные тексты обратно в индексы в `corpus`.

Ожидаемый (Expected output) результат для `bm25_retrieve("What are the recent news about GDP?")`:

```
[752, 673, 289, 626, 43]
```

Тест: `unittests.test_bm25_retrieve(bm25_retrieve)`.

#### 3.3–3.4 Semantic Search и Embeddings

Markdown поясняет: ключевой компонент semantic search — embeddings, векторные представления текста, отражающие смысл; для сравнения векторов часто используется cosine similarity. Корпус уже заранее превращён в embeddings — их нужно только загрузить.

```python
EMBEDDINGS = joblib.load("embeddings.joblib")

model_name = os.path.join(os.environ['MODEL_PATH'], "BAAI/bge-base-en-v1.5")
model = SentenceTransformer(model_name)
```

Демонстрационные (не graded) примеры:

```python
query = "RAG is awesome"
model.encode(query)[:40]  # результат в notebook усечён, чтобы не засорять вывод
```

```python
query1 = "What are the primary colors"
query2 = "Yellow, red and blue"
query3 = "Cats are friendly animals"
...
print(f"Similarity between '{query1}' and '{query2}' = {cosine_similarity(query1_embed, query2_embed)[0]}")
print(f"Similarity between '{query1}' and '{query3}' = {cosine_similarity(query1_embed, query3_embed)[0]}")
```

Markdown отдельно предупреждает (**ATTENTION!**): вывод `cosine_similarity` — всегда список сходств между первым вектором и вторым вектором/массивом векторов.

Пример с полным набором embeddings:

```python
query = "Taylor Swift"
query_embed = model.encode(query)
similarity_scores = cosine_similarity(query_embed, EMBEDDINGS)
similarity_indices = np.argsort(-similarity_scores)
top_2_indices = similarity_indices[:2]
```

В комментариях кода поясняется: `-similarity_scores` используется, чтобы отсортировать по убыванию (поскольку `argsort` по умолчанию сортирует по возрастанию).

**Exercise 2 — `semantic_search_retrieve(query, top_k=5)`** (GRADED CELL, шаблон):

```python
def semantic_search_retrieve(query, top_k=5):
    ### START CODE HERE ###
    query_embedding = None
    similarity_scores = None
    similarity_indices = None
    top_k_indices_array = None
    ### END CODE HERE ###
    top_k_indices = [int(x) for x in top_k_indices_array]
    return top_k_indices
```

По докстрингу и hint-ам ожидаемое решение: закодировать `query` через `model.encode(query)`, посчитать `cosine_similarity(query_embedding, EMBEDDINGS)`, отсортировать индексы по убыванию через `np.argsort(-similarity_scores)`, взять первые `top_k`.

Ожидаемый (Expected output) результат для `semantic_search_retrieve("What are the recent news about GDP?")`:

```
[743, 673, 626, 752, 326]
```

Тест: `unittests.test_semantic_search_retrieve(semantic_search_retrieve, EMBEDDINGS)`.

#### 3.5 RRF Retrieve

Markdown описывает `Reciprocal Rank Fusion` (RRF) — технику информационного поиска для объединения результатов нескольких ранжирующих систем, повышающую общую эффективность retrieval за счёт использования сильных сторон разных подходов. Формула:

$$\text{Score}(d) = \sum_{r=1}^{n} \frac{1}{k + \text{rank}_r(d)}$$

где `n` — число ранжирующих систем, `rank_r(d)` — ранг документа `d` в `r`-м списке результатов, `k` — константа, масштабирующая вклад каждого ранга.

**Exercise 3 — `reciprocal_rank_fusion(list1, list2, top_k=5, K=60)`** (GRADED CELL, шаблон):

```python
def reciprocal_rank_fusion(list1, list2, top_k=5, K=60):
    ### START CODE HERE ###
    rrf_scores = None
    for lst in [list1, list2]:
        for rank, item in enumerate(lst, start=1):
            if item not in rrf_scores:
                rrf_scores[item] = None
            rrf_scores[item] += None
    sorted_items = sorted(None, key=rrf_scores.get, reverse=True)
    top_k_indices = [int(x) for x in None]
    ### END CODE HERE ###
    return top_k_indices
```

По докстрингу, hint-ам и комментариям в теле функции ожидаемое решение: инициализировать `rrf_scores = {}`, для каждого из двух списков перечислить элементы с рангом, начинающимся с 1 (`enumerate(lst, start=1)` — по конвенции ранжирования, где первый элемент имеет ранг 1, а не 0), инициализировать счёт нового документа значением `0`, прибавлять к нему `1 / (rank + K)`, затем отсортировать индексы по убыванию скора (`sorted(rrf_scores, key=rrf_scores.get, reverse=True)`) и взять первые `top_k`.

Демонстрационный вызов:

```python
list1 = semantic_search_retrieve('What are the recent news about GDP?')
list2 = bm25_retrieve('What are the recent news about GDP?')
rrf_list = reciprocal_rank_fusion(list1, list2)
```

Ожидаемый (Expected output, порядок может отличаться):

```
Semantic Search List: [743 673 626 752 326]
BM25 List: [752, 673, 289, 626, 43]
RRF List: [673, 752, 626, 743, 289]
```

Тест: `unittests.test_reciprocal_rank_fusion(reciprocal_rank_fusion)`.

### Раздел 4: завершение RAG-системы

#### 4.1 Создание финального промпта

Даны (не graded) функции, аналогичные использованным в задании Module 1, но адаптированные под несколько retrieval-функций:

**`generate_final_prompt(query, top_k, retrieve_function=None, use_rag=True)`**:

1. если `use_rag=False` — возвращает исходный `query` без изменений;
2. если имя переданной `retrieve_function` равно `'reciprocal_rank_fusion'` — вызывает и `semantic_search_retrieve(query, top_k)`, и `bm25_retrieve(query, top_k)`, затем объединяет результаты через `retrieve_function(list1, list2, top_k)`;
3. иначе — вызывает переданную `retrieve_function(query=query, top_k=top_k)` напрямую;
4. извлекает документы по полученным индексам через `query_news(top_k_indices)`;
5. форматирует каждый документ в строку вида `Title: ..., Description: ..., Published at: ...\nURL: ...` (тот же формат, что и в assignment Module 1);
6. собирает итоговый промпт с инструкцией использовать «2024 News» как часть общих знаний модели, не полагаясь только на них.

**`llm_call(query, retrieve_function=None, top_k=5, use_rag=True)`** — вызывает `generate_final_prompt`, передаёт результат в `generate_with_single_input`, возвращает `generated_response['content']`.

Демонстрационный вызов (без явного результата в тексте notebook, так как зависит от нерешённых функций выше):

```python
query = "Recent news in technology. Provide sources."
print(llm_call(query, retrieve_function=semantic_search_retrieve))
```

#### 4.2 Эксперименты с RAG-системой

`display_widget(llm_call, semantic_search_retrieve, bm25_retrieve, reciprocal_rank_fusion)` строит интерактивный виджет на `ipywidgets` с полем ввода запроса, слайдером `Top K` (от 1 до 20) и кнопкой `Get Responses`. По нажатию кнопки одновременно выводятся четыре ответа LLM в четырёх колонках:

- **Semantic Search**;
- **BM25 Search**;
- **Reciprocal Rank Fusion**;
- **Without RAG**.

Markdown предлагает тестовые запросы: *«What were the most important events of the past year?»*, *«How is global warming progressing in 2024?»*, *«Tell me about the most recent advances in AI.»*, *«Give me the most important facts from past year.»*.

#### 4.3 Ask yourself

Заключительный вопрос для рефлексии слушателя: какая из настроек retrieval дала лучшие результаты по его мнению и есть ли типы запросов, где один метод превосходит другой.

Notebook завершается поздравлением с выполнением второго задания.

### Helper-файл `utils.py`

Импорты: `requests`, `json`, `dateutil.parser`, `pandas as pd`, `pprint` (как `original_pprint`), `os`, `Together` из `together`, `numpy as np`.

Функции:

- **`cosine_similarity(v1, array_of_vectors)`** — реализация, аналогичная использованной в ungraded-лабораторных: приводит входы к `numpy`, поддерживает как один вектор, так и массив векторов, возвращает `np.array` со значениями `dot_product / (norm_v1 * norm_v2)` (в отличие от версии из Module 1/ungraded-лабораторных, здесь возвращается `numpy`-массив, а не обычный `list`).
- **`euclidean_distance(v1, array_of_vectors)`** — аналогична версии из ungraded-лабораторной работы 1: проверяет совпадение форм векторов (`raise ValueError` при несовпадении), возвращает список расстояний.
- **`format_date(date_string)`** — парсит дату через `dateutil.parser`, возвращает строку `YYYY-MM-DD`.
- **`pprint(*args, **kwargs)`** — обёртка над стандартным `pprint.pprint` с параметром `sort_dicts=False` по умолчанию (сохраняет исходный порядок ключей словаря при печати).
- **`generate_with_single_input(...)`** — по общей структуре аналогична версиям из предыдущих notebook курса, но с отличиями: параметр `role` по умолчанию — `'assistant'` (а не `'user'`); `top_p` и `temperature` по умолчанию равны `0` (а не `None`) и, если явно переданы как `None`, заменяются на строку `'none'`; модель по умолчанию — `"meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"` (а не `"Qwen/Qwen3.5-9B"`, как в notebook Module 1); proxy-URL для запроса без API-ключа зашит напрямую как `'https://proxy.dlai.link/coursera_proxy/together'` (без проверки на переменную окружения `IN_COURSERA_ENVIRON`); в payload нет отключения reasoning (`reasoning: {"enabled": False}` здесь не устанавливается).
- **`read_dataframe(path)`** — идентична версии из Module 1: читает CSV, форматирует `published_at`/`updated_at`, возвращает список записей.
- **`display_widget(llm_call_func, semantic_search_retrieve, bm25_retrieve, reciprocal_rank_fusion)`** — строит четырёхколоночный виджет сравнения ответов (описан выше в разделе 4.2); внутри обработчика кнопки последовательно вызывает `llm_call_func` для каждой из четырёх конфигураций (`semantic_search_retrieve` с `use_rag=True`, `bm25_retrieve` с `use_rag=True`, `reciprocal_rank_fusion` с `use_rag=True`, и `None`/`use_rag=False` для варианта без RAG), отображая каждый ответ через `display(Markdown(response))`.

### Helper-файл `unittests.py`

Импортирует `test_case`, `print_feedback` из `dlai_grader.grading`, `FunctionType` из `types`, весь модуль `utils`. Загружает `data = utils.read_dataframe("news_data_dedup.csv")` (переменная `data` в показанном коде далее не используется).

- **`test_bm25_retrieve(learner_func)`** — проверяет тип функции; для запроса `"Should I invest in startups?"` и `top_k=3` проверяет тип результата (`list`), его длину и точное совпадение с ожидаемыми индексами `[863, 848, 716]`; затем повторяет проверку типа и длины для `top_k=10` (без проверки конкретных индексов).
- **`test_semantic_search_retrieve(learner_func, EMBEDDING)`** — аналогичная структура: для `top_k=3` ожидает точные индексы `[863, 416, 624]`; для `top_k=10` проверяет только тип и длину.
- **`test_reciprocal_rank_fusion(learner_func)`** — использует заранее заданные списки `l1 = [17, 29, 28, 26, 18, 14, 1, 0, 16, 11]` и `l2 = [17, 26, 16, 25, 18, 24, 13, 11, 6, 12]`; для `top_k=10` ожидает точный результат `[17, 26, 18, 16, 11, 29, 28, 25, 14, 24]`; для `top_k=4` проверяет только тип и длину.
- **`exercise_5(learner_func)`** — присутствует в файле, но не вызывается ни в одной ячейке `C1M2_Assignment.ipynb`: проверяет некую функцию `recall`, принимающую два списка индексов и возвращающую `float` (например, recall для `l1=[1,2,4]`, `l2=[1,2,3,4]` должен равняться `0.75`). Это, по всей видимости, задел на упражнение, отсутствующее в текущей версии задания — в конспекте зафиксировано как факт из файла, без домысливания его роли.

### Ограничения и предпосылки

Для полного выполнения notebook требуются: локальный файл `news_data_dedup.csv`; локальный файл `embeddings.joblib` с предвычисленными embeddings корпуса; переменная окружения `MODEL_PATH` (путь к локально сохранённой/кэшированной модели `BAAI/bge-base-en-v1.5`); доступ к Together.ai или proxy-серверу Coursera (`TOGETHER_API_KEY` или прямой доступ к `https://proxy.dlai.link/coursera_proxy/together`); установленные зависимости `bm25s`, `sentence_transformers`, `joblib`, `numpy`, `pandas`, `python-dateutil`, `together`, `requests`, `ipywidgets`, а для тестов — `dlai_grader`.

Поскольку изучен именно шаблон задания без выполненного решения, реальные числовые результаты для `bm25_retrieve`, `semantic_search_retrieve`, `reciprocal_rank_fusion` и итоговых ответов `llm_call`/`display_widget` в notebook не зафиксированы как visible output — они присутствуют только как «Expected output» в markdown-ячейках. В рамках конспекта код изучался статически, без запуска notebook, скриптов или отдельных ячеек и без попытки самостоятельно решить graded-упражнения.
