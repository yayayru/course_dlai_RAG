# Evaluating Retrieval

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\09_lec_Evaluating_retrieval.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Что важно оценивать

Once a `retriever` is up and running, нужно понять, actually working ли он.

Можно оценивать:

- latency;
- throughput;
- resource usage;
- другие software metrics.

Но для `retriever` ultimately matters search quality.

Главный вопрос: is it finding relevant documents?

## Ingredients для retrieval quality metrics

Most retriever quality metrics require several common ingredients.

1. Prompt itself.
   `retriever` may perform well on one prompt and poorly on another.

2. Ranked list of documents returned by the `retriever` from that prompt.

3. Ground truth list of all relevant documents in the `knowledge base` that the `retriever` should return.

> Важное условие: to grade a retriever, you need to know the correct answers.

## Precision и recall

Two of the most common retriever quality metrics are `precision` and `recall`.

`precision`:

- number of relevant retrieved documents divided by total number of documents retrieved.

`recall`:

- number of relevant documents retrieved divided by total number of relevant documents in the `knowledge base`.

## Example: first run

Suppose:

- `knowledge base` has 10 documents relevant to a prompt;
- these documents are hand marked;
- `retriever` returns 12 documents;
- 8 of those returned documents are relevant.

Then:

- precision is 66%, because 8 of 12 returned documents are relevant;
- recall is 80%, because 8 of 10 relevant documents were retrieved.

## Example: second run and tradeoff

After adjusting retriever settings:

- `retriever` returns 15 documents;
- 9 of them are relevant.

Now:

- precision drops to 60%, or 9 out of 15;
- recall increases to 90%, because 9 of 10 relevant documents were found.

This trades away some precision to get more recall.

## Interpretation

Precision penalizes a `retriever` for returning irrelevant documents.

It can be thought of as capturing how trustworthy the results are.

Recall penalizes a `retriever` for leaving out relevant documents.

It measures how comprehensive the `retriever` is.

The only way to have perfect recall and precision is:

- rank relevant documents most highly;
- return only those documents.

Otherwise there is often a tradeoff.

## Top K metrics

Retrieval metrics are influenced by how many documents the `retriever` returns.

To standardize, metrics are usually discussed in terms of top K documents:

- K documents ranked most highly by the `retriever`.

Example:

- `Precision@5` is 40%, because only 2 of the top 5 documents are relevant;
- `Precision@10` is 60%, because 6 of top 10 documents are relevant;
- if there are 8 relevant documents in the `knowledge base`, `Recall@10` is 6 out of 8, or 75%.

Different top K values produce different precision and recall values.

Use cases:

- top 5, top 2, top 1 for stricter standards;
- often a slightly more generous range between top 5 and top 15.

## Mean Average Precision

`Mean Average Precision`, or `MAP@K`, gives a more holistic view of retriever performance.

It evaluates average precision for relevant documents in the first K documents retrieved.

### Average Precision example

For `Average Precision@6`:

1. list the 6 documents ranked highest by the `retriever`;
2. calculate `Precision@K` for every row;
3. add precisions only for rows that contain relevant documents;
4. divide by number of relevant documents retrieved in top K.

In the lecture example, relevant rows are:

- row 1;
- row 4;
- row 5.

The precisions added are:

- `1`;
- `0.5`;
- `0.6`.

Divide by 3 relevant documents retrieved in top K:

- average precision is `0.7`.

### MAP across prompts

To calculate `Mean Average Precision`:

1. calculate average precision across many prompts and retrieved document sets;
2. average those values.

MAP tells what average precision would be for a typical prompt the `retriever` receives.

MAP rewards ranking relevant documents highly.

If an irrelevant document appears high in ranking, it decreases precision at the rank of every relevant document below it.

A high MAP indicates that `retriever` places relevant documents it finds high in the ranking.

## Reciprocal Rank and MRR

`Reciprocal Rank` measures the rank of the first relevant object in a returned list.

Examples:

- if first relevant object appears at rank 2, reciprocal rank is `1/2 = 0.5`;
- if it appears at rank 4, reciprocal rank is `0.25`.

The further down the first relevant document appears, the worse reciprocal rank becomes.

Usually this is performed over multiple prompts to get `Mean Reciprocal Rank`, or `MRR`.

`MRR` reflects how soon, on average, a relevant item can be found in retriever ranking.

It emphasizes the importance of including at least one relevant document as high in ranking as possible.

Example:

- four searches;
- first relevant document appears at ranks 1, 3, 6, and 2;
- reciprocal ranks are `1`, `1/3`, `1/6`, and `1/2`;
- averaging these values gives `MRR = 0.5`.

## How to use metrics together

There are many metrics, and they should be used with understanding.

`Recall@K`:

- most foundational and most cited metric for retrievers;
- captures the fundamental goal of a `retriever`: finding relevant documents.

`Precision` and `MAP`:

- build on recall;
- assess whether retriever includes many irrelevant documents;
- assess how effectively retriever ranks documents.

`MRR`:

- more specialized;
- helps identify how well the model performs at the very top of its ranking.

## Metrics for tuning

These metrics help:

- evaluate retriever performance;
- decide whether adjustments are working.

Example:

- adjust how heavily semantic search or keyword search is weighted in hybrid retrieval;
- observe effect on recall or precision for a collection of sample prompts.

## Downside: ground truth

The downside of these metrics is that all depend on having ground truth relevant documents for a collection of sample prompts.

Compiling this can be:

- time-consuming;
- manual.

The result is useful because it enables monitoring system quality:

- during development;
- once in production.

## Вывод

The module covers the most important concepts underlying a `retriever` in a typical RAG system.

Evaluation completes the loop: after building and tuning retrieval techniques, one needs metrics that show whether relevant documents are found and ranked well.
