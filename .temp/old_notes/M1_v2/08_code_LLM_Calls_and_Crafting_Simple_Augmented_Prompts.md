См. practice\Module1\ungraded_labs\ungraded_lab_2

## Конспект по коду

### Источники кода

В папке `practice\Module1\ungraded_labs\ungraded_lab_2` релевантны:

- `C1M1_Ungraded_Lab_2.ipynb` — основной notebook лабораторной;
- `utils.py` — локальный вспомогательный файл, из которого notebook импортирует функции вызова `LLM`.

### Назначение notebook

Notebook `C1M1_Ungraded_Lab_2.ipynb` называется `LLM Calls and Crafting Simple Augmented Prompts`.

Он дает hands-on practice с двумя essential functions для взаимодействия с `LLM`:

- отправка single prompt;
- ведение back-and-forth conversation через список сообщений.

Главная цель лабораторной — показать, как добавлять extra information в prompts. Такой дополнительный context делает prompt более detailed и useful, а ответы модели — более precise.

Notebook заявляет две учебные цели:

- настроить и отправлять questions to an `LLM` для single questions и conversations;
- использовать additional data, чтобы делать prompts richer и улучшать replies модели.

### Импорты из `utils.py`

В начале notebook импортирует:

```python
from utils import (
    generate_with_single_input,
    generate_with_multiple_input,
    get_proxy_url,
    get_proxy_headers,
    get_together_key
)
```

Файл `utils.py` использует:

- `requests`;
- `json`;
- `os`;
- `Path` из `pathlib`;
- `List` и `Dict` из `typing`;
- `Together` из пакета `together`.

В `utils.py` есть загрузка `.env` из текущей папки или родительских директорий. Функция `_load_dotenv_from_parents()` ищет ближайший `.env`, читает строки формата `KEY=VALUE` и добавляет значения в `os.environ`, если переменная еще не установлена.

### Настройки API и ключей

`get_proxy_url()` возвращает URL для API calls:

- сначала читает `TOGETHER_BASE_URL`;
- если переменная не задана, использует `https://api.together.xyz/`.

`get_together_key()` возвращает `TOGETHER_API_KEY` из environment variables или пустую строку.

`get_proxy_headers()` возвращает Authorization header, если API key доступен. Для этого используется helper `_with_bearer_prefix()`, который добавляет `Bearer `, если ключ еще не начинается с этого prefix.

Для прямого вызова Together API используется `_without_bearer_prefix()`, который удаляет `Bearer ` перед передачей ключа в `Together(api_key=...)`.

### `generate_with_single_input`

Функция `generate_with_single_input()` генерирует text from a language model based on a single input prompt.

Важные параметры:

- `prompt: str` — input text prompt;
- `role: str = 'user'` — роль сообщения;
- `top_p: float = None`;
- `temperature: float = None`;
- `max_tokens: int = 500`;
- `model: str = "Qwen/Qwen3.5-9B"`;
- `together_api_key = None`;
- `**kwargs` для дополнительных параметров payload.

Функция формирует payload:

- `model`;
- `messages` как list с одним dictionary `{'role': role, 'content': prompt}`;
- `max_tokens`;
- `reasoning: {"enabled": False}`;
- дополнительные `kwargs`.

`temperature` и `top_p` добавляются в payload только если они не `None`. Это явно сделано, чтобы не передавать строку `'none'` или лишние значения в Together API.

Дальше функция выбирает способ вызова:

- если `together_api_key` не передан и не найден в environment, выполняется `requests.post()` в proxy endpoint `v1/chat/completions` с `verify=False`;
- если ключ есть, создается `Together` client и вызывается `client.chat.completions.create(**payload)`.

Функция возвращает dictionary:

```python
{'role': ..., 'content': ...}
```

Если response нельзя разобрать как JSON или достать из него ожидаемые поля, функция выбрасывает `Exception`.

### Первый single-input вызов

Notebook вызывает:

```python
output = generate_with_single_input(
    prompt="What is the capital of France?"
)
```

Затем печатает:

- `Role`;
- `Content`.

Видимый output:

- role: `assistant`;
- content сообщает, что capital of France — Paris, и добавляет краткое описание Paris как political, economic и cultural center, а также упоминает Eiffel Tower, Louvre Museum и Notre-Dame Cathedral.

Этот пример демонстрирует базовый single prompt call без retrieval и без дополнительного пользовательского context.

### `generate_with_multiple_input`

Функция `generate_with_multiple_input()` предназначена для conversational context.

Входной формат — `messages`, list of dictionaries. Каждый dictionary содержит:

- `role` — обычно `assistant`, `system` или `user`;
- `content` — prompt/message content.

Важные параметры:

- `messages: List[Dict]`;
- `top_p`;
- `temperature`;
- `max_tokens`;
- `model = "Qwen/Qwen3.5-9B"`;
- `together_api_key`;
- `**kwargs`.

Логика почти совпадает с `generate_with_single_input()`:

- формируется payload с `messages`;
- reasoning disabled через `reasoning: {"enabled": False}`;
- optional `temperature` и `top_p` добавляются только если заданы;
- вызов идет либо через proxy, либо напрямую через Together client;
- возвращается dictionary с `role` и `content`.

### Multi-message example

Notebook создает conversation:

```python
messages = [
    {'role': 'user', 'content': 'Hello, who won the FIFA world cup in 2018?'},
    {'role': 'assistant', 'content': 'France won the 2018 FIFA World Cup.'},
    {'role': 'user', 'content': 'Who was the captain?'}
]
```

Затем вызывает `generate_with_multiple_input(messages=messages, max_tokens=100)`.

Видимый output:

- role: `assistant`;
- content отвечает, что captain was `Antoine Griezmann`, после чего текст обрывается на фразе `Griezmann is universally`.

Этот output показывает формат conversational call и то, что ответ может зависеть от модели и ее генерации.

### Integration with OpenAI library

Notebook отдельно показывает, что Together.ai endpoints are OpenAI compatible. Поэтому можно использовать OpenAI library.

Импорты:

```python
from openai import OpenAI, DefaultHttpxClient
import httpx
```

Далее код:

1. получает `base_url = get_proxy_url()`;
2. создает `httpx.HTTPTransport(local_address="0.0.0.0", verify=False)`;
3. создает `DefaultHttpxClient(transport=transport, headers=get_proxy_headers())`;
4. создает `OpenAI` client с `api_key=get_together_key()`, `base_url=base_url` и custom `http_client`.

Комментарий в notebook уточняет:

- SSL bypass нужен только для proxy;
- при запуске через Together endpoint его можно убрать;
- для proxy API key фактически не используется, а для Together endpoint нужно указать Together API key.

Затем notebook использует тот же `messages` example и вызывает:

```python
response = client.chat.completions.create(
    messages=messages,
    model="Qwen/Qwen3.5-9B",
    extra_body={"reasoning": False}
)
```

Видимый `print(response)` показывает объект `ChatCompletion`:

- `finish_reason='stop'`;
- `model='Qwen/Qwen3.5-9B'`;
- `usage` с `completion_tokens=372`, `prompt_tokens=52`, `total_tokens=424`;
- `reasoning_tokens=0`;
- content ответа сообщает, что captain of the France national team during the 2018 FIFA World Cup was Hugo Lloris.

Для доступа к тексту ответа notebook использует:

```python
response.choices[0].message.content
```

Видимый output этой ячейки:

```text
Hugo Lloris was the captain of the France national team during the 2018 FIFA World Cup.
```

### Note on Together.ai Integration for This Course

Notebook поясняет условия Together.ai integration for this course.

Together.ai предоставил credits для использования hosted `LLM` throughout the course. В notebook сказано, что credit limit технически есть, но он установлен примерно в 10 раз выше typical usage, даже при extensive usage.

Два основных типа ошибок:

- `500` и `429 Error` — возникают, когда слишком много calls сделано к системе и она overloaded; обычно решается ожиданием;
- если credits закончатся, пользователь будет notified, и нужно обратиться к команде курса в Discourse community.

Отдельно указано, что grading assignment никогда не использует credits учащегося.

### Integrating Data into an LLM Prompt

Вторая часть notebook показывает, как эффективно include data into a prompt before passing it to an `LLM`.

Для демонстрации используется tiny dataset of houses. Это small dataset как list, содержащий one dictionary per house.

`house_data` содержит два объекта.

Первый house:

- `address`: `123 Maple Street`;
- `city`: `Springfield`;
- `state`: `IL`;
- `zip`: `62701`;
- `bedrooms`: `3`;
- `bathrooms`: `2`;
- `square_feet`: `1500`;
- `price`: `230000`;
- `year_built`: `1998`.

Второй house:

- `address`: `456 Elm Avenue`;
- `city`: `Shelbyville`;
- `state`: `TN`;
- `zip`: `37160`;
- `bedrooms`: `4`;
- `bathrooms`: `3`;
- `square_feet`: `2500`;
- `price`: `320000`;
- `year_built`: `2005`.

### `house_info_layout`

Функция `house_info_layout(houses)` преобразует list of house dictionaries в readable text block.

Шаги функции:

1. создает empty string `layout`;
2. итерируется по `houses`;
3. для каждого house добавляет строку с address, city, state, zip, bedrooms, bathrooms, square feet, price и year built;
4. использует f-strings;
5. добавляет newline character `\n` в конце каждой house line;
6. возвращает `layout`.

Видимый output для `house_data`:

```text
House located at 123 Maple Street, Springfield, IL 62701 with 3 bedrooms, 2 bathrooms, 1500 sq ft area, priced at $230000, built in 1998.
House located at 456 Elm Avenue, Shelbyville, TN 37160 with 4 bedrooms, 3 bathrooms, 2500 sq ft area, priced at $320000, built in 2005.
```

### `generate_prompt`

Функция `generate_prompt(query, houses)` создает prompt for the `LLM`.

Шаги функции:

1. вызывает `house_info_layout(houses)`;
2. сохраняет результат в `houses_layout`;
3. создает hard-coded prompt через triple-quoted f-string;
4. вставляет house information;
5. добавляет строку `Query: {query}`;
6. возвращает `PROMPT`.

В комментарии notebook отмечает, что код modular enough to accept any list of houses. Это позволяет передать subset of the dataset в более complex context, где нужно дать `LLM` только часть информации, а не entire data.

Видимый prompt для query `What is the most expensive house?` содержит instruction:

```text
Use the following houses information to answer users queries.
```

Затем идут две строки с house information и строка:

```text
Query: What is the most expensive house?
```

### Сравнение без augmented prompt и с augmented prompt

Notebook задает query:

```python
query = "What is the most expensive house? And the bigger one?"
```

Сначала вызывается `LLM` без house information:

```python
query_without_house_info = generate_with_single_input(prompt=query, role='user')
```

Затем создается enhanced query:

```python
enhanced_query = generate_prompt(query, houses=house_data)
```

И вызывается `LLM` с этим prompt:

```python
query_with_house_info = generate_with_single_input(prompt=enhanced_query, role='assistant')
```

Видимый output без house information дает generic answer о real estate records и globally reported expensive/biggest houses. Ответ не опирается на `house_data`, потому что эти данные не были переданы модели.

Видимый output с house information отвечает по предоставленным данным:

- most expensive house — `456 Elm Avenue, Shelbyville, TN`, price `$320,000`;
- bigger house — тот же дом, `2,500 sq ft`;
- сравнение проводится с домом на Maple Street, у которого `1,500 sq ft`.

> **Вывод:** augmented prompt с явно включенными structured data дает `LLM` context, достаточный для ответа по конкретному dataset, а не по general world knowledge.

### Ограничения и предпосылки

Для запуска notebook нужны:

- доступ к Coursera proxy или Together.ai endpoint;
- `TOGETHER_API_KEY`, если notebook запускается вне Coursera proxy;
- сетевой доступ к API;
- установленные packages `requests`, `together`, `openai`, `httpx`.

`utils.py` отключает SSL verification (`verify=False`) для proxy calls. В notebook указано, что это нужно для proxy и может быть удалено при direct Together.ai endpoint.

Лабораторная не реализует полноценный `retriever` и не строит `knowledge base`. Она демонстрирует более простую форму prompt augmentation: данные вручную форматируются и вставляются в prompt перед вызовом `LLM`.
