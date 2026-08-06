См. practice\Module3\Graded_Assignments\C1M3_Assignment.ipynb

## Конспект по коду

### Назначение assignment notebook

`C1M3_Assignment.ipynb` («Module 3 Assignment - Building RAG systems with a Vector Database») — третье графируемое задание курса. В нём слушатель работает с [Weaviate API](https://weaviate.io/), чтобы построить небольшую RAG-систему: загружает collection с данными BBC News, использует Weaviate API для извлечения документов, создаёт функции извлечения на основе Semantic Search, BM25 и Hybrid Search (с RRF) через Weaviate API, и использует LLM для генерации ответов.

Вводная ячейка отдельно отмечает: задание предполагает, что слушатель уже умеет работать с коллекциями в Weaviate API (рекомендуется прочитать Ungraded Lab по Weaviate API) и что данные в этом задании уже прочанкованы (*chunked*) — практику по chunking предлагается получить в соответствующем Ungraded Lab.

> Важно: как и в задании Module 2, изучен именно шаблон задания (`C1M3_Assignment.ipynb`), а не отдельный файл с готовым решением — файла `..._Solution.ipynb` в папке `Graded_Assignments` нет. При этом состояние графируемых ячеек в этом notebook неоднородно: Exercise 1 (`filter_by_metadata`) содержит незавершённую/ошибочную попытку решения, тогда как Exercises 2–5 (`semantic_search_retrieve`, `bm25_retrieve`, `hybrid_retrieve`, `semantic_search_with_reranking`) оставлены как шаблоны с плейсхолдером `None`. Часть ранних ячеек notebook (импорт `joblib`, загрузка `bbc_data.joblib`) в сохранённом выводе показывает ошибки `ModuleNotFoundError`/`NameError`, тогда как более поздние ячейки (`len(collection)`, `fetch_objects`) показывают успешный результат — то есть видимые outputs в этом notebook не отражают единый последовательный прогон сверху вниз. Всё это зафиксировано ниже как факт, без домысливания причин.

Оглавление notebook:

1. Loading the libraries.
2. Setting up the Weaviate Client and loading the data — Loading the Weaviate Client, Loading the data.
3. Loading the Collection — Metadata filtering (Exercise 1), Semantic search (Exercise 2), BM25 Search (Exercise 3), Hybrid search (Exercise 4, Exercise 5 — reranking).
4. Incorporating the Weaviate API into our previous schema — Generating the final prompt, LLM call.
5. Experimenting with Your RAG System.

### Локальные источники кода

Помимо notebook изучены файлы из той же папки `practice\Module3\Graded_Assignments`:

- `utils.py`;
- `unittests.py`;
- `weaviate_server.py`;
- `flask_app.py`;
- `data/bbc_data.joblib` (данные);
- `README.md` — краткое неавторитетное описание задания (структура директории, компоненты, инструкции по установке), использовано только для сверки, основной источник — сам notebook и код.

### 1. Импорты

```python
import joblib
import weaviate
from weaviate.classes.query import (
    Filter,
    Rerank
)
```

Visible output этой ячейки в сохранённом notebook — `ModuleNotFoundError: No module named 'joblib'` с полным traceback.

Далее:

```python
import flask_app
import weaviate_server
from utils import (
    generate_with_single_input,
    print_object_properties,
    display_widget
)
import unittests
```

Импорт `weaviate_server` запускает подключение к embedded Weaviate на уровне модуля (см. ниже), а импорт `flask_app` поднимает локальный inference-сервер, как и в ungraded labs модуля.

### 2. Настройка клиента Weaviate и загрузка данных

#### 2.1 Клиент

```python
client = weaviate.connect_to_local(port=8079, grpc_port=50050)
```

Markdown поясняет: сервер уже запущен в бэкенде (в отличие от ungraded lab, где клиент создавался через `connect_to_embedded` напрямую в самом notebook, здесь клиент подключается к уже поднятому серверу — который в действительности запускается при импорте `weaviate_server` в разделе 1). Указана инструкция на случай проблем: перезапустить ядро (kernel).

#### 2.2 Загрузка данных

Датасет — адаптированный [BBC news dataset](https://www.kaggle.com/datasets/gpreda/bbc-news) с полями: `title`, `pubDate`, `guid`, `link`, `description`, `article_content`.

```python
bbc_data = joblib.load('data/bbc_data.joblib')
```

Visible output — `NameError: name 'joblib' is not defined` (следствие несостоявшегося импорта `joblib` в разделе 1).

`print_object_properties(bbc_data[0])` — visible output показывает первую запись датасета: статью *«Justin Welby: Political leaders should treat opponents as human beings»* (архиепископ Кентерберийский призывает политиков избегать «wedge issues»), с полями `article_content` (усечено), `description`, `guid`, `link`, `pubDate: 2024-01-01 00:00:04`, `title`.

### 3. Загрузка коллекции

```python
collection = client.collections.get("bbc_collection")
print(f"The number of elements in the collection is: {len(collection)}")
```

Visible output: `The number of elements in the collection is: 75256`.

Пример объекта коллекции с вектором:

```python
object = collection.query.fetch_objects(limit=1, include_vector=True).objects[0]
```

Visible output показывает свойства объекта (статья *«Kamala Harris slams Trump at first rally as he hits back»*, с полями `article_content`, `chunk`, `chunk_index: 0`, `description`, `link`, `pubDate`, `title`) и первые 15 значений вектора `main_vector`, а также его длину: `Vector length: 768`. Markdown поясняет: каждый chunk в vector database отображается в 768-мерный вектор — именно этот вектор Weaviate API использует для semantic search.

#### 3.1 Metadata filtering — Exercise 1

Задача: реализовать `filter_by_metadata(metadata_property, values, collection, limit=5)`, используя `collection.query.fetch_objects` с фильтром вида `Filter.by_property(metadata_property).contains_any(values)` (согласно hint-ам в markdown).

Фактическое содержимое ячейки решения в сохранённом notebook:

```python
from weaviate.collections.filters import Filter, Operator
def filter_by_metadata(metadata_property: str,
                       values: list[str],
                       collection: "weaviate.collections.collection.sync.Collection",
                       limit: int = 5) -> list:
    ### START CODE HERE ###
    filter = Filter(
        Operator.ContainsAny,
        metadata_property,
        values
    )
    response = collection.query.fetch_objects(
        where=filter,
        limit=limit)
    ### END CODE HERE ###
    response_objects = [x.properties for x in response.objects]
    return response_objects
```

Visible output импорта — `ModuleNotFoundError: No module named 'weaviate'`. При вызове `filter_by_metadata('title', ['Taylor Swift'], collection, limit=2)` сохранённый вывод показывает другую ошибку: `TypeError: _FetchObjectsQueryExecutor.fetch_objects() got an unexpected keyword argument 'where'` — то есть в этой версии решения используется параметр `where=filter` и низкоуровневый конструктор `Filter(Operator.ContainsAny, ...)`, тогда как согласно hint-ам markdown и реальной сигнатуре метода `fetch_objects` (это же видно по коду в ungraded lab 1) ожидается параметр `filters=` и высокоуровневый вызов `Filter.by_property(metadata_property).contains_any(values)`. Этот код и его ошибка зафиксированы здесь как есть, без исправления.

Ожидаемый (Expected output) результат для `filter_by_metadata` (по markdown) — два объекта о Golden Globes с упоминанием Margot Robbie и Taylor Swift, с полями `article_content`, `chunk`, `chunk_index: 4` и `5`, `description`, `link`, `pubDate: 2024-01-08 03:23:58+00:00`, `title: Margot Robbie, Taylor Swift and more on Golden Globes red carpet`.

Тест: `unittests.test_filter_by_metadata(filter_by_metadata, client)`.

#### 3.2 Semantic search — Exercise 2

```python
def semantic_search_retrieve(query: str,
                             collection: "weaviate.collections.collection.sync.Collection",
                             top_k: int = 5) -> list:
    ### START CODE HERE ###
    response = None
    ### END CODE HERE ###
    response_objects = [x.properties for x in response.objects]
    return response_objects
```

По докстрингу и hint-у ожидаемое решение должно вызывать `collection.query.near_text(query, limit=top_k)`.

Ожидаемый (Expected Output) результат для `semantic_search_retrieve(query='Tell me about the last Taylor Swift show', collection=collection, top_k=2)` — два chunk из статьи *«'I've never had it this good' - Taylor Swift thanks fans after new Wembley record»* (`chunk_index: 10` и `4`).

Тест: `unittests.test_semantic_search_retrieve(semantic_search_retrieve, client)`.

#### 3.3 BM25 Search — Exercise 3

```python
def bm25_retrieve(query: str,
                  collection: "weaviate.collections.collection.sync.Collection",
                  top_k: int = 5) -> list:
    ### START CODE HERE ###
    response = None
    ### END CODE HERE ###
    response_objects = [x.properties for x in response.objects]
    return response_objects
```

Ожидаемое решение (по hint) — `collection.query.bm25(query, limit=top_k)`.

Ожидаемый (Expected Output) для `bm25_retrieve('Tell me about the last Taylor Swift show', collection, top_k=2)` — два chunk из статьи *«Killer Mike dismisses arrest at Grammys as 'speed bump'»* (`chunk_index: 4` и `3`) — то есть для этого конкретного запроса BM25 находит документ, вообще не связанный по смыслу с Taylor Swift, поскольку опирается только на точное совпадение ключевых слов.

Тест: `unittests.test_bm25_retrieve(bm25_retrieve, client)`.

#### 3.4 Hybrid search — Exercise 4

```python
def hybrid_retrieve(query: str,
                    collection: "weaviate.collections.collection.sync.Collection",
                    alpha: float = 0.5,
                    top_k: int = 5
                   ) -> list:
    ### START CODE HERE ###
    response = None
    ### END CODE HERE ###
    response_objects = [x.properties for x in response.objects]
    return response_objects
```

Ожидаемое решение (по hint) — `collection.query.hybrid(query, alpha=alpha, limit=top_k)`.

Ожидаемый (Expected Output) для `hybrid_retrieve('Tell me about the last Taylor Swift show', collection, top_k=2)` — один chunk про Killer Mike (`chunk_index: 4`) и один chunk про Taylor Swift/Wembley (`chunk_index: 10`) — то есть объединение keyword- и vector-компонентов даёт смешанный результат из результатов BM25 и semantic search.

Тест: `unittests.test_hybrid_retrieve(hybrid_retrieve, client)`.

#### Reranking — Exercise 5

```python
def semantic_search_with_reranking(query: str,
                                   rerank_property: str,
                                   collection: "weaviate.collections.collection.sync.Collection",
                                   rerank_query: str = None,
                                   top_k: int = 5
                                   ) -> list:
    ### START CODE HERE ###
    if rerank_query is None:
        rerank_query = query
    reranker = None
    response = None
    ### END CODE HERE ###
    response_objects = [x.properties for x in response.objects]
    return response_objects
```

По докстрингу и hint-ам ожидаемое решение: создать `reranker = Rerank(query=rerank_query, prop=rerank_property)` и вызвать `collection.query.near_text(query, limit=top_k, rerank=reranker)`.

Markdown поясняет: reranker-модель принимает запрос и пассаж (в данном случае — chunk результата), чтобы вычислить оценку сходства (similarity score).

Пример вызова: `semantic_search_with_reranking(query='Tell me about the conflicts in Latin America', collection=collection, top_k=2, rerank_property='chunk')`.

Ожидаемый (Expected Results) вывод — два chunk: о дипломатическом конфликте Испания–Аргентина из-за обвинения в употреблении наркотиков (*«Spain-Argentina row over drug-use accusation»*) и о протестах в Венесуэле по поводу оспариваемых результатов выборов (*«Protests across Venezuela as election dispute goes on»*).

Тест: `unittests.test_semantic_search_with_reranking(semantic_search_with_reranking, client)`.

### 4. Встраивание Weaviate API в предыдущую схему (без грейдинга)

#### 4.1 `generate_final_prompt(query, top_k, retrieve_function, rerank_query=None, rerank_property=None, use_rerank=False, use_rag=True)`

Функция аналогична `generate_final_prompt` из задания Module 2, но адаптирована под Weaviate:

1. если `use_rag=False` — возвращает исходный `query`;
2. если `use_rerank=True` — требует, чтобы был передан `rerank_property` (иначе `raise ValueError`), и вызывает `retrieve_function(query=query, top_k=top_k, collection=collection, rerank_property=rerank_property, rerank_query=rerank_query)`;
3. иначе — вызывает `retrieve_function(query=query, top_k=top_k, collection=collection)`;
4. форматирует каждый найденный документ в строку `Title: ..., Chunk: ..., Published at: ...\nURL: ...` (используется поле `chunk`, а не `description`, как в предыдущих заданиях);
5. собирает финальный промпт с инструкцией использовать «2024 News» как часть общих знаний модели, дополнительно отмечая, что новостные данные упорядочены по релевантности (*«The news data is ordered by relevance.»*).

Пример: `generate_final_prompt("Tell me the economic situation of the US in 2024.", top_k=5, retrieve_function=semantic_search_retrieve, use_rerank=False, rerank_property='title')` — печатается собранный промпт (без явно приведённого текста в сохранённом notebook, так как сама переменная `collection` внутри функции берётся из внешней области видимости, а не из параметров — это видно из тела функции, где `retrieve_function(..., collection=collection, ...)` использует глобальную переменную `collection`, а не аргумент функции).

#### 4.2 `llm_call(query, retrieve_function=None, top_k=5, use_rag=True, use_rerank=False, rerank_property=None, rerank_query=None)`

Вызывает `generate_final_prompt(...)`, передаёт результат в `generate_with_single_input(PROMPT)`, возвращает `generated_response['content']`.

Демонстрационный вызов:

```python
query = "Tell me about United States and Brazil's relationship over the course of 2024. Provide links for the resources you use in the answer."
print(llm_call(query=query, top_k=5, retrieve_function=hybrid_retrieve))
```

### 5. Эксперименты с RAG-системой

```python
display_widget(llm_call, semantic_search_retrieve, bm25_retrieve, hybrid_retrieve, semantic_search_with_reranking)
```

Markdown поясняет: виджет позволяет ввести запрос, выбрать rerank property и вывести пять разных ответов LLM: (1) с semantic search, (2) с semantic search и reranking, (3) с BM25 search, (4) с hybrid search, (5) без RAG.

### Helper-файл `utils.py`

По структуре в основном совпадает с `utils.py` из ungraded labs модуля (`print_object_properties` с сортировкой ключей, `generate_embedding`, `print_properties`), но с отличиями:

- **`generate_with_single_input` / `generate_with_multiple_input`** — модель по умолчанию здесь `"meta-llama/Llama-3.2-3B-Instruct-Turbo"` (отличается от `"Qwen/Qwen3.5-9B"` в ungraded labs и от `"meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"` в задании Module 2); в payload не отключается reasoning (`reasoning: {"enabled": False}` здесь не устанавливается); proxy-URL зашит напрямую как `'https://proxy.dlai.link/coursera_proxy/together'`.
- **`display_widget(llm_call_func, semantic_search_retrieve, bm25_retrieve, hybrid_retrieve, semantic_search_with_reranking)`** — здесь эта функция уже полностью используется в самом assignment-notebook (в отличие от одноимённой функции в `utils.py` ungraded_lab_2, которая там не вызывалась). Строит виджет с пятью колонками результатов (`Semantic Search`, `Semantic Search with Reranking`, `BM25 Search`, `Hybrid Search`, `Without RAG`), полем запроса с предзаполненным примером про отношения США и Бразилии в 2024 году, слайдером `Top K` и выпадающим списком `Rerank Property` (`title`/`chunk`); по нажатию кнопки `Get Responses` вызывает `llm_call_func` для каждой из пяти конфигураций и отображает результаты через `display(Markdown(response))`.

### Файл `weaviate_server.py`

Отдельный модуль, который при импорте (на уровне модуля, вне какой-либо функции) сразу устанавливает соединение с embedded Weaviate:

```python
with suppress_subprocess_output():
    client = weaviate.connect_to_embedded(
        persistence_data_path=os.environ["COLLECTIONS_PATH"],
        environment_variables={
            "ENABLE_API_BASED_MODULES": "true",
            "ENABLE_MODULES": 'text2vec-transformers,reranker-transformers',
            "TRANSFORMERS_INFERENCE_API": "http://127.0.0.1:5000/",
            "RERANKER_INFERENCE_API": "http://127.0.0.1:5000/"
        }
    )
```

Содержит собственную копию контекстного менеджера `suppress_subprocess_output()` (идентичную версиям из `utils.py` других лабораторных работ). Требует переменную окружения `COLLECTIONS_PATH`, указывающую путь к персистентному хранилищу коллекций Weaviate (именно там, судя по всему, заранее подготовлена и провекторизована коллекция `bbc_collection`, которую notebook затем подключает через `client.collections.get("bbc_collection")`).

### Файл `flask_app.py`

Практически идентичен `flask_app.py` из `ungraded_lab_1` модуля: поднимает Flask-сервер на порту 5000 с эндпоинтами `GET /.well-known/ready`, `GET /meta`, `POST /rerank` (реранкинг через `FlagReranker('BAAI/bge-reranker-base', cache_dir='.models/', use_fp16=True)` — здесь `use_fp16=True`, тогда как в `ungraded_lab_1` было `use_fp16=False`, и `cache_dir` задан как константа `'.models/'`, а не через переменную окружения `MODEL_M3`) и `POST /vectors` (векторизация через `generate_embedding` из `utils.py`). Запускается в отдельном потоке при импорте модуля.

### Helper-файл `unittests.py`

Импортирует `test_case`, `print_feedback` из `dlai_grader.grading`, `FunctionType`, `numpy`. Содержит вспомогательные функции `check_object` и `check_object_equal`, проверяющие, что указанное свойство присутствует в объекте и содержит (либо точно равно) ожидаемому значению.

- **`test_filter_by_metadata`** — для свойств `title` (эталонные значения `['US', 'China']`) и `chunk` (`['Brazil', 'France']`) вызывает функцию с разными `limit`, проверяет отсутствие исключений, правильную длину результата и то, что каждый возвращённый объект действительно содержит соответствующее эталонное значение в нужном свойстве.
- **`test_semantic_search_retrieve`** — для запросов `"Conflicts in France"` (ожидается `title == "After France's election shock comes the real power struggle"`) и `"Famous actor marries"` (ожидается `title == "Sandi Toksvig officiates wedding of Abba's Björn Ulvaeus"`) проверяет длину результата и точное совпадение `title`.
- **`test_bm25_retrieve`** — для тех же двух запросов, но с другими ожидаемыми `title`: `"D-Day remembrance planes will be found, says Shapps"` и `"Media tycoon Rupert Murdoch marries for fifth time"` — то есть у BM25 и semantic search разные «правильные» результаты для одинаковых запросов, что подтверждает разницу в механике этих техник поиска.
- **`test_hybrid_retrieve`** — для запроса `"Conflicts in France"` ожидается `title == "Whistles and boos at France-Israel football match"` (дважды, `top_k=2`); для `"Famous actor marries"` ожидается список из трёх `title` (`top_k=3`), включая `"Media tycoon Rupert Murdoch marries for fifth time"` (дважды) и `"Lana Del Rey reportedly marries alligator tour guide in Louisiana "`; сравнение точное, поэлементное (`zip`), то есть проверяется не только состав, но и порядок результатов.
- **`test_semantic_search_with_reranking`** — для тестового запроса `"This is a test query"` с `rerank_query="This is a test rerank query"`, `rerank_property='chunk'`, `top_k=5` ожидается точный список из пяти заголовков в конкретном порядке: *«The Papers: Israel's 'tragic error' and Labour's 'pro-building' bid»*, *«MoT boss says 72-day wait for test is new normal»*, *«Pour a proper pint, Trading Standards tells pubs»*, *«Our interactive guide to the latest voting trends»*, *«Tories need a Budget bounce but can Hunt deliver?»*.

### Ограничения и предпосылки

Для полного выполнения notebook требуются: локальный файл `data/bbc_data.joblib` (75 256 статей BBC News с полями `title`, `pubDate`, `guid`, `link`, `description`, `article_content`, `chunk`, `chunk_index`); заранее подготовленная и провекторизованная коллекция `bbc_collection` в персистентном хранилище Weaviate по пути, заданному переменной окружения `COLLECTIONS_PATH`; свободные локальные порты для embedded Weaviate (`8079`/`50050` со стороны клиента) и для Flask-инференс-сервера (`5000`); установленные зависимости `weaviate-client`, `joblib`, `flask`, `httpx`, `openai`, `FlagEmbedding`, `torch`, `together`, `ipywidgets`, а для тестов — `dlai_grader`. Для вызовов LLM нужен доступ к Together.ai или прокси-серверу Coursera. В README.md отдельно указано, что Weaviate-сервер должен быть запущен для работы задания и что датасет уже прочанкован и провекторизован. В рамках конспекта код изучался статически, без запуска notebook, Flask/Weaviate-серверов или отдельных ячеек и без попытки самостоятельно исправить или решить graded-упражнения.