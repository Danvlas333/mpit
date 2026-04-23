import json
import os
import re
from datetime import datetime, timedelta
from typing import Any

import ollama

# Глобальная переменная модели — меняется через /api/settings/model
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

CHAT_SYSTEM_PROMPT = """Ты дружелюбный помощник Jarvis Study.
Отвечай по-русски, кратко и понятно.
Если вопрос про учебу, объясняй доступно.
Если вопрос про действие или план, предлагай ясные шаги."""


# ─────────────────────────────────────────
# ЭТАП 1: Классификация
# ─────────────────────────────────────────
CLASSIFY_PROMPT = """Ты классификатор задач. Возвращай ТОЛЬКО валидный JSON.

КАТЕГОРИИ:
- 1 = заметка/напоминание/задача (сделать, купить, позвонить, запомнить)
- 2 = учёба/поиск (узнать, найти, объяснить, что такое, как работает)

ПРИМЕРЫ:
Вход: "Создай напоминание купить молоко"
Выход: {"category": 1}

Вход: "Что такое квантовая физика"
Выход: {"category": 2}

Вход: "Найди рецепт борща"
Выход: {"category": 2}

Вход: "Напомни позвонить врачу"
Выход: {"category": 1}

Отвечай СТРОГО: {"category": <1 или 2>}"""


# ─────────────────────────────────────────
# ЭТАП 1.5: Очистка служебных слов
# ─────────────────────────────────────────
CLEAN_PROMPT = """Ты чистишь текст от служебных слов. Возвращай ТОЛЬКО валидный JSON.

Удали из текста слова-команды:
- создай, создать, запомни, запомнить
- напомни, напомнить, добавь, добавить
- заметку, заметка, напоминание, задачу, задача
- найди, найти, объясни, объяснить, расскажи

Оставь всё остальное без изменений — даты, числа, суть.

ПРИМЕРЫ:
Вход: "Создай напоминание собрать ядерный реактор 10 января 2026"
Выход: {"cleaned": "Собрать ядерный реактор 10 января 2026"}

Вход: "Запомни купить молоко завтра"
Выход: {"cleaned": "Купить молоко завтра"}

Вход: "Найди рецепт борща"
Выход: {"cleaned": "Рецепт борща"}

Вход: "Добавь задачу позвонить врачу 15 февраля 2026"
Выход: {"cleaned": "Позвонить врачу 15 февраля 2026"}

Отвечай СТРОГО: {"cleaned": "<очищенный текст>"}"""


# ─────────────────────────────────────────
# ЭТАП 2б: Извлечение для ПОИСКА
# ─────────────────────────────────────────
EXTRACT_SEARCH_PROMPT = """Ты извлекаешь тему из уже очищенного текста. Возвращай ТОЛЬКО валидный JSON.

Текст уже без служебных слов — просто верни тему как есть.

ПРИМЕРЫ:
Вход: "Квантовая запутанность"
Выход: {"topic": "Квантовая запутанность"}

Вход: "Рецепт борща"
Выход: {"topic": "Рецепт борща"}

Отвечай СТРОГО: {"topic": "<тема>"}"""


def _note_prompt() -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    return f"""Ты извлекаешь данные из уже очищенного текста. Возвращай ТОЛЬКО валидный JSON.

Текст уже без служебных слов — просто раздели на задачу и дату.

ПРАВИЛА:
- task: что нужно сделать (без даты)
- date: дата в формате YYYY-MM-DD, если есть. Если нет — null
- Сегодня: {today}, завтра: {tomorrow}

ПРИМЕРЫ:
Вход: "Собрать ядерный реактор 10 января 2026"
Выход: {{"task": "Собрать ядерный реактор", "date": "2026-01-10"}}

Вход: "Купить молоко завтра"
Выход: {{"task": "Купить молоко", "date": "{tomorrow}"}}

Вход: "Позвонить врачу"
Выход: {{"task": "Позвонить врачу", "date": null}}

Отвечай СТРОГО: {{"task": "<суть>", "date": "<YYYY-MM-DD или null>"}}"""


# ─────────────────────────────────────────
# БАЗОВЫЕ ХЕЛПЕРЫ
# ─────────────────────────────────────────
def _extract_json(raw: str) -> dict[str, Any]:
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if not match:
        raise ValueError("Model response does not contain JSON object")
    return json.loads(match.group())


def _ollama_json(system_prompt: str, user_input: str) -> dict[str, Any]:
    """Вызов ollama.chat() с format=json. Читает глобальный MODEL."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_input},
        ],
        format="json",
        options={"temperature": 0.0},
    )
    raw = response["message"]["content"]
    return _extract_json(raw)


def _ollama_chat_free(messages: list[dict[str, str]]) -> str:
    """Вызов ollama.chat() для свободного диалога. Читает глобальный MODEL."""
    response = ollama.chat(
        model=MODEL,
        messages=messages,
        options={"temperature": 0.4},
    )
    return (response["message"]["content"] or "").strip()


# ─────────────────────────────────────────
# ЭТАП 1: Классификация
# ─────────────────────────────────────────
def classify(user_input: str) -> int:
    parsed = _ollama_json(CLASSIFY_PROMPT, user_input)
    category = int(parsed.get("category", 1))
    return 1 if category == 1 else 2


# ─────────────────────────────────────────
# ЭТАП 1.5: Очистка
# ─────────────────────────────────────────
def clean_input(user_input: str) -> str:
    parsed = _ollama_json(CLEAN_PROMPT, user_input)
    cleaned = str(parsed.get("cleaned", user_input)).strip()
    return cleaned or user_input.strip()


# ─────────────────────────────────────────
# ЭТАП 2а: Извлечение для ЗАМЕТКИ
# ─────────────────────────────────────────
def extract_note(cleaned_input: str) -> dict[str, Any]:
    parsed = _ollama_json(_note_prompt(), cleaned_input)
    task = str(parsed.get("task", cleaned_input)).strip() or cleaned_input
    date = parsed.get("date")
    if date in ("", "null"):
        date = None
    return {"task": task, "date": date}


# ─────────────────────────────────────────
# ЭТАП 2б: Извлечение для ПОИСКА
# ─────────────────────────────────────────
def extract_search(cleaned_input: str) -> dict[str, Any]:
    parsed = _ollama_json(EXTRACT_SEARCH_PROMPT, cleaned_input)
    topic = str(parsed.get("topic", cleaned_input)).strip() or cleaned_input
    return {"topic": topic}


# ─────────────────────────────────────────
# ДИАЛОГ (чат)
# ─────────────────────────────────────────
def chat_reply(messages: list[dict[str, str]]) -> str:
    prepared = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}, *messages]
    return _ollama_chat_free(prepared)


# ─────────────────────────────────────────
# ГЛАВНАЯ ФУНКЦИЯ
# ─────────────────────────────────────────
def smart_processor(user_input: str) -> dict[str, Any]:
    normalized = user_input.strip()
    if not normalized:
        return {"category": 1, "task": "", "date": None}

    try:
        category = classify(normalized)
        cleaned = clean_input(normalized)

        if category == 1:
            data = extract_note(cleaned)
            return {
                "category": 1,
                "task": data.get("task", cleaned),
                "date": data.get("date", None),
            }

        data = extract_search(cleaned)
        return {
            "category": 2,
            "topic": data.get("topic", cleaned),
        }
    except Exception:
        return {"category": 1, "task": normalized, "date": None}
