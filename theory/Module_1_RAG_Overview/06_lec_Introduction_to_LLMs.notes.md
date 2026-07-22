# Introduction to LLMs

## Источники

- Транскрипция: `06_lec_Introduction_to_LLMs.trans.txt`
- Дополнительная сверка: `slides_M1.pdf`

## Состояние транскрипции

Файл транскрипции пуст. Поэтому содержательные заметки ниже составлены только по соответствующему разделу `slides_M1.pdf` с заголовком `Introduction to LLMs`.

## LLMs as fancy autocomplete

Слайды формулируют базовую интуицию так:

> LLMs are just fancy autocomplete.

Пример prompt:

> What a beautiful day, the sun is

Возможные completions:

- shining;
- rising;
- out.

## Neural Network

Neural Network описана на слайде как complex mathematical model of language.

Она stores:

- which words frequently appear together;
- in which order;
- contextual meaning.

LLMs use this model to generate text.

В примере модель продолжает фразу `What a beautiful day, the sun is` токеном `shining`.

## Token

Token defined as a piece of a word.

На слайде указано:

- some words get single tokens;
- compound words use multiple tokens;
- punctuation marks can be tokens;
- LLM vocabulary contains approximately 10,000-100,000 tokens;
- this vocabulary allows models to represent any possible word with fewer tokens.

Примеры tokenization со слайда:

- `un` + `happy`;
- `prog` + `ram` + `m` + `atically`;
- `London`;
- `door`;
- `Com` + `pletely`;
- `,`;
- `I`;
- `agree`;
- `!`.

## Calculate Probabilities и Select Next Token

Слайды показывают процесс next token prediction:

- Process Current State;
- Calculate Probabilities over Vocabulary;
- Select Next Token.

Vocabulary size again shown as approximately 10,000-100,000 tokens.

Для prompt:

> What a beautiful day, the sun is

на слайде приведены example probabilities:

- `shining`: 80%;
- `rising`: 5%;
- `out`: 4%;
- `bright`: 1%;
- `snoring`: .00001%;
- `exploding`: .00002%.

Selected next token in the example is `shining`.

## Контекст после нового токена

После выбора `shining` следующий token выбирается в контексте уже сгенерированной последовательности.

Слайд показывает фразу:

> What a beautiful day, the sun is shining

и example probabilities для следующих токенов:

- `on`: 35%;
- `,`: 25%;
- `through`: 20%;
- `in`: 10%.

Смысл слайда: new tokens make sense in context of old ones.

## Autoregressive generation

Autoregressive объясняется как self-influencing.

На слайде указано:

- new tokens make sense in context of old ones;
- running the same prompt leads to different completion.

Пример generated sequence:

> What a beautiful day, the sun is shining in the sky warming our faces

## How LLMs Learn

Before training, LLMs generate gibberish.

Слайд приводит пример:

> "Forward to Saturn’s dance floor!" she yowled, tail transmitting disco beats.

LLM trains on large text collections.

В модели обычно billions of parameters.

## Training loop

На слайдах training показан как процесс:

- LLM Training;
- predictions;
- check whether predictions are accurate;
- update parameters.

Примеры training prompts:

- `What a beautiful day is, the sun _____`;
- `Roses are red, violets are ___`.

Если predictions не accurate, параметры модели обновляются.

## Why LLMs Hallucinate

Слайды перечисляют причины hallucination.

### LLMs generate probable word sequences

LLMs reproduce statistical patterns from their training data.

### Knowledge gaps cause inaccurate responses

Responses can sound right but aren’t true.

### Truthful is not the same as probable

Truthful != probable.

LLMs are designed to generate probable text, not truthful text.

## How RAG solves the problem

RAG adds relevant context.

Схема на слайде:

- Retriever;
- Knowledge Base;
- LLM + relevant context;
- relevant context grounds the LLM’s responses.

## Why not add everything

Слайды объясняют, почему нельзя просто add everything into the prompt.

### Higher Computational Cost

Longer prompts take more computation to run.

Model performs computationally complex scan of every token.

This scan happens before generating each new token.

### Context Window Limit

Eventually you hit the limit of LLM’s context window.

На слайде указаны масштабы:

- smaller models: only a few thousand tokens;
- largest models: millions.

## Пустой слайд

Slide 43 в извлеченном тексте не содержит содержательных подписей.
