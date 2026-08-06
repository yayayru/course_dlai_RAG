practice\Module4\ungraded_labs\ungraded_lab_2\C1M4_Ungraded_Lab_2.ipynb

## Конспект по коду

### Назначение

Ноутбук `C1M4_Ungraded_Lab_2.ipynb` (в репозитории фактически находится по пути `practice/Module4/ungraded_labs/ungraded_labs_2/C1M4_Ungraded_Lab_2.ipynb`) — необязательная (`ungraded`) лабораторная работа на тему prompt engineering. Цели работы:

1. Научиться заставлять LLM генерировать конкретные выводы, например, разметку (`labeling`) предложения.
2. Делать вызов LLM с разными параметрами в зависимости от природы задачи промпта.
3. Заставить LLM возвращать конкретный тип объекта в своём ответе, например, JSON.

### Импорты и зависимости

Из `utils` импортируются `generate_with_single_input`, `generate_with_multiple_input`, `generate_params_dict` — те же функции вызова LLM через прокси DLAI/Together, что и в первой ungraded lab модуля (см. [04_code_Exploring_LLM_capabilities.md](04_code_Exploring_LLM_capabilities.md)). Модель по умолчанию — `Qwen/Qwen3.5-9B`.

### Раздел 1 — Text Classification with LLMs

Демонстрируется практическое применение LLM как классификатора текста. Рассматривается сценарий: чат-бот для компании, продающей спортивную одежду и пищевые добавки, должен решать, относится ли запрос к одежде (`outfit`) или к питанию (`nutritional`), чтобы направить запрос в правильную базу данных.

Рекомендации по построению такого промпта:

1. Быть точным — явно объяснить, что именно должна сделать и вывести модель.
2. Добавлять примеры с ожидаемым результатом.
3. Добавлять «пограничные» (edgy) примеры — те, что могут оказаться сложными для LLM.

Функция `check_if_outfit_or_supplement(query)` строит промпт с определениями категорий `nutritional`/`outfit`, шестью примерами запрос→ожидаемая метка, и инструкцией ответить одним словом.

Демонстрация:

- Одиночный вызов: `generate_with_single_input(check_if_outfit_or_supplement(query), max_tokens=2)` для запроса про витамины → `{'role': 'assistant', 'content': 'Nutritional'}`.
- Проверка на наборе из 9 запросов (`queries` со списком словарей `{"query": ..., "label": ...}`) с цветным выводом (ANSI-коды `GREEN`/`RED`) для сравнения фактического и ожидаемого результата — во всех 9 случаях, показанных в выводе ноутбука, метка LLM совпала с ожидаемой (например: *«Where can I buy whey protein?»* → `Nutritional`, *«Latest fashion for women's dresses»* → `Outfit` и т.д.).

### Раздел 2 — Parameter Setting Based on Tasks

Демонстрируется, как настраивать параметры вызова LLM в зависимости от природы задачи: технические запросы (`technical`) выигрывают от низкой случайности, творческие (`creative`) — от более высокой.

- `decide_if_technical_or_creative(query)` — строит промпт, классифицирующий запрос как `'creative'` или `'technical'`, вызывает `generate_with_single_input(PROMPT)` и возвращает `result['content']` как метку.
  - Демонстрация: *«What is Pi-hole?»* → `technical`; *«Suggest to me three places to visit in South America»* → `creative`.
- `answer_query(query)` — сначала определяет метку через `decide_if_technical_or_creative(query).lower()`, затем выбирает параметры генерации:
  - `technical` → `generate_params_dict(query, temperature=0, top_p=0.1)` (точность, низкая случайность);
  - `creative` → `generate_params_dict(query, temperature=1.1, top_p=0.4)` (вариативность, более высокая случайность);
  - иначе (неопределённая классификация) → `generate_params_dict(query, temperature=0.5, top_p=0.5)` (нейтральные параметры).
  - Затем вызывает `generate_with_single_input(**kwargs)` и возвращает `response['content']`.
  - Демонстрация на тех же двух запросах: для *«What is Pi-hole?»* модель даёт развёрнутое техническое объяснение работы Pi-hole (DNS-фильтрация рекламы, network-wide ad blocker); для *«Suggest to me three places to visit in South America»* — творческий список из трёх мест (Machu Picchu в Перу, Галапагосские острова в Эквадоре, водопады Игуасу на границе Аргентины и Бразилии) с описаниями и лучшим временем для посещения.

### Раздел 3 — Guiding the LLM to Output Specific Objects

Рассматривается сценарий автоматизации умного дома: пользовательский запрос нужно перевести в структурированный JSON, понятный серверу домашней автоматизации. Формат для каждого действия:

```json
{
  "room": "room where the action will occur",
  "object_id": "unique identifier of the targeted object",
  "object_name": "name of the object",
  "action": "action to be performed",
  "parameters": "dictionary containing action-specific parameters"
}
```

#### 3.1 «Старомодный» способ (детальный промпт)

Функция `generate_system_call(command)` строит развёрнутый промпт, включающий:

- список доступных устройств и действий (Light, Automatic Lock, Sound System/Speaker, TV, Air Conditioner) с допустимыми параметрами для каждого;
- список комнат и устройств в них с ID (Office, Living Room, Kitchen, Bedroom, Bathroom);
- несколько примеров «команда → JSON»;
- инструкцию всегда выводить список JSON-объектов, даже если команда одна, и не выводить ничего, кроме требуемой структуры.

Вызывает `generate_params_dict(PROMPT, temperature=0.4, top_p=0.1)`, затем `generate_with_single_input(**kwargs)`, возвращает `result['content']`.

Отмечается важность двойных фигурных скобок `{{ }}` внутри f-строки Python, чтобы JSON-примеры внутри промпта не интерпретировались как f-string плейсхолдеры.

Демонстрация:

- *«Play a chill playlist very loud»* → корректный JSON с одним объектом: `living_room_speaker`, `action: "play"`, `parameters: {"playlist_style": "chill", "volume": "100"}`.
- *«I'm tired today, please make my living room a very cozy ambient, it is really cold today too.»* → корректный JSON с двумя объектами: `living_room_light` (`turn on`, тёплый белый свет, 60% интенсивности) и `living_room_airconditioner` (`set temperature`, 24 градуса, низкая скорость вентилятора).

#### 3.2 Использование параметра структурированного вывода LLM (Pydantic)

Показано, что можно заставить LLM выводить JSON, используя `Pydantic` для валидации структуры данных — гарантируя, что вывод всегда является корректным JSON.

- Определяется схема `VoiceNote(BaseModel)` с полями `title: str`, `summary: str`, `actionItems: list[str]`, каждое поле снабжено `Field(description=...)`.
- Формируется список `messages` с `system`-сообщением («The following is a voice message transcript. Only answer in JSON.») и `user`-сообщением с текстом транскрипта голосовой заметки (про утренние сборы, завтрак и проверку почты).
- Формируется `response_format = {"type": "json_schema", "schema": VoiceNote.model_json_schema()}`.
- Вызов `generate_with_multiple_input(messages, response_format=response_format)`, затем `json.loads(result['content'])` и вывод через `json.dumps(..., indent=2)`.

Результат в выводе ноутбука — корректный JSON-объект с полями `title` («Morning Routine and Breakfast Plans»), `summary` (краткое описание) и `actionItems` (список из трёх пунктов: приготовить яичницу и тосты, заварить кофе, проверить почту на срочные письма).

### Ограничения и предпосылки

- Для работы ноутбука требуется доступ к LLM через прокси DLAI (`https://proxy.dlai.link/coursera_proxy/together`) либо собственный `TOGETHER_API_KEY` в переменных окружения — как и в первой ungraded lab модуля.
- Модель по умолчанию — `Qwen/Qwen3.5-9B`.
- Для раздела 3.2 требуется установленная библиотека `pydantic` (импортируются `BaseModel`, `validator`, `conint`, `Field` из `pydantic`, а также `Literal`, `Union`, `Optional`, `List` из `typing`).
- Изображение `images/toc.png` используется в markdown-ячейке для иллюстрации навигации по Table of Contents.