См. practice\Module2\Graded_Assignments\C1M2_Assignment.ipynb

## Конспект по коду

### Назначение assignment notebook

Notebook `C1M2_Assignment.ipynb` asks learner to enhance a RAG system by implementing retrieval functions.

Main tasks:

- use a library to implement BM25 search;
- implement semantic search using vector embeddings;
- implement `Reciprocal Rank Fusion` to combine BM25 and semantic search;
- compare RAG responses with different retrieval functions;
- compare responses with and without RAG.

The assignment focuses on the retrieve part of RAG.

### Imports и зависимости

Notebook imports:

- `joblib`;
- `numpy`;
- `bm25s`;
- `os`;
- `SentenceTransformer` from `sentence_transformers`;
- helper functions from local `utils.py`;
- `unittests`.

From `utils.py` it uses:

- `read_dataframe`;
- `pprint`;
- `generate_with_single_input`;
- `cosine_similarity`;
- `display_widget`.

Local files used:

- `news_data_dedup.csv`;
- `embeddings.joblib`;
- `utils.py`;
- `unittests.py`.

Model path:

- `os.environ['MODEL_PATH']`;
- model `BAAI/bge-base-en-v1.5`.

LLM helper:

- `generate_with_single_input` calls Together API through `TOGETHER_API_KEY` or proxy endpoint.

### Loading the dataset

Assignment uses the same Kaggle BBC News dataset as Module 1.

Dataset is loaded:

```python
NEWS_DATA = read_dataframe("news_data_dedup.csv")
```

`read_dataframe` in `utils.py`:

1. reads CSV with `pandas`;
2. formats `published_at` and `updated_at` as `YYYY-MM-DD`;
3. converts DataFrame to list of dictionaries.

Saved example `NEWS_DATA[5]`:

- `guid`: `18ba9f2676859f393a271d15692a9c6e`;
- `title`: `WATCH: Would you pay a tourist fee to enter Venice?`;
- `description`: visitors to the city at peak times will be charged a trial entrance fee;
- `venue`: `BBC`;
- `url`: BBC News URL;
- `published_at`: `2024-04-25`;
- `updated_at`: `2024-04-26`.

### query_news

Function `query_news(indices)`:

- receives list of integer indices;
- returns corresponding elements from `NEWS_DATA`;
- acts as helper for converting retrieval indices into news records.

### BM25 retrieve example

The corpus is built as:

```python
corpus = [x['title'] + " " + x['description'] for x in NEWS_DATA]
```

BM25 setup:

1. instantiate `BM25_RETRIEVER = bm25s.BM25(corpus=corpus)`;
2. tokenize corpus with `bm25s.tokenize(corpus)`;
3. index tokenized chunks with `BM25_RETRIEVER.index(tokenized_data)`;
4. tokenize sample query;
5. retrieve top documents with `BM25_RETRIEVER.retrieve(tokenized_sample_query, k=3)`.

Sample query:

```text
What are the recent news about GDP?
```

Saved output retrieves:

1. index `752`: `GDP and the Dow Are Up. But What About American Well-Being?`;
2. index `673`: `What the GDP Report Says About Inflation: A Hot First Quarter`;
3. index `289`: `A GDP Warning as Signs of Stagflation Appear`.

The saved progress outputs show `bm25s` tokenization, count tokens, compute scores, and retrieve steps.

### Exercise 1: bm25_retrieve

Learner must implement:

```python
def bm25_retrieve(query: str, top_k: int = 5):
```

Expected behavior:

1. tokenize query with `bm25s.tokenize`;
2. use pre-indexed `BM25_RETRIEVER`;
3. retrieve top `k` documents;
4. extract retrieved documents;
5. convert documents to corpus indices;
6. return `List[int]`.

Expected notebook output for GDP query:

```text
[752, 673, 289, 626, 43]
```

`unittests.py` additionally checks query `Should I invest in startups?`:

- for `top_k = 3`, expected indices are `[863, 848, 716]`;
- output type must be `list`;
- output length must match `top_k`.

The graded cell in the notebook contains `None` placeholders and is not solved in the source.

### Semantic search and embeddings

Assignment explains:

- semantic search focuses on meaning behind queries, not keyword matching;
- embeddings are vector representations of text;
- cosine similarity is used to compare query embedding and document embeddings.

Precomputed embeddings are loaded:

```python
EMBEDDINGS = joblib.load("embeddings.joblib")
```

Model is loaded from:

```python
model_name = os.path.join(os.environ['MODEL_PATH'], "BAAI/bge-base-en-v1.5")
model = SentenceTransformer(model_name)
```

Notebook includes an example encoding `"RAG is awesome"` and truncates output to first 40 values to avoid polluting output.

It also compares:

- `What are the primary colors`;
- `Yellow, red and blue`;
- `Cats are friendly animals`.

The point of this example is to show cosine similarity over embeddings; no saved numeric output is present in the notebook extraction.

### Full embedding example

Notebook uses query:

```text
Taylor Swift
```

Steps:

1. encode query;
2. compute `cosine_similarity(query_embed, EMBEDDINGS)`;
3. sort with `np.argsort(-similarity_scores)` to get descending order;
4. take first two indices;
5. call `query_news(top_2_indices)`.

This demonstrates semantic retrieval over the full precomputed embedding matrix.

### Exercise 2: semantic_search_retrieve

Learner must implement:

```python
def semantic_search_retrieve(query, top_k=5):
```

Expected behavior:

1. encode query with `model.encode(query)`;
2. calculate cosine similarity against `EMBEDDINGS`;
3. sort similarity scores descending;
4. select top K indices;
5. cast indices to `int`;
6. return `List[int]`.

Expected notebook output for GDP query:

```text
[743, 673, 626, 752, 326]
```

`unittests.py` checks query `Should I invest in startups?`:

- for `top_k = 3`, expected indices are `[863, 416, 624]`;
- output type must be `list`;
- output length must match `top_k`.

The graded cell contains `None` placeholders and is not solved in the source.

### Reciprocal Rank Fusion

Notebook introduces `Reciprocal Rank Fusion` (`RRF`) as information retrieval technique for combining multiple ranking systems.

Formula in notebook:

```text
Score(d) = sum from r=1 to n of 1 / (k + rank_r(d))
```

Where:

- `n` is number of ranking systems;
- `rank_r(d)` is rank of document `d` in the r-th result list;
- `k` is a constant scaling contribution of rank.

RRF gives higher score to documents that appear with high rankings across multiple systems.

### Exercise 3: reciprocal_rank_fusion

Learner must implement:

```python
def reciprocal_rank_fusion(list1, list2, top_k=5, K=60):
```

Inputs:

- `list1`: top-ranked document indices from one retrieval system;
- `list2`: top-ranked document indices from another retrieval system;
- `top_k`: number of final indices to return;
- `K`: constant in RRF formula, default `60`.

Expected implementation:

1. create `rrf_scores = {}`;
2. iterate through both lists;
3. enumerate ranks starting at `1`;
4. initialize missing document score to `0`;
5. update score with `1 / (rank + K)`;
6. sort document indices by RRF score descending;
7. return top K as integers.

Expected output example:

```text
Semantic Search List: [743 673 626 752 326]
BM25 List: [752, 673, 289, 626, 43]
RRF List: [673, 752, 626, 743, 289]
```

The notebook says order may vary.

`unittests.py` checks a fixed example:

- `l1 = [17, 29, 28, 26, 18, 14, 1, 0, 16, 11]`;
- `l2 = [17, 26, 16, 25, 18, 24, 13, 11, 6, 12]`;
- for `top_k = 10`, expected result is `[17, 26, 18, 16, 11, 29, 28, 25, 14, 24]`.

The graded cell contains `None` placeholders and is not solved in the source.

### Completing the RAG system

Function `generate_final_prompt(query, top_k, retrieve_function=None, use_rag=True)` creates an `augmented prompt`.

Behavior:

- starts with original query;
- if `use_rag` is `False`, returns original query;
- if `retrieve_function.__name__ == 'reciprocal_rank_fusion'`, it:
  - calls `semantic_search_retrieve(query, top_k)`;
  - calls `bm25_retrieve(query, top_k)`;
  - combines lists with RRF;
- otherwise it calls the provided retrieval function directly;
- gets news records with `query_news(top_k_indices)`;
- formats each retrieved document with title, description, published date, and URL;
- inserts formatted news into final prompt.

The final prompt instructs the model:

- answer the user query;
- use additional information from 2024;
- do not rely only on this information;
- add it to overall knowledge.

### llm_call

Function `llm_call(query, retrieve_function=None, top_k=5, use_rag=True)`:

1. calls `generate_final_prompt`;
2. passes prompt to `generate_with_single_input`;
3. returns generated message content.

`generate_with_single_input` in `utils.py` calls Together API using:

- `TOGETHER_API_KEY`, if available;
- otherwise proxy URL `https://proxy.dlai.link/coursera_proxy/together`.

Default model in this helper is:

```text
meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
```

### Experiment widget

`display_widget(llm_call, semantic_search_retrieve, bm25_retrieve, reciprocal_rank_fusion)` creates interactive UI with:

- query input;
- `Top K` slider from `1` to `20`;
- button `Get Responses`;
- four output panels:
  - Semantic Search;
  - BM25 Search;
  - Reciprocal Rank Fusion;
  - Without RAG.

Suggested test questions:

- `What were the most important events of the past year?`
- `How is global warming progressing in 2024?`
- `Tell me about the most recent advances in AI.`
- `Give me the most important facts from past year.`

The final reflection asks which setup gave better results and whether one method outperforms another for a type of query.

### Ограничения и предпосылки

- Notebook requires local CSV `news_data_dedup.csv`.
- Semantic search requires `embeddings.joblib`.
- Model path depends on `MODEL_PATH`.
- LLM calls require Together API key or course proxy availability.
- The graded retrieval cells are intentionally incomplete with `None` placeholders.
- Notebook should be studied statically here; no cells were run.
