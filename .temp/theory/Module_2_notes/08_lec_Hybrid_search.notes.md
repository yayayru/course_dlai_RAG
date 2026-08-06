# Hybrid Search

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\08_lec_Hybrid_search.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Зачем combining techniques

После обзора search and filtering techniques внутри `retriever` лекция показывает, как использовать их together as part of a `hybrid search` technique.

Цель: take advantage of their different strengths.

## Review: metadata filtering

`metadata filtering` uses rigid criteria stored in document metadata to narrow down search results.

Benefits:

- fast;
- easy to implement;
- easy to interpret;
- provides strict yes-no filter that neither keyword search nor semantic search provides.

Limitation:

- may not be a great search technique on its own.

## Review: keyword search

`keyword search` scores and ranks documents based on having the same keywords found in the prompt.

Benefits:

- still quite fast;
- easy to implement;
- can do an excellent job finding relevant documents;
- performs particularly well when prompts and documents contain technical keywords or product names;
- results contain exact words from the prompt.

Limitation:

- relies on exact matches;
- cannot retrieve documents with similar meanings but different words.

## Review: semantic search

`semantic search` scores and ranks documents based on having similar meaning to the prompt.

Mechanism:

- documents and prompts are embedded as vectors;
- vector location captures meaning;
- most similar documents are those whose vector embeddings are closest to the prompt vector.

Tradeoff:

- slower and more computationally intensive than keyword search;
- provides flexibility no other search technique can.

## Typical hybrid search pipeline

Hybrid search pipeline combines all three approaches.

1. Prompt is received by the `retriever`.
2. `retriever` performs both keyword search and semantic search using that prompt.
3. Result is two ranked lists of documents:
   - keyword ranked list;
   - semantic ranked list.
4. Each search technique may return 50 documents.
5. Many documents can appear in both rankings, possibly in different order.
6. Both lists are filtered with metadata filter.
7. Metadata filter removes irrelevant documents by strict criteria.
8. Two filtered ranked lists are combined into one final ranking.

Example from lecture:

- keyword search list after filtering: 35 documents;
- semantic search list after filtering: 30 documents.

## Reciprocal Rank Fusion

A commonly used algorithm for combining rankings is `reciprocal rank fusion`, or `RRF`.

`RRF` rewards documents for being ranked highly on either list and allows control over whether keyword or semantic ranking receives more weight.

Documents score points based on their ranking in each list.

When hyperparameter `K` is treated as zero:

- first place scores `1` point;
- second place scores `1/2`;
- tenth place scores `1/10`;
- documents acquire points from each ranked list;
- total scores produce the final ranking.

In this `retriever` there are two rankings:

- keyword rank;
- semantic rank.

Example:

- document appears second in one list: score `1/2 = 0.5`;
- same document appears tenth in another list: score `1/10 = 0.1`;
- total score is `0.6`.

The scores are then used to re-rank all documents.

## Hyperparameter K in RRF

`K` controls impact of the highest ranked document.

When `K = 0`:

- top ranked document in any list can instantly shoot to top of overall ranking;
- top document scores `1`;
- tenth ranked document scores `1/10`;
- difference is `10x`.

Increasing `K` to something like `50` balances scores:

- top ranked document scores `1/50`;
- tenth ranked document scores `1/60`;
- difference becomes much more modest.

It still pays to be ranked first, but not so much that one ranking dominates.

## RRF uses ranks, not original scores

RRF only cares about rank of the document in each list.

It does not use the scores that led to those rankings.

Even if top ranked document scored considerably better than second, that information is not considered by RRF.

## Hyperparameter beta

Inside a `retriever`, hybrid search typically has a second hyperparameter called `beta`.

`beta` allows weighting rankings produced by semantic or keyword search.

Example:

- `beta = 0.8`;
- 80% of importance assigned to semantic search ranking;
- 20% assigned to keyword search ranking.

A 70-30 split is typically a good starting point:

- 70% semantic;
- 30% keyword.

This should be tuned for a particular system.

Guidance from lecture:

- when exact word matching is really important but semantic similarity is still useful, weight keyword search more heavily;
- when semantic similarity is more important and keywords are less crucial, weight vector search more heavily.

## Returning top K

After final hybrid ranking is built, `retriever` can return results.

The number of documents requested is usually called `top K`.

The most similar K documents from the final hybrid ranking are returned by the `retriever`.

## Tuning hybrid search

Hybrid search lets `retriever` use the benefits of:

- keyword search: exact word matching;
- semantic search: fuzzier matching based on meaning;
- metadata filtering: strict criteria.

There are multiple tuning opportunities:

- adjust BM25 parameters;
- choose which metadata to filter on;
- change weighting of keyword vs semantic search in reciprocal rank fusion.

## Вывод

Hybrid search plays to each approach's strengths and allows tuning system performance to:

- data in the `knowledge base`;
- needs of the overall project.

To tune the system, one needs a way to measure how well `retriever` performs, which leads to retriever evaluation.
