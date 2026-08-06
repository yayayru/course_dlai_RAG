# Keyword Search: TF-IDF

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\04_lec_Keyword_search-TF-IDF.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Keyword search в retrieval

`keyword search` powered retrieval in databases and search engines for decades.

Несмотря на простоту, keyword search остается key component of retrieval in modern RAG systems.

> `keyword search` retrieves documents based on whether they share words in common with the prompt.

Основная идея: documents that contain a lot of words from the prompt are more likely to be relevant.

## Bag of words

И prompt, и каждый document рассматриваются as a `bag of words`.

Это означает:

- order of words is totally ignored;
- important only which words are in the text;
- important how often each word appears.

Пример: text `making pizza without a pizza oven` содержит:

- word `pizza` twice;
- words `making`, `without`, `a`, `oven` once.

## Sparse vectors

Word counts are stored inside a vector.

Vector имеет one spot for each word in the system's vocabulary. В vocabulary может быть tens of thousands of spots.

Each number in the vector counts how often that word appears in the text.

Most locations hold zeros, поэтому такие vectors are called `sparse vectors`.

## Term document matrix и inverted index

Чтобы подготовить `knowledge base` for retrieval, для каждого document генерируется sparse vector.

All vectors can be arranged in a grid:

- each column is a different document;
- each row is a different word.

Эта grid называется `term document matrix`.

Она also sometimes called an `inverted index`, because it makes it easy to start from a word and find every document that contains it.

Index is inverted because:

- обычно начинают с document и спрашивают, which words it contains;
- здесь начинают с word и находят documents that include that word.

Такой inverted index can be created once before processing searches.

## Scoring по наличию keyword

Когда prompt отправляется в `retriever`, sparse vector quickly generated for the prompt.

После этого each document and prompt have sparse vectors, and documents can be scored and ranked.

Самый простой подход:

1. each word in the prompt is called a `keyword`;
2. для первого keyword находится его row in the index;
3. each document that contains at least one copy of the keyword gets one point;
4. same process repeats for every keyword in prompt;
5. total scores used to rank documents;
6. highest scoring documents are retrieved.

В примере prompt содержит five keywords, поэтому highest possible score is five.

## Учет repeated keywords

Shortcoming simple scoring: it does not capture whether a document contains keywords multiple times.

Multiple occurrences likely indicate greater relevance.

Simple fix:

- increase a document's score every time it contains a keyword;
- not just the first time.

Теперь для каждого keyword нужно пройти across its row in the matrix and award each document the number of points in its column.

## Проблема long documents и normalization

У учета repeated keywords появляется новая проблема: longer documents may contain keywords many times simply because they are longer.

Correction:

- divide each document's score by the number of words in that document.

This normalized score:

- levels the playing field;
- rewards documents where keywords make up a greater share of total text;
- de-emphasizes long documents that contain keywords many times only because they are long.

## Проблема common words

Normalized scoring still awards points for all keywords equally.

Это плохо, потому что:

- filler words like `the` are common;
- less common words like `pizza` are better indicators of relevance.

Чтобы исправить это, terms are weighted with `inverse document frequency`, or `IDF`.

## IDF

Для использования IDF нужно calculate an IDF value for each word in the system's vocabulary.

Для каждого word:

1. count how many documents it appears in;
2. divide by total number of documents.

Example:

- `knowledge base` has 100 documents;
- word `pizza` appears in 5 of them;
- document frequency is 5/100 = 0.05.

Common word `the` might appear in all 100 documents:

- document frequency is 100/100 = 1.

Because rare words should be rewarded, the fraction is flipped, or inverted:

- `pizza` IDF becomes 20;
- `the` IDF becomes 1.

Rare words now have much higher IDF than common words. Это может overly reward rare words.

For this reason, normally the log of the IDF is used:

- rare words still have greater weight;
- weight is less exaggerated.

> `IDF` captures how rare a word is across the `knowledge base`.

## TF-IDF matrix

To use IDF values in scoring, values in inverted index are updated:

- numbers in each row are multiplied by that word's IDF score.

The resulting matrix is a `term frequency inverse document frequency matrix`, or `TF-IDF matrix`.

To score documents:

1. for each keyword in the prompt, go across its row;
2. award each document the `TF-IDF` score it has in that row;
3. use total scores to rank documents.

## Что означает высокий TF-IDF score

TF-IDF scores are a standard baseline for keyword retrieval performance.

Highest scoring documents:

- frequently use keywords;
- especially feature many keywords rare across the entire `knowledge base`.

В примере prompt documents containing rare words like `pizza` or `oven` will likely score much better than documents containing common words like `a` or `without`.

## Вывод

TF-IDF is a foundational approach to keyword search.

Modern systems tend to use a slightly refined version of this approach called `BM25`, который рассматривается дальше.
