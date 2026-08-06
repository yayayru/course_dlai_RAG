См. practice\Module4\Graded_Assignments\C1M4_Assignment.ipynb

## Конспект по коду

### Назначение

`C1M4_Assignment.ipynb` — итоговое оцениваемое (graded) задание модуля 4: построение чат-бота на основе RAG для вымышленного интернет-магазина одежды **Fashion Forward Hub**. В отличие от graded-заданий модулей 2 и 3, в данном репозитории этот ноутбук содержит **решённые** (заполненные) ячейки с кодом — все 5 упражнений реализованы, и почти все ячейки с выводами показывают успешное выполнение и прохождение unit-тестов (`[92m All tests passed!`), за одним отмеченным ниже исключением.

Задачи задания (по вводной ячейке):

- **LLM routing** — функции для категоризации и определения типа каждого запроса, создающие маршрутизатор, который в зависимости от природы запроса применяет разную обработку.
- **Conditional parameter setting** — методы для определения, является ли запрос пользователя творческим или техническим, чтобы LLM могла подстроить свои настройки для лучшего ответа.
- **Producing JSON Responses** — программирование LLM для генерации валидных JSON-ответов с информацией о товарах.
- **Adding Contextual Information** — включение релевантных данных в запросы перед их обработкой LLM.
- **Chatbot Development** — создание чат-бота, взаимодействующего с пользователями естественным и эффективным образом.

### Ключевые импорты и настройка

- `json`, `weaviate`, `weaviate.classes.query.Filter`, `joblib` — работа с vector database и данными.
- `unittests`, `flask_app`, `weaviate_server` — служебные модули (импорт `flask_app` запускает Flask-приложение: `* Serving Flask app 'flask_app'`, `* Debug mode: off`).
- Из `utils` импортируются `ChatWidget`, `generate_with_single_input`, `generate_params_dict`.
- Клиент Weaviate подключается локально: `client = weaviate.connect_to_local(port=8079, grpc_port=50050)`.
- Модель по умолчанию в `generate_params_dict` — `meta-llama/Llama-3.2-3B-Instruct-Turbo` (в этом задании отличается от `Qwen/Qwen3.5-9B`, использовавшейся в ungraded-лабах модуля).

### Вспомогательные файлы

- **`weaviate_server.py`** — при импорте подключает embedded Weaviate-клиент через `weaviate.connect_to_embedded(persistence_data_path="/home/jovyan/data/collections/collections_assignment_4/", environment_variables={"ENABLE_API_BASED_MODULES": "true", "ENABLE_MODULES": "text2vec-transformers", "TRANSFORMERS_INFERENCE_API": "http://127.0.0.1:5000/"})`, используя `suppress_subprocess_output()` (context manager, патчащий `subprocess.Popen`, чтобы скрыть его stdout/stderr).
- **`flask_app.py`** — Flask-приложение с эндпоинтами `/.well-known/ready`, `/meta` (readiness checks), `/rerank` (принимает `query`/`documents` от Weaviate) и `/vectorize` (использует `generate_embedding` из `utils.py`, модель `BAAI/bge-base-en-v1.5`).
- **`utils.py`** — содержит `generate_with_single_input`, `generate_with_multiple_input`, `generate_params_dict` (вызовы LLM через прокси `https://proxy.dlai.link/coursera_proxy/together` или `TOGETHER_API_KEY`), `generate_embedding` (модель `BAAI/bge-base-en-v1.5`, через `OpenAI`-совместимый клиент с обходом SSL через кастомный `httpx`-транспорт), `call_llm_with_context`, `print_object_properties`, `print_properties`, а также классы `ChatBot` и `ChatWidget` (виджет на `ipywidgets` с полем ввода, кнопкой отправки, HTML-областью для истории чата и областью для отображения изображений товаров, извлекаемых по `ID` из текста ответа ассистента через regex `r'ID:\s*(\d+(?:,\s*\d+)*)'`).
- **`unittests.py`** — 6 тестовых функций: `test_check_if_faq_or_product`, `test_query_on_faq`, `test_decide_task_nature`, `test_get_params_for_task`, `test_generate_metadata_from_query`, плюс вспомогательная `parse_json_output`.
- **`README.md`** — дополнительное (не авторитетное, вспомогательное) описание структуры задания; в целом согласуется с содержимым ноутбука.

### Раздел 1 — Введение и данные Fashion Forward Hub

Показана структура двух источников данных:

- **Products Database** (`joblib.load('dataset/clothes_json.joblib')`, переменная `PRODUCTS_DATA`) — список словарей с полями `gender`, `masterCategory`, `subCategory`, `articleType`, `baseColour`, `season`, `year`, `usage`, `productDisplayName`, `price`, `product_id`. Пример: `{'gender': 'Men', 'masterCategory': 'Apparel', ..., 'productDisplayName': 'Turtle Check Men Navy Blue Shirt', 'price': 67, 'product_id': 15970}`.
- **FAQ Database** (`joblib.load("dataset/faq.joblib")`, переменная `FAQ`) — список словарей с полями `question`, `answer`, `type` (например, вопрос про часы работы магазина). В задании FAQ используется как жёстко закодированная (hardcoded) строка внутри промпта, отдельная коллекция для FAQ не создаётся.

Также демонстрируется recap функции `generate_params_dict` (совпадает по сигнатуре с ungraded-лабами, но с моделью `meta-llama/Llama-3.2-3B-Instruct-Turbo` по умолчанию) и пример вызова LLM для решения уравнения `x^2 - 1 = 0`.

### Раздел 3 — Task routing

#### Exercise 1 — `check_if_faq_or_product(query)`

Строит хардкоженный промпт, классифицирующий запрос как `"FAQ"` или `"Product"` для розничной компании Fashion Forward Hub, с определениями обеих категорий и 6 примерами (запрос → ожидаемая метка), инструкцией отвечать одним словом. Вызывает `generate_params_dict(prompt, temperature=0.4, top_p=0.4)`, затем `generate_with_single_input(**kwargs)`, возвращает `response['content']` как метку.

Проверка на 5 запросах в выводе ноутбука показала 3 успешных классификации (*«What is your return policy?»* → `FAQ`, *«Give me three examples of blue T-shirts...»* → `Product`, *«How can I contact the user support?»* → `FAQ`), после чего четвёртый вызов (*«Do you have blue Dresses?»*) прервался ошибкой **`504 Gateway Timeout`** от прокси-сервера (`Exception: Error while calling LLM: ... 504 Gateway Timeout ERROR ... We can't connect to the server for this app or website at this time`) — временная сетевая/инфраструктурная ошибка прокси, а не ошибка в коде решения. Тем не менее, юнит-тест `unittests.test_check_if_faq_or_product(check_if_faq_or_product)` в отдельном последующем вызове прошёл успешно (`All tests passed!`).

#### Exercise 2 — `query_on_faq(query, **kwargs)`

Сначала дана вспомогательная (не оцениваемая) функция `generate_faq_layout(faq_dict)`, которая форматирует список FAQ в текстовый layout вида `Question: ... Answer: ... Type: ...\n` для каждой записи — результат сохранён в глобальную `FAQ_LAYOUT`.

`query_on_faq` строит промпт, включающий `FAQ_LAYOUT` и вопрос пользователя (*«Answer the user query using this list of FAQs {FAQ_LAYOUT}. Query: {query}»*), формирует `kwargs = generate_params_dict(prompt, temperature=0.4, top_p=0.4)` и возвращает `kwargs` (сам вызов LLM выполняется отдельно вызывающим кодом). Продемонстрирован пример: вопрос про возврат нежелаемого товара — LLM отвечает про Returns Center и 30-дневный срок возврата, корректно опираясь на соответствующие пункты FAQ. Юнит-тест пройден (`All tests passed!`).

#### Exercise 3 — `decide_task_nature(query)`

Строит промпт, классифицирующий запрос как `"creative"` или `"technical"` для Fashion Forward Hub, с определениями категорий и 6 примерами, вызывает `generate_params_dict(prompt, temperature=0.4, top_p=0.4)` и `generate_with_single_input(**kwargs)`, возвращает `response['content']`.

Проверка на 5 запросах в выводе ноутбука: все 5 меток совпали с логически ожидаемыми (*«Give me two sneakers with vibrant colors.»* → `creative`; *«What are the most expensive clothes...»* → `technical`; *«...suggestion on an accessory to match...»* → `creative`; *«Give me three trousers with vibrant colors...»* → `technical`; *«Create a look for a woman walking in a park...»* → `creative`) — при этом markdown-ячейка с «Expected Output» показывает иные ожидаемые метки для первого запроса (`technical` вместо полученного `creative`), то есть фактический вывод модели частично разошёлся с текстом ожидаемого вывода в задании; тем не менее юнит-тест `unittests.test_decide_task_nature` пройден успешно (`All tests passed!`).

#### Exercise 4 — `get_params_for_task(task)`

Возвращает словарь `{"top_p": ..., "temperature": ...}` в зависимости от типа задачи:

- `"technical"` → `{"top_p": 0.4, "temperature": 0.4}` (низкая случайность);
- `"creative"` → `{"top_p": 0.8, "temperature": 1.5}` (более высокая случайность);
- иное значение → `{"top_p": 0.5, "temperature": 1.0}` (параметры по умолчанию).

Пример вызова `get_params_for_task("technical")` → `{'top_p': 0.4, 'temperature': 0.4}`. Юнит-тест пройден.

### Раздел 4 — Извлечение товаров на основе метаданных из запроса

#### Подготовка возможных значений метаданных

В ячейке (не градируемой) строится словарь `values` — множество всех встречающихся в `PRODUCTS_DATA` значений для ключей `gender`, `masterCategory`, `articleType`, `baseColour`, `season`, `usage` (исключая `product_id`, `price`, `productDisplayName`, `subCategory`, `year`). Пример: `values['season']` → `{'All seasons', 'Fall', 'Spring', 'Summer', 'Winter'}`.

#### Exercise 5 — `generate_metadata_from_query(query)`

Строит промпт, инструктирующий LLM сгенерировать JSON с полями `gender`, `masterCategory`, `articleType`, `baseColour`, `price` (объект с `min`/`max`, по умолчанию `{"min": 0, "max": "inf"}`), `usage`, `season` для фильтрации товаров по запросу, с примером ожидаемого формата JSON внутри промпта (с двойными фигурными скобками `{{ }}` для экранирования в f-string). Вызывает `generate_params_dict(prompt, temperature=0.0, top_p=0.4, max_tokens=1500)` и `generate_with_single_input(**kwargs)`, возвращает `response['content']`.

Пример: для запроса *«Create a look for a man that suits a sunny day in the park. I don't want to spend more than 300 dollars on each piece.»* LLM возвращает корректный JSON: `{"gender": "Men", "masterCategory": "Apparel", "articleType": ["Shirts", "Pants"], "baseColour": ["Light", "Pastel"], "price": {"min": 0, "max": 300}, "usage": ["Casual"], "season": ["Summer"]}`. Юнит-тест `unittests.test_generate_metadata_from_query` пройден успешно.

#### Вспомогательные (не градируемые) функции

- `parse_json_output(llm_output)` — очищает вывод LLM (убирает `\n`, одинарные кавычки, двойные фигурные скобки) и парсит через `json.loads`; при `JSONDecodeError` печатает ошибку и возвращает `None`.
- `get_filter_by_metadata(json_output)` — для каждого ключа из `('gender', 'masterCategory', 'articleType', 'baseColour', 'price', 'usage', 'season')` строит объект `Filter` Weaviate: для `price` — `Filter.by_property('price').greater_than(min_price)` и `.less_than(max_price)` (только если `min_price > 0` и `max_price != 'inf'`), для остальных ключей — `Filter.by_property(key).contains_any(value)`.
- `generate_filters_from_query(query)` — обёртка, последовательно вызывающая `generate_metadata_from_query` → `parse_json_output` → `get_filter_by_metadata`.
- `get_relevant_products_from_query(query)` — генерирует фильтры, выполняет `products_collection.query.near_text(query, filters=Filter.all_of(filters), limit=20)`; если результатов меньше 10, постепенно убирает менее важные фильтры (в порядке `['baseColour', 'masterCategory', 'usage', 'masterCategory', 'season', 'gender']`), пока не наберётся хотя бы 5 результатов.
- `generate_items_context(results)` — форматирует список найденных товаров в текстовый контекст вида `Product ID: ... Product name: ... Product Category: ... ...`.

Коллекция `products_collection = client.collections.get('products')` содержит `len(products_collection) = 44423` объектов.

**Наблюдаемая ошибка (в выводе ноутбука, не связана с решением упражнений):** вызов `get_relevant_products_from_query("Give me three blue colour tshirts for men between £100 and £300")` завершился ошибкой `TypeError: object of type 'NoneType' has no len()` (внутри функции, при попытке применить `len()` к результату запроса, вернувшему `None`), а последующая попытка обратиться к `t[0].properties` — ошибкой `IndexError: list index out of range`, так как переменная `t` в итоге оказалась пустым списком `[]`. Это демонстрационные (не оцениваемые) ячейки — ошибка не влияет на прохождение юнит-тестов заданий.

### Раздел 5 — Финальная функция и ЧатБот

- `query_on_products(query)` — определяет природу запроса (`decide_task_nature`), получает параметры (`get_params_for_task`), извлекает релевантные товары (`get_relevant_products_from_query`), строит контекст (`generate_items_context`), формирует промпт с инструкцией указывать ID товара в ответе и ограничением до пяти товаров, если число не указано в запросе, и возвращает `kwargs = generate_params_dict(prompt, role='assistant', **parameters_dict)`.
- `answer_query(query)` — финальная объединяющая функция: вызывает `check_if_faq_or_product(query)`; если метка не `'FAQ'`/`'Product'`, возвращает запасной (fallback) промпт с просьбой ответить на основе имеющегося контекста; если `'FAQ'` — вызывает `query_on_faq`; если `'Product'` — вызывает `query_on_products` в `try/except`, при исключении возвращая запасной промпт с просьбой попросить пользователя переформулировать запрос.
- `ChatWidget(generator_function=answer_query)` — создаёт интерактивный виджет чат-бота на `ipywidgets`, использующий `answer_query` как функцию генерации ответа; предлагаемые тестовые запросы: *«Do you have blue t-shirts on your catalogue?»*, *«I bought a dress and I didn't like it. How can I get a refund?»*, *«I am going to a party at the beach. Can you suggest a nice look for me? It will be a warm night, and I'm a man.»*

### Ограничения и предпосылки

- Требуется запущенный локальный/embedded Weaviate-сервер (порт `8079`, gRPC-порт `50050`) с уже загруженной коллекцией `products` (44423 объекта) и векторизатором `text2vec-transformers`, указывающим на локальный Flask-сервис (`http://127.0.0.1:5000/`), поднимаемый через `flask_app.py`.
- Для вызовов LLM требуется доступ к прокси DLAI (`https://proxy.dlai.link/coursera_proxy/together`) либо собственный `TOGETHER_API_KEY`.
- Модель по умолчанию для генерации — `meta-llama/Llama-3.2-3B-Instruct-Turbo`; `ChatBot`/`ChatWidget` использует `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo`.
- Для эмбеддингов используется модель `BAAI/bge-base-en-v1.5`.
- Раздел 5.2 (`ChatWidget`) — интерактивный виджет, требующий среды Jupyter с `ipywidgets` и не предназначенный для автоматического запуска без участия пользователя; изображения товаров подгружаются с локального диска по пути `/home/jovyan/data/collections/collections_assignment_4/images/{id}.jpg`.
- В выводах ноутбука присутствуют признаки нестабильности внешнего прокси-сервиса (ошибка `504 Gateway Timeout` в разделе 3.1) и одна необъяснённая в тексте ноутбука ошибка `TypeError`/`IndexError` в демонстрационных (не градируемых) ячейках раздела 4.3 — обе зафиксированы как наблюдаемые факты без предположений об их причине.