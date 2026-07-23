См. practice\Module2\ungraded_labs\ungraded_lab_2\C1M2_Ungraded_Lab_2.ipynb

## Конспект по коду

### Назначение notebook

Notebook `C1M2_Ungraded_Lab_2.ipynb` показывает, как оценивать retrieval component в RAG system.

Основные цели:

- compute precision and recall metrics;
- apply these metrics in information retrieval;
- use concrete labeled dataset to test semantic-based retrieval;
- use `sentence-transformers` to convert text to embeddings;
- evaluate retrieval against known labels.

Notebook подчеркивает: retrieval metrics require a labeled dataset, because system output must be compared with known correct categories.

### Imports и зависимости

Notebook импортирует:

- `pandas`;
- `SentenceTransformer`;
- `numpy`;
- `matplotlib.pyplot`;
- `joblib`;
- `os`;
- `fetch_20newsgroups` from `sklearn.datasets`.

Используются локальные или окруженческие ресурсы:

- dataset under `./dataset`;
- precomputed `embeddings.joblib`;
- model `BAAI/bge-base-en-v1.5` from `os.environ['MODELS']`.

### Dataset

Notebook loads `20 Newsgroups dataset`:

```python
newsgroups_train = fetch_20newsgroups(
    subset='train',
    shuffle=True,
    random_state=42,
    data_home='./dataset'
)
```

Data converted to `DataFrame` with columns:

- `text`;
- `category`.

Saved output:

- dataset size: `(11314, 2)`;
- number of categories: `20`;
- categories include `alt.atheism`, `comp.graphics`, `rec.autos`, `sci.space`, `talk.politics.misc`, and others.

Notebook prints first row:

- text begins with email header `From: lerxst@wam.umd.edu`;
- subject is `WHAT car is this!?`;
- category is `rec.autos`.

### Preprocessing and vectorizing data

Notebook explains:

- text is preprocessed by cleaning;
- text is vectorized with pre-trained `sentence-transformers` model;
- `BAAI/bge-base-en-v1.5` is used for encoding prompts;
- dataset embeddings are precomputed to save time.

The model is loaded:

```python
model = SentenceTransformer(os.path.join(os.environ['MODELS'], model_name))
```

Precomputed embeddings are loaded:

```python
embedding_vectors = joblib.load('embeddings.joblib')
```

Saved output for `len(embedding_vectors)`:

```text
11314
```

### Basic retrieval functions

Notebook defines `preprocess_text(text)`:

- strips leading and trailing whitespace;
- returns cleaned text.

Defines `cosine_similarity(v1, array_of_vectors)`:

- handles PyTorch tensors and NumPy arrays;
- converts values to `float32`;
- supports single vector and 2D array;
- returns float for 1D input or list of floats for 2D input;
- avoids division by zero by returning `0.0` where denominator is zero.

Defines `top_k_greatest_indices(lst, k)`:

1. enumerates list values with indices;
2. sorts by value descending;
3. returns indices of top k values.

### retrieve_documents

Function `retrieve_documents(query, embeddings, model, top_k=5)`:

1. preprocesses query with `preprocess_text`;
2. encodes query using the model;
3. iterates through document embeddings;
4. computes cosine similarity between query embedding and each document embedding;
5. selects top indices with `top_k_greatest_indices`;
6. prints query, first 200 characters of each retrieved document, and category.

Example query:

```text
space exploration
```

Saved output for top 2 documents:

- both retrieved documents are in category `sci.space`;
- first document begins `From: u1452@penelope.sdsc.edu`;
- second begins `From: dennisn@ecs.comm.mot.com`.

### Precision@K

Notebook defines `precision_at_k(relevant_count, k)`.

Formula in notebook:

```text
Precision@K = Number of Relevant Documents in Top K / K
```

Function behavior:

- raises `ValueError` if inputs are negative;
- returns `0.0` if `k == 0`;
- otherwise returns `relevant_count / k`.

Precision@K evaluates relevancy of top K retrieved documents.

### Recall@K

Notebook defines `recall_at_k(relevant_count, total_relevant)`.

Formula in notebook:

```text
Recall@K = Number of Relevant Documents in Top K / Total Number of Relevant Documents in Corpus
```

Function behavior:

- raises `ValueError` if inputs are negative;
- returns `0.0` if `total_relevant == 0`;
- otherwise returns `relevant_count / total_relevant`.

Recall@K evaluates ability to find all relevant documents from corpus within top K results.

### Test queries

Notebook defines 10 test queries with desired categories:

- space exploration technology -> `sci.space`;
- computer graphics rendering -> `comp.graphics`;
- cardiovascular medical research -> `sci.med`;
- NHL playoffs -> `rec.sport.hockey`;
- cryptography and online security -> `sci.crypt`;
- electronics in computing devices -> `sci.electronics`;
- motorcycle maintenance -> `rec.motorcycles`;
- baseball tactics -> `rec.sport.baseball`;
- politics and society -> `talk.politics.misc`;
- Windows operating system -> `comp.os.ms-windows.misc`.

### compute_metrics

Function `compute_metrics(queries, embeddings, model, top_k=5)`:

1. normalizes all embeddings to NumPy arrays;
2. stacks embeddings into matrix `E`;
3. encodes each query;
4. computes vectorized cosine similarities;
5. selects top K document indices;
6. maps retrieved documents to category names;
7. counts retrieved documents matching desired category;
8. counts all documents in corpus matching desired category;
9. computes `precision_at_k`;
10. computes `recall_at_k`;
11. returns list of result dictionaries.

Each result contains:

- `query`;
- `precision@k`;
- `recall@k`.

### Saved metric outputs

Notebook runs metrics for:

- `K = 5`;
- `K = 20`;
- `K = 50`.

At `K=5`:

- most queries have `Precision@5: 1.00`;
- `historical influence of politics on society` has `Precision@5: 0.40`;
- Windows query has `Precision@5: 0.80`;
- recall values are around `0.01` or `0.00`.

At `K=20`:

- many queries remain at `Precision@20: 1.00`;
- electronics query drops to `0.80`;
- motorcycles query is `0.95`;
- politics query is `0.50`;
- Windows query is `0.65`;
- recall values are around `0.02` to `0.03`.

At `K=50`:

- space, medicine, cryptography, and baseball remain at `Precision@50: 1.00`;
- computer graphics is `0.88`;
- electronics is `0.66`;
- politics is `0.52`;
- Windows is `0.60`;
- recall values reach about `0.05` to `0.08`.

### Interpretation in notebook

Notebook explains precision-recall tradeoff:

- as K increases, recall increases because more relevant documents are retrieved;
- as K increases, precision can decrease because more irrelevant documents are included.

Key observations:

- K=5 gives high precision for most queries;
- K=20 starts to reduce precision for some queries;
- K=50 increases recall but lowers precision further;
- politics query is consistently harder;
- for RAG systems, K=5 to K=20 is often optimal because context size stays manageable for `LLM`;
- recall remains low even at K=50 because each category has hundreds of documents.

### Ограничения и предпосылки

- Metrics depend on labeled ground truth categories.
- Dataset and precomputed embeddings must be available locally.
- Model path is read from `os.environ['MODELS']`.
- Notebook evaluates semantic search over embeddings; it does not call an `LLM`.
- It uses category labels as relevance proxy, so relevance is defined by dataset category match.
