# Metadata Filtering

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\03_lec_Metadata_filtering.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Определение

`Metadata filtering` - straightforward и familiar technique, используемая внутри `retriever`.

> `metadata filtering` использует rigid criteria, чтобы narrow down documents, returned by a retriever, на основе metadata документов.

Metadata может включать:

- title;
- author;
- creation date;
- access privileges;
- другие свойства документа.

## Пример с газетой

Предположим, нужно построить `retriever` для статей, написанных за историю newspaper.

`knowledge base` содержит thousands of different articles.

Каждая article помечена metadata:

- title;
- date, когда article was published;
- author;
- newspaper section;
- другие признаки.

Полный текст article лежит где-то в `knowledge base`, но система может искать articles only based on metadata.

## Как выглядит query по metadata

Querying this kind of index looks a lot like writing a SQL query.

Если фильтровать по одной metadata field, можно найти:

- every article published on a given day;
- every article written by a particular author.

Можно писать more complex queries и filter on multiple pieces of metadata.

Пример:

- все articles, written for the opinion section;
- between June and July of 2024;
- by a favorite journalist.

Only articles that meet every condition are returned. Остальные filtered out.

Если пользователь когда-либо фильтровал table in a spreadsheet, он уже делал metadata filtering: использовал strict set of criteria, чтобы выбрать members of a larger collection of data.

## Роль metadata filtering в RAG

В typical RAG system metadata filtering обычно не используется as retrieval itself.

Его роль:

- narrow down results returned by other retrieval techniques;
- refine результаты keyword search и semantic search.

Filters обычно определяются not by what the user said in the prompt, а other attributes of the user making the request.

## Примеры фильтров по пользователю

### Paid subscriber

В газетном примере часть articles может быть freely published to the open internet, а другая часть accessible only by paid subscribers.

Каждая article может иметь metadata, где хранится whether it is free or paid.

Когда пользователь ищет по database:

1. system detects whether the user is signed in as a paid subscriber;
2. if not, metadata filter excludes paid articles from search results.

### Region

Если newspaper prints articles in many regions of the world, каждая article может иметь metadata with the region where the article was published.

Когда reader queries the system:

1. system detects where the reader is located;
2. retrieval returns only articles from that region.

## Преимущества metadata filtering

Metadata filtering has a number of advantages.

1. It is conceptually simple.
   Это облегчает understanding how the system works и debugging issues.

2. It is fast, mature, and well-optimized.

3. It supports rigid criteria.
   Это самое важное преимущество: metadata filtering - единственный подход из рассмотренных, который позволяет system decide whether documents are retrieved based on strict criteria.

> Важный вывод: если нужно строго определить, какие documents should or should not be included in retrieval, metadata filtering gives that behavior.

## Ограничения

Metadata filtering имеет significant limitations.

Он:

- not really a search technique, а tool for refining results of other techniques;
- overly rigid;
- ignores document content;
- lacks any way of ranking documents after they pass the filter.

Metadata filtering likely appears in many RAG systems, but `retriever`, relying exclusively on metadata filtering, would be essentially useless.

## Вывод

Metadata filtering is simple and effective, но его нужно pairing with other search techniques.

Он помогает строго отфильтровать документы, но не отвечает на главный вопрос retrieval: relevant ли contents of a document to the prompt.

Следующая техника, keyword search, адресует часть этой потребности.
