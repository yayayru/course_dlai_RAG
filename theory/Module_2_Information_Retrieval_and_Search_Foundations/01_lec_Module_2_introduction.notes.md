# Module 2 Introduction

## Источники

- Основной источник: `theory\Module_2_Information_Retrieval_and_Search_Foundations\01_lec_Module_2_introduction.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_2_Information_Retrieval_and_Search_Foundations\RAG_M2.pdf`

## Задача retriever

Задачу `retriever` легко сформулировать: он должен находить в `knowledge base` документы, которые помогут `LLM` ответить на prompt.

На практике это сложная задача, потому что пользователь не отправляет в RAG-систему хорошо структурированный SQL query. Пользователь общается с `LLM` так, как говорил бы с другим человеком.

## Почему retrieval сложен

Документы в `knowledge base` могут быть очень разными:

- personal emails;
- internal company memos;
- articles from a medical journal.

Они могут содержать много информации, но обычно написаны и структурированы для людей, а не для компьютерного поиска.

`retriever` должен:

1. работать с messy structured information;
2. быстро находить наиболее релевантные фрагменты;
3. возвращать результат за fractions of a second.

> Важный вывод: простая формулировка задачи `retriever` скрывает сложность поиска по слабо структурированным человеческим текстам.

## Что изучается в модуле

В модуле рассматриваются основные техники, с помощью которых `retriever` выполняет свою задачу.

Курс обещает:

- построить theoretical understanding того, как работает каждая техника;
- рассмотреть relative strengths and weaknesses этих техник;
- показать, как `retriever` использует техники в combination, чтобы получить лучшие результаты;
- познакомить со стратегиями evaluation performance of a retriever.

## Практическая часть

Как и в предыдущем модуле, предусмотрены:

- hands-on coding exercises;
- programming assignment;
- прямое применение изученных техник.

## Вывод

Модуль посвящен deep dive on information retrieval: тому, как `retriever` в RAG-системе ищет релевантные документы в `knowledge base`, комбинирует разные подходы поиска и оценивает качество своей работы.
