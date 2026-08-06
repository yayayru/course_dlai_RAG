См. practice\Module5\Graded_Assignments\C1M5_Assignment.ipynb

## Конспект по коду

### Назначение

`C1M5_Assignment.ipynb` — финальное оцениваемое (graded) задание курса: «Improving a RAG System» для чат-бота **Fashion Forward Hub** (продолжение задания модуля 4). Задание фокусируется на трёх темах, заявленных во вводной ячейке:

1. **Cost Measurement** — оценка потенциальной стоимости работы RAG-приложения.
2. **Prompt Improvement** — улучшение промптов для ускорения ответов, при поиске баланса между временем, производительностью и стоимостью.
3. **Tracing System** — настройка системы для отслеживания входов и выходов при взаимодействии с RAG-системой (через Phoenix).

Ноутбук полностью решён — все 4 упражнения реализованы, юнит-тесты из вызванных проходят успешно.

### Ключевые импорты и настройка

- `json`, `weaviate.classes.query.Filter`, `weaviate`, `joblib`, `pandas` — стандартный набор для работы с данными и Weaviate.
- `flask_app`, `weaviate_server`, `unittests` — служебные модули; импорт `flask_app` запускает Flask-приложение (`* Serving Flask app 'flask_app'`).
- Из `utils` импортируются `ChatWidget`, `generate_with_single_input`, `parse_json_output`, `get_filter_by_metadata`, `generate_filters_from_query`, `process_and_print_query`, `print_properties`, `make_url`.
- Клиент Weaviate: `client = weaviate.connect_to_local(port=8079, grpc_port=50050)`.
- Телеметрия настраивается через `phoenix as px`, `phoenix.otel.register`, `opentelemetry.trace.Status`/`StatusCode` — аналогично ungraded lab 1 модуля 5.

### Раздел 1 — Introduction: Your Role at Fashion Forward Hub

Сюжетная вводная: чат-бот успешно снизил число звонков в поддержку и увеличил продажи, но привёл к двум новым проблемам — **растущим затратам** (нет системы мониторинга их источника) и **высоким временем ответа** для отдельных запросов. Задача — заняться этими проблемами, добавив мониторинг стоимости и времени ответа, и улучшив промпты для баланса стоимости, производительности и скорости.

#### 1.2 Loading the Weaviate client

Как и в задании модуля 4, база данных уже загружена — не требуется её самостоятельно наполнять.

#### 1.3 Preparing the Tracing with Phoenix

```python
phoenix_project_name = "chatbot"
tracer_provider_phoenix = register(project_name=phoenix_project_name, endpoint="http://127.0.0.1:6006/v1/traces")
tracer = tracer_provider_phoenix.get_tracer(__name__)
```

В отличие от ungraded lab модуля 5, здесь **не** используется `auto_instrument=True`, так как в модуле присутствуют LLM-вызовы, которые не должны трассироваться (примеры, вызовы внутри юнит-тестов и т.д.) — трассировка расставляется вручную через `tracer.start_as_current_span(...)` и декоратор `@tracer.chain`. Трассировка в этом задании явно отмечена как **необязательная для оценки** (`Don't worry, you won't be graded in the tracing part!`).

#### 1.4 (Optional) Setting model cost per token

Необязательный раздел: инструкция настроить в UI Phoenix (`/settings/models`) стоимость двух используемых моделей — `meta-llama/Llama-3.2-3B-Instruct-Turbo` и `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` — с иллюстративной (заведомо завышенной для наглядности) ценой **1000 USD** и **2000 USD** за миллион токенов соответственно (реальная цена для `Llama-3.2-3B-Instruct-Turbo` на together.ai — 0.08 USD за миллион токенов). Показаны скриншоты UI (`images/settings_1.png`, `images/create_model_1.png`, `images/create_model_2.png`).

### Раздел 2 — A Quick Recap on the Database Structure

Повтор структуры данных из модуля 4: **Products Database** (`joblib.load('dataset/clothes_json.joblib')`, поля `gender`, `masterCategory`, `subCategory`, `articleType`, `baseColour`, `season`, `year`, `usage`, `productDisplayName`, `price`, `product_id`) и **FAQ Database** (`joblib.load("dataset/faq.joblib")`, поля `question`/`answer`/`type`).

### Раздел 3 — Recap on LLM calls and new output

Функция `generate_with_single_input` теперь возвращает **полный объект OpenAI** (а не только `{'role', 'content'}`, как в модуле 4), содержащий поля `id`, `choices` (с `message.content`, `finish_reason`, `seed` и т.д.), `created`, `model`, `usage` (`prompt_tokens`, `completion_tokens`, `total_tokens`, `cached_tokens`) и `prompt`. Пример вызова `generate_with_single_input("What are the primary colors?")` показывает JSON-структуру ответа целиком; извлечение текста — через `result['choices'][0]['message']['content']`, извлечение числа токенов — через `result['usage']['total_tokens']`. Отмечается, что именно так устроен формат ответов OpenAI API.

#### 3.1 `generate_params_dict`

Идентична версии из модуля 4 (собирает `prompt`, `role`, `temperature`, `top_p`, `max_tokens`, `model` в словарь), но модель по умолчанию — `meta-llama/Llama-3.2-3B-Instruct-Turbo`.

### Раздел 4 — Improving task handling

#### Exercise 1 — `check_if_faq_or_product(query, simplified=False)`

Добавлены два новых требования по сравнению с версией модуля 4: (1) функция теперь возвращает также общее число использованных токенов (`total_tokens`, уже дано в шаблоне); (2) новый параметр `simplified` — при `True` используется **более короткий промпт**, который нужно написать самостоятельно.

**Требования к решению**: новый (`simplified=True`) промпт должен использовать **менее 180 токенов** и сохранять ту же точность классификации на тестовом наборе.

Реализованный `simplified`-промпт:
```
Classify this query for a clothing store as either FAQ or Product.
FAQ means general store questions (like refund policy, locations, contact info).
Product means questions about specific products, sizes, colors, or prices.
Return only 'FAQ' or 'Product'.

Query: {query}
```

Вызов LLM обёрнут в трассировку (`tracer.start_as_current_span("routing_faq_or_product", openinference_span_kind='tool')`, вложенный span `router_call` с `openinference_span_kind='llm'`, записывающий атрибуты `llm.token_count.prompt/completion/total`, `llm.model_name`, `llm.provider`). Есть постобработка: если в ответе LLM встречается `'faq'` (без учёта регистра) — метка `FAQ`, если `'product'` — `Product`, иначе `'undefined'`.

Тест `unittests.test_check_if_faq_or_product(check_if_faq_or_product)` — пройден (`All tests passed!`).

**Сравнение standard vs simplified** на 5 тестовых запросах (через `process_and_print_query` из `utils.py`) в выводе ноутбука:

| Запрос | Standard | Simplified |
|---|---|---|
| «What is your return policy?» | FAQ / 218 токенов | FAQ / 113 токенов |
| «Give me three examples of blue T-shirts...» | Product / 224 | **FAQ** (неверно) / 111 |
| «How can I contact the user support?» | FAQ / 220 | FAQ / 115 |
| «Do you have blue Dresses?» | Product / 218 | **FAQ** (неверно) / 105 |
| «Create a look suitable for a wedding party...» | Product / 224 | **FAQ** (неверно) / 111 |

Таким образом, в фактическом выводе ноутбука `simplified`-версия укладывается в лимит по токенам (все значения < 180), но **допускает 3 ошибки классификации из 5** демонстрационных запросов (путает Product с FAQ) — то есть визуально показанный результат расходится с требованием сохранить ту же точность классификации, хотя формальный юнит-тест (`test_check_if_faq_or_product`), запущенный на своём отдельном наборе примеров, отчитался об успехе.

#### 4.2 Answering a FAQ question — `generate_faq_layout` (не градируется)

Функция дана целиком (декорирована `@tracer.tool`) и форматирует список FAQ в текст `Question: ... Answer: ... Type: ...\n` для каждой записи (идентична версии модуля 4). Результат сохраняется в `faq_layout`.

#### 4.3 Querying on FAQ

Показано, что в модуле 4 весь FAQ добавлялся в промпт целиком, что резко увеличивает расход токенов и время выполнения — задание предлагает использовать более эффективную коллекцию Weaviate.

Данные FAQ загружаются в коллекцию `Faq` через batch-вставку:
```python
with faq_collection.batch.fixed_size(batch_size=20, concurrent_requests=5) as batch:
    for document in tqdm(faq):
        uuid = generate_uuid5(document['question'])
        batch.add_object(properties=document, uuid=uuid)
```
(в выводе: `100%|██████████| 25/25`). Демонстрация семантического поиска: `faq_collection.query.near_text("What is the return policy?", limit=5)` возвращает 5 релевантных FAQ-объектов про возвраты.

**Exercise 2 — `query_on_faq(query, simplified=False, **kwargs)`**: при `simplified=False` — используется весь `faq_layout` (как в модуле 4), промпт обёрнут в тег `<FAQ_ITEMS>`. При `simplified=True` требовалось реализовать: получить топ-5 наиболее релевантных FAQ через семантический поиск и использовать только их. Реализованный код:
```python
results = faq_collection.query.near_text(query=query, limit=5)
```
Далее результаты трассируются (span `retrieve_faq_questions`, `openinference_span_kind="retriever"`), конвертируются в список свойств, **разворачиваются в обратном порядке** (`results.reverse()`, чтобы наиболее релевантный элемент оказался ближе к концу промпта, то есть ближе к вопросу), формируется `faq_layout` через `generate_faq_layout(results)`. Используется другой промпт, поясняющий, что FAQ упорядочены по убыванию релевантности.

**Требование**: решение должно возвращать **менее 500 токенов** для приведённого тестового запроса.

Юнит-тест `unittests.test_query_on_faq(query_on_faq)` — пройден.

Демонстрация на запросе *«I received the dress I ordered but I don't like it. How can I return it?»*:
- Standard (`simplified=False`): промпт — 788 «слов» (подсчёт через `.split()`, не точный токенайзер), итоговый ответ LLM использует **1190** токенов.
- Simplified (`simplified=True`): промпт — 250 «слов», итоговый ответ использует **400** токенов — заметно меньше, при этом ответ по существу корректен (описывает процесс возврата через Returns Center).

#### 4.4 Improving the Decision Between Creative or Technical Product Queries

**Exercise 3 — `decide_task_nature(query, simplified=True)`**: аналогичная структура — при `not simplified` используется более длинный промпт из модуля 4 (шесть примеров), при `simplified` нужно написать более компактный промпт.

**Требования к решению**: точность **не ниже 80%** на тестовом наборе (допускается ошибиться максимум в одном вопросе из набора) и **менее 170 токенов** на **каждый** запрос.

Реализованный `simplified`-промпт:
```
Classify this query as either 'creative' or 'technical' for a clothing store.
Creative → making suggestions, composing outfits, generating new ideas.
Technical → asking about product details, availability, prices, or sizes.
Return only one word: creative or technical.

Query: {query}
```
Вызов LLM обёрнут в трассировку (span `decide_task_nature`, вложенный span `router_call`).

Юнит-тест `unittests.test_decide_task_nature(decide_task_nature)` — пройден.

Демонстрация на 5 запросах — все метки совпали с ожидаемыми, все значения токенов ниже 170 (диапазон 103–119):
- «Give me two sneakers with vibrant colors.» → technical / 103
- «What are the most expensive clothes...» → technical / 107
- «...suggestion on an accessory to match...» → creative / 113
- «Give me three trousers with vibrant colors...» → technical / 108
- «Create a look for a woman walking in a park...» → creative / 119

#### 4.5 Retrieving the parameters for a given task — `get_params_for_task(task)`

Функция дана целиком (не градируется в этом задании, декорирована `@tracer.tool`): `PARAMETERS_DICT = {"creative": {'top_p': 0.9, 'temperature': 1}, "technical": {'top_p': 0.7, 'temperature': 0.3}}`, возвращает соответствующий набор параметров по `task`, либо `{'top_p': 0.5, 'temperature': 1}` по умолчанию. В отличие от модуля 4 (где параметры технической/творческой задачи были другими — `0.4/0.4` и `0.8/1.5`), здесь значения изменены. В `unittests.py` для этой функции присутствует тест `test_get_params_for_task`, однако в изученной версии ноутбука вызов этого теста **не встречается** — юнит-тест определён, но не запускается ни в одной ячейке.

### Раздел 5 — Retrieving Items Based on Metadata from a Query

Повторяется трёхшаговый процесс из модуля 4 (генерация JSON-метаданных → семантический поиск с фильтрами → возврат результатов), с указанием тех же шести категорий метаданных (`gender`, `masterCategory`, `articleType`, `baseColour`, `season`, `usage`).

#### 5.1 `generate_metadata_from_query(query)` — дана целиком

Промпт идентичен по структуре модулю 4, но обёрнут в трассировку (span `generate_metadata_from_query`, вложенный `llm_call`) и теперь возвращает пару `(content, total_tokens)`.

Демонстрация: запрос про мужской образ для солнечного дня в парке (бюджет до 300$) → JSON `{"gender": ["Men"], "masterCategory": ["Apparel"], "articleType": ["Shirts", "Shorts", "Sweaters", "Socks"], "baseColour": ["Yellow", "Orange", "Green", "Nude"], "price": {"min": 0, "max": 300}, "usage": ["Casual", "Travel"], "season": ["Summer"]}`, при этом **`total_tokens = 1464`** — комментарий в markdown отмечает, что «до сих пор каждый product-запрос обрабатывал около 1500 токенов — в основном из-за генерации фильтров по множеству категорий перед поиском».

**Ключевое архитектурное решение задания**: вместо детальной генерации метаданных-фильтров предлагается **упростить** процесс — просто выполнять семантический поиск напрямую по запросу пользователя, без генерации метаданных вообще (быстрее, дешевле по токенам, по-прежнему эффективно для большинства запросов).

#### 5.2 Loading the Weaviate Product Collection

`products_collection = client.collections.get('products')`, `len(products_collection)` → **44423**.

#### 5.3 Filtering by Metadata

Функции `parse_json_output(llm_output)` и `get_filter_by_metadata(json_output)` **перенесены в `utils.py`** и здесь показаны лишь для справки (идентичны версиям из модуля 4: очистка JSON-строки, построение списка `Filter` по валидным ключам `gender`/`masterCategory`/`articleType`/`baseColour`/`price`/`usage`/`season`, с особой обработкой `price` через `greater_than`/`less_than`). Обёрнутая функция `generate_filters_from_query(query)` теперь также возвращает пару `(filters, total_tokens)`.

**Exercise 4 — `get_relevant_products_from_query(query, simplified=False)`**: нужно было добавить параметр `simplified`; при `True` функция должна **пропускать генерацию метаданных и фильтрацию**, выполняя только простой семантический поиск (`products_collection.query.near_text(query, limit=20)`), возвращая `(results.objects, 0)` — 0 токенов, так как LLM не вызывается. При `simplified=False` сохраняется прежняя логика модуля 4 (генерация фильтров → поиск с фильтрами → при недостатке результатов (< 10) постепенное ослабление фильтров в порядке важности `['baseColour', 'masterCategory', 'usage', 'masterCategory', 'season', 'articleType', 'gender']`, пока не наберётся ≥ 5 объектов), обёрнутая в трассировку (span `get_relevant_products_from_query`, вложенные spans `refilter_{i}` для каждой попытки ослабления фильтров).

Юнит-тест `unittests.test_get_relevant_products_from_query(get_relevant_products_from_query)` — пройден.

Демонстрация на запросе *«Give me three T-shirts to use in sunny days»*:
- `simplified=False` → **1432** токена.
- `simplified=True` → **0** токенов (запрос отправляется напрямую в vector search без LLM-вызова).

#### 5.4 Generating the retrieved items as context — `generate_items_context(results)` (не градируется, дана целиком, `@tracer.tool`)

Идентична версии из модуля 4 — форматирует список найденных товаров в текст с полями Product ID/name/Category/usage/gender/Type/Color/Season/Year. Пример вывода показывает товары вида *«Inkfruit Mens D day T-shirt»*, *«Inkfruit Mens Little Bit More T-shirt»* и т.д.

#### 5.5 Query on Products — `query_on_products(query, simplified=False)` (не градируется, дана целиком, `@tracer.tool`)

Суммирует токены на каждом шаге (`decide_task_nature` + `get_relevant_products_from_query`), строит промпт с явным ограничением **«Never use more than 5 clothing products available below to compose your answer»** и требованием указывать ID товара, генерирует `kwargs` через `generate_params_dict(PROMPT, role='assistant', **parameters_dict)`.

Сравнение на запросе *«Make a wonderful look for a man attending a wedding party happening during night.»*:
- Previous setup (`simplified=False`): суммарно **3275** токенов (kwargs-генерация + финальный LLM-вызов), ответ рекомендует 3 пары обуви (Product ID 33698, 41475, 50775).
- New setup (`simplified=True`): суммарно **1836** токенов, ответ рекомендует другой набор товаров (обувь + галстук с зажимом и платком, ID 8960, 17375, 40245) с более развёрнутым описанием образа.

### Раздел 6 — The final function!

**6.1 `answer_query(query, model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", simplified=False)`** (дана целиком, `@tracer.tool`): определяет тип запроса через `check_if_faq_or_product` (суммируя токены), для `FAQ` вызывает `query_on_faq`, для `Product` — `query_on_products` в `try/except` (при исключении — запасной промпт с просьбой переформулировать запрос), в конце принудительно выставляет `kwargs['model'] = model` («обычно лучшая модель» для финального ответа) и возвращает `(kwargs, total_tokens)`.

**Наблюдение о несоответствии документации коду**: в docstring и в markdown-описании раздела 6 явно указано, что функция должна «Add the information into a dataframe» (добавлять информацию в dataframe) как один из шагов обработки. В изученном коде `answer_query`, однако, никакой логики работы с `pandas.DataFrame` не реализовано — функция лишь возвращает `(kwargs, total_tokens)` без записи в датафрейм или иной лог. Соответственно, в `unittests.py` присутствует тест `test_generate_log`, но соответствующая функция `generate_log` в ноутбуке не определена и нигде не вызывается.

Демонстрация на запросе *«Give me three examples of blue t-shirts available on your catalogue.»*:
- `simplified=False`: суммарно **3392** токена, ответ перечисляет 3 синих футболки с ID.
- `simplified=True`: суммарно **1744** токена, тот же по существу ответ (те же 3 товара: ID 1847, 3103, 3754).

### Раздел 7 — The ChatBot

Финальный раздел запускает виджет чат-бота дважды — для сравнения «стандартной» и «упрощённой» версий:

```python
chat_widget_standard = ChatWidget(generator_function=lambda x: answer_query(x, simplified=False), tracer=tracer)
...
chat_widget_simplified = ChatWidget(generator_function=lambda x: answer_query(x, simplified=True), tracer=tracer)
```

Предлагаемые для сравнения запросы: *«I bought a T-shirt and I didn't like it. Can I get a refund?»*, *«I want a look to wear to a beach party at night. It's winter, and I'm a woman.»* После каждого запуска предлагается перейти в UI Phoenix через `make_url()`, чтобы сравнить трассировки и расход токенов.

### Вспомогательные файлы

- **`utils.py`** (663 строки) — расширенная версия из модуля 4: `make_url(endpoint=None)` (формирование ссылки на Phoenix UI под Coursera/Learning Platform/локально), `process_and_print_query(...)` (цветной вывод сравнения standard/simplified с подсветкой превышения лимита токенов), `generate_with_single_input`/`generate_with_multiple_input` (теперь возвращают полный OpenAI-объект, а не только `{role, content}`), `generate_params_dict`, `generate_embedding` (модель `BAAI/bge-base-en-v1.5`), классы `ChatBot`/`ChatWidget` (тот же UI на `ipywidgets`, что и в модуле 4, но `ChatBot`/`ChatWidget` принимают также `tracer` для интеграции с Phoenix), `print_object_properties`, `call_llm_with_context`, `print_properties`, а также перенесённые сюда `parse_json_output`, `get_filter_by_metadata`, `generate_filters_from_query`, `generate_metadata_from_query` (в модуле 4 эти функции были определены прямо в ноутбуке).
- **`weaviate_server.py`** — подключает embedded Weaviate через `weaviate.connect_to_embedded(...)`. Примечательно, что `persistence_data_path` указывает на `"/home/jovyan/data/collections/collections_assignment_4/"` — то есть на путь коллекций **модуля 4**, а не модуля 5; это наблюдаемый факт кода (возможно, унаследованный путь), без предположений о том, является ли это ошибкой или намеренным переиспользованием одной и той же базы данных между заданиями.
- **`flask_app.py`** — идентичен по структуре версии из ungraded lab 1 модуля 5: эндпоинты `/.well-known/ready`, `/meta`, `/vectors` (POST, использует `generate_embedding` из `utils.py`), запуск на порту 5000 в отдельном потоке.
- **`unittests.py`** (368 строк) — 6 тестовых функций: `test_check_if_faq_or_product`, `test_query_on_faq`, `test_decide_task_nature`, `test_get_params_for_task`, `test_get_relevant_products_from_query`, `test_generate_log`; в ноутбуке фактически вызываются только первые четыре из них за вычетом `test_get_params_for_task` (см. выше — не вызывается) и `test_generate_log` (соответствующая функция `generate_log` не реализована).
- **`README.md`** — вспомогательное (не авторитетное) описание задания; в целом согласуется по структуре с содержимым ноутбука.

### Ограничения и предпосылки

- Требуется запущенный локальный Weaviate (порт `8079`, gRPC `50050`) с уже загруженными коллекциями `products` (44423 объекта) и `Faq` (25 объектов), а также Flask-сервис на порту 5000 для эмбеддингов.
- Для вызовов LLM требуется доступ к прокси DLAI либо `TOGETHER_API_KEY`; используемые модели — `meta-llama/Llama-3.2-3B-Instruct-Turbo` (промежуточные вызовы: маршрутизация, классификация, генерация метаданных) и `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` (финальный ответ пользователю через `ChatBot`/`answer_query`).
- Для эмбеддингов используется модель `BAAI/bge-base-en-v1.5`.
- Требуется библиотека `phoenix` (Arize) для трассировки через `phoenix.otel.register`; UI доступен через `make_url()` (по умолчанию `localhost:6006`, либо специфичная для платформы ссылка).
- Раздел 1.4 (настройка стоимости моделей в Phoenix UI) и весь раздел 7 (запуск `ChatWidget`) требуют интерактивного взаимодействия в среде Jupyter и явно отмечены как необязательные/демонстрационные части задания.
- Для батч-вставки FAQ используется `tqdm` и `weaviate.util.generate_uuid5`.
