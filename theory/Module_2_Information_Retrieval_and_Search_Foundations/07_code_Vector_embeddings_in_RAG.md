См. practice\Module2\ungraded_labs\ungraded_lab_1\C1M2_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение notebook

`C1M2_Ungraded_Lab_1.ipynb` («Ungraded Lab - Vector Embeddings in RAG») — практическая лабораторная работа про `vector embeddings`. Согласно вводной markdown-ячейке, в ней рассматривается:

- как использовать vector embeddings для поиска и понимания контекстной информации;
- основы cosine similarity и Euclidean distance для сравнения embeddings;
- практическая реализация embeddings с помощью transformer-based модели;
- визуализация высокоразмерных embeddings с помощью PCA.

Оглавление notebook:

1. Introduction — A Bit of Theory, The framework.
2. The Embedding Model — Introduction, Loading the model, Embeddings in Practice, Visualizing Word Embeddings.
3. Embeddings and Input Size — An Example.

### Теория (раздел 1)

В markdown поясняется роль vector embeddings в RAG:

1. **Powering Search** — embeddings превращают слова и предложения в позиции в векторном пространстве, отражающие смысл (`capturing meaning`); при получении промпта он тоже превращается в вектор, и через сравнение сходства (similarity) с другими векторами в базе находятся тексты, наиболее близкие по смыслу.
2. **Understanding Context** — embeddings помогают учитывать контекст слов в запросе, обеспечивая нахождение наиболее подходящей информации, и позволяют гибко улавливать детали, которые иначе могли бы быть упущены.

Раздел 1.1 «A Bit of Theory» приводит формулы двух мер расстояния между вектором запроса `q` и вектором документа `d_i`:

- **Cosine Similarity** — оценивает, насколько близки два вектора по углу между ними: `Cosine Similarity(q, d_i) = (q · d_i) / (‖q‖ ‖d_i‖)`. Значение, близкое к 1, означает, что векторы (а значит, и тексты) очень похожи.
- **Euclidean Distance** — вычисляет «прямолинейное» расстояние между двумя векторами в пространстве embeddings: `Euclidean Distance(q, d_i) = sqrt(Σ(q_j − d_ij)²)`. Меньшие расстояния означают более тесно связанный контент.

Раздел 1.2 «The framework» описывает общий алгоритм поиска по векторам:

1. **Create the embedding** — с помощью embedding-метода превратить запрос и документы в векторы.
2. **Metric measurement** — с помощью метрики сходства определить, насколько близок каждый документ к запросу.
3. **Sorting** — отсортировать документы по их similarity-баллу и выбрать несколько лучших как наиболее релевантные; при этом отмечается, что для одних метрик более высокий балл означает большее сходство (как у cosine similarity), а для других — более низкий балл означает большее сходство (как у Euclidean distance).

### Импорты и зависимости

В самом notebook:

```python
import numpy as np
import os
from utils import (
    display_widget,
    plot_vectors
)
```

Далее, при загрузке модели, импортируется `from sentence_transformers import SentenceTransformer`.

`utils.py` дополнительно импортирует: `requests`, `json`, `typing.List`/`Dict`, `matplotlib.pyplot`, `sklearn.decomposition.PCA`, виджеты `ipywidgets` (`Text`, `Button`, `VBox`, `Output`, `Layout`, `HTML`), `IPython.display`, `matplotlib.cm`, `matplotlib.colors.ListedColormap`, `adjust_text` из `adjustText`, `io.BytesIO`, `base64`, `Together` из `together`.

### Функции расстояния (реализованы прямо в notebook)

В комментарии подчёркивается, что в этой лабораторной работе формулы расстояний реализованы вручную, а в будущих заданиях они будут импортироваться из специализированных библиотек.

- **`cosine_similarity(v1, array_of_vectors)`** — приводит `v1` и каждый вектор из `array_of_vectors` к `numpy`-массиву (поддерживает как один вектор, так и массив векторов), вычисляет `dot_product` и нормы `norm_v1`/`norm_v2`, возвращает список значений `dot_product / (norm_v1 * norm_v2)`.
- **`euclidean_distance(v1, array_of_vectors)`** — аналогично проверяет форму входных данных, для каждой пары векторов проверяет совпадение размерностей (`raise ValueError` при несовпадении) и вычисляет `sqrt(sum((v1 - v2) ** 2))`.

Обе функции всегда возвращают `list`.

Пример на векторах `v1 = [1, 2]`, `v2 = [1, 1]`, `array_v = [[3, 2], [5, 6]]`:

```python
cosine_v1_v2 = cosine_similarity(v1, v2)
cosine_v1_array_v = cosine_similarity(v1, array_v)
euclidean_v1_v2 = euclidean_distance(v1, v2)
euclidean_v1_array_v = euclidean_distance(v1, array_v)
```

Visible output:

```
Cosine Similarity between v1 and v2: [0.9486832980505138]
Cosine Similarities between v1 and array_v: [0.8682431421244593, 0.973417168333576]
Euclidean Distance between v1 and v2: [1.0]
Euclidean Distances between v1 and array_v: [2.0, 5.656854249492381]
```

Markdown отдельно поясняет результат: по **cosine similarity** ближайший к `v1` вектор — второй в массиве, а по **Euclidean distance** — первый. Это происходит потому, что метрики измеряют разные свойства: cosine similarity — угол между векторами, Euclidean distance — фактическое расстояние между ними; поэтому для cosine similarity фактическое расстояние между точками не имеет значения.

Далее вызывается `plot_vectors()` из `utils.py` — функция строит график (`matplotlib`), на котором стрелками показаны векторы `v1`, `v2`, `array_v[0]`, `array_v[1]`, а на самом графике текстом выведены посчитанные значения cosine similarity и Euclidean distance для каждой пары.

### 2. Embedding-модель

Раздел 2.1 поясняет, что embedding-модель отвечает за превращение слова или предложения в вектор фиксированного размера; она обучена на миллионах примеров и специализируется на группировке семантически близких предложений.

Раздел 2.2 «Loading the model» загружает модель [`BAAI/bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5) — transformer-based модель, способную вкладывать (embed) целые предложения и генерирующую вектор с 768 измерениями:

```python
from sentence_transformers import SentenceTransformer
model_name = "BAAI/bge-base-en-v1.5"
model = SentenceTransformer(os.path.join(os.environ['MODELS'], model_name))
```

Модель загружается из локального пути, собранного из переменной окружения `MODELS` и имени модели (то есть модель должна быть заранее скачана/закэширована по этому пути).

Проверка вывода модели:

```python
res = model.encode("RAG is awesome")
print(res.shape)
```

Visible output: `(768,)`.

```python
model.encode(['apple', 'car'])
```

Visible output — массив формы `(2, 768)` с числами типа `float32`.

Печать первых 100 элементов вектора (`print(res[:100])`) показывает набор чисел в диапазоне примерно от −0.07 до 0.09.

Markdown поясняет: предложение превращается в точку в 768-мерном векторном пространстве, где можно применять различные метрики для измерения расстояния между предложениями или словами; более близкие векторы подразумевают семантически более похожие предложения.

### 2.3 Embeddings на практике

Задаётся список слов и их embeddings:

```python
words = ['apple', 'car', 'fruit', 'automobile', 'love', 'sentiment']
vectorized_words = model.encode(words)
```

Для слова `'apple'` печатаются cosine similarity и Euclidean distance до каждого слова из списка. Visible output:

```
apple:
	apple:		Cosine Similarity: 1.0000
	car:		Cosine Similarity: 0.5749
	fruit:		Cosine Similarity: 0.7461
	automobile:		Cosine Similarity: 0.6485
	love:		Cosine Similarity: 0.5540
	sentiment:		Cosine Similarity: 0.5020

	apple:		Euclidean Distance: 0.0000
	car:		Euclidean Distance: 0.9221
	fruit:		Euclidean Distance: 0.7126
	automobile:		Euclidean Distance: 0.8384
	love:		Euclidean Distance: 0.9445
	sentiment:		Euclidean Distance: 0.9980
```

Markdown-вывод: для cosine similarity чем ближе к 1, тем более похожи два слова, тогда как для Euclidean distance похожие слова имеют меньшее расстояние.

#### `retrieve_relevant(query, documents, metric='cosine_similarity')`

Функция кодирует `query` и `documents` через `model.encode`, затем в зависимости от `metric`:

- `'cosine_similarity'` — вычисляет `cosine_similarity(query_emb, documents_emb)`, формирует список пар `(document, score)` и сортирует по убыванию (`reverse=True`);
- `'euclidean'` — вычисляет `euclidean_distance(query_emb, documents_emb)`, формирует пары и сортирует по возрастанию.

Возвращает отсортированный список кортежей `(документ, оценка)`.

Пример на списке из 10 предложений о путешествиях (`documents`) и запросе `query = "Suggest to me great places to visit in Asia."`:

- по `cosine_similarity` на первом месте — *«The Great Wall of China is a spectacular site to experience during winter.»* (0.6081), далее Mt. Fuji (0.5821), The Maldives (0.5605), и так далее по убыванию до Prague (0.4484);
- по `euclidean` порядок документов идентичен (та же ранжировка от Great Wall of China до Prague), но с возрастающими значениями расстояния от 0.8854 до 1.0504.

Markdown-ячейка после вывода отдельно комментирует результат: хотя можно было бы ожидать, что предложение про цветение сакуры в Киото (*«Kyoto's cherry blossoms create a beautiful scene to witness during spring.»*) окажется выше в рейтинге из-за релевантности запросу об Азии, transformer-модели embedding улавливают сходство на основе контекстов, в которых слова совместно встречаются в обучающих данных. Поэтому, хотя Киото фактически более релевантен, модель могла усвоить более сильные ассоциации между типичными «туристическими» формулировками (вроде «places to visit») и другими направлениями (Santorini, Banff) из-за их частой совместной встречаемости в туристических контекстах при обучении — это и приводит к их более высокому рангу.

### 2.4 Визуализация embeddings

Раздел поясняет, что embeddings превращают предложения/слова в высокоразмерные векторы, отражающие семантические свойства, и что для их визуализации применяется `PCA` (Principal Component Analysis) — метод снижения размерности до двух измерений.

Вызов `display_widget(model)` (из `utils.py`) строит интерактивный виджет:

- начальный список из 12 слов/предложений: `'apple', 'king', 'queen', 'cellphone', 'car', 'automobile', 'fruit', 'man', 'woman'` и три предложения — *«He spoke softly in class»*, *«He whispered quietly during class»*, *«Her daughter brightened the gloomy day»*;
- эти строки кодируются через `model.encode(sentences)`, затем `PCA(n_components=2)` сокращает размерность embeddings до 2D;
- строится `scatter`-график точек с подписями (с использованием `adjust_text` для избежания наложения подписей);
- текстовое поле `Word/Sentence` и кнопка `Add Word or Sentence!` позволяют добавить новое слово/предложение: оно кодируется моделью, проецируется в уже обученное PCA-пространство через `pca.transform(...)`, добавляется к списку точек, и график перестраивается.

Notebook output для ячейки `display_widget(model)` включает HTML/виджет-объекты (`IPython.core.display.HTML object`, `VBox(...)`), содержимое графика в статике не приводится (интерактивный вывод).

### 3. Embeddings и размер входного текста

Раздел поясняет, что у моделей embeddings есть предел объёма текста, который они могут обработать за раз; текст, превышающий этот предел, обрезается (`truncation`), и вся информация после точки обрезки теряется, что может повлиять на точность embedding.

#### Пример с большим текстом

```python
big_text = open("large_text.txt").read()
len(big_text)
```

Visible output: `3955` (символов).

```python
big_text_embedding = model.encode(big_text)
big_text_embedding_few_characters = model.encode(big_text[:3000])
np.array_equal(big_text_embedding, big_text_embedding_few_characters)
```

Visible output: `True`.

Markdown поясняет: два вектора полностью совпадают, потому что context window этой модели — 512 токенов, и всё, что выходит за эти рамки, полностью игнорируется. Отмечено, что способы работы с большими текстами будут рассмотрены в следующих модулях курса.

Notebook завершается сообщением о том, что ungraded lab про принцип работы embeddings пройден.

### Ограничения и предпосылки

Для работы notebook требуется локальная копия/кэш модели `BAAI/bge-base-en-v1.5`, доступная по пути `os.environ['MODELS']/BAAI/bge-base-en-v1.5` (переменная окружения `MODELS` должна быть установлена), а также локальный файл `large_text.txt` в рабочей директории. Зависимости: `sentence_transformers`, `numpy`, `matplotlib`, `scikit-learn` (`PCA`), `ipywidgets`, `adjustText`. `utils.py` также содержит функции для вызова LLM (`generate_with_single_input`, `generate_with_multiple_input`, аналогичные другим лабораторным работам курса) и работы с Together.ai (`get_proxy_url`, `get_proxy_headers`, `get_together_key`), но в показанном коде самого notebook эти функции для вызова LLM не используются — сам notebook посвящён исключительно embeddings и не выполняет вызовов LLM. В рамках конспекта код изучался статически, без запуска notebook или отдельных ячеек.
