См. practice\Module2\ungraded_labs\ungraded_lab_1\C1M2_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение notebook

Notebook `C1M2_Ungraded_Lab_1.ipynb` показывает, как vector embeddings используются в RAG:

- превращают words и sentences в vectors;
- позволяют сравнивать prompt и documents через distance measures;
- помогают находить contextual information;
- демонстрируют cosine similarity и Euclidean distance;
- используют transformer-based embedding model;
- визуализируют high-dimensional embeddings через PCA.

### Основные зависимости и локальные файлы

Notebook импортирует:

- `numpy`;
- `os`;
- `display_widget` и `plot_vectors` из локального `utils.py`;
- `SentenceTransformer` из `sentence_transformers`.

Локальный `utils.py` дополнительно содержит:

- plotting code на `matplotlib`;
- `PCA` из `sklearn.decomposition`;
- interactive widget на `ipywidgets`;
- `adjustText` для подписей на графике;
- helper-функции для Together API, хотя в основном ходе этого lab они не являются центральной частью.

Notebook использует:

- images из папки `images`;
- `large_text.txt`;
- embedding model `BAAI/bge-base-en-v1.5`, загружаемую из `os.environ['MODELS']`.

### Теоретическая рамка

В начале notebook объясняется, что в RAG vector embeddings нужны для:

1. powering search;
2. capturing meaning;
3. comparing similarity;
4. understanding context;
5. flexibility with different meanings.

Основной framework:

1. create the embedding для query и documents;
2. measure distance или similarity;
3. sort documents by score;
4. select top relevant documents.

Notebook подчеркивает различие metrics:

- for cosine similarity higher score means greater similarity;
- for Euclidean distance lower score means greater similarity.

### Реализация distance functions

В notebook вручную реализованы:

- `cosine_similarity(v1, array_of_vectors)`;
- `euclidean_distance(v1, array_of_vectors)`.

Обе функции:

- приводят input к `numpy.array`;
- поддерживают single vector и array of vectors;
- возвращают `list` чисел.

`cosine_similarity` считает dot product и vector norms.

`euclidean_distance` проверяет matching shapes и считает square root of squared differences.

### Пример с маленькими vectors

Используются:

- `v1 = [1, 2]`;
- `v2 = [1, 1]`;
- `array_v = [[3, 2], [5, 6]]`.

Сохранённый output:

- cosine similarity между `v1` и `v2`: `[0.9486832980505138]`;
- cosine similarities между `v1` и `array_v`: `[0.8682431421244593, 0.973417168333576]`;
- Euclidean distance между `v1` и `v2`: `[1.0]`;
- Euclidean distances между `v1` и `array_v`: `[2.0, 5.656854249492381]`.

Notebook делает вывод: по cosine similarity ближе second vector in the array, а по Euclidean distance ближе first vector. Это происходит потому, что cosine similarity measures angle, а Euclidean distance measures actual distance.

`plot_vectors()` из `utils.py` визуализирует эти vectors и подписи с cosine similarity и Euclidean distance.

### Loading the embedding model

Notebook загружает:

```python
model_name = "BAAI/bge-base-en-v1.5"
model = SentenceTransformer(os.path.join(os.environ['MODELS'], model_name))
```

Model described as transformer-based model capable of embedding entire sentences.

Она generates embeddings with 768 dimensions.

Для строки `"RAG is awesome"` сохранённый output shape:

```text
(768,)
```

Для массива `['apple', 'car']` output is an array with shape `(2, 768)`.

Notebook также печатает first 100 elements embedding для `"RAG is awesome"`.

### Embeddings in practice

Список words:

- `apple`;
- `car`;
- `fruit`;
- `automobile`;
- `love`;
- `sentiment`.

Notebook кодирует эти words и сравнивает слово `apple` со всеми остальными через cosine similarity и Euclidean distance.

Сохранённые значения показывают:

- `apple` vs `apple`: cosine `1.0000`, Euclidean `0.0000`;
- `apple` vs `fruit`: cosine `0.7461`, Euclidean `0.7126`;
- `apple` vs `car`: cosine `0.5749`, Euclidean `0.9221`;
- `apple` vs `sentiment`: cosine `0.5020`, Euclidean `0.9980`.

Notebook напоминает:

- cosine similarity closer to `1` means more similar;
- Euclidean distance smaller means more similar.

### retrieve_relevant

Function `retrieve_relevant(query, documents, metric='cosine_similarity')`:

1. encodes query with `model.encode`;
2. encodes documents with `model.encode`;
3. computes cosine similarity or Euclidean distance;
4. pairs each document with score;
5. sorts descending for cosine similarity;
6. sorts ascending for Euclidean distance;
7. returns list of tuples `(document, score)`.

### Travel document example

Documents are travel-related sentences about:

- Mt. Fuji;
- Santorini;
- Banff National Park;
- Great Wall of China;
- fjords of Norway;
- Prague;
- Kyoto;
- Marrakech;
- Maldives;
- Christmas markets in Vienna.

Query:

```text
Suggest to me great places to visit in Asia.
```

For both cosine similarity and Euclidean distance saved outputs rank top documents as:

1. Great Wall of China;
2. Mt. Fuji;
3. Maldives;
4. Santorini;
5. Banff National Park.

Notebook notes that Kyoto might be expected to rank higher, but transformer embedding models capture similarity based on contexts where words appear together in training data. The model may have stronger associations between common travel-related sentences and destinations like Santorini and Banff.

### PCA visualization

Section `Visualizing Word Embeddings` explains that 768-dimensional embeddings cannot be visualized directly.

The helper `display_widget(model)`:

- starts with words and sentences such as `apple`, `king`, `queen`, `car`, `automobile`, and sentence pairs from lecture examples;
- encodes them;
- applies `PCA(n_components=2)`;
- displays a 2D scatter plot;
- lets the user add a new word or sentence through an interactive widget.

### Embeddings and input size

Notebook loads:

```python
big_text = open("large_text.txt").read()
```

Saved output for `len(big_text)`:

```text
3955
```

Then it computes embeddings for:

- full `big_text`;
- `big_text[:3000]`.

Saved output:

```text
True
```

This means both embeddings are exactly the same.

Notebook explanation: context window for this model is 512 tokens, so anything beyond that is completely ignored.

### Ограничения и предпосылки

- Notebook assumes environment variable `MODELS` points to local model files.
- It depends on local `large_text.txt` and `images`.
- It does not require running external API calls for the main embedding examples.
- The helper `utils.py` contains Together API functions requiring `TOGETHER_API_KEY` or proxy setup, but those functions are not the main path of this lab.
- The input-size section demonstrates a limitation of the embedding model: text beyond its token window is truncated/ignored.
