См. practice\Module1\ungraded_labs\ungraded_lab_1\C1M1_Ungraded_Lab_1.ipynb

## Конспект по коду

### Назначение notebook

Notebook `C1M1_Ungraded_Lab_1.ipynb` — optional Python refresher для базовых конструкций Python, которые используются в курсе по `RAG`.

Он рассчитан на разработчиков, которые лучше знакомы с другими языками программирования, или на тех, кому нужно быстро повторить Python fundamentals. Уверенным Python-программистам notebook предлагает пропустить лабораторную.

Notebook покрывает:

- работу со strings;
- lists;
- list comprehensions;
- dictionaries;
- prompt augmentation через f-strings.

### Импорты, настройки и зависимости

В notebook нет внешних imports, API calls или зависимостей. Все примеры используют built-in Python.

Notebook не требует:

- API key;
- внешнего сервиса;
- локальных данных;
- вспомогательных `.py` файлов.

### Lists

Первая часть показывает, что list — built-in data type для хранения collection of items. В markdown-описании list названы:

- ordered;
- changeable;
- допускающими duplicate values.

Код создает list:

```python
l1 = ['RAG', 'is', 'awesome']
```

Затем демонстрируются операции:

- `append('!')` добавляет элемент в конец list;
- `remove('awesome')` удаляет указанный элемент;
- `print` показывает состояние list после каждой операции.

Видимый output:

- исходный list: `['RAG', 'is', 'awesome']`;
- после добавления `!`: `['RAG', 'is', 'awesome', '!']`;
- после удаления `awesome`: `['RAG', 'is', '!']`.

Отдельная ячейка показывает важное свойство методов `.append` и `.remove`: они изменяют list на месте и не возвращают новое значение. Поэтому результат `l1.append("this is a test")` печатается как `None`.

### List comprehensions

Раздел объясняет list comprehensions как concise way to create lists. Они подаются как более читаемая и выразительная альтернатива `for` loops. Notebook отмечает, что небольшой performance gain возможен, но основное преимущество — readability и simplicity.

Первый пример создает squares numbers from 0 to 9:

```python
squares = [x**2 for x in range(10)]
```

Затем тот же результат собирается через обычный `for` loop и `.append`.

Видимый output в обоих случаях одинаковый:

```text
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Второй пример добавляет условие:

```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

Так создаются squares только для even numbers. Такой же результат затем повторяется через `for` loop с `if`.

Видимый output:

```text
[0, 4, 16, 36, 64]
```

### Dictionaries

Следующая часть вводит dictionaries как структуру для хранения data values in `key:value` pairs. В markdown указано, что dictionaries:

- unordered;
- changeable;
- do not allow duplicates.

Пример создает dictionary `person`:

```python
person = {
    'name': 'Alice',
    'age': 25,
    'city': 'New York'
}
```

Код показывает:

- печать всего dictionary;
- доступ к значению по ключу `person['name']`;
- добавление новой пары `person['email'] = 'alice@example.com'`.

Видимый output показывает обновленный dictionary с ключом `email`.

### Метод `.items`

Notebook показывает, как iterate over key/value pairs через `.items()`:

```python
for key, value in person.items():
    print(f"Key: {key}\tValue: {value}")
```

Видимый output выводит пары:

- `name` / `Alice`;
- `age` / `25`;
- `city` / `New York`;
- `email` / `alice@example.com`.

После этого notebook показывает, что если итерироваться напрямую по dictionary, цикл идет по keys:

```python
for val in person:
    print(val)
```

Видимый output:

```text
name
age
city
email
```

### f-strings

Раздел вводит f-strings, или formatted string literals. Они позволяют embed expressions inside string literals через curly braces `{}`. Чтобы строка стала f-string, перед ней добавляется `f`.

Базовый пример:

```python
name = "John"
age = 30
greeting = f"Hello, {name}. You are {age} years old."
```

Видимый output:

```text
Hello, John. You are 30 years old.
```

### f-strings для структурированных данных

Notebook показывает пример, который связан с будущей работой курса: list of dictionaries. В комментарии прямо указано, что такая структура будет часто встречаться в курсе.

Создается list `people`, где каждый элемент — dictionary с полями:

- `name`;
- `age`;
- `email`;
- `location`.

Далее код:

1. создает empty list `t`;
2. итерируется по `people`;
3. для каждого `person_info_dict` собирает `layout_string` через f-string;
4. добавляет строку в `t`;
5. объединяет строки через `"\n".join(t)`;
6. печатает `formatted_string`.

Видимый output — пять строк с данными людей:

- Alice Johnson, 28, `alice.johnson@example.com`, New York, NY;
- Michael Smith, 34, `michael.smith@example.com`, Los Angeles, CA;
- Emily Davis, 22, `emily.davis@example.com`, Austin, TX;
- John Brown, 45, `john.brown@example.com`, Chicago, IL;
- Sarah Wilson, 31, `sarah.wilson@example.com`, Seattle, WA.

### Важное ограничение с кавычками

Notebook отдельно предупреждает: при доступе к значениям dictionary keys являются strings, поэтому нужно последовательно использовать quotation marks.

В примере single quotes используются для keys внутри dictionary access, а double quotes ограничивают f-string. Если кавычки использовать непоследовательно, parser не сможет корректно обработать строку, и возникнет error.

### Альтернатива через `.format`

Notebook показывает второй способ создать строки, зависящие от параметров:

```python
template = "Name: {name}, Age: {age}, E-mail: {email}, Location: {location}"
```

Затем для каждого dictionary вызывается:

```python
template.format(
    name=person_info_dict['name'],
    age=person_info_dict['age'],
    email=person_info_dict['email'],
    location=person_info_dict['location']
)
```

Результат снова объединяется через `"\n".join(t)` и печатается. Видимый output совпадает с вариантом на f-strings.

### Что демонстрирует лабораторная

Лабораторная показывает минимальные Python-инструменты, которые нужны для дальнейших `RAG` notebook:

- хранить данные в lists и dictionaries;
- обходить structured data;
- строить readable transformations через list comprehensions;
- собирать prompt-like text из данных через f-strings или `.format`;
- объединять строки в форматированный блок через `.join`.

Эта лабораторная не реализует `retriever`, `knowledge base` или вызовы `LLM`; она готовит синтаксическую базу для следующих примеров prompt augmentation.
