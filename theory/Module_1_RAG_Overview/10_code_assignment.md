См. practice\Module1\Graded_Assignments\C1M1_Assignment_Solution.ipynb

## Конспект по коду

### Назначение assignment notebook

Notebook `C1M1_Assignment_Solution.ipynb` - первое graded assignment модуля. В нем строится простой RAG pipeline на dataset с news information.

Цель: дать `LLM` возможность retrieve relevant news details из dataset и использовать эту информацию для более информированных ответов. В markdown указано, что используется модель `llama-3-1-8b-instruct-turbo`, trained on data up to December 2023, а RAG нужен, чтобы модель могла включать информацию о событиях 2024 года.

В assignment нужно:

- использовать query и retrieval function для доступа к relevant data;
- format data appropriately;
- generate prompt с query и relevant data;
- передать prompt в `LLM`;
- сравнить ответы with RAG и without RAG.

### Локальные источники кода

Помимо notebook изучены helper-файлы:

- `practice\Module1\Graded_Assignments\utils.py`;
- `practice\Module1\Graded_Assignments\unittests.py`.

Также assignment использует локальные данные и assets:

- `news_data_dedup.csv`;
- `embeddings.joblib`;
- `images\toc.png`;
- `images\rag_overview.png`.

### Импорты notebook

Notebook импортирует из `utils`:

```python
from utils import (
    retrieve,
    pprint,
    generate_with_single_input,
    read_dataframe,
    display_widget
)
import unittests
```

Эти функции покрывают:

- retrieval;
- pretty printing;
- LLM call;
- loading dataframe;
- interactive comparison widget;
- unit tests для graded functions.

### Dataset

Данные загружаются так:

```python
NEWS_DATA = read_dataframe("news_data_dedup.csv")
```

Notebook указывает, что используется Kaggle dataset `News Headlines 2024`, содержащий thousands of news headlines and related information from BBC News.

Visible output с `pprint(NEWS_DATA[9:11])` показывает records со структурой:

- `guid`;
- `title`;
- `description`;
- `venue`;
- `url`;
- `published_at`;
- `updated_at`.

В notebook отдельно отмечено, что важные поля для ответов `LLM`:

- `title`;
- `description`;
- `url`;
- `published_at`.

### Helper-файл `utils.py`

`utils.py` импортирует:

- `json`;
- `numpy as np`;
- `pandas as pd`;
- `pprint` как `original_pprint`;
- `dateutil.parser`;
- `SentenceTransformer` из `sentence_transformers`;
- `joblib`;
- `cosine_similarity` из `sklearn.metrics.pairwise`;
- `requests`;
- `os`;
- `Together` из `together`;
- `ipywidgets`;
- `display`, `Markdown` из `IPython.display`.

Ключевые настройки:

- `model_name` собирается из `os.environ['MODEL_PATH']` и `BAAI/bge-base-en-v1.5`;
- `model = SentenceTransformer("BAAI/bge-base-en-v1.5", cache_folder=os.environ['MODEL_PATH'])`;
- `EMBEDDINGS = joblib.load("embeddings.joblib")`;
- `NEWS_DATA = pd.read_csv("./news_data_dedup.csv").to_dict(orient='records')`.

Это означает, что для работы helper-кода нужен environment variable `MODEL_PATH`, локальный файл `embeddings.joblib` и dataset `news_data_dedup.csv`.

Функции API:

- `get_proxy_url()`: в Coursera environment возвращает `https://proxy.dlai.link/coursera_proxy/together`, иначе `TOGETHER_BASE_URL` или `https://api.together.xyz/`;
- `get_proxy_headers()`: возвращает `Authorization` из `TOGETHER_API_KEY`;
- `get_together_key()`: читает `TOGETHER_API_KEY`;
- `generate_with_single_input(...)`: формирует chat completion payload и вызывает proxy или Together client.

Функции обработки данных:

- `format_date(date_string)`: парсит дату и возвращает формат `YYYY-MM-DD`;
- `read_dataframe(path)`: читает CSV, форматирует `published_at` и `updated_at`, возвращает list of records;
- `concatenate_fields(dataset, fields)`: соединяет значения выбранных fields в text, обрезая результат до `493` символов;
- `retrieve(query, top_k=5)`: кодирует query через embedding model, считает cosine similarity между query embedding и `EMBEDDINGS`, сортирует индексы по убыванию similarity и возвращает top `k` indices.

`display_widget(llm_call_func)` строит интерактивный UI на `ipywidgets`, где можно:

- ввести query;
- задать custom augmented prompt layout;
- выбрать `Top K` от 1 до 20;
- нажать `Get Responses`;
- увидеть ответы `With RAG` и `Without RAG`.

### `unittests.py`

`unittests.py` содержит тесты для graded functions.

`test_get_relevant_data(learner_func)` проверяет:

- что передана function;
- что функция не падает для query `"This is a test query"` и `top_k=3`;
- что output имеет type `list`;
- что длина output равна `top_k`;
- что retrieved documents имеют ожидаемые `guid`.

`test_format_relevant_data(learner_func)` проверяет:

- что передана function;
- что результат содержит keywords `title`, `url`, `published`, `description`;
- что для `relevant_data = NEWS_DATA[5:9]` каждое из нужных слов встречается нужное количество раз.

### Основные функции notebook

#### `query_news(indices)`

Функция возвращает documents из `NEWS_DATA` по списку indices:

```python
output = [NEWS_DATA[index] for index in indices]
```

Visible example с `indices = [3, 6, 9]` печатает три news records, включая:

- `Europe risks dying and faces big decisions - Macron`;
- `Supreme Court divided on whether Trump has immunity`;
- `Paris's Moulin Rouge loses windmill sails overnight`.

#### `retrieve(query, top_k)`

В notebook `retrieve` описана как essential part of RAG system. Она принимает:

- `query`: string search query;
- `top_k`: number of top similar documents to return.

Возвращает list of indices для top `k` most similar documents based on similarity scores.

Visible example:

```python
indices = retrieve("Concerts in North America", top_k=1)
```

Output:

```text
[350]
```

Затем `query_news(indices)` возвращает соответствующую новость про touring и Taylor Swift's Eras tour.

#### `get_relevant_data(query, top_k=5)`

Первая graded function объединяет retrieval и lookup документов.

Solution steps:

1. вызвать `retrieve(query=query, top_k=top_k)`;
2. сохранить результат в `relevant_indices`;
3. вызвать `query_news(relevant_indices)`;
4. вернуть `relevant_data`.

Пример:

```python
query = "Greatest storms in the US"
relevant_data = get_relevant_data(query, top_k=1)
```

Visible output возвращает news record:

- title: `Large tornado seen touching down in Nebraska`;
- description: severe and powerful storms moved across several US states;
- published_at: `2024-04-26`;
- updated_at: `2024-04-28`.

Unit test `unittests.test_get_relevant_data(get_relevant_data)` показывает visible output `All tests passed!`.

#### `format_relevant_data(relevant_data)`

Вторая graded function форматирует list of relevant documents в string для RAG prompt.

Требования assignment:

- output должен включать news title;
- news description;
- news published date;
- news URL;
- exact keywords `title`, `url`, `published_at`, `description` в любом регистре.

Solution:

1. создать `formatted_documents = []`;
2. пройти по каждому `document` в `relevant_data`;
3. сформировать строку:

```python
f"Title: {document['title']}, Description: {document['description']}, Published at: {document['published_at']}\nURL: {document['url']}"
```

4. добавить строку в `formatted_documents`;
5. вернуть `"\n".join(formatted_documents)`.

Visible output для `NEWS_DATA[4:8]` показывает четыре formatted news entries, включая titles, descriptions, dates и URLs.

Unit test `unittests.test_format_relevant_data(format_relevant_data)` показывает visible output `All tests passed!`.

#### `generate_final_prompt(query, top_k=5, use_rag=True, prompt=None)`

Функция создает final prompt.

Если `use_rag=False`, функция возвращает исходный `query`.

Если `use_rag=True`, функция:

1. вызывает `get_relevant_data(query, top_k=top_k)`;
2. форматирует retrieved data через `format_relevant_data`;
3. если custom `prompt` не передан, строит default prompt;
4. если custom `prompt` передан, делает `prompt.format(query=query, documents=retrieve_data_formatted)`.

Default prompt говорит модели, что additional information from 2024 should be added as overall knowledge to answer the query, но модель не должна rely only on this information.

Visible output для query `"Tell me about the US GDP in the past 3 years."` показывает prompt с `2024 News`, включая несколько retrieved articles о US economy, GDP и IMF projections.

#### `llm_call(query, top_k=5, use_rag=True, prompt=None)`

Функция:

1. вызывает `generate_final_prompt(...)`;
2. отправляет prompt в `generate_with_single_input(prompt)`;
3. достает `generated_response['content']`;
4. возвращает generated message.

В notebook вызов `print(llm_call(query, use_rag=True))` завершился visible error from proxy/API:

- exception: `Error while calling LLM`;
- response содержит `Internal server error`;
- error type: `server_error`.

Следующая ячейка `print(llm_call(query, use_rag=False))` в solution notebook не имеет visible output.

### Experimenting with RAG System

Последний раздел предлагает экспериментировать с queries и сравнивать with RAG / without RAG через `display_widget(llm_call)`.

Примеры queries:

- важные события прошлого года;
- global warming in 2024;
- recent advances in AI;
- important facts from past year.

Также можно задать custom layout для `augmented prompt` с placeholders:

- `{query}`;
- `{documents}`.

### Ограничения и предпосылки

Для полного выполнения notebook нужны:

- локальный CSV `news_data_dedup.csv`;
- локальный `embeddings.joblib`;
- environment variable `MODEL_PATH` для cache folder embedding model;
- доступ к Together.ai или Coursera proxy;
- возможно `TOGETHER_API_KEY`;
- зависимости `sentence_transformers`, `sklearn`, `joblib`, `pandas`, `numpy`, `ipywidgets`, `together`, `requests`.

Notebook и helper-код выполняют реальные API calls при запуске LLM-ячеек. В рамках конспекта код изучался статически, без запуска notebook, scripts или cells.
