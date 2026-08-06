practice\Module3\ungraded_labs\ungraded_lab_2\C1M3_Ungraded_Lab_2.ipynb

## Конспект по коду

### Назначение notebook

`C1M3_Ungraded_Lab_2.ipynb` («Ungraded Lab: Chunking») даёт практическое знакомство с техниками chunking. Согласно вводной ячейке, chunking разбивает большие тексты на меньшие, управляемые фрагменты, что необходимо для эффективной работы с vector database и языковыми моделями.

Оглавление notebook:

1. Introduction — Importing necessary libraries, Downloading the data.
2. Fixed-size chunking — Example Chunking Code, Chunking with overlap.
3. Variable-size chunking - Recursive Character Splitting — Pseudo-code for variable-size chunking methods, Mixing fixed and variable-sized chunking.
4. Chunking on real data — Getting the data, Chunking the chapters, Loading Chunks into a Vector Database.
5. Searching.
6. Incorporating in a RAG system.

Раздел 1 поясняет: chunking играет важную роль в information retrieval. Например, при построении vector database из коллекции книг разные размеры chunk служат разным целям — каталогизация целых книг как единых векторов помогает выявлять широкие темы, но упускает конкретные детали, тогда как chunking ближе к уровню абзаца или предложения позволяет извлекать конкретную информацию или концепции. У языковых моделей обычно есть ограничение на объём обрабатываемого за раз текста («context window»); chunking помогает удерживать текстовые входы в этих границах, позволяя моделям обрабатывать большие документы (например, романы), разбивая их на меньшие секции.

### Импорты и зависимости

```python
from typing import List
import requests
import re
import weaviate
from weaviate.classes.config import Configure, Property, DataType, Tokenization
from weaviate.util import generate_uuid5
import tqdm
from weaviate.classes.query import Filter
```

Из `utils.py` импортируются `generate_with_single_input`, `suppress_subprocess_output`, `kill_processes_on_ports`. Как и в предыдущей лабораторной, перед `import flask_app` вызывается `kill_processes_on_ports([5000, 8080, 8097, 50050, 50051])` с тем же предупреждением про риск для активного ядра notebook при повторном запуске ячейки. Visible output этой ячейки идентичен по характеру предыдущей лабораторной работе (служебная ошибка кэширования файла и лог запуска Flask-сервера).

### 1.2 Загрузка данных

Используется часть [Pro Git book](https://git-scm.com/book/en/v2) — глава «What is Git?»:

```python
url = "https://raw.githubusercontent.com/progit/progit2/main/book/01-introduction/sections/what-is-git.asc"
source_text = requests.get(url).text
```

Печать `print(f"There are about {len(source_text.split())} words...")` — visible output: *«There are about 1403 words in this chapter. Depending on how your LLM tokenizes words, you'd expect roughly 1824 tokens.»*

### 2. Fixed-size chunking

Markdown поясняет: fixed-size chunking означает разбиение текста на части одного размера (например, по 100 слов или по 200 символов) — популярный метод благодаря простоте и хорошей работе на практике. Единицами могут быть слова, символы или токены; число единиц в каждой части одинаково (до максимального предела), между частями может быть опциональное перекрытие.

#### 2.1 `get_chunks_fixed_size(text, chunk_size)`

```python
def get_chunks_fixed_size(text: str, chunk_size: int) -> List[str]:
    text_words = text.split()
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[i: i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks
```

Функция режет текст на слова и группирует их по `chunk_size` слов в chunk (без перекрытия).

Пример: `get_chunks_fixed_size(source_text, chunk_size=100)` — visible output: `15` chunks; первые три chunks выведены полностью (начинаются с `"[[what_is_git_section]] === What is Git?..."`).

#### 2.2 `get_chunks_fixed_size_with_overlap(text, chunk_size, overlap_fraction)`

```python
def get_chunks_fixed_size_with_overlap(text: str, chunk_size: int, overlap_fraction: float) -> List[str]:
    text_words = text.split()
    overlap_int = int(chunk_size * overlap_fraction)
    chunks = []
    for i in range(0, len(text_words), chunk_size):
        chunk_words = text_words[max(i - overlap_int, 0): i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks
```

Функция аналогична предыдущей, но каждый chunk (кроме первого) захватывает дополнительно `overlap_int = chunk_size * overlap_fraction` слов из конца предыдущего диапазона.

Пример для `overlap_fraction=0.2` и `chosen_size in [5, 25, 100]`. Visible output:

- размер 5 → 281 chunks (например, chunk 1: `"[[what_is_git_section]] === What is Git?"`, chunk 2: `"Git? So, what is Git in"`);
- размер 25 → 57 chunks;
- размер 100 → 15 chunks.

Markdown-вывод после примера: маленькие chunks очень детальны, но могут не содержать достаточно информации, чтобы быть полезными для поиска; более крупные chunks начинают содержать больше информации (по объёму похожи на типичный абзац); по мере дальнейшего роста размера связанные с chunks векторные embeddings становятся всё более общими (generalized) и в итоге перестают быть эффективными для информационного поиска.

### 3. Variable-size chunking — Recursive Character Splitting

В отличие от fixed-size chunking, здесь размер каждого chunk — результат, а не отправная точка: текст делится по конкретному маркеру (например, разрыв предложения/абзаца или структурный элемент вроде markdown-заголовка).

#### 3.1 Псевдокод для variable-size chunking

- **`get_chunks_by_paragraph(source_text)`** — разбивает текст по двойному переводу строки: `return source_text.split("\n\n")`.
- **`get_chunks_by_asciidoc_sections(source_text)`** — разбивает по маркерам AsciiDoc-секций: `return source_text.split("\n==")`.

Пример сравнения обоих маркеров: маркер `'\n\n'` даёт 31 chunk, маркер `'\n=='` даёт 7 chunks (полные примеры первых трёх chunks для каждого варианта приведены в notebook как `repr(...)`, показывая точное содержимое строк, включая символы `\n`).

Markdown отмечает проблему: при простом chunking по маркеру заголовки часто становятся отдельными chunks — что не всегда желательно. На практике можно использовать смешанную стратегию, присоединяя короткие chunks (например, заголовки) к следующему chunk.

#### 3.2 Смешение fixed- и variable-size chunking: `mixed_chunking(source_text)`

```python
def mixed_chunking(source_text):
    chunks = source_text.split("\n==")
    new_chunks = []
    chunk_buffer = ""
    min_length = 25
    for chunk in chunks:
        new_buffer = chunk_buffer + chunk
        new_buffer_words = new_buffer.split(" ")
        if len(new_buffer_words) < min_length:
            chunk_buffer = new_buffer
        else:
            new_chunks.append(new_buffer)
            chunk_buffer = ""
    if len(chunk_buffer) > 0:
        new_chunks.append(chunk_buffer)
    return new_chunks
```

Логика: текст сначала делится по маркеру AsciiDoc-секции (`\n==`); затем накопительный буфер (`chunk_buffer`) объединяет соседние части, пока их суммарная длина в словах не достигнет `min_length = 25`; только тогда накопленный текст фиксируется как отдельный chunk. Это гарантирует, что заголовки (короткие фрагменты) не остаются отдельными chunks, а прикрепляются к следующему содержательному фрагменту.

Пример: `mixed_chunking(source_text)` — первые три chunks в выводе начинаются с заголовка, слитого с последующим текстом секции (например, chunk 1 начинается с `"[[what_is_git_section]]= What is Git?\n\n..."`).

### 4. Chunking на реальных данных

#### 4.1 Получение данных: `get_book_text_objects()`

Функция обращается к GitHub API репозитория `progit/progit2`, получает список файлов секций для двух глав (`/01-introduction/sections`, `/02-git-basics/sections`), скачивает содержимое каждого файла и формирует список объектов `{"body": ..., "chapter_title": ..., "filename": ...}`. Вызов `book_text_objs = get_book_text_objects()` возвращает список из 14 элементов (по числу секций/файлов в этих двух главах). `book_text_objs[0].keys()` — visible output: `dict_keys(['body', 'chapter_title', 'filename'])`.

#### 4.2 Chunking глав: `build_chunk_objs(book_text_obj, chunks)`

Функция превращает список chunks в список словарей-объектов с полями `chapter_title`, `filename`, `chunk` (сам текст chunk), `chunk_index` (порядковый номер chunk).

К каждой из 14 секций применяются 4 стратегии chunking:

```python
for strategy_name, chunks in [
    ["fixed_size_25", get_chunks_fixed_size_with_overlap(text, 25, 0.2)],
    ["fixed_size_100", get_chunks_fixed_size_with_overlap(text, 100, 0.2)],
    ["para_chunks", get_chunks_by_paragraph(text)],
    ["para_chunks_min_25", mixed_chunking(text)]
]:
```

Результаты накапливаются в словаре `chunk_obj_sets` с ключами `fixed_size_25`, `fixed_size_100`, `para_chunks`, `para_chunks_min_25`.

#### 4.3 Загрузка chunks в vector database

Раздел поясняет, что здесь работа идёт с уже предзагруженной (pre-loaded) коллекцией, чтобы сэкономить время, и рекомендует пройти ungraded lab по Weaviate API для лучшего понимания процесса.

Подключение к embedded Weaviate:

```python
collection_base = os.getenv('COLLECTION_M3', './')
persistence_path = os.path.join(collection_base, 'ungraded_lab_2')

with suppress_subprocess_output():
    try:
        client = weaviate.connect_to_embedded(
            persistence_data_path=persistence_path,
            environment_variables={
                "ENABLE_API_BASED_MODULES": "true",
                "ENABLE_MODULES": 'text2vec-transformers',
                "TRANSFORMERS_INFERENCE_API": "http://127.0.0.1:5000/",
            }
        )
    except Exception as e:
        ...
        client = weaviate.connect_to_local(port=8079, grpc_port=50050)
        ...
```

Код содержит запасные (fallback) варианты подключения через `weaviate.connect_to_local` на альтернативных портах, если embedded-подключение не удаётся.

Создаётся коллекция `chunking_example` со свойствами `chunk` (TEXT), `chapter_title` (TEXT), `filename` (TEXT), `chunking_strategy` (TEXT, с `tokenization=Tokenization.FIELD` — то есть всё значение поля рассматривается как единый токен), `chunk_index` (INT); вектор конфигурируется через `Configure.NamedVectors.text2vec_transformers(name="vector", vectorize_collection_name=False, inference_url="http://127.0.0.1:5000")`.

Отдельная markdown-ячейка (в предупреждающем стиле, alert box) показывает код вставки данных в коллекцию (`collection.batch.fixed_size(batch_size=1, concurrent_requests=20)`, итерация по `chunk_obj_sets`, `generate_uuid5(chunk_obj)`), но явно отмечает, что этот код **не должен запускаться**, поскольку коллекция уже провекторизована заранее.

Проверка числа объектов через `collection.aggregate.over_all()` с фильтрами по `chunking_strategy` — visible output:

```
Total count: 1487
Object count for fixed_size_25: 672
Object count for fixed_size_100: 173
Object count for para_chunks: 549
Object count for para_chunks_min_25: 93
```

### 5. Поиск (Searching)

Раздел исследует semantic search с разными размерами chunk, чтобы визуализировать влияние размера на information retrieval.

**Пример 1** — широкий запрос `search_string = "history of git"`: для каждой стратегии chunking выполняется `collection.query.near_text(search_string, filters=where_filter, limit=2)`, фильтруя по `chunking_strategy`. (Полный вывод этой ячейки в notebook отмечен как слишком большой для включения.) Комментарий после примера поясняет: более длинные chunks работают лучше для такого широкого запроса — 25-словные chunks могут быть семантически близки к запросу, но не дают достаточно контекста, чтобы реально расширить понимание темы читателем, тогда как chunks по абзацам (особенно `para_chunks_min_25`) дают исчерпывающую информацию об истории Git.

**Пример 2** — более узкий запрос `search_string = "how to add the url of a remote repository"`. Visible output приводит извлечённые chunks для всех четырёх стратегий:

- `fixed_size_25` — короткие фрагменты, один из которых прямо содержит команду `git remote add <shortname> <url>`;
- `fixed_size_100` — более длинные фрагменты с полным примером команд `git remote`, `git fetch`;
- `para_chunks` — короткие абзацы, включая отдельный chunk-заголовок `"==== Adding Remote Repositories"`;
- `para_chunks_min_25` — крупные, насыщенные секции целиком, включая заголовок, слитый с содержанием.

Markdown-вывод после примера: для такого конкретного запроса 25-словные chunks оказываются более полезными — благодаря узости вопроса Weaviate смог точно указать на chunk с наиболее релевантным фрагментом (командой добавления remote-репозитория). Хотя другие наборы результатов тоже содержат эту информацию, важно учитывать, как результат будет использоваться и отображаться — более длинные результаты могут требовать больше когнитивных усилий пользователя для извлечения релевантной информации.

### 6. Встраивание в RAG-систему

Задаётся шаблон промпта:

```python
PROMPT = "Using this information and only this information, please explain {search_string} in a few short points.\nContext: {context}"
```

Чтобы компенсировать разное число слов в chunks разных стратегий, задаётся число извлекаемых chunks для каждой стратегии:

```python
n_chunks_by_strat = dict()
n_chunks_by_strat['fixed_size_25'] = 8
n_chunks_by_strat['para_chunks'] = 8
n_chunks_by_strat['fixed_size_100'] = 2
n_chunks_by_strat['para_chunks_min_25'] = 2
```

Для запроса `"history of git"` и каждой стратегии: извлекаются chunks (`collection.query.near_text(...)` с фильтром по стратегии и `limit=n_chunks_by_strat[...]`), объединяются в `context_string`, подставляются в `PROMPT`, промпт передаётся в `generate_with_single_input(prompt, role='assistant')`.

Visible output — по одному сгенерированному ответу LLM на каждую из четырёх стратегий chunking, каждый в виде списка пунктов по истории Git:

- **`fixed_size_25`** — фрагментарный, местами неточный ответ, ссылающийся на отдельные коммиты (например, коммит от Scott Chacon 15 марта 2008 года) вместо связной истории происхождения Git;
- **`fixed_size_100`** — связная хронология: истоки в 1991–2002 годах, эпоха BitKeeper (2002), разрыв отношений в 2005 году, ставший катализатором создания Git, взросление инструмента;
- **`para_chunks`** — краткий ответ, сфокусированный на дате рождения Git (2005) и одном примере коммита от 15 марта 2008 года (Scott Chacon);
- **`para_chunks_min_25`** — наиболее полный и точный ответ: происхождение в поддержке ядра Linux, переход на BitKeeper в 2002, разрыв в 2005, создание Git Линусом Торвальдсом, цели дизайна (скорость, простота, поддержка нелинейной разработки, полная распределённость, эффективная работа с большими проектами), последующее взросление инструмента.

В конце клиент закрывается: `client.close()`.

### Helper-файл `utils.py`

Файл во многом аналогичен `utils.py` из `ungraded_lab_1` (та же реализация `generate_with_single_input`, `generate_with_multiple_input`, `get_proxy_url`, `get_proxy_headers`, `get_together_key`, `kill_processes_on_ports`, `suppress_subprocess_output`, `print_object_properties`, `SentenceTransformer`-модель `BAAI/bge-base-en-v1.5`), но с двумя заметными отличиями:

- `print_object_properties` сортирует ключи словаря перед печатью (`keys = list(obj.keys()); keys.sort()`), а для списков рекурсивно вызывает саму себя для каждого элемента (в `ungraded_lab_1` — отдельная копия логики форматирования внутри цикла, без сортировки ключей);
- в файле присутствует функция **`display_widget(llm_call_func, semantic_search_retrieve, bm25_retrieve, hybrid_retrieve, semantic_search_with_reranking)`**, которая строит расширенный интерактивный виджет сравнения пяти конфигураций поиска (`Semantic Search`, `BM25 Search`, `Hybrid Search`, `Semantic Search with Reranking`, `Without RAG`) с выпадающим списком `Rerank Property` (`title`/`chunk`) и полем запроса, предзаполненным примером *«Tell me about United States and Brazil's relationship over the course of 2024...»*. Эта функция в показанных ячейках самого `C1M3_Ungraded_Lab_2.ipynb` не вызывается — судя по сигнатуре (`semantic_search_with_reranking`, `hybrid_retrieve`), она рассчитана на более широкий набор retrieval-функций, чем определены в этой лабораторной работе, и, по всей видимости, относится к материалу, отрабатываемому в графируемом задании модуля.

### Ограничения и предпосылки

Notebook обращается к внешним сетевым ресурсам: скачивает текст главы книги напрямую с GitHub (`raw.githubusercontent.com`) и список файлов через GitHub API (`api.github.com`), поэтому требует доступа в интернет. Для работы embedded Weaviate и локального Flask-сервера нужны свободные порты (`5000, 8080, 8097, 50050, 50051`, а также `8079`), которые заранее освобождаются через `kill_processes_on_ports`; предусмотрен fallback на `weaviate.connect_to_local` при сбое embedded-подключения. Персистентное хранилище коллекции задаётся через переменную окружения `COLLECTION_M3` (по умолчанию `'./'`) и подпапку `ungraded_lab_2`. Для генерации ответов LLM (`generate_with_single_input`) нужен доступ к Together.ai или прокси-серверу Coursera. Как и в предыдущей лабораторной работе, `utils.py` использует локально кэшированную модель `SentenceTransformer("BAAI/bge-base-en-v1.5", cache_folder=".models")`. В рамках конспекта код изучался статически, без запуска notebook, Flask-сервера или отдельных ячеек.