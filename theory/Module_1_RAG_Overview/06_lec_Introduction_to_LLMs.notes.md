# Introduction to LLMs

## Источники

- Основной источник: `theory\Module_1_RAG_Overview\06_lec_Introduction_to_LLMs.trans.txt`
- Дополнительный источник для сверки структуры и терминов: `theory\Module_1_RAG_Overview\slides_M1.pdf`

## Почему в модуле обсуждаются LLM

После обзора архитектуры RAG лекция переходит к каждому компоненту, начиная с `LLM`.

Понимание того, как `LLM` работают, в чем их strengths и limitations, помогает объяснить, почему другие компоненты RAG-системы устроены так, чтобы улучшать performance модели.

## LLM как fancy autocomplete

`LLM` иногда называют fancy autocomplete. Лекция подчеркивает, что это справедливое описание: `LLM` предсказывает next word, который должен появиться в тексте.

Пример incomplete phrase:

- prompt: `what a beautiful day the sun is ...`;
- вероятное completion: `shining`;
- другие возможные completions: `rising`, `out`;
- improbable completion: `exploding`.

Фраза с `exploding` может быть grammatically valid, но improbable. Солнце обычно не взрывается, особенно в таком контексте. Люди имеют intuitive sense for how words are used; language models в некотором смысле тоже.

Термины:

- `prompt`: исходная неполная или входная фраза;
- `completion`: сгенерированное продолжение.

## Neural network как модель языка

Под капотом `LLM` использует neural network: огромную и сложную mathematical model of language.

Эта модель хранит информацию о том:

- какие words commonly used with each other;
- в каком порядке они обычно появляются;
- что эти words mean in context.

Именно это mathematical representation of language используется для генерации нового текста.

Когда `LLM` генерирует completion, она добавляет новые элементы к prompt по одному. В примере модель может добавить `shining`, затем `in`, `the`, `sky`, а потом signal, что completion done.

## Tokens вместо words

Технически `LLM` генерирует не words, а tokens.

`token`: более общий термин для pieces of words.

Примеры из лекции:

- некоторые слова, например `London` и `door`, могут иметь собственный token;
- compound words вроде `programmatically` и `unhappy` обычно split into multiple tokens;
- punctuation, например period, comma и question mark, тоже может иметь собственные tokens.

Most LLMs имеют vocabulary примерно от 10,000 до более чем 100,000 tokens. В транскрипции прозвучало `10 to more than 100,000`, но презентация подтверждает формулировку `~10,000 - 100,000 tokens`.

Гибкость tokenization позволяет модели строить почти любое слово из smaller word pieces, не назначая отдельный token каждому возможному слову.

## Как выбирается следующий token

Перед добавлением каждого нового token `LLM` проходит процесс:

1. обрабатывает current state of completion;
2. формирует deep understanding of relationships между словами и overall meaning of text;
3. проходит по каждому token в vocabulary, обычно десятки или сотни тысяч вариантов;
4. рассчитывает probability, что каждый token должен появиться next;
5. получает probability distribution across every token;
6. randomly chooses next token from that distribution.

В примере `shining` может иметь highest probability, `rising` - smaller probability, а improbable words вроде `exploding` или `snoring` - tiny chance.

Приведен числовой пример: 80 times out of 100 модель выберет `shining`, но все еще возможны `rising` или даже `exploding`.

## Autoregressive generation

После выбора очередного token модель повторяет весь процесс.

При следующем шаге current completion уже включает token, который модель только что сгенерировала. Поэтому early token choices влияют на later selections.

Это желательное поведение, потому что новые tokens должны make sense in context of tokens already chosen.

Примеры:

- если первым выбран `shining`, дальше могут появиться `in`, `the`, `sky`;
- если первым выбран `warming`, дальше может появиться `our faces`, потому что это лучше соответствует выбранному направлению.

Такое поведение называется autoregressive, то есть self-influencing.

Из-за randomness и autoregressive nature один и тот же prompt, запущенный несколько раз через одну и ту же `LLM`, обычно приводит к different completions.

## Как LLM обучаются

`LLM` понимает meaning of a prompt и делает reasonable predictions, потому что была trained on large collections of text.

Mathematical model имеет billions of individual parameters, или numerical weights. До training такая модель генерировала бы gibberish.

Во время training:

1. `LLM` показывают incomplete pieces of text from training data;
2. модель пытается predict which word comes next;
3. на основе accuracy этих predictions модель updates internal parameters.

Таким образом модель учится воспроизводить:

- factual information из training data;
- linguistic styles из training data.

Многие современные large language models trained on trillions of tokens of text, largely taken from the open internet. Поэтому они могут генерировать text in a wide variety of styles и по wide variety of topics, если такие styles и topics были в training data.

## Почему возникают hallucinations

Понимание обучения объясняет поведение `LLM`, включая hallucinations.

`LLM` генерирует probable sequences of words based on patterns learned in training data. Если спросить о private internal data компании или today's news, модель почти наверняка не была trained on that information.

В таких случаях модель иногда дает responses that sound right but aren't actually true.

Лекция подчеркивает: hallucination не означает psychological episode и не обязательно malfunction. `LLM` designed to generate probable text, not truthful text.

Для `LLM` truth фактически сводится к тому, что sequence of words probabilistically likely based on training data. При high quality training data intuitive truth и mathematical probability могут быть aligned, но challenge состоит в том, чтобы дать модели доступ к максимально relevant information.

> Важный вывод: hallucination возникает не потому, что модель "знает правду и скрывает ее", а потому что она продолжает генерировать probable text при недостатке релевантной информации.

## Как RAG использует сильную сторону LLM

RAG решает проблему, используя способность `LLM` понимать context.

Если RAG-система добавляет relevant information в prompt, `LLM` может понять и incorporate that information into response, даже если эта информация не была part of training data.

Обычно говорят, что такая информация grounds responses модели.

## Почему нельзя добавить в prompt все

Может показаться, что нужно добавить в prompt как можно больше relevant information. На практике есть ограничения.

Первое ограничение: longer prompts take more computation to run. Перед генерацией каждого нового token модель выполняет computationally complex scan of every token already in the completion, включая original prompt.

Второе ограничение: `context window` - longest sequence, которую модель может process at once.

Примеры из лекции:

- older models могут иметь `context window` only a few thousand tokens;
- newer models могут process millions.

По мере того как `retriever` добавляет больше информации в `augmented prompt`, сначала prompt становится more costly, а затем можно полностью use up the model's context window.

## LLM provider в курсе

В курсе используется TogetherAI, который hosts many popular open source models.

Использование open source models упрощает возможность look under the hood of large language models и исследовать концепции курса.

## Выводы лекции

Главный takeaway: дизайн `LLM` позволяет ей incorporate information in the prompt into response, даже если эта информация не была included in training data. Именно поэтому RAG работает: `retriever` добавляет relevant context, а `LLM` использует его при generation. Ограничения prompt length и `context window` объясняют, почему retrieval должен быть избирательным.

