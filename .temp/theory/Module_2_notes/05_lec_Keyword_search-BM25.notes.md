# Keyword Search: BM25

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\05_lec_Keyword_search-BM25.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## BM25

TF-IDF remains a classic keyword search algorithm, but the algorithm used in most retrievers is `Best Matching 25`, or `BM25`.

Название связано с тем, что BM25 was the 25th variant in a series of scoring functions proposed by its creators.

BM25 improves upon TF-IDF while working very similarly to it.

## Как BM25 scores documents

BM25 formula generates a relevance score for a single keyword for a particular document.

Чтобы получить total relevance score для document:

1. BM25 score считается for a single keyword;
2. scores summed across all keywords;
3. total score used for ranking.

## Improvement 1: term frequency saturation

First improvement: documents score diminishing returns as they include more instances of a keyword.

Идея:

- document containing keyword `pizza` 20 times is not actually twice as relevant as one containing `pizza` 10 times.

Discounting additional instances of a keyword is called `term frequency saturation`.

> `term frequency saturation` снижает дополнительную выгоду от повторяющихся occurrences одного keyword.

## Improvement 2: document length normalization

Second improvement: longer documents are still penalized, as in TF-IDF, but in BM25 these penalties are also diminishing.

Penalizing long documents is important, but TF-IDF can do so too aggressively and overly discount longer documents.

BM25 applies diminishing additional penalties as documents grow in length.

Result:

- long documents can still score highly;
- this happens if they have fairly high frequency of keywords.

This process of adjusting scores based on document length is called `document length normalization`.

## Tunable hyperparameters

BM25 differs from TF-IDF because it includes two tunable hyperparameters.

They allow control over:

- degree of `term frequency saturation`;
- degree of `document length normalization`;
- how rapidly documents stop being rewarded for repeated keywords;
- how rapidly documents stop being penalized for increased length.

In a production `retriever`, these hyperparameters are tuned to land on an overall scoring system that fits the data in the `knowledge base`.

## BM25 в production retriever

In a production `retriever`, the standard keyword search algorithm is BM25.

BM25 tends to:

- perform significantly better than TF-IDF at finding relevant documents;
- require roughly equivalent computational resources;
- be more flexible because hyperparameters can be tuned to dataset.

## Review keyword search

Core idea of keyword search:

- match documents to prompt based on how frequently keywords from the prompt appear in each document.

As part of this process:

- prompts and documents are converted to `sparse vectors`;
- sparse vectors count how often each word in the system's vocabulary appears in a piece of text.

TF-IDF and BM25 are different approaches for processing these sparse vectors to score and rank documents.

These methods account for:

- rarity of a keyword;
- how often a document contains a keyword;
- document length.

## Strengths of keyword search

BM25 is the most commonly used keyword search algorithm and has withstood the test of time for decades since its invention.

It strikes a good balance between complexity and performance in real-world applications.

Primary strength of keyword search: simplicity.

Keyword search:

- is relatively straightforward;
- works well in practice;
- can perform quite well on its own;
- frequently sets a competitive benchmark that more advanced techniques may struggle to surpass.

It also ensures that retrieved documents contain keywords from the user's prompt.

This exact keyword matching is especially important when users are expected to use:

- technical terminology;
- exact product names.

## Weaknesses of keyword search

Keyword search depends on query containing keywords that exactly match words in the document.

If a user sends a prompt with similar meaning to a document but does not include the right words, keyword search will not find that match.

## Вывод

BM25 is the standard keyword search algorithm for production retrievers because it improves TF-IDF with term frequency saturation, document length normalization, and tunable hyperparameters.

Its weakness is exact word dependence, which motivates semantic search.
