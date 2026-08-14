См. `practice\Module1\Graded_Assignments\C1M1_Assignment.ipynb`

## Конспект по коду

### Назначение assignment notebook

`C1M1_Assignment.ipynb` — решённое первое графируемое задание (`Assignment: Introduction to RAG Systems`) модуля (ранее в этой же папке лежали отдельные файлы `C1M1_Assignment_Solution.ipynb` и `C1M1_Assignment_2026_03_27_13_57_53.ipynb` — они удалены, актуальный и единственный файл теперь `C1M1_Assignment.ipynb`). В нём строится простой RAG pipeline на датасете с новостной информацией.

Согласно вводной markdown-ячейке, используется модель [`llama-3-1-8b-instruct-turbo`](https://www.together.ai/models/llama-3-1), обученная на данных до декабря 2023 года; RAG нужен, чтобы модель могла включать в ответы информацию о событиях, произошедших в 2024 году.

В задании нужно:

- использовать `query` и функцию retrieval, чтобы получить доступ к релевантным данным по заданному запросу;
- отформатировать данные соответствующим образом;
- сгенерировать промпт с `query` и релевантными данными для передачи в `LLM`.

Раздел 1.1 «RAG architecture overview» отсылает к упрощённой диаграмме RAG из лекций (`images/rag_overview.png`) и поясняет общий план работы: слушатель использует уже реализованный retriever, чтобы получить релевантные данные по запросу, форматирует эти данные и создаёт новый промпт, включающий и запрос, и извлечённую информацию, а в конце сравнивает результаты запросов с RAG и без него.

Раздел 1.2 сообщает про правила проверки (`grading`): все ячейки, кроме предназначенных для решения, заморожены; новые ячейки для экспериментов не учитываются grader'ом; глобальные переменные, кроме определённых заглавными буквами, могут быть недоступны при изолированном тестировании кода.

### Локальные источники кода

Помимо самого notebook изучены helper-файлы и вспомогательные данные из той же папки `practice\Module1\Graded_Assignments`:

- `utils.py`;
- `unittests.py`;
- `news_data_dedup.csv` (данные);
- `embeddings.joblib` (предвычисленные эмбеддинги);
- `images\toc.png`, `images\rag_overview.png` (иллюстрации, используемые в markdown-ячейках).

`utils.py` и `unittests.py` не изменились по сравнению с предыдущей версией задания.

### Импорты notebook

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

Эти функции покрывают: retrieval, «красивую» печать JSON (`pprint`), вызов LLM, загрузку датафрейма и интерактивный виджет для сравнения ответов; `unittests` содержит тесты для graded-функций.

### Раздел 2: загрузка датасета

```python
NEWS_DATA = read_dataframe("news_data_dedup.csv")
```

В markdown указано, что используется Kaggle-датасет [`News Headlines 2024`](https://www.kaggle.com/datasets/dylanjcastillo/news-headlines-2024), содержащий тысячи новостных заголовков и связанной информации от BBC News. Проверка размера датасета — `len(NEWS_DATA)` — visible output: `870`.

Проверка структуры данных через `pprint(NEWS_DATA[9:11])` показывает записи со структурой: `guid`, `title`, `description`, `venue`, `url`, `published_at`, `updated_at` (пример — новости про Moulin Rouge в Париже и об использовании Украиной ракет большей дальности).

В markdown отдельно отмечено, что важные для ответов LLM поля — `title`, `description`, `url` и `published_at`: они дают модели достаточно хорошую информацию, чтобы отвечать на большинство вопросов.

### Раздел 3: основные функции

Notebook поясняет, что заранее предоставлены две функции:

- **`query_news`** — по списку индексов возвращает все документы, соответствующие этим индексам;
- **`retrieve`** — по запросу и числу `top_k` извлекает `top_k` наиболее релевантных документов.

А слушатель реализует:

- **`get_relevant_data`** — принимает `query` и `top_k`, возвращает `top_k` релевантных документов;
- **`format_relevant_data`** — по списку документов создаёт форматированную строку с информацией о документах.

Далее эти функции используются для построения собственного небольшого RAG pipeline.

#### 3.1 `query_news(indices)`

Дана готовой:

```python
def query_news(indices):
    output = [NEWS_DATA[index] for index in indices]
    return output
```

Пример с `indices = [3, 6, 9]` возвращает три новости, включая:

- *«Europe risks dying and faces big decisions - Macron»*;
- *«Supreme Court divided on whether Trump has immunity»*;
- *«Paris's Moulin Rouge loses windmill sails overnight»*.

#### 3.2 Функция `retrieve`

Полный код `retrieve` находится в `utils.py` (описан ниже); в этом разделе notebook фокусируется на входных параметрах и выходных данных, поясняя, что подробное устройство и различные техники document retrieval будут разбираться в Module 2.

- **Параметры:** `query` (строка поискового запроса), `top_k` (число документов для возврата).
- **Выход:** список индексов, соответствующих `top_k` наиболее похожим документам корпуса на основе similarity-баллов с запросом.
- **Вызов:** `retrieve(query: str, top_k: int)`.

Пример:

```python
indices = retrieve("Concerts in North America", top_k=1)
print(indices)
```

Visible output: `[350]`. Затем `query_news(indices)` возвращает соответствующую новость — статью о заработках музыкантов на турах, где также упоминается, что Taylor Swift превысила `$1bn` дохода со своего Eras tour (издание The Guardian).

#### 3.3 Exercise 1 — `get_relevant_data`

Graded-функция объединяет `retrieve` и `query_news`:

```python
def get_relevant_data(query: str, top_k: int = 5) -> list[dict]:
    relevant_indices = retrieve(query=query, top_k=top_k)
    relevant_data = query_news(relevant_indices)
    return relevant_data
```

Пример:

```python
query = "Greatest storms in the US"
relevant_data = get_relevant_data(query, top_k=1)
```

Visible output и ожидаемый (Expected output) результат совпадают — новость *«Large tornado seen touching down in Nebraska»* (`guid: 3ca548fe82c3fcae2c4c0c635d03eb2e`, опубликовано `2024-04-26`).

Проверка: `unittests.test_get_relevant_data(get_relevant_data)` — visible output: `All tests passed!`.

#### 3.4 Exercise 2 — `format_relevant_data`

Требования из markdown: итоговая строка должна включать заголовок новости (news title), описание (description), дату публикации (published date) и URL; в выводе должны присутствовать ключевые слова `title`, `url`, `published_at`, `description` (регистр не важен) — это нужно для проверки grader'ом.

Solution:

```python
def format_relevant_data(relevant_data):
    formatted_documents = []
    for document in relevant_data:
        formatted_document = f"Title: {document['title']}, Description: {document['description']}, Published at: {document['published_at']}\nURL: {document['url']}"
        formatted_documents.append(formatted_document)
    return "\n".join(formatted_documents)
```

Тест на `example_data = NEWS_DATA[4:8]`: `print(format_relevant_data(example_data))` выводит четыре отформатированные новости (например, про судебное дело против жены премьер-министра Испании, туристический сбор в Венеции, дело о неприкосновенности Trump в Верховном суде США, ливни в Танзании).

Проверка: `unittests.test_format_relevant_data(format_relevant_data)` — visible output: `All tests passed!`.

#### 3.5 `generate_final_prompt` (дано, редактируемая ячейка)

Функция создаёт финальный промпт:

```python
def generate_final_prompt(query, top_k=5, use_rag=True, prompt=None):
    if not use_rag:
        return query

    relevant_data = get_relevant_data(query, top_k=top_k)
    retrieve_data_formatted = format_relevant_data(relevant_data)

    if prompt is None:
        prompt = (
            f"Answer the user query below. There will be provided additional information for you to compose your answer. "
            f"The relevant information provided is from 2024 and it should be added as your overall knowledge to answer the query, "
            f"you should not rely only on this information to answer the query, but add it to your overall knowledge."
            f"Query: {query}\n"
            f"2024 News: {retrieve_data_formatted}"
        )
    else:
        prompt = prompt.format(query=query, documents=retrieve_data_formatted)

    return prompt
```

Если `use_rag=False`, функция возвращает исходный `query` без изменений. Если передан кастомный `prompt`-шаблон, он форматируется через `.format(query=..., documents=...)` — то есть шаблон должен содержать плейсхолдеры `{query}` и `{documents}`.

Пример:

```python
print(generate_final_prompt("Tell me about the US GDP in the past 3 years."))
```

Visible output — собранный промпт с инструкцией про использование информации 2024 года как часть общих знаний модели, вопросом (`Query: ...`) и блоком `2024 News:` с пятью отформатированными статьями об экономике США и ВВП (например, из WSJ: *«America's Economy Is No. 1. That Means Trouble»*, *«Live Markets: Stock Futures Fall, Yields Jump After GDP Report»* и другие).

#### 3.6 `llm_call`

```python
def llm_call(query, top_k=5, use_rag=True, prompt=None):
    prompt = generate_final_prompt(query, top_k, use_rag, prompt)
    generated_response = generate_with_single_input(prompt)
    generated_message = generated_response['content']
    return generated_message
```

Параметры, поясняемые в markdown: `query` — запрос для LLM; `use_rag` — флаг, использовать ли RAG (позволяет сравнивать запросы с RAG-системой и без неё); `model` — используемая модель (по умолчанию упоминается модель на 3 миллиарда параметров Llama, стандартная для задания — фраза из markdown буквально гласит *«the standard is the Llama 3 Billion parameter»*).

Тестовый запрос:

```python
query = "Tell me about the US GDP in the past 3 years."
print(llm_call(query, use_rag=True))
```

Visible output — развёрнутый ответ LLM, заземлённый в извлечённых новостях 2024 года: модель по годам (2022, 2023, 2024) описывает динамику доли США в мировом ВВП, ссылаясь на конкретные цифры из отформатированных новостей (например, «26.3% of the global gross domestic product... the highest in almost two decades»), и в конце добавляет ремарку про альтернативную метрику благополучия, упомянутую в одной из статей.

Следующая ячейка `print(llm_call(query, use_rag=False))` тоже имеет visible output — ответ без RAG, основанный только на собственных знаниях модели (обучена до декабря 2023): перечисляются оценки роста ВВП США за 2021 (+5.7%, $22.67 трлн), 2022 (+2.1%, $23.32 трлн) и 2023 (+1.8% за 1 квартал, $23.65 трлн), с оговоркой, что цифры могут быть неточными и стоит свериться с BEA/ФРС.

Сравнение двух ответов наглядно демонстрирует цель задания: версия с RAG оперирует конкретными данными из новостей 2024 года (например, точной цифрой доли США в мировом ВВП на 2024 год), а версия без RAG — общими оценками из параметрической памяти модели, ограниченной декабрём 2023 года.

### Раздел 4: эксперименты с RAG-системой

Последний раздел предлагает экспериментировать с собственными запросами и сравнивать ответы с RAG и без него через `display_widget(llm_call)`. В markdown отмечено, что датасет посвящён новостям 2024 года, поэтому не каждый запрос хорошо продемонстрирует фреймворк. Примеры предлагаемых запросов:

- *«What were the most important events of the past year?»*;
- *«How is global warming progressing in 2024?»*;
- *«Tell me about the most recent advances in AI.»*;
- *«Give me the most important facts from past year.»*.

Также можно задать собственный layout для augmented prompt с плейсхолдерами `{query}` и `{documents}`, например:

```
This is the query: {query}
These are the documents: {documents}
```

Notebook завершается сообщением о поздравлении с созданием первой простой RAG-системы.

### Helper-файл `utils.py`

Импорты: `json`, `numpy as np`, `pandas as pd`, `pprint` (как `original_pprint`, хотя далее в файле определяется собственная функция `pprint`), `dateutil.parser`, `SentenceTransformer` из `sentence_transformers`, `joblib`, `cosine_similarity` из `sklearn.metrics.pairwise`, `requests`, `os`, `Together` из `together`, `ipywidgets`, `display`/`Markdown` из `IPython.display`.

Настройки и загрузка на уровне модуля (выполняются при импорте `utils.py`):

```python
model_name = os.path.join(os.environ['MODEL_PATH'], "BAAI/bge-base-en-v1.5")
model = SentenceTransformer("BAAI/bge-base-en-v1.5", cache_folder=os.environ['MODEL_PATH'])
EMBEDDINGS = joblib.load("embeddings.joblib")
NEWS_DATA = pd.read_csv("./news_data_dedup.csv").to_dict(orient='records')
```

Переменная `model_name` вычисляется, но далее в файле не используется — модель `SentenceTransformer` создаётся напрямую по строковому имени `"BAAI/bge-base-en-v1.5"` с параметром `cache_folder`, взятым из переменной окружения `MODEL_PATH`. Это означает, что для успешного импорта `utils.py` необходимы установленная переменная окружения `MODEL_PATH`, локальный файл `embeddings.joblib` и файл `news_data_dedup.csv` в рабочей директории.

Функции API:

- **`get_proxy_url()`** — в среде Coursera (определяется по наличию переменной окружения `IN_COURSERA_ENVIRON`) возвращает `https://proxy.dlai.link/coursera_proxy/together`; иначе — значение `TOGETHER_BASE_URL` или, по умолчанию, `https://api.together.xyz/`.
- **`get_proxy_headers()`** — возвращает заголовок `Authorization` со значением переменной окружения `TOGETHER_API_KEY` (пустая строка, если не задана).
- **`get_together_key()`** — читает `TOGETHER_API_KEY` из окружения.
- **`generate_with_single_input(...)`** — по устройству аналогична версии из `ungraded_lab_2`, но с двумя отличиями: (1) условие выбора между proxy-запросом и прямым клиентом Together — `if (not together_api_key) and ('TOGETHER_API_KEY' not in os.environ)`, то есть прямой клиент Together используется, если ключ передан явно **или** переменная окружения `TOGETHER_API_KEY` установлена; (2) вызов `requests.post` не передаёт заголовки (`get_proxy_headers()` в вызове не используется), только `verify=False`.

Функции обработки данных:

- **`pprint(*args, **kwargs)`** — печатает данные как JSON с отступом `indent=2` (через `json.dumps`).
- **`format_date(date_string)`** — парсит дату произвольного формата через `dateutil.parser` и возвращает строку `YYYY-MM-DD`.
- **`read_dataframe(path)`** — читает CSV через `pandas`, применяет `format_date` к колонкам `published_at` и `updated_at`, возвращает список записей (`to_dict(orient='records')`).
- **`concatenate_fields(dataset, fields)`** — для каждой записи датасета склеивает значения указанных полей в одну строку (через пробел, пропуская отсутствующие поля), обрезает результат до 493 символов и возвращает список таких строк. В показанном коде notebook эта функция не вызывается напрямую — она присутствует в `utils.py` как вспомогательная функция для подготовки текста к эмбеддингу.
- **`retrieve(query, top_k=5)`** — кодирует `query` через `model.encode(query)`, вычисляет `cosine_similarity` между эмбеддингом запроса и предвычисленной матрицей `EMBEDDINGS`, сортирует индексы по убыванию similarity через `np.argsort(-similarity_scores)` и возвращает первые `top_k` индексов.

**`display_widget(llm_call_func)`** строит интерактивный UI на `ipywidgets`:

- текстовое поле `Query`;
- многострочное поле `Augmented prompt layout` для кастомного шаблона промпта (с плейсхолдерами `{query}` и `{documents}`);
- слайдер `Top K` от 1 до 20 (значение по умолчанию — 5);
- кнопка `Get Responses`, по нажатию на которую вызывается `llm_call_func` дважды — с `use_rag=True` и с `use_rag=False` — и результаты отображаются рядом в двух колонках, подписанных `With RAG` и `Without RAG`, с использованием `display(Markdown(...))`.
- во время генерации в отдельной области статуса выводится сообщение `"Generating..."`.

### Helper-файл `unittests.py`

Импортирует `test_case`, `print_feedback` из `dlai_grader.grading`, `FunctionType` из `types`, `pandas as pd`, и повторно загружает `NEWS_DATA` из `news_data_dedup.csv`. Определяет собственную вспомогательную функцию `query_by_index(list_of_indices, dataset)`, дублирующую логику `query_news` из notebook.

**`test_get_relevant_data(learner_func)`** проверяет:

- что передан объект типа `FunctionType`;
- что вызов `learner_func("This is a test query", top_k=3)` не выбрасывает исключение;
- что тип результата — `list`;
- что длина результата равна `top_k` (3);
- что множество `guid` возвращённых документов совпадает с заранее заданным ожидаемым множеством `guid` (три конкретных новости: про ООН и Газу, про случай на Airbnb, про Basic Materials Roundup).

**`test_format_relevant_data(learner_func)`** проверяет для `relevant_data = NEWS_DATA[5:9]`:

- что передан объект типа `FunctionType`;
- что в результате (приведённом к нижнему регистру) присутствуют ключевые слова `title`, `url`, `published`, `description`;
- что число вхождений каждого из этих ключевых слов равно числу документов (`len(relevant_data)`, то есть 4) — иначе тест засчитывается как неудачный с сообщением о неверном количестве вхождений.

### Ограничения и предпосылки

Для полного выполнения notebook требуются:

- локальный файл `news_data_dedup.csv`;
- локальный файл `embeddings.joblib` с предвычисленными эмбеддингами;
- переменная окружения `MODEL_PATH` (папка кэша для embedding-модели `BAAI/bge-base-en-v1.5`);
- доступ к Together.ai или proxy-серверу Coursera (переменные окружения `IN_COURSERA_ENVIRON`, `TOGETHER_BASE_URL`, `TOGETHER_API_KEY`);
- установленные зависимости: `sentence_transformers`, `scikit-learn` (`sklearn`), `joblib`, `pandas`, `numpy`, `ipywidgets`, `together`, `requests`, `python-dateutil`, а для тестов — `dlai_grader`.

Notebook и helper-код выполняют реальные сетевые вызовы (embedding-модель, LLM API) при исполнении соответствующих ячеек; в рамках данного конспекта код изучался статически, без запуска notebook, скриптов или отдельных ячеек. В сохранённых outputs текущей версии notebook оба вызова `llm_call` (с `use_rag=True` и `use_rag=False`) завершаются успешно и содержат развёрнутые ответы — в отличие от более ранней версии этого файла, где вызов с `use_rag=True` был зафиксирован с ошибкой `Internal server error` со стороны LLM-провайдера.
