См. `practice\Module1\ungraded_labs\ungraded_lab_1\C1M1_Ungraded_Lab_1.ipynb`

## Конспект по коду

### Назначение notebook

`C1M1_Ungraded_Lab_1.ipynb` — необязательная (`[Optional]`) вводная лабораторная работа «A Brief Python Refresher». Она предназначена для разработчиков, которым нужно быстро освежить базовые конструкции Python перед практикой по RAG, либо для тех, кто больше знаком с другими языками программирования. В самой markdown-ячейке указано, что уверенные Python-программисты могут этот ungraded lab пропустить.

По оглавлению (Table of Contents) notebook разбирает:

1. Lists — Introduction, List Comprehensions.
2. Dictionaries — Introduction, метод `.items`.
3. f-strings — Introduction, f-strings in Action.

В заключительной вводной ячейке перечислены цели: научиться работать со строками, списками и list comprehensions, словарями для структурирования промптов, и prompt augmentation с помощью f-strings для динамической генерации текста.

### Импорты и зависимости

Notebook не использует внешние импорты и сторонние библиотеки — все примеры построены на встроенных типах и функциях Python: `list`, `dict`, `print`, `range`, `.append()`, `.remove()`, `.items()`, `.join()`, `.format()`, f-strings.

### 1. Lists

Markdown-ячейка определяет `list` как встроенный тип данных для хранения коллекций элементов и отмечает, что списки: ordered, changeable, allow duplicate values.

Код создаёт список:

```python
l1 = ['RAG', 'is', 'awesome']
```

Далее демонстрируются операции и печатается состояние списка после каждой из них:

- `l1.append('!')` — добавляет элемент в конец списка;
- `l1.remove('awesome')` — удаляет элемент из списка.

Visible output:

```
Original list: ['RAG', 'is', 'awesome']
List after adding '!': ['RAG', 'is', 'awesome', '!']
List after removing 'awesome': ['RAG', 'is', '!']
```

Отдельная ячейка показывает важное поведение мутирующих (`mutating`) методов списка — `.append()` и `.remove()` изменяют список in place и ничего не возвращают:

```python
result = l1.append("this is a test")
print(result)
```

Visible output: `None`.

#### List comprehensions

Markdown поясняет, что list comprehensions дают лаконичный способ создавать списки и делают код более читаемым, служа более простой альтернативой циклам `for`. Со ссылкой на внешний источник (Stack Overflow) отмечается, что list comprehensions дают небольшой прирост производительности, но их главное преимущество — читаемость и простота, а не значимое ускорение.

Пример 1 — квадраты чисел от 0 до 9, сначала через list comprehension, затем эквивалентно через `for`-цикл с `.append()`:

```python
squares = [x**2 for x in range(10)]
```

```python
squares_for_loop = []
for x in range(10):
    squares_for_loop.append(x**2)
```

Visible output для обоих вариантов одинаков:

```
Squares of numbers from 0 to 9: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81] (with list comprehension)
Squares of numbers from 0 to 9: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81] (without list comprehension)
```

Пример 2 — добавляется условие (только чётные числа):

```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

Также показан эквивалентный вариант через `for` и `if`. Visible output для обоих вариантов:

```
Squares of even numbers from 0 to 9: [0, 4, 16, 36, 64] (with list comprehension)
Squares of even numbers from 0 to 9: [0, 4, 16, 36, 64] (without list comprehension)
```

### 2. Dictionaries

Markdown определяет `dictionary` как структуру для хранения данных в парах `key:value`, отмечая, что словари: unordered, changeable, do not allow duplicates.

Код создаёт словарь `person`:

```python
person = {
    'name': 'Alice',
    'age': 25,
    'city': 'New York'
}
```

Демонстрируются:

- доступ к значению по ключу: `person['name']`;
- добавление новой пары: `person['email'] = 'alice@example.com'`.

Visible output:

```
Person dictionary: {'name': 'Alice', 'age': 25, 'city': 'New York'}
Name: Alice
Updated person dictionary: {'name': 'Alice', 'age': 25, 'city': 'New York', 'email': 'alice@example.com'}
```

#### Метод `.items()`

Метод `.items()` используется для итерации по парам key/value:

```python
for key, value in person.items():
    print(f"Key: {key}\tValue: {value}")
```

Visible output печатает все четыре пары: `name`, `age`, `city`, `email` вместе со значениями.

Markdown-ячейка отдельно поясняет, что при прямой итерации по словарю (`for val in person:`) итерация идёт по его `keys`. Visible output соответствующей ячейки:

```
name
age
city
email
```

### 3. f-strings

Markdown представляет f-strings (`formatted string literals`) как способ встраивать выражения внутрь строковых литералов через фигурные скобки `{}`, для чего перед строкой добавляется буква `f`.

Базовый пример:

```python
name = "John"
age = 30
greeting = f"Hello, {name}. You are {age} years old."
print(greeting)
```

Visible output:

```
Hello, John. You are 30 years old.
```

#### f-strings в действии: формирование строк из списка словарей

Markdown ставит задачу: имея список словарей с информацией о людях, сгенерировать для каждого строку вида `Name: ..., Age: ..., E-mail: ..., Location: ...`.

Создаётся список `people` — список из пяти словарей (structure, которая, как отмечено в markdown, будет часто встречаться в курсе), каждый с ключами `name`, `age`, `email`, `location`. Данные: Alice Johnson (28, Нью-Йорк), Michael Smith (34, Лос-Анджелес), Emily Davis (22, Остин), John Brown (45, Чикаго), Sarah Wilson (31, Сиэтл).

**Первый способ — через f-string:**

1. создаётся пустой список `t`;
2. цикл по `people`;
3. для каждого `person_info_dict` формируется `layout_string` через f-string;
4. строка добавляется в `t`;
5. список склеивается в единую строку через `"\n".join(t)`.

Visible output — пять отформатированных строк с данными всех пяти людей.

Отдельная markdown-ячейка с пометкой **IMPORTANT** предупреждает: при обращении к значениям словаря по ключам-строкам нужно последовательно использовать кавычки. В примере одинарные кавычки используются для ключей словаря, а двойные — для внешней f-string, иначе парсер не сможет корректно обработать кавычки и возникнет ошибка.

**Второй способ — через `template` и `.format()`:**

```python
template = "Name: {name}, Age: {age}, E-mail: {email}, Location: {location}"
```

Далее `template.format(name=..., age=..., email=..., location=...)` подставляет значения из каждого словаря по тому же алгоритму (пустой список → цикл → добавление строки → `"\n".join`). Visible output идентичен варианту с f-strings.

### Итог notebook

Завершающая markdown-ячейка отмечает, что ungraded lab по базовым концепциям Python, используемым в этом курсе по RAG, пройден.

### Ограничения и предпосылки

Notebook не требует API-ключа, модели, внешнего сервиса или локальных данных. Он не выполняет сетевых вызовов; все примеры построены на простых встроенных структурах Python, а outputs уже видны в самом notebook.
