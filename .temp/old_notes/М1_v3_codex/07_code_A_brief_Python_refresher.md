См. practice\Module1\ungraded_labs\ungraded_lab_1\C1M1_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение notebook

Notebook `C1M1_Ungraded_Lab_1.ipynb` - optional Python refresher для слушателей, которым нужен быстрый повтор базовых конструкций Python перед практикой по RAG. Он не строит RAG-систему напрямую, но показывает структуры и приемы, которые дальше используются при подготовке prompts и данных.

В notebook разбираются:

- lists;
- list comprehensions;
- dictionaries;
- `.items()` для обхода key/value pairs;
- `f-strings`;
- `.format()`;
- сборка formatted strings из list of dictionaries.

### Импорты и зависимости

Notebook не использует внешние импорты. Все примеры работают на встроенных структурах Python и функциях `print`, `range`, `.append()`, `.remove()`, `.items()`, `.join()`, `format`.

### Lists

Сначала вводится `list` как built-in data type для хранения collections of items. В markdown-ячейке указано, что lists:

- ordered;
- changeable;
- allow duplicate values.

Код создает список:

```python
l1 = ['RAG', 'is', 'awesome']
```

Затем демонстрируются операции:

- `append('!')`: добавляет элемент в конец списка;
- `remove('awesome')`: удаляет элемент из списка;
- `print(...)`: показывает состояние списка после каждой операции.

Visible output показывает:

- исходный список `['RAG', 'is', 'awesome']`;
- список после добавления `!`;
- список после удаления `awesome`.

Отдельная ячейка показывает важное поведение mutating methods: `.append()` меняет список in place и не возвращает новое значение. Поэтому:

```python
result = l1.append("this is a test")
print(result)
```

печатает `None`.

### List comprehensions

List comprehensions представлены как concise way to create lists. Они используются как более простой и читаемый вариант `for` loops. Notebook отмечает небольшой performance gain, но главным преимуществом называет readability and simplicity.

Первый пример строит squares для чисел от 0 до 9:

```python
squares = [x**2 for x in range(10)]
```

Затем тот же результат собирается через обычный `for` loop и `.append()`. Visible output показывает одинаковый список квадратов:

```text
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Следующий пример добавляет условие:

```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

Он возвращает squares только для even numbers от 0 до 9:

```text
[0, 4, 16, 36, 64]
```

Notebook снова показывает эквивалентный вариант через `for` loop и `if`.

### Dictionaries

Далее вводится `dictionary` как структура для хранения data values in `key:value` pairs. В markdown-ячейке указано, что dictionaries:

- unordered;
- changeable;
- do not allow duplicates.

Код создает `person`:

```python
person = {
    'name': 'Alice',
    'age': 25,
    'city': 'New York'
}
```

Затем демонстрируются:

- доступ к значению по key: `person['name']`;
- добавление новой пары: `person['email'] = 'alice@example.com'`;
- печать обновленного dictionary.

Visible output показывает исходный dictionary, значение `Name: Alice` и обновленную структуру с `email`.

### `.items()` и обход dictionary

Метод `.items()` используется для итерации по key/value pairs:

```python
for key, value in person.items():
    print(f"Key: {key}\tValue: {value}")
```

Visible output печатает пары `name`, `age`, `city`, `email` вместе с их значениями.

Затем notebook показывает отличие прямой итерации по dictionary:

```python
for val in person:
    print(val)
```

В этом случае iteration идет по keys, поэтому output содержит только `name`, `age`, `city`, `email`.

### f-strings

`f-strings` представлены как formatted string literals. Они позволяют embed expressions inside string literals через curly braces `{}`. Чтобы строка стала `f-string`, перед ней ставится `f`.

Пример:

```python
name = "John"
age = 30
greeting = f"Hello, {name}. You are {age} years old."
```

Visible output:

```text
Hello, John. You are 30 years old.
```

### Формирование строк из list of dictionaries

Notebook показывает структуру, которая будет часто встречаться в курсе: list of dictionaries. Создается список `people`, где каждый dictionary содержит:

- `name`;
- `age`;
- `email`;
- `location`.

Задача: создать строки вида `Name: ..., Age: ..., E-mail: ..., Location: ...` для каждого человека.

Первый вариант:

1. создать пустой list `t`;
2. пройти по `people`;
3. для каждого `person_info_dict` создать `layout_string` через `f-string`;
4. добавить строку в `t`;
5. соединить строки через `"\n".join(t)`.

Visible output печатает пять строк для Alice Johnson, Michael Smith, Emily Davis, John Brown и Sarah Wilson.

Notebook отдельно предупреждает, что при доступе к values в dictionary keys являются strings. Поэтому нужно аккуратно использовать quotation marks. В примере одинарные кавычки используются для dictionary keys, а двойные - для внешней `f-string`, чтобы не сломать parser.

Второй вариант использует `template` и `.format()`:

```python
template = "Name: {name}, Age: {age}, E-mail: {email}, Location: {location}"
```

Затем `template.format(...)` подставляет значения из каждого dictionary. Output совпадает с вариантом на `f-strings`.

### Связь с RAG

Notebook подготавливает к работе с RAG через базовые операции над структурами данных:

- list of dictionaries похож на набор retrieved documents;
- форматирование строк нужно для превращения structured data в prompt text;
- `f-strings`, `.format()` и `.join()` используются для prompt augmentation.

### Ограничения и предпосылки

Notebook не требует API key, модели, внешнего сервиса или локальных данных. Все outputs уже видны в notebook и получены на простых встроенных примерах.
