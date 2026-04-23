# Jarvis Study

Jarvis Study — локальный учебный сайт с:

- домашними заданиями;
- напоминаниями;
- архивом выполненных и пропущенных задач;
- оценками и успеваемостью;
- учебным чат-ботом;
- озвучкой ответов.

## Что нужно загрузить в GitHub

Чтобы другой пользователь смог скачать проект, запустить его и сразу войти в систему, в репозиторий лучше положить:

- `app.py`
- `auth.py`
- `planner.py`
- `user_store.py`
- `tts_engine.py`
- `requirements.txt`
- `jarvis_study.db`
- папку `templates/`
- папку `user_data/` с примерами данных

### Зачем нужны `jarvis_study.db` и `user_data`

`jarvis_study.db` нужна для входа на сайт, потому что в ней лежат пользователи.

`user_data/` нужна для примеров:

- оценок;
- напоминаний;
- домашек;
- архива;
- истории чатов.

Без этих файлов сайт запустится, но у пользователя не будет готового входа и стартовых примеров.

## Тестовые логины

После запуска можно войти так:

- `student` / `student123`
- `teacher` / `teacher123`

## Установка

### 1. Установить Python-зависимости

```powershell
pip install -r requirements.txt
```

Будут установлены Python-пакеты:

- `ollama`
- `piper-tts`
- `onnxruntime`

### 2. Установить Ollama

Скачать Ollama:

- [Windows](https://ollama.com/download/windows)
- [Главная страница Ollama](https://ollama.com/download)

После установки скачать модель:

```powershell
ollama pull qwen2.5:3b
ollama pull mistral:7b-instruct-v0.3-q4_0
```

Если хочешь использовать другую модель, можно перед запуском указать её так:

```powershell
$env:OLLAMA_MODEL="qwen2.5:3b"
```

### 3. Какие модели нужны

Для полного запуска в проекте нужны такие модели:

- модель для чата в Ollama: `qwen2.5:3b`
- умная модель в Ollama: `mistral:7b-instruct-v0.3-q4_0`
- мужской голос Piper: `ru_RU-ruslan-medium.onnx`
- женский голос Piper: `ru_RU-irina-medium.onnx`

### 4. Скачать голосовые модели Piper

Создай папку `mpit`, если её нет:

```powershell
New-Item -ItemType Directory -Force -Path .\mpit
```

Скачать мужской голос `ruslan`:

```powershell
Invoke-WebRequest -Uri "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx?download=true" -OutFile ".\mpit\ru_RU-ruslan-medium.onnx"
Invoke-WebRequest -Uri "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json?download=true" -OutFile ".\mpit\ru_RU-ruslan-medium.onnx.json"
```

Скачать женский голос `irina`:

```powershell
Invoke-WebRequest -Uri "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx?download=true" -OutFile ".\mpit\ru_RU-irina-medium.onnx"
Invoke-WebRequest -Uri "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json?download=true" -OutFile ".\mpit\ru_RU-irina-medium.onnx.json"
```

Источники голосов:

- [Ruslan ONNX](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx)
- [Irina ONNX](https://huggingface.co/rhasspy/piper-voices/blob/v1.0.0/ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx)

## Запуск

```powershell
python app.py
```

После запуска сайт будет доступен по адресу:

```text
http://127.0.0.1:8000
```

## Как пользоваться

1. Открой сайт.
2. Войди под одним из тестовых аккаунтов.
3. На главном экране смотри домашки и напоминания.
4. В календаре выбирай дату.
5. Во вкладке успеваемости смотри оценки и четверти.
6. Через чат можно задавать учебные вопросы и добавлять задачи.

## Если что-то не работает

### Не работает чат

Проверь, что Ollama установлен, запущен и модель скачана:

```powershell
ollama list
```

### Не работает голос

Проверь, что в папке `mpit/` лежат файлы:

- `ru_RU-ruslan-medium.onnx`
- `ru_RU-ruslan-medium.onnx.json`
- `ru_RU-irina-medium.onnx`
- `ru_RU-irina-medium.onnx.json`
