См. practice\Module2\ungraded_labs\ungraded_lab_2\C1M2_Ungraded_Lab_2.ipynb

## Конспект по коду

### Назначение notebook

`C1M2_Ungraded_Lab_2.ipynb` («Ungraded Lab - Retrieval Metrics») посвящён извлечению и анализу метрик для RAG-системы. Согласно вводной markdown-ячейке, цель — оценить компонент retrieval, вычисляя метрики precision и recall (в тексте вводной ячейки также упомянуты «context precision» и «context recall», хотя далее по коду фактически реализуются и используются только Precision@K и Recall@K).

Заявленные цели лабораторной работы:

- научиться вычислять метрики precision и recall;
- научиться применять эти метрики в information retrieval;
- поработать с конкретным датасетом, чтобы протестировать возможности semantic-based поиска.

Указано, что используется библиотека `sentence-transformers` для превращения текста в embeddings, что позволяет эффективно вычислять сходство; для расчёта retrieval-метрик нужен размеченный (labeled) датасет.

Оглавление notebook:

1. The dataset — Preprocessing and Vectorizing Data, Basic functions for retrieve.
2. Retrieving metric — Precision, Recall, Computing metrics over some queries.

Во вводном разделе (Introduction) поясняется: чтобы эффективно оценить производительность, нужен размеченный датасет — такой, где известны ответы на конкретные запросы, — что позволяет сравнивать эти ответы с результатами, которые выдаёт RAG-система. В этой лабораторной работе используется предварительно размеченный датасет, а фокус сделан на метриках Precision и Recall.

### Импорты и зависимости

```python
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
```

Отдельный helper-файл `utils.py` в этой папке отсутствует — все функции (препроцессинг, cosine similarity, retrieval, метрики) реализованы прямо в ячейках notebook.

### 1. Датасет: 20 Newsgroups

Используется классический текстовый датасет [20 Newsgroups](https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html) с текстами на разные темы и размеченными категориями, загружаемый через `sklearn.datasets`:

```python
from sklearn.datasets import fetch_20newsgroups

newsgroups_train = fetch_20newsgroups(subset='train', shuffle=True, random_state=42, data_home='./dataset')

df = pd.DataFrame({
    'text': newsgroups_train.data,
    'category': newsgroups_train.target
})
```

Visible output:

```
Dataset Size: (11314, 2)
Number of Categories: 20
Categories: ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles',
'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med', 'sci.space',
'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast', 'talk.politics.misc',
'talk.religion.misc']
```

То есть датасет содержит 11314 документов, распределённых по 20 категориям. Печать первой записи датасета (`df['text'][0]`) показывает письмо про автомобиль неизвестной модели с категорией `rec.autos`.

### 1.1 Препроцессинг и векторизация данных

В этом разделе текст очищается, а затем векторизуется предобученной моделью `sentence-transformers`. Используется модель `BAAI/bge-base-en-v1.5` — та же модель, что и в предыдущей лабораторной работе про embeddings. Отмечено, что, чтобы сэкономить время, датасет заранее превращён в embeddings, поэтому в этой лабораторной работе модель используется только для векторизации промптов (запросов).

```python
model_name = "BAAI/bge-base-en-v1.5"
model = SentenceTransformer(os.path.join(os.environ['MODELS'], model_name))

embedding_vectors = joblib.load('embeddings.joblib')
```

`len(embedding_vectors)` — visible output: `11314` (по одному embedding-вектору на документ датасета).

### 1.2 Базовые функции для retrieval

Реализуется базовый механизм RAG через similarity search по предвычисленным embeddings на основе cosine similarity.

- **`preprocess_text(text)`** — минимальный препроцессинг: убирает начальные/конечные пробельные символы (`text.strip()`).
- **`cosine_similarity(v1, array_of_vectors)`** — собственная реализация (независимая от одноимённой функции из предыдущей лабораторной работы), безопасно обрабатывает как `numpy`-массивы, так и PyTorch-тензоры (переносит их на CPU через `.detach().cpu().numpy()`, если есть атрибут `detach`). Поддерживает два случая: `array_of_vectors` — один вектор (1D, возвращает единственное `float`-значение) или матрица векторов (2D, возвращает список значений через матричное умножение `A @ v1`, делённое на произведение норм; при нулевом знаменателе результат безопасно приравнивается к `0.0` через `np.errstate` и явную маску).
- **`top_k_greatest_indices(lst, k)`** — нумерует список, сортирует пары `(индекс, значение)` по убыванию значения и возвращает первые `k` индексов.

#### `retrieve_documents(query, embeddings, model, top_k=5)`

Функция:

1. очищает `query` через `preprocess_text`;
2. кодирует его моделью (`model.encode(query_clean, convert_to_tensor=False)`), приводя к `np.float32`;
3. для каждого документа из `embeddings` приводит его к `numpy`-массиву и считает `cosine_similarity` с вектором запроса;
4. находит `top_k` индексов документов с наибольшим сходством через `top_k_greatest_indices`;
5. печатает запрос, и для каждого найденного документа — первые 200 символов текста и его категорию.

Пример:

```python
example_query = "space exploration"
retrieve_documents(example_query, embedding_vectors, model, top_k=2)
```

Visible output — два документа из категории `sci.space`: письмо про «End of the Space Age?» (San Diego Supercomputer Center) и про «Space class for teachers near Chicago» (Motorola).

### 2. Метрики извлечения

Раздел рассматривает две наиболее распространённые метрики для retrieval-систем: Precision@K и Recall@K.

#### 2.1 Precision@K

Precision@K оценивает релевантность топ-K извлечённых документов: доля релевантных документов среди топ-K результатов.

$$\text{Precision@K} = \frac{\text{Number of Relevant Documents in Top K}}{\text{K}}$$

```python
def precision_at_k(relevant_count, k):
    if relevant_count < 0 or k < 0:
        raise ValueError("All input values must be non-negative.")
    if k == 0:
        return 0.0
    return relevant_count / k
```

Функция принимает число релевантных документов среди топ-K (`relevant_count`) и `k`; выбрасывает `ValueError` при отрицательных значениях; возвращает `0.0`, если `k == 0`.

#### 2.2 Recall@K

Recall@K оценивает способность retrieval-системы найти все релевантные документы датасета среди топ-K результатов: доля релевантных документов среди топ-K относительно общего числа релевантных документов во всём корпусе.

$$\text{Recall@K} = \frac{\text{Number of Relevant Documents in Top K}}{\text{Total Number of Relevant Documents in Corpus}}$$

```python
def recall_at_k(relevant_count, total_relevant):
    if relevant_count < 0 or total_relevant < 0:
        raise ValueError("All input values must be non-negative.")
    if total_relevant == 0:
        return 0.0
    return relevant_count / total_relevant
```

Аналогично: `ValueError` при отрицательных значениях, `0.0`, если `total_relevant == 0`.

#### 2.3 Вычисление метрик по набору запросов

Задаётся список из 10 тестовых запросов с «желаемой» категорией (`desired_category`) для каждого — например, `"advancements in space exploration technology"` → `sci.space`, `"real-time rendering techniques in computer graphics"` → `comp.graphics`, `"NHL playoffs and team performance statistics"` → `rec.sport.hockey`, и так далее (всего 10 пар запрос/категория, покрывающих разные темы датасета: наука, спорт, техника, политика).

**`compute_metrics(queries, embeddings, model, top_k=5)`**:

1. приводит все embeddings к единой `numpy`-матрице `E` формы `(N, D)`;
2. для каждого запроса из `queries` — кодирует его, вычисляет cosine similarity со всеми документами (`cosine_similarity(q_emb, E)`), берёт `top_k` индексов через `top_k_greatest_indices`;
3. получает категории извлечённых документов (`retrieved_categories`);
4. считает `relevant_in_top_k` — сколько из `top_k` документов относятся к `desired_category`;
5. считает `total_relevant_in_corpus` — сколько документов во всём датасете `df` относятся к `desired_category`;
6. вычисляет `precision_at_k(relevant_in_top_k, top_k)` и `recall_at_k(relevant_in_top_k, total_relevant_in_corpus)`;
7. возвращает список словарей `{"query": ..., "precision@k": ..., "recall@k": ...}` для всех запросов.

Метрики вычисляются для трёх значений `K`: `k_values = [5, 20, 50]`.

Visible output (сокращённо, ключевые значения):

- **K=5**: у 8 из 10 запросов Precision@5 = 1.00; у запроса про политику (`"historical influence of politics on society"`) Precision@5 = 0.40; у запроса про Windows — 0.80. Recall@5 у всех запросов ≈ 0.01 (кроме политики — 0.00).
- **K=20**: Precision снижается для части запросов — например, `"electronics in computing devices"` до 0.80, `"Windows operating system"` до 0.65, `"motorcycles maintenance"` до 0.95; Recall@20 у большинства ≈ 0.03 (у политики — 0.02).
- **K=50**: Precision снижается ещё сильнее — `"computer graphics"` до 0.88, `"electronics in computing devices"` до 0.66, `"Windows operating system"` до 0.60; запрос про политику остаётся самым слабым (Precision в диапазоне 0.50–0.52 на всех K); Recall@50 в диапазоне 0.05–0.08.

### Интерпретация результатов (markdown-ячейка после вывода)

Notebook подробно разбирает компромисс между precision и recall (`precision-recall tradeoff`) при изменении K с 5 на 20 и 50:

- **Тренд Precision@K** — как правило, снижается с ростом K: при K=5 большинство запросов показывают очень высокую точность (0.80–1.00), при K=20 и K=50 точность падает для части запросов по мере включения менее релевантных документов.
- **Тренд Recall@K** — растёт с ростом K: при K=5 recall очень низкий (~0.01, то есть ~1% всех релевантных документов найдено); при K=20 recall утраивается до ~0.03; при K=50 recall достигает 0.05–0.08.

Ключевые наблюдения, сформулированные в notebook:

1. Компромисс очевиден: при увеличении K находится больше релевантных документов (выше recall), но ценой включения части нерелевантных (ниже precision).
2. Некоторые запросы сложнее других: запрос про «historical influence of politics on society» стабильно показывает самую низкую precision (0.40–0.52), что говорит о семантической неоднозначности запроса либо о том, что категорию `talk.politics.misc` труднее отличить от смежных категорий.
3. Для RAG-систем диапазон K=5–20 часто оптимален: он даёт высокую precision (большинство извлечённых документов релевантны), сохраняя при этом приемлемый размер контекста для LLM. Хотя recall низкий, цель — найти *наиболее релевантные* документы, а не *все* релевантные.
4. Recall остаётся относительно низким даже при K=50: это ожидаемо, поскольку каждая категория содержит сотни документов (500–600), поэтому извлечение 50 документов покрывает лишь ~8–10% всех релевантных документов; для высокого recall потребовались бы K в сотнях, что резко ухудшило бы precision и было бы непрактично для RAG-приложений.

### Ограничения и предпосылки

Для работы notebook требуются: локальный/кэшированный экземпляр модели `BAAI/bge-base-en-v1.5`, доступный по пути `os.environ['MODELS']/BAAI/bge-base-en-v1.5` (переменная окружения `MODELS` должна быть установлена); файл `embeddings.joblib` с предвычисленными embeddings всех 11314 документов; папка `./dataset`, куда `fetch_20newsgroups` скачивает (или откуда читает уже скачанный) датасет `20 Newsgroups`. Зависимости: `pandas`, `sentence_transformers`, `numpy`, `matplotlib`, `joblib`, `scikit-learn` (`sklearn.datasets.fetch_20newsgroups`). В рамках конспекта код изучался статически, без запуска notebook или отдельных ячеек.
