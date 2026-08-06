practice\Module3\ungraded_labs\ungraded_lab_1\C1M3_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение notebook

`C1M3_Ungraded_Lab_1.ipynb` («Ungraded Lab - Introduction to Weaviate API») даёт практическое введение в [Weaviate API](https://weaviate.io/) — vector database, используемую в курсе. Согласно вводной ячейке, лабораторная работа готовит к предстоящему графируемому заданию: показывает, как работает Weaviate, что она умеет и как максимально эффективно использовать её возможности.

Оглавление notebook:

1. Introduction — Loading the necessary libraries, The Weaviate Client.
2. Configuring the database — Creating a Collection, Configuring the Vectorizer, The Properties, Adding elements into a Collection.
3. Querying on a collection — Filters, Semantic Search, BM25 search, Hybrid Search, Reranking.

### Импорты и зависимости

```python
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import Filter
from typing import List
from tqdm import tqdm
import joblib
import weaviate
import re
from weaviate.util import generate_uuid5
from pprint import pprint
import os
```

Из `utils.py` импортируются `suppress_subprocess_output`, `generate_with_single_input`, `print_object_properties`, `kill_processes_on_ports`. Перед импортом `flask_app` вызывается `kill_processes_on_ports([5000, 8080, 8097, 50050, 50051])`, чтобы освободить порты, которые понадобятся локальному Flask-серверу и embedded-инстансу Weaviate (в комментарии кода — предупреждение, что повторный запуск этой ячейки может убить активное ядро notebook). Далее выполняется `import flask_app`, что на уровне импорта запускает Flask-приложение в отдельном потоке (см. ниже).

Visible output этой ячейки содержит служебное сообщение об ошибке кэширования файла (`Could not cache non-existence of file... Read-only file system`, которая игнорируется) и лог запуска Flask: `* Serving Flask app 'flask_app'`, `* Debug mode: off`.

### 1.2 Клиент Weaviate

Markdown поясняет: чтобы начать работу с Weaviate API, нужно запустить `client`. В этом курсе используется *embedded client* — способ использовать Weaviate внутри приложения без отдельного (standalone) запущенного инстанса Weaviate.

При первом запуске `Embedded Weaviate` создаётся файл хранения данных по пути, указанному в `persistence_data_path`; даже после закрытия клиента и остановки embedded-инстанса данные там сохраняются.

При создании клиента нужно передать embedding-модель для векторизации. Weaviate поддерживает разные модели через свои модули (например, для вызова моделей OpenAI); поскольку OpenAI — платный сервис, в лабораторной работе используется локальная модель.

Клиент создаётся так:

```python
with suppress_subprocess_output():
    client = weaviate.connect_to_embedded(
        persistence_data_path="./.collections",
        environment_variables={
            "ENABLE_API_BASED_MODULES": "true",
            "ENABLE_MODULES": 'text2vec-transformers, reranker-transformers',
            "TRANSFORMERS_INFERENCE_API": "http://127.0.0.1:5000/",
            "RERANKER_INFERENCE_API": "http://127.0.0.1:5000/"
        }
    )
```

`suppress_subprocess_output()` — контекстный менеджер из `utils.py`, подавляющий логи Weaviate. Параметры: `persistence_data_path` — путь, где создаются и сохраняются коллекции (персистентно, не удаляются при закрытии клиента); `environment_variables` — переменные, нужные для работы локального embedding-сервера, включая адреса `TRANSFORMERS_INFERENCE_API` и `RERANKER_INFERENCE_API`, указывающие на локальный Flask-сервер на порту 5000.

### 2. Настройка базы данных

#### 2.1 Создание коллекции

Раздел вводит центральный объект лабораторной и всего задания — `collection` (коллекция) — так Weaviate называет группу объектов данных, индексируемых для извлечения.

Датасет для примера — `data.joblib`, загружаемый через `joblib.load("data.joblib")`: набор мест для посещения (`place`) со свойствами `place, state, description, best_season_to_visit, attractions, budget, user_ratings, last_updated`. Пример первой записи, выведенной через `print_object_properties(data[0])`: `place: Grand Canyon`, `state: Arizona`, `description: A stunning canyon with vast vistas and incredible geology.`, `best_season_to_visit: Spring, Fall`, `attractions: South Rim, Havasu Falls, Skywalk`, `budget: Moderate`, `user_ratings: 4.8`, `last_updated: 2023-10-01T00:00:00Z`.

Ключевые параметры при создании коллекции: `name` — имя коллекции; `vectorizer_config` — список конфигураций векторизатора (можно передать несколько, чтобы векторизовать датапоинты разными embedding-моделями; в лабораторной используется только одна).

#### 2.2 Настройка векторизатора

Используется модель `text2vec_transformers`. В векторизуемые свойства (`source_properties`) включены: `place, state, description, best_season_to_visit, attractions, budget` — они конкатенируются друг с другом и затем векторизуются:

```python
vectorizer_config = [Configure.NamedVectors.text2vec_transformers(
    name="vector",
    source_properties=['place', 'state', 'description', 'best_season_to_visit', 'attractions', 'budget'],
    vectorize_collection_name=False,
    inference_url="http://127.0.0.1:5000",
)]
```

В markdown отмечено: при определении свойства можно решить, включать ли имя свойства в текст для векторизации — например, для `budget` имеет смысл включить название свойства, поскольку одно только слово «Moderate» не даёт достаточно информации о том, что оно означает.

#### 2.3 Properties (свойства)

Свойства (properties) каждого объекта коллекции задаются явно с типами данных:

```python
collection = client.collections.create(
    name='example_collection',
    vectorizer_config=vectorizer_config,
    reranker_config=Configure.Reranker.transformers(),
    properties=[
        Property(name="place", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="state", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="description", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="best_season_to_visit", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="attractions", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="budget", vectorize_property_name=True, data_type=DataType.TEXT),
        Property(name="user_ratings", data_type=DataType.NUMBER),
        Property(name="last_updated", data_type=DataType.DATE),
    ]
)
```

Перед созданием проверяется, существует ли коллекция (`client.collections.exists(...)`), и при необходимости она удаляется (`client.collections.delete(...)`), либо создание пропускается и коллекция просто загружается через `client.collections.get(...)`.

Visible output `print(collection)` показывает полную конфигурацию коллекции `Example_collection`: `inverted_index_config` с параметрами BM25 (`b: 0.75`, `k1: 1.2`), все восемь properties с их `vectorizer_configs`, `reranker_config` со значением `reranker-transformers`, а также `vector_config` с деталями `vector_index_config` (`distance_metric: "cosine"`, `ef_construction: 128`, `max_connections: 32` и другие параметры HNSW-индекса).

Попытка повторно создать уже существующую коллекцию приводит к исключению: *«Collection may not have been created properly.! Unexpected status code: 422... 'class name Example_collection already exists'»*. Полный список сохранённых коллекций можно получить через `client.collections.list_all().keys()` — visible output: `dict_keys(['Example_collection'])`.

#### 2.4 Добавление элементов в коллекцию

При добавлении элемента в фоне происходят два шага: (1) информация векторизуется согласно конфигурации коллекции; (2) обновляется HNSW-индекс для оптимизации поиска (это может занимать некоторое время и не видно напрямую).

Добавление выполняется через `collection.batch`, что даёт дополнительные возможности: контроль числа объектов на батч, обработку ошибок импорта, уменьшение числа отдельных сетевых вызовов. Каждому элементу присваивается `uuid`, сгенерированный из содержимого документа (`generate_uuid5(document)`), что предотвращает дублирование записей:

```python
with collection.batch.fixed_size(batch_size=1, concurrent_requests=1) as batch:
    for document in tqdm(data):
        uuid = generate_uuid5(document)
        batch.add_object(
            properties=document,
            uuid=uuid,
        )
```

Visible output — прогресс-бар `tqdm`: `100%|██████████| 20/20 [00:01<00:00, 11.75it/s]`. Проверка `len(collection)` — visible output: `20` (то есть в коллекции 20 объектов/векторов).

### 3. Запросы к коллекции

Markdown перечисляет возможные типы запросов: по метаданным, semantic search, BM25, с фильтрацией.

#### 3.1 Filters

Фильтры ограничивают поиск по критерию и обычно передаются как аргумент запроса. Пример:

```python
result = collection.query.fetch_objects(
    limit=2,
    filters=Filter.by_property('user_ratings').greater_or_equal(3.5)
)
```

Результат — объект `QueryReturn`, доступ к элементам — через `result.objects`; каждый элемент имеет `.properties` (словарь) и `.uuid`. Visible output показывает два объекта: `Hollywood` (California, user_ratings 4.2) и `Times Square` (New York, user_ratings 4.3), с полными свойствами каждого.

В курсе способ фильтрации — `.by_property`.

#### 3.2 Semantic Search

Semantic search выполняется через `.near_text`, которая векторизует переданный текстовый запрос и сравнивает его с векторами объектов коллекции:

```python
result = collection.query.near_text(
    query='I want suggestions to travel during Winter. I want cheap places.',
    limit=4
)
```

Visible output — 4 места: Times Square (Winter, Low), Glacier National Park (Summer, Moderate), Zion National Park (Spring/Fall, Moderate), Cape Cod (Summer, Moderate).

Показан пример с фильтром `Filter.by_property('budget').equal('Low')` — visible output: Times Square, Alcatraz Island, Gettysburg National Military Park, Statue of Liberty (все с `budget: Low`).

Также показан пример со списком допустимых значений через `.contains_any(['Low', 'Moderate'])` — visible output: Times Square, Glacier National Park, Zion National Park, Cape Cod.

#### 3.3 BM25 search

```python
result = collection.query.bm25(
    query='I want suggestions to travel during Winter. I want cheap places.',
    filters=Filter.by_property('budget').contains_any(['Low', 'Moderate']),
    limit=4
)
```

Visible output — только один результат: Times Square (Winter, Low) — то есть, в отличие от semantic search, BM25 возвращает единственный документ, поскольку остальные три из фильтра не совпадают по ключевым словам с запросом.

#### 3.4 Hybrid Search

Markdown отмечает, что это тот самый RRF-поиск, рассмотренный в лекциях; помимо стандартных параметров передаётся `alpha`, контролирующий долю BM25 в смешивании:

```python
result = collection.query.hybrid(
    query='I want suggestions to travel during Winter. I want cheap places.',
    filters=Filter.by_property('budget').contains_any(['Low', 'Moderate']),
    alpha=0.3,
    limit=4
)
```

Visible output — те же четыре места, что и в примере semantic search (Times Square, Glacier National Park, Zion National Park, Cape Cod).

#### 3.5 Reranking

Reranking выполняется передачей дополнительного аргумента `rerank` в запрос:

```python
from weaviate.classes.query import Rerank

response = collection.query.near_text(
    query="'I want suggestions to travel during Winter. I want cheap and fun places.'",
    limit=5,
    rerank=Rerank(
        prop="attractions",
        query="Fun places"
    )
)
```

`Rerank` принимает `prop` — свойство, по которому выполняется reranking, и опциональный `query` — если не передан, используется исходный запрос. (Отдельная ячейка, выводящая свойства объектов после этого запроса, в notebook по факту печатает `result` из предыдущего hybrid-запроса, а не `response` из reranking-запроса — это видно из идентичности выведенных мест с примером из раздела Hybrid Search; никаких новых мест `response` не показывается.)

В конце клиент закрывается: `client.close()` — с комментарием в коде «Don't forget to close the client!».

### Helper-файл `utils.py`

Ключевые функции:

- **`kill_processes_on_ports(ports, ...)`** — через `psutil` находит и завершает (сначала `terminate()`, затем при необходимости `kill()`) процессы, слушающие указанные TCP/UDP-порты; возвращает подробный словарь с результатами (`pids_targeted`, `terminated`, `killed`, `errors`, `ports_with_no_match`).
- **`get_proxy_url()`, `get_proxy_headers()`, `get_together_key()`** — аналогичны версиям из предыдущих модулей курса, читают `TOGETHER_BASE_URL`/`TOGETHER_API_KEY` из окружения.
- **`generate_embedding(prompt)`** — в текущей реализации сразу возвращает `model.encode(prompt).tolist()` (используя глобальную `SentenceTransformer`-модель `BAAI/bge-base-en-v1.5`, загруженную в `flask_app.py` — см. ниже); код ниже этой строки (вызов через OpenAI-совместимый клиент или Together) фактически недостижим (`return` обрывает выполнение раньше).
- **`generate_with_single_input(...)` / `generate_with_multiple_input(...)`** — по структуре аналогичны версиям из предыдущих модулей: формируют payload с `model` (по умолчанию `"Qwen/Qwen3.5-9B"`), `messages`, `top_p`, `temperature`, `max_tokens`, `reasoning: {"enabled": False}`; при отсутствии `TOGETHER_API_KEY` обращаются к прокси `https://proxy.dlai.link/coursera_proxy/together`, иначе — напрямую к `Together`.
- **`print_object_properties(obj)`** — печатает свойства объекта (или списка объектов), усекая длинные текстовые поля (`article_content`, `main_vector`, `chunk`) до первых 100 (или 30 для `main_vector`) символов с пометкой `...(truncated)`.
- **`print_properties(item)`** — печатает `item.properties` как отформатированный JSON (`json.dumps(..., indent=2, sort_keys=True, default=str)`).
- **`suppress_subprocess_output()`** — контекстный менеджер, временно подменяющий `subprocess.Popen`, чтобы перенаправлять `stdout`/`stderr` дочерних процессов в `DEVNULL` (используется при запуске embedded Weaviate, чтобы не засорять вывод notebook).

На уровне модуля `utils.py` загружается модель `SentenceTransformer("BAAI/bge-base-en-v1.5", cache_folder=".models")` и настраивается `httpx`-транспорт с отключённой проверкой SSL (`verify=False`) для обращений через прокси курса.

### Локальный Flask-сервер `flask_app.py`

`flask_app.py` поднимает локальный Flask-сервер, который эмулирует API-based модули Weaviate (`text2vec-transformers`, `reranker-transformers`), обращающиеся к `inference_url`/`RERANKER_INFERENCE_API`, указанным при подключении клиента.

Ключевые элементы:

- на уровне модуля загружается `reranker = FlagReranker('BAAI/bge-reranker-base', cache_dir=os.environ["MODEL_M3"], use_fp16=False)` — модель для reranking из библиотеки `FlagEmbedding`;
- Flask-приложение `app` регистрирует маршруты:
  - `GET /.well-known/ready` и `GET /meta` — служебные health-check эндпоинты, которые Weaviate использует, чтобы убедиться, что inference-сервер готов (`readiness_check` и `readiness_check_2`);
  - `POST /rerank` — принимает JSON с ключами `query` и `documents`, формирует пары `(query, doc)` для каждого документа, вычисляет оценки через `reranker.compute_score(compares)`, возвращает JSON вида `{"scores": [{"document": ..., "score": ...}, ...]}` — именно в этом формате их ожидает модуль `reranker-transformers` Weaviate; при пустом списке документов возвращает `{"scores": []}`; ошибки парсинга или неверный формат входных данных обрабатываются с кодами `400`/`500`;
  - `POST /vectors` — принимает текст (одну строку или структуру с ключом `text`), вызывает `generate_embedding(text)` из `utils.py` и возвращает `{"vector": embeddings}` — этот эндпоинт используется модулем `text2vec-transformers` для векторизации.
- логирование Flask (`werkzeug`) подавляется (`app.logger.disabled = True`, `log.setLevel(logging.ERROR)`), чтобы не засорять вывод notebook;
- сервер запускается в отдельном потоке при импорте модуля: `flask_thread = threading.Thread(target=run_app); flask_thread.start()`, где `run_app()` вызывает `app.run(host='0.0.0.0', port=5000, debug=False)`.

### Ограничения и предпосылки

Notebook требует локально установленных и импортируемых пакетов `weaviate-client`, `sentence-transformers`, `FlagEmbedding`, `torch`, `flask`, `joblib`, `tqdm`, `psutil`, `httpx`, `openai`, `together`. Для работы reranker-модели нужна переменная окружения `MODEL_M3` (путь кэша модели `BAAI/bge-reranker-base`); для embedding-модели в `utils.py` используется локальная папка кэша `.models`. Embedded Weaviate создаёт локальное хранилище данных по пути `./.collections` (сохраняется между запусками). Для работы notebook требуются свободные порты `5000, 8080, 8097, 50050, 50051` — их предварительно освобождает `kill_processes_on_ports(...)` (с явным предупреждением в коде, что повторный запуск этой ячейки может завершить активное ядро notebook). Опциональные вызовы LLM через `generate_with_single_input`/`generate_with_multiple_input` требуют доступа к Together.ai или прокси Coursera (`TOGETHER_API_KEY`), но в показанном коде самого notebook эти функции для вызова LLM не используются — лабораторная работа сфокусирована на CRUD-операциях и поиске в Weaviate. В рамках конспекта код изучался статически, без запуска notebook, Flask-сервера или отдельных ячеек.