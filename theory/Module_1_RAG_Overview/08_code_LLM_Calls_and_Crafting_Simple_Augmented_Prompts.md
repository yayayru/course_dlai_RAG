См. `practice\Module1\ungraded_labs\ungraded_lab_2` (notebook `C1M1_Ungraded_Lab_2.ipynb` + `utils.py`)

## Конспект по коду

### Назначение notebook и папки

Папка `practice\Module1\ungraded_labs\ungraded_lab_2` содержит notebook `C1M1_Ungraded_Lab_2.ipynb` («Ungraded Lab 2: LLM Calls and Crafting Simple Augmented Prompts») и helper-файл `utils.py`.

Согласно вводной markdown-ячейке, в этой лабораторной работе даётся практика с двумя основными функциями для взаимодействия с `LLM`: отправка одиночного промпта и ведение диалога (back-and-forth conversation). Главная цель — показать, как добавлять дополнительную информацию к промптам, делая их более подробными и полезными, чтобы модель давала более точные и качественные ответы.

Цели лабораторной работы (по markdown):

- научиться настраивать и отправлять вопросы в LLM как для одиночных вопросов, так и для диалогов;
- научиться использовать дополнительные данные, чтобы обогащать промпты, улучшая ответы модели.

Оглавление notebook:

1. Understanding the functions to call LLMs — `generate_with_single_input`, `generate_with_multiple_input`.
2. Integrating Data into an LLM Prompt — Understanding the data structure, Creating the Prompt.

### Helper-файл `utils.py`

Импорты: `requests`, `json`, `os`, `Path` из `pathlib`, `List`, `Dict` из `typing`, `Together` из библиотеки `together`.

Ключевые функции:

- **`_load_dotenv_from_parents()`** — ищет ближайший файл `.env`, поднимаясь от директории `utils.py` вверх по родительским папкам, и построчно загружает простые пары `KEY=VALUE` в переменные окружения (`os.environ`), если такая переменная ещё не установлена. Это позволяет notebook работать локально без зависимости `python-dotenv`. Вызывается сразу на уровне модуля (`_load_dotenv_from_parents()` вызывается один раз при импорте `utils.py`).
- **`_with_bearer_prefix(api_key)`** / **`_without_bearer_prefix(api_key)`** — нормализуют строку API-ключа, добавляя или убирая префикс `Bearer `.
- **`get_proxy_url()`** — возвращает значение переменной окружения `TOGETHER_BASE_URL`, а если она не задана — значение по умолчанию `https://api.together.xyz/`.
- **`get_proxy_headers()`** — возвращает словарь заголовков с `Authorization`, если `get_together_key()` вернул непустой ключ, иначе пустой словарь.
- **`get_together_key()`** — читает переменную окружения `TOGETHER_API_KEY` (по умолчанию — пустая строка).

Основные функции вызова LLM — `generate_with_single_input` и `generate_with_multiple_input`. Обе:

- принимают опциональные `top_p`, `temperature` (по умолчанию `None`, и если `None` — не добавляются в payload), `max_tokens` (по умолчанию `500`), `model` (по умолчанию `"Qwen/Qwen3.5-9B"`), `together_api_key` (по умолчанию `None`) и произвольные `**kwargs`;
- формируют `payload` с полями `model`, `messages`, `max_tokens`, `reasoning: {"enabled": False}` (чтобы не тратить токены на reasoning) и переданными `**kwargs`;
- если `together_api_key` не передан явно и не найден через `get_together_key()`, выполняют HTTP-запрос через `requests.post` на `get_proxy_url() + 'v1/chat/completions'` с заголовками `get_proxy_headers()` и `verify=False` (то есть отключена проверка SSL-сертификата);
- если API-ключ есть, создают клиента `Together(api_key=...)` и вызывают `client.chat.completions.create(**payload).model_dump()`, дополнительно приводя роль сообщения к нижнему регистру (`.name.lower()`);
- при ошибке HTTP-ответа (`not response.ok`) выбрасывают исключение с текстом ответа; при ошибке разбора JSON или структуры ответа — отдельные исключения с описанием;
- возвращают нормализованный словарь `{'role': ..., 'content': ...}`, взятый из последнего элемента `choices` ответа.

Отличие двух функций — во входных данных: `generate_with_single_input(prompt, role='user', ...)` принимает один текстовый промпт и роль, из которых сам формирует список `messages` из одного сообщения; `generate_with_multiple_input(messages, ...)` принимает уже готовый список сообщений (`List[Dict]`) для диалогового контекста.

### Раздел 1: вызовы LLM

Notebook импортирует helper-функции:

```python
from utils import (
    generate_with_single_input,
    generate_with_multiple_input,
    get_proxy_url,
    get_proxy_headers,
    get_together_key
)
```

В markdown указано, что функции вызывают API [together.ai](https://www.together.ai/); в среде Coursera часть шагов обращения к Together API выполняется через proxy-сервер, поэтому вне среды Coursera notebook «из коробки» не заработает — для запуска на локальной машине можно передать опциональный параметр с API-ключом together.ai.

#### `generate_with_single_input`

Описанные в markdown параметры: `prompt` (str) — входной текстовый промпт; `max_tokens` (int) — максимум токенов в ответе; `model` (str, по умолчанию `"Qwen/Qwen3.5-9B"`); в payload запроса reasoning отключается через `reasoning={"enabled": False}`, чтобы избежать генерации лишних reasoning-токенов; `together_api_key` — опциональный ключ для аутентификации (по умолчанию `None`, тогда используется proxy, иначе выполняется прямой вызов к together.ai).

Пример вызова:

```python
output = generate_with_single_input(
    prompt="What is the capital of France?"
)
print("Role:", output['role'])
print("Content:", output['content'])
```

Visible output:

```
Role: assistant
Content: The capital of France is **Paris**.

It is located in the north-central part of the country and serves as the nation's political, economic, and cultural center. Paris is also home to iconic landmarks such as the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral.
```

#### `generate_with_multiple_input`

Функция принимает список сообщений для диалогового контекста, где каждое сообщение — словарь с ключами `role` (`assistant`, `system` или `user`) и `content`. Параметры: `messages` (`List[Dict]`), `max_tokens`, `model` (по умолчанию тот же `"Qwen/Qwen3.5-9B"`); reasoning также отключён.

Пример диалога:

```python
messages = [
    {'role': 'user', 'content': 'Hello, who won the FIFA world cup in 2018?'},
    {'role': 'assistant', 'content': 'France won the 2018 FIFA World Cup.'},
    {'role': 'user', 'content': 'Who was the captain?'}
]

output = generate_with_multiple_input(
    messages=messages,
    max_tokens=100
)
```

Visible output:

```
Role: assistant
Content: The captain of the France national football team during the 2018 FIFA World Cup was **Antoine Griezmann**.

He was the only player in France's starting XI to feature in every match of the tournament, captaining the team from the first game against Australia to the final victory against Croatia. Although Blaise Matuidi was sometimes cited as a vice-captain or having served as captain for the opening match under specific circumstances in some squad lists, Griezmann is universally
```

В самом notebook этот ответ модели фактически называет капитаном сборной Франции Antoine Griezmann. Далее, в ячейке с интеграцией OpenAI-совместимого клиента (тот же вопрос, тот же диалог), модель отвечает, что капитаном был Hugo Lloris. Оба ответа зафиксированы здесь как видимые (и противоречащие друг другу) результаты работы notebook, без самостоятельного исправления содержания — вопрос капитанства сборной Франции на ЧМ-2018 в реальности отмечен как `[неясно]`, поскольку сам notebook выдаёт разные ответы в разных ячейках.

### 1.3 Интеграция с библиотекой OpenAI

Markdown поясняет, что эндпоинты Together.ai совместимы с OpenAI (`OpenAI compatible`), поэтому для вызовов можно использовать библиотеку OpenAI.

Импорты:

```python
from openai import OpenAI, DefaultHttpxClient
import httpx
```

Настройка клиента:

```python
base_url = get_proxy_url()
transport = httpx.HTTPTransport(local_address="0.0.0.0", verify=False)
http_client = DefaultHttpxClient(transport=transport, headers=get_proxy_headers())
client = OpenAI(
    api_key=get_together_key(),
    base_url=base_url,
    http_client=http_client,
)
```

В комментариях notebook поясняется, что `httpx.HTTPTransport` с `verify=False` нужен только для обхода SSL-проверки при работе через proxy курса и не требуется при прямом обращении к эндпоинту together.ai.

Далее используется тот же список `messages` (тот же диалог про ЧМ-2018), и выполняется вызов:

```python
response = client.chat.completions.create(
    messages=messages,
    model="Qwen/Qwen3.5-9B",
    extra_body={"reasoning": False}
)
print(response)
```

Visible output — полный объект `ChatCompletion`, включающий:

- `model='Qwen/Qwen3.5-9B'`;
- `usage` с `prompt_tokens=52`, `completion_tokens=372`, `total_tokens=424`, `reasoning_tokens=0`;
- содержимое сообщения: *«Hugo Lloris was the captain of the France national team during the 2018 FIFA World Cup.»*;
- поле `reasoning` внутри `message` с развёрнутым текстом рассуждений модели (`Thinking Process: ...`), несмотря на то, что `reasoning_tokens` в `usage` указан как `0`.

Следующая ячейка показывает, что содержимое ответа можно получить через `response.choices[0].message.content`; visible output печатает краткий ответ про Hugo Lloris.

### 1.4 Заметка о Together.ai для этого курса

Markdown-ячейка отдельно поясняет условия использования Together.ai в рамках курса:

- Together.ai предоставили кредиты (credits) для использования хостящихся у них LLM на протяжении курса;
- лимит кредитов установлен примерно в 10 раз выше типичного объёма использования, даже при интенсивной работе;
- ошибки `500` и `429` означают перегрузку системы слишком большим количеством вызовов — обычно решается ожиданием;
- если кредиты закончатся, пользователь будет уведомлён и должен обратиться в Discourse-сообщество курса;
- проверка (grading) задания никогда не расходует кредиты пользователя.

### Раздел 2: интеграция данных в промпт LLM

Раздел посвящён тому, как эффективно встраивать данные в промпт перед передачей его в LLM, на примере небольшого датасета домов (аналог JSON-файлов с информацией о домах). Это помогает понять, как augmentation промпта работает в контексте RAG.

#### Структура данных

`house_data` — список из двух словарей-домов, каждый с ключами `address`, `city`, `state`, `zip`, `bedrooms`, `bathrooms`, `square_feet`, `price`, `year_built`:

- `123 Maple Street`, Springfield, IL 62701 — 3 спальни, 2 ванные, 1500 sq ft, `$230000`, построен в 1998;
- `456 Elm Avenue`, Shelbyville, TN 37160 — 4 спальни, 3 ванные, 2500 sq ft, `$320000`, построен в 2005.

#### `house_info_layout(houses)`

Функция превращает список домов в отформатированный текст:

1. создаётся пустая строка `layout`;
2. цикл по каждому `house`;
3. к `layout` через f-string добавляется строка с адресом, городом, штатом, индексом, числом спален и ванных, площадью, ценой и годом постройки, с символом новой строки `\n` в конце;
4. функция возвращает `layout`.

Visible output — две строки вида *«House located at 123 Maple Street, Springfield, IL 62701 with 3 bedrooms, 2 bathrooms, 1500 sq ft area, priced at \$230000, built in 1998.»* (и аналогичная для второго дома).

#### `generate_prompt(query, houses)`

Функция создаёт `augmented prompt`:

1. вызывает `house_info_layout(houses)`, чтобы получить `houses_layout`;
2. встраивает `houses_layout` и переданный `query` в промпт, оформленный как многострочная f-string (`"""..."""`) с инструкцией *«Use the following houses information to answer users queries.»*;
3. возвращает получившийся `PROMPT`.

В комментарии кода отмечено, что функция достаточно модульна, чтобы принимать любой список домов — например, подмножество датасета, если в более сложном контексте LLM нужно дать не все данные.

Пример:

```python
print(generate_prompt("What is the most expensive house?", houses=house_data))
```

Visible output показывает собранный промпт с инструкцией, списком домов и строкой `Query: What is the most expensive house?`.

#### Сравнение ответа без контекста и с augmented prompt

Задаётся запрос:

```python
query = "What is the most expensive house? And the bigger one?"
```

Далее выполняются два вызова:

```python
query_without_house_info = generate_with_single_input(prompt=query, role='user')
enhanced_query = generate_prompt(query, houses=house_data)
query_with_house_info = generate_with_single_input(prompt=enhanced_query, role='assistant')
```

В комментариях кода поясняется выбор роли: без augmented prompt роль передаётся как `user`; при передаче уже готового промпта, включающего структуру инструкции, роль передаётся как `assistant`.

**Ответ без house info** (`query_without_house_info['content']`) — LLM рассуждает об этом в терминах общих знаний о недвижимости: упоминает, что сделки с недвижимостью часто закрыты NDA, и называет в качестве «самого дорогого дома» поместье Gamala в Hidden Hills (Калифорния, ~\$158 359 000, продано в сентябре 2021), а в качестве «самого большого дома» — резиденцию Deer Valley в Неваде (~72 000–75 000 sq ft). Ответ никак не связан с датасетом `house_data`, поскольку модели не был предоставлен локальный датасет.

**Ответ с house info** (`query_with_house_info['content']`) использует данные из промпта:

- самый дорогой: `456 Elm Avenue, Shelbyville, TN`, цена `$320,000` (выше, чем `$230,000` у второго дома);
- самый большой: тот же дом на `456 Elm Avenue`, `2,500 sq ft`, по сравнению с `1,500 sq ft` у дома на Maple Street.

> Основной практический вывод раздела: даже простой `augmented prompt` с маленьким структурированным датасетом меняет поведение LLM — модель отвечает по предоставленным данным, а не по общим знаниям, полученным при обучении.

### Ограничения и предпосылки

Notebook выполняет реальные сетевые вызовы к LLM (через proxy курса Coursera или напрямую к Together.ai) и требует рабочего доступа к сети. Для запуска вне среды Coursera нужен `TOGETHER_API_KEY` или рабочий `TOGETHER_BASE_URL`/proxy — иначе вызовы `generate_with_single_input`/`generate_with_multiple_input` и клиент OpenAI не смогут выполнить запрос. Для работы через proxy в `utils.py` и в самом notebook явно отключена проверка SSL-сертификата (`verify=False`, `httpx.HTTPTransport(..., verify=False)`). Зависимости: `requests`, `together` (пакет `Together`), `openai`, `httpx`. В рамках конспекта код изучался статически, без запуска notebook или отдельных ячеек.
