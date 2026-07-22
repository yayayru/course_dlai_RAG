# Introduction to Information Retrieval

## Источники

- Транскрипция: `09_lec_Introduction to information retrieval.trans.txt`
- Дополнительная сверка: `slides_M1.pdf`

## Назначение retriever

К этому моменту purpose of the retriever должен быть понятен: он needs to provide useful information to the LLM that was potentially not available when the model was trained.

Эта лекция объясняет, how this component actually works.

## Library analogy

Лекция начинается с analogy.

Question:

> How can I make New York-style pizza at home?

Library has a large collection of books on many topics.

To help browse the collection, books are organized in sections and shelves based on characteristics such as:

- topics;
- genre;
- authors;
- and so forth.

If the question is shared with the librarian, the librarian can help find:

- sections of the library relevant to the question;
- exact books most relevant to the question.

## Retriever components in the analogy

Retrievers have many similar components.

Where a library has a collection of books, a retriever has a knowledge base of documents.

Retriever creates an index of the documents in the knowledge base. The index:

- keeps the documents organized;
- makes them easy to search.

На слайде эта аналогия представлена как соответствие:

- Library collection -> documents in a database;
- different shelves and sections -> index for search;
- librarian search -> retriever searches the index.

## How search works with a librarian

In the library, the user can ask the librarian directly.

The librarian is able to:

- understand the meaning of the question;
- identify the right shelves of the library to search through;
- eventually find relevant books.

Для вопроса про New York-style pizza librarian might search sections on:

- cooking;
- Italian cuisine;
- possibly New York.

## How retriever searches

Inside a RAG system, retriever does something similar.

It first needs to process the prompt to understand its underlying meaning.

Then it uses that understanding to search the index of documents.

The retriever returns the documents from the knowledge base that it determines are most relevant to the prompt.

На слайдах это выражено двумя вопросами:

- What does the prompt mean?
- What documents in the knowledge base are similar?

## Ranking and relevance scores

When completing its search, retriever ranks documents in the knowledge base by how relevant they are to the prompt.

Each document receives a numerical score that quantifies its relevance.

Usually this means some measure of similarity between:

- the text of the prompt;
- the text of the document.

Documents with the highest scores are returned.

На слайде с вопросом про New York-style pizza shown example relevance scores:

- 0.95;
- 0.8;
- 0.7;
- 0.6.

Документы на слайде названы:

- A History of NYC;
- Sauce Secrets;
- Cooking at Home;
- Pizza Basics.

The course will later cover a variety of approaches to calculating these similarity scores.

## Relevance vs irrelevance

A well-designed retriever should return relevant documents, but it also needs to withhold irrelevant documents.

If the user asks for information about making New York-style pizza at home and retriever returns all documents in the knowledge base, then technically every relevant document is included.

But relevant information would be lost in a mountain of irrelevant information.

This would also lead to:

- costly prompts;
- possibly using up the LLM’s context window entirely.

## Returning too few documents

The opposite problem is returning only the highest-ranked documents.

If only the highest-ranked document is retrieved, valuable relevant information in documents ranked 2nd, 3rd, or 4th might be missed.

## Ideal and practical retrieval

In a perfect world:

- retriever perfectly ranks documents;
- retriever chooses the exact right number of documents to return.

In practice:

- relevant documents may be ranked too low;
- irrelevant documents may be ranked too high;
- it is difficult to confidently decide how many documents to return.

## Optimizing retriever performance

To optimize retriever performance, it is necessary to:

- monitor it over time;
- experiment with different settings.

The course will cover this extensively.

## Information retrieval as a broader field

Many familiar pieces of software perform tasks very similar to a retriever.

Examples:

- web search engine retrieves web pages relevant to a web search;
- relational database retrieves rows and tables that match a SQL query.

The broader field of information retrieval was already mature when large language models were first developed.

Ideas from information retrieval underlie the way retrievers and RAG systems are designed.

## Implementation choices

In theory, there are many ways to implement the retriever in a RAG system.

Since most companies already have their data in traditional relational databases, it would be useful to keep data there and retrieve from that database to power a RAG system.

At scale, most retrievers will be built on top of a vector database, although vector databases are not strictly necessary.

Vector database is described as a specialized type of database optimized for rapidly finding the documents in the knowledge base that most closely match a prompt.

## What the course will cover next

The course will cover:

- general principles of information retrieval that power many search technologies;
- vector databases, which are typically used as retrievers inside production-scale RAG systems.

The lecture closes by noting that there is much more to learn about retrievers, but the most important points for this introduction have been covered.
