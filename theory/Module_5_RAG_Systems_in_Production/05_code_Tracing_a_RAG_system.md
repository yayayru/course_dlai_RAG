practice\Module5\ungraded_labs\ungraded_lab_1\C1M5_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение

Ноутбук `C1M5_Ungraded_Lab_1.ipynb` (в репозитории фактически находится по пути `practice/Module5/ungraded_labs/ungraded_labs_1/C1M5_Ungraded_Lab_1.ipynb`) — необязательная (`ungraded`) лабораторная работа на тему трассировки и оценки RAG-системы с использованием `Weaviate` и `Phoenix`. Задачи ноутбука:

- понять, как настраивать и использовать телеметрию (`telemetry`) для мониторинга RAG-системы;
- изучить `traces` и `spans`;
- исследовать trace, чтобы увидеть полный путь и взаимодействия внутри процессов системы;
- использовать инструмент `Phoenix Arize` (https://phoenix.arize.com/) для визуализации и анализа данных телеметрии;
- увидеть небольшой RAG pipeline в действии с использованием Phoenix и Weaviate.

### Ключевые импорты и зависимости

- `utils` — локальный вспомогательный модуль (см. ниже).
- `opentelemetry` — библиотека `trace`, `Resource` (из `opentelemetry.sdk.resources`), `Status`/`StatusCode` (из `opentelemetry.trace`), `TracerProvider` (из `opentelemetry.sdk.trace`), `ConsoleSpanExporter`/`SimpleSpanProcessor` (из `opentelemetry.sdk.trace.export`).
- `phoenix as px` и `phoenix.otel.register` — библиотека Phoenix для наблюдаемости.
- `weaviate` — клиент vector database.
- `httpx`, `openai.OpenAI`/`DefaultHttpxClient` — для вызова LLM через OpenAI-совместимый клиент (Together.ai OpenAI-совместим).

### Раздел 2 — Quick Introduction on Telemetry (Spans)

`Span` в телеметрии представляет одну операцию или задачу внутри системы — снимок конкретного действия, фиксирующий, когда оно начинается и заканчивается. Spans также включают детали о том, что делает задача, и любые важные события.

Демонстрируется настройка простого локального (не глобального) `tracer` через `OpenTelemetry` — это сделано намеренно локально, чтобы продемонстрировать концепции OpenTelemetry, не мешая tracer provider Phoenix, который будет использован позже:

- `resource = Resource(attributes={"service.name": "Test Service"})` — описывает приложение.
- `local_tracer_provider = TracerProvider(resource=resource)` — локальный tracer provider.
- `console_exporter = ConsoleSpanExporter()` — выводит spans в консоль (для демонстрации; в реальности использовался бы OTLP-экспортёр).
- `span_processor = SimpleSpanProcessor(console_exporter)` — отправляет каждый span в экспортёр сразу по завершении.
- `tracer = local_tracer_provider.get_tracer(__name__)`.

#### 2.1.1 Игрушечная функция retrieve

Функция `retrieve(query, fail=False)` иллюстрирует настройку трассировки через spans для операции извлечения документов: внутри `with tracer.start_as_current_span("retrieving_documents") as span:` логируется событие начала извлечения (`span.add_event("Starting retrieve")`), записывается входной запрос как атрибут (`span.set_attribute("input.query", query)`), симулируется список из трёх извлечённых документов (`retrieved doc1/2/3`) с атрибутами id/content/metadata для каждого. При `fail=True` выбрасывается `ValueError`, статус span устанавливается в `Status(StatusCode.ERROR, ...)` с атрибутами `error.type`/`error.message`, исключение перевыбрасывается. При успехе статус — `Status(StatusCode.OK)`.

Вызов `retrieve("Test")` выводит в консоль полный JSON span с полями `trace_id`, `span_id`, `start_time`/`end_time`, `status`, `attributes`, `events`, `resource` — демонстрируя структуру одного span.

### 2.2 Traces

`Trace` — коллекция spans, представляющая путь запроса или транзакции по мере прохождения через различные компоненты системы (набор spans, относящихся к одной задаче).

Строится игрушечный RAG pipeline из четырёх трассируемых функций (каждая оборачивает свою логику в собственный `tracer.start_as_current_span`):

- `format_documents(retrieved_docs)` — span `call_format_documents`, логирует событие для каждого обработанного документа, записывает атрибут `input.documents_count`.
- `augment_prompt(query, formatted_documents)` — span `augment_prompt`, строит `PROMPT = f"Answer the query: {query}.\nRelevant documents:\n{formatted_documents}"`.
- `generate(prompt)` — span `generate`, симулирует генерацию текста строкой `f"Generated text for prompt {prompt}"` (без реального вызова LLM).
- `rag_pipeline(query, fail=False)` — span `rag_pipeline`, последовательно вызывает `retrieve` → `format_documents` → `augment_prompt` → `generate`; при исключении на любом шаге статус верхнего span устанавливается в `ERROR`, исключение перевыбрасывается.

Демонстрация:

- **Trace example 1** (`fail=False`): вывод в консоль полного дерева spans (`retrieving_documents`, `call_format_documents`, ...) с общим `trace_id` и `parent_id`, указывающим на родительский `rag_pipeline` span — статус всех spans `OK`.
- **Trace example 2** (`fail=True`): вывод показывает span `retrieving_documents` со статусом `ERROR`, описанием `"ValueError: Retrieve failed for query: This is a test query"`, событием `exception` с полным `exception.stacktrace`, а затем span `rag_pipeline`, также помёченный ошибкой. Отмечается (markdown-ячейка), что эта вторая трассировка намеренно завершилась неудачей, чтобы показать, как это могло бы выглядеть в production-системе.

Комментарий ноутбука: трассировки могут стать довольно сложными и трудночитаемыми в сыром виде, особенно в крупных системах со множеством взаимосвязанных компонентов — поэтому важны инструменты вроде Phoenix, которые помогают управлять трассировками и визуализировать их.

### Раздел 3 — Telemetry Using Phoenix

Phoenix — мощный инструмент, упрощающий управление и визуализацию данных телеметрии, помогающий обрабатывать сложные трассировки для анализа и диагностики проблем.

#### 3.1 Запуск Phoenix App

`utils.make_url()` выводит URL для доступа к UI Phoenix (учитывая ограничения окружения Coursera, предоставляется альтернативная ссылка), `px.launch_app()` запускает локальный сервер и хостит UI (по умолчанию `localhost:6006`). В выводе видна ссылка вида `https://s172-29-11-144p6006.lab-aws-production.deeplearning.ai`.

#### 3.2 Подготовка телеметрии

Поскольку Phoenix тоже использует OpenTelemetry, настройка очень похожа на показанную выше:

```python
from phoenix.otel import register
phoenix_project_name = "example-rag-pipeline"
endpoint = "http://127.0.0.1:6006/v1/traces"
tracer_provider_phoenix = register(project_name=phoenix_project_name, endpoint=endpoint)
tracer = tracer_provider_phoenix.get_tracer(__name__)
```

В выводе отображается блок «🔭 OpenTelemetry Tracing Details 🔭» с деталями: имя проекта Phoenix, тип span processor (`SimpleSpanProcessor`), endpoint коллектора, транспорт (`HTTP + protobuf`), а также предупреждение, что в production рекомендуется использовать `BatchSpanProcessor`, и что `register` устанавливает данный tracer provider как глобальный OpenTelemetry по умолчанию.

#### 3.3 Working the Pipeline (Retrieve)

Функция `retrieve` переписывается с двумя отличиями от предыдущей версии: передаётся `openinference_span_kind='retriever'` в `tracer.start_as_current_span`, и вместо `set_attribute("input.query", ...)` используется `span.set_input(query)` — специфичный для Phoenix метод.

#### 3.4 Chains

`Chain` — точка соединения между разными шагами в LLM-приложении, связывающая операции вроде старта запроса или передачи информации от `retriever` к вызову LLM.

Остальные функции RAG-пайплайна (`format_documents`, `augment_prompt`, `generate`, `rag_pipeline`) переписываются с декоратором `@tracer.chain` — достаточно добавить его перед функцией, чтобы она была добавлена как chain, без ручной работы со spans внутри.

#### 3.5 Using the UI to analyze the traces

Запускаются два запроса — `rag_pipeline("This is a test query")` и `rag_pipeline("This is a test query that failed", fail=True)` (второй — в `try/except`), затем `utils.make_url()` снова выводит ссылку на UI, где можно проинспектировать обе трассировки в организованном виде.

Далее вызывается `utils.restart_kernel()` — перезапуск ядра для демонстрации свежей настройки Phoenix с включённым `auto_instrument`, показывая две разные конфигурации Phoenix: базовая трассировка (предыдущий раздел) и автоматическая трассировка вызовов OpenAI (следующий раздел). Отмечается, что в production обычно настраивают Phoenix один раз при старте приложения.

### Раздел 4 — Tracing and Evaluation with Weaviate

Реализуется более конкретный сценарий: берутся FAQ-вопросы из задания модуля 4 и строится небольшой RAG pipeline для ответа на FAQ-вопрос для магазина одежды.

#### Настройка

```python
utils.kill_processes_on_ports([5000, 8080, 8097, 50050, 50051])
import flask_app
import weaviate_server
```

Комментарий предупреждает, что повторный запуск этой ячейки может убить активное ядро. В выводе видна ошибка кэширования файла модели (`Could not cache non-existence of file... Read-only file system`) — не мешает работе — и строки запуска Flask-приложения.

`utils.cleanup_phoenix_projects()` очищает существующие сессии Phoenix для решения конфликтов ID проектов, затем `px.launch_app()` перезапускает сессию.

#### 4.1 Configuring the tracer

Новый аргумент `auto_instrument=True` при вызове `register(...)` автоматически трассирует OpenAI-совместимые вызовы LLM (Together.ai OpenAI-совместим). Используется динамически сгенерированное имя проекта `f"example-rag-pipeline-with-weaviate-{int(time.time())}"` во избежание конфликтов.

#### 4.2 Preparing the Weaviate client and collection

```python
client = weaviate.connect_to_local(port=8079, grpc_port=50050)
utils.setup_faq_collection()
```

`utils.setup_faq_collection()` (описана в `utils.py`) подключается к Weaviate, проверяет существование коллекции `Faq`, при отсутствии создаёт её со свойствами `question`/`answer`/`type` (тип `TEXT`) и `vectorizer_config=Configure.Vectorizer.text2vec_transformers()`, загружает данные из `faq.joblib` и вставляет их через `collection.data.insert_many(faq_data)`. В выводе: `Successfully created FAQ collection with 25 items`.

Далее данные также загружаются напрямую через `joblib.load("faq.joblib")` для инспекции (`data[0]` показывает структуру `{'question': ..., 'answer': ..., 'type': 'general information'}`), коллекция загружается через `client.collections.get("Faq")`, `len(collection)` → `25`.

#### 4.3 The Retriever

Функция `retrieve(query_text, limit=5)` создаёт span `query_weaviate` с `openinference_span_kind="retriever"`, вызывает `span.set_input(query_text)`, выполняет `chunks.query.near_text(query=query_text, limit=limit)` на коллекции `Faq`, и для каждого найденного документа записывает атрибуты `retrieval.documents.{i}.document.id/metadata/content`.

#### 4.4 LLM call with openai library

Поскольку Phoenix интегрируется с OpenAI-подобными системами, а Together.ai OpenAI-совместим, используется `openai.OpenAI`-клиент с кастомным `httpx`-транспортом, обходящим проверку SSL:

```python
transport = httpx.HTTPTransport(local_address="0.0.0.0", verify=False)
http_client = DefaultHttpxClient(transport=transport, headers=utils.get_proxy_headers())
llm_client = OpenAI(api_key=utils.get_together_key(), base_url=utils.get_proxy_url(), http_client=http_client)
```

Определяются вспомогательные функции:

- `format_context(results)` (декорирована `@tracer.chain`) — форматирует найденные FAQ-объекты в текст вида `Question: ... \nAnswer: ...\n`.
- `create_prompt(query_text, context)` (декорирована `@tracer.chain`) — строит промпт `f"Based on the following information, please answer the FAQ related question: \"{query_text}\"\n\nRelevant FAQ (ordered by relevance):\n{context}\n"`.
- `query_openai(prompt)` — вызывает `llm_client.chat.completions.create(model="Qwen/Qwen3.5-9B", extra_body={"reasoning": False}, messages=[{"role": "system", "content": "You are a helpful assistant from a customer support."}, {"role": "user", "content": prompt}])`. Комментарий отмечает, что трассировать вручную не нужно, так как `auto_instrument=True`.
- `rag_pipeline(query)` (декорирована `@tracer.chain`) — объединяет `retrieve` → `format_context` → `create_prompt` → `query_openai`.

Демонстрация:

- `rag_pipeline("Can I get a refund or exchange for another shirt?")` → развёрнутый ответ про условия возврата (30 дней, Returns Center, исключение для sale-товаров, доставка).
- `rag_pipeline("What are your working hours?")` → «Our online store is open 24/7. However, our customer service team is available from 9:00 AM to 6:00 PM, Monday through Friday.»

Финальный вызов `utils.make_url()` предлагает проверить трассировки в UI Phoenix.

### Вспомогательный файл `utils.py`

Ключевые функции: `kill_processes_on_ports(ports, ...)` — находит и завершает процессы, слушающие указанные порты (через `psutil`); `get_proxy_url()`/`get_proxy_headers()`/`get_together_key()` — получение URL прокси DLAI/Together и заголовков авторизации из переменных окружения; `make_url(endpoint=None)` — генерирует ссылку на UI Phoenix в зависимости от платформы (Coursera через `WORKSPACE_ID`, Learning Platform через `HOSTNAME`/`REV_PROXY_BASE_DOMAIN`, либо `localhost:6006` локально); `restart_kernel()` — принудительный перезапуск ядра через `os._exit(00)`; `generate_with_single_input(...)` — вызов LLM (аналогично предыдущим модулям, но добавлено поле `total_tokens` в возвращаемый словарь); `generate_embedding(prompt)` — использует локальную модель `SentenceTransformer("BAAI/bge-base-en-v1.5", cache_folder=".models")` (метод `model.encode(prompt).tolist()`), в отличие от предыдущих модулей, где эмбеддинг генерировался через API; `cleanup_phoenix_projects()` — закрывает активные сессии Phoenix (`px.close_app()`) для избежания конфликтов ID проектов; `setup_faq_collection()` — создаёт (если не существует) коллекцию `Faq` в Weaviate и загружает в неё данные из `faq.joblib`.

### Вспомогательные файлы `weaviate_server.py` и `flask_app.py`

- `weaviate_server.py` — при импорте подключает embedded Weaviate-клиент через `weaviate.connect_to_embedded(persistence_data_path="./.collections", environment_variables={"ENABLE_API_BASED_MODULES": "true", "ENABLE_MODULES": "text2vec-transformers", "TRANSFORMERS_INFERENCE_API": "http://127.0.0.1:5000/"})`, используя `suppress_subprocess_output()` (context manager, подавляющий stdout/stderr subprocess-вызовов).
- `flask_app.py` — поднимает Flask-приложение на порту 5000 с эндпоинтами `/.well-known/ready`, `/meta` (readiness checks) и `/vectors` (POST) — принимает текст, вызывает `generate_embedding` из `utils.py` и возвращает `{'vector': embeddings}`; запускается в отдельном потоке (`threading.Thread(target=run_app).start()`).

### Ограничения и предпосылки

- Требуется установленные пакеты `opentelemetry`, `phoenix` (Arize Phoenix), `weaviate`, `openai`, `httpx`.
- Для вызовов LLM требуется доступ к прокси DLAI (через `utils.get_proxy_url()`) либо `TOGETHER_API_KEY` в окружении; используемая модель — `Qwen/Qwen3.5-9B`.
- Для эмбеддингов требуется локальная модель `BAAI/bge-base-en-v1.5` (через `sentence-transformers`), загружаемая в `.models`.
- Требуется запущенный локальный Weaviate (порт `8079`, gRPC `50050`) и Flask-сервис на порту 5000 (`flask_app.py`), а также свободные порты `8080`, `8097`, `50051`.
- UI Phoenix доступен по адресу `localhost:6006` либо через специальную ссылку, формируемую `utils.make_url()` в зависимости от платформы (Coursera/Learning Platform/локально).
- Раздел 5, упомянутый в оглавлении ноутбука («5 - Evaluating a RAG system»), не содержит отдельных ячеек с этим заголовком в изученной версии ноутбука — после раздела 4.4 сразу следует финальная markdown-ячейка с поздравлением.
