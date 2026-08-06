См. practice\Module1\ungraded_labs\ungraded_lab_2

## Конспект по коду

### Назначение notebook и папки

Папка `practice\Module1\ungraded_labs\ungraded_lab_2` содержит notebook `C1M1_Ungraded_Lab_2.ipynb` и helper-файл `utils.py`.

Notebook показывает, как:

- отправлять single prompt в `LLM`;
- вести conversation через list of messages;
- использовать Together.ai API через helper functions;
- вызывать Together.ai endpoint через OpenAI-compatible client;
- добавлять structured data в prompt;
- сравнивать ответ без дополнительного context и ответ с `augmented prompt`.

Главная практическая идея: дополнительная информация, встроенная в prompt, помогает модели дать более конкретный и точный ответ.

### Helper-файл `utils.py`

`utils.py` импортирует:

- `requests`;
- `json`;
- `os`;
- `Path` из `pathlib`;
- `List`, `Dict` из `typing`;
- `Together` из `together`.

Файл содержит `_load_dotenv_from_parents()`, которая ищет ближайший `.env` вверх от папки файла и загружает простые пары `KEY=VALUE` в environment variables. Это позволяет notebook работать локально без `python-dotenv`.

Функции для ключа и endpoint:

- `get_proxy_url()`: возвращает `TOGETHER_BASE_URL` или fallback `https://api.together.xyz/`;
- `get_proxy_headers()`: возвращает `Authorization` header, если есть Together API key;
- `get_together_key()`: читает `TOGETHER_API_KEY`;
- `_with_bearer_prefix()` и `_without_bearer_prefix()`: нормализуют API key для разных способов вызова.

Основные функции вызова `LLM`:

- `generate_with_single_input(prompt, role='user', top_p=None, temperature=None, max_tokens=500, model="Qwen/Qwen3.5-9B", together_api_key=None, **kwargs)`;
- `generate_with_multiple_input(messages, top_p=None, temperature=None, max_tokens=500, model="Qwen/Qwen3.5-9B", together_api_key=None, **kwargs)`.

Обе функции формируют payload с:

- `model`;
- `messages`;
- `max_tokens`;
- `reasoning: {"enabled": False}`;
- optional `temperature` и `top_p`, если они не `None`;
- дополнительными `kwargs`.

Если explicit `together_api_key` не передан и ключ не найден, используется proxy URL и `requests.post`. Если ключ есть, используется `Together(api_key=...)` и `client.chat.completions.create(...)`. Возврат нормализуется к dictionary:

```python
{'role': ..., 'content': ...}
```

### Раздел 1: вызовы LLM

Notebook начинается с импорта helper functions:

```python
from utils import (
    generate_with_single_input,
    generate_with_multiple_input,
    get_proxy_url,
    get_proxy_headers,
    get_together_key
)
```

В markdown указано, что в Coursera environment часть доступа к Together API выполняется через proxy server. При запуске вне Coursera может понадобиться optional `together_api_key`.

#### `generate_with_single_input`

Функция предназначена для генерации текста по одному prompt.

Ключевые параметры, описанные в notebook:

- `prompt`: input text prompt;
- `max_tokens`: maximum tokens in response;
- `model`: default `Qwen/Qwen3.5-9B`;
- request payload disables reasoning through `reasoning={"enabled": False}`;
- `together_api_key`: optional API key for direct Together.ai call.

Пример вызывает:

```python
generate_with_single_input(prompt="What is the capital of France?")
```

Visible output показывает role `assistant` и content с ответом, что столица France - Paris, с дополнительным описанием Paris.

#### `generate_with_multiple_input`

Функция принимает list of messages для conversational context. Каждый message - dictionary с ключами:

- `role`;
- `content`.

Пример conversation:

1. user спрашивает, кто выиграл FIFA World Cup in 2018;
2. assistant отвечает, что France выиграла;
3. user спрашивает, кто был captain.

Вызов:

```python
generate_with_multiple_input(messages=messages, max_tokens=100)
```

Visible output показывает ответ assistant, но в notebook этот ответ называет Antoine Griezmann captain. Позже в OpenAI-compatible вызове выводится Hugo Lloris. В конспекте это фиксируется как видимый результат notebook, без самостоятельного исправления содержания.

### OpenAI-compatible интеграция

Notebook показывает, что Together.ai endpoints OpenAI compatible и могут вызываться через OpenAI library.

Импорты:

```python
from openai import OpenAI, DefaultHttpxClient
import httpx
```

Настройка клиента:

- `base_url = get_proxy_url()`;
- `httpx.HTTPTransport(local_address="0.0.0.0", verify=False)` используется для bypass SSL verification при работе через proxy;
- `DefaultHttpxClient` получает transport и headers;
- `OpenAI` создается с `api_key=get_together_key()`, `base_url=base_url`, `http_client=http_client`.

Затем используется тот же conversational `messages`. Вызов:

```python
client.chat.completions.create(
    messages=messages,
    model="Qwen/Qwen3.5-9B",
    extra_body={"reasoning": False}
)
```

Visible output полного объекта `ChatCompletion` содержит:

- `model='Qwen/Qwen3.5-9B'`;
- `usage` с `prompt_tokens`, `completion_tokens`, `total_tokens`;
- message content: Hugo Lloris был captain of the France national team during the 2018 FIFA World Cup;
- поле `reasoning` внутри message, хотя reasoning tokens в usage указаны как `0`.

Следующая ячейка показывает, что content можно получить через:

```python
response.choices[0].message.content
```

Visible output печатает краткий ответ про Hugo Lloris.

### Together.ai credits и ошибки

Notebook содержит note о Together.ai integration для курса.

Указано:

- Together.ai provided credits для использования hosted LLMs;
- credit limit установлен примерно в 10 раз выше typical usage;
- при ошибках `500` и `429` система может быть overloaded, обычно помогает подождать;
- если credits заканчиваются, пользователь будет notified и должен обратиться в Discourse community;
- grading assignment не использует credits.

### Раздел 2: интеграция данных в prompt

Notebook переходит к prompt augmentation на маленьком dataset с houses. Данные задаются прямо в notebook как list of dictionaries `house_data`.

Каждый house dictionary содержит:

- `address`;
- `city`;
- `state`;
- `zip`;
- `bedrooms`;
- `bathrooms`;
- `square_feet`;
- `price`;
- `year_built`.

В dataset две записи:

- `123 Maple Street`, Springfield, IL, 1500 sq ft, price `230000`, built in `1998`;
- `456 Elm Avenue`, Shelbyville, TN, 2500 sq ft, price `320000`, built in `2005`.

### `house_info_layout`

Функция `house_info_layout(houses)` превращает list of houses в formatted text.

Основные шаги:

1. создать empty string `layout`;
2. пройти по каждому `house`;
3. добавить к `layout` строку с address, city, state, zip, bedrooms, bathrooms, square feet, price и year built;
4. добавить newline в конце каждой house строки;
5. вернуть `layout`.

Visible output показывает две formatted строки с данными домов.

### `generate_prompt`

Функция `generate_prompt(query, houses)` создает `augmented prompt`.

Основные шаги:

1. вызвать `house_info_layout(houses)`;
2. встроить полученный `houses_layout` в hard-coded prompt;
3. добавить пользовательский `query`;
4. вернуть prompt.

Пример:

```python
generate_prompt("What is the most expensive house?", houses=house_data)
```

Visible output показывает prompt с инструкцией использовать house information и query.

### Сравнение ответа без context и с augmented prompt

Notebook задает query:

```python
query = "What is the most expensive house? And the bigger one?"
```

Затем делает два вызова:

- `query_without_house_info = generate_with_single_input(prompt=query, role='user')`;
- `enhanced_query = generate_prompt(query, houses=house_data)`;
- `query_with_house_info = generate_with_single_input(prompt=enhanced_query, role='assistant')`.

Ответ без house info уходит в общие сведения о дорогих и больших домах в мире, потому что модели не предоставлен локальный dataset.

Ответ с house info использует данные из prompt:

- most expensive: `456 Elm Avenue, Shelbyville, TN`, price `$320,000`;
- bigger: тот же дом, `2,500 sq ft`, по сравнению с `1,500 sq ft` у Maple Street.

> Важный вывод: даже простой `augmented prompt` с маленьким structured dataset меняет поведение `LLM`: модель отвечает по предоставленным данным, а не по общим знаниям.

### Ограничения и предпосылки

Notebook не должен запускаться без настройки доступа к Together.ai или proxy. Для локального запуска нужен `TOGETHER_API_KEY` или рабочий `TOGETHER_BASE_URL`/proxy. В `utils.py` SSL verification отключается для proxy-сценария через `verify=False` или custom `httpx` transport; это указано как условие работы с proxy.
