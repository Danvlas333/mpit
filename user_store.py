import json
import os
import secrets
from datetime import datetime, timezone
from typing import Any


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _user_root(data_root: str, storage_key: str) -> str:
    return os.path.join(data_root, storage_key)


def _state_path(data_root: str, storage_key: str) -> str:
    return os.path.join(_user_root(data_root, storage_key), "state.json")


def _chat_dir(data_root: str, storage_key: str) -> str:
    return os.path.join(_user_root(data_root, storage_key), "chats")


def _chat_path(data_root: str, storage_key: str, chat_id: str) -> str:
    return os.path.join(_chat_dir(data_root, storage_key), f"{chat_id}.json")


def _completed_tasks_path(data_root: str, storage_key: str) -> str:
    return os.path.join(_user_root(data_root, storage_key), "completed_tasks.json")


def _student_performance_path(data_root: str, storage_key: str) -> str:
    return os.path.join(_user_root(data_root, storage_key), "student_performance.json")


def _student_grades_path(data_root: str, storage_key: str) -> str:
    return os.path.join(_user_root(data_root, storage_key), "student_grades.json")


def _seed_missed_homework() -> dict[str, Any]:
    return {
        "id": "seed-missed-homework-2026-04-20",
        "kind": "homework",
        "status": "missed",
        "title": "Литература",
        "description": "Прочитать рассказ Чехова и подготовить краткий пересказ.",
        "date": "2026-04-20",
        "archived_at": _utc_now(),
    }


def _seed_example_homework() -> dict[str, Any]:
    return {
        "id": "seed-homework-overdue-2026-04-21",
        "subject": "Алгебра",
        "task": "Решить №531-536 и повторить формулы сокращенного умножения.",
        "date": "2026-04-21",
        "done": False,
        "volume": "medium",
        "priority": "high",
    }


def _default_archive() -> dict[str, list[dict[str, Any]]]:
    return {
        "completed": [],
        "missed": [_seed_missed_homework()],
        "trash": [],
    }


def _default_performance() -> dict[str, list[dict[str, Any]]]:
    return {
        "days": [
            {
                "date": "2026-04-20",
                "title": "Понедельник, 20 апреля",
                "lessons": [
                    {
                        "number": 1,
                        "subject": "алгебра",
                        "time": "8:00 - 8:40",
                        "task": "Учебник стр. 227-232 учить определения, №168-170",
                        "status": "done",
                        "tone": "sky",
                    },
                    {
                        "number": 2,
                        "subject": "алгебра",
                        "time": "8:50 - 9:30",
                        "task": "",
                        "status": "none",
                        "tone": "sky",
                    },
                    {
                        "number": 3,
                        "subject": "геометрия",
                        "time": "9:45 - 10:25",
                        "task": "",
                        "status": "none",
                        "tone": "sky",
                    },
                    {
                        "number": 4,
                        "subject": "физкультура",
                        "time": "10:45 - 11:25",
                        "task": "",
                        "status": "none",
                        "tone": "sky",
                    },
                    {
                        "number": 5,
                        "subject": "литература",
                        "time": "11:45 - 12:25",
                        "task": "Учить \"Войну и мир\" наизусть",
                        "status": "done",
                        "tone": "sky",
                    },
                ],
            },
            {
                "date": "2026-04-21",
                "title": "Вторник, 21 апреля",
                "lessons": [
                    {
                        "number": 1,
                        "subject": "физика",
                        "time": "8:00 - 8:40",
                        "task": "",
                        "status": "none",
                        "tone": "indigo",
                    },
                    {
                        "number": 2,
                        "subject": "физика",
                        "time": "8:50 - 9:30",
                        "task": "Физика: №12-15, 15-17 урока 148. Повторить МКТ",
                        "status": "pending",
                        "tone": "indigo",
                    },
                ],
            },
        ],
    }




def _default_student_grades() -> dict[str, Any]:
    return json.loads(r'''{
  "title": "\u041c\u043e\u044f \u0443\u0441\u043f\u0435\u0432\u0430\u0435\u043c\u043e\u0441\u0442\u044c",
  "assistant_prompt": "\u0427\u0442\u043e \u0434\u0435\u043b\u0430\u0442\u044c, \u0435\u0441\u043b\u0438 \u0443 \u043c\u0435\u043d\u044f \u043f\u0440\u043e\u0431\u043b\u0435\u043c\u044b \u0441 \u0430\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u043c?",
  "current_quarter": "q4",
  "quarters": [
    {
      "id": "q1",
      "label": "1 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c",
      "columns": [
        "2.09",
        "5.09",
        "9.09",
        "12.09",
        "16.09",
        "19.09",
        "23.09",
        "26.09",
        "30.09",
        "3.10",
        "7.10",
        "10.10"
      ],
      "subjects": [
        {
          "name": "\u0410\u043b\u0433\u0435\u0431\u0440\u0430",
          "grades": [
            "4",
            "",
            "5",
            "",
            "",
            "4",
            "",
            "5",
            "",
            "",
            "4",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a",
          "grades": [
            "",
            "3",
            "",
            "",
            "4",
            "",
            "",
            "",
            "3",
            "",
            "",
            "4"
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0411\u0438\u043e\u043b\u043e\u0433\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "",
            "4",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430",
          "grades": [
            "",
            "",
            "4",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0413\u0435\u043e\u0433\u0440\u0430\u0444\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "",
          "tone": "none"
        },
        {
          "name": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f",
          "grades": [
            "5",
            "",
            "",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0425\u0438\u043c\u0438\u044f",
          "grades": [
            "",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "",
            "4",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0424\u0438\u0437\u0438\u043a\u0430",
          "grades": [
            "",
            "4",
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "5",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430",
          "grades": [
            "5",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        }
      ],
      "completion_percent": 93,
      "risk_subjects": [
        {
          "key": "\u0430\u043b\u0433",
          "value": 4,
          "tone": "good"
        },
        {
          "key": "\u0430\u043d\u0433\u043b",
          "value": 3,
          "tone": "bad"
        },
        {
          "key": "\u0431\u0438\u043e",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0432\u0438\u0441",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0433\u0435\u043e\u0433",
          "value": 0,
          "tone": "none"
        }
      ]
    },
    {
      "id": "q2",
      "label": "2 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c",
      "columns": [
        "5.11",
        "8.11",
        "12.11",
        "15.11",
        "19.11",
        "22.11",
        "26.11",
        "29.11",
        "3.12",
        "6.12",
        "10.12",
        "13.12"
      ],
      "subjects": [
        {
          "name": "\u0410\u043b\u0433\u0435\u0431\u0440\u0430",
          "grades": [
            "5",
            "",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "5",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a",
          "grades": [
            "",
            "2",
            "",
            "",
            "",
            "3",
            "",
            "",
            "",
            "",
            "3",
            ""
          ],
          "average": "3",
          "tone": "bad"
        },
        {
          "name": "\u0411\u0438\u043e\u043b\u043e\u0433\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "5",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430",
          "grades": [
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0413\u0435\u043e\u0433\u0440\u0430\u0444\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "",
          "tone": "none"
        },
        {
          "name": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f",
          "grades": [
            "4",
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "5",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0425\u0438\u043c\u0438\u044f",
          "grades": [
            "",
            "",
            "3",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "4",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0424\u0438\u0437\u0438\u043a\u0430",
          "grades": [
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "",
            "5"
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430",
          "grades": [
            "5",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "5"
          ],
          "average": "5",
          "tone": "good"
        }
      ],
      "completion_percent": 90,
      "risk_subjects": [
        {
          "key": "\u0430\u043b\u0433",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0430\u043d\u0433\u043b",
          "value": 2,
          "tone": "bad"
        },
        {
          "key": "\u0431\u0438\u043e",
          "value": 4,
          "tone": "good"
        },
        {
          "key": "\u0432\u0438\u0441",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0433\u0435\u043e\u0433",
          "value": 0,
          "tone": "none"
        }
      ]
    },
    {
      "id": "q3",
      "label": "3 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c",
      "columns": [
        "13.01",
        "16.01",
        "20.01",
        "23.01",
        "27.01",
        "30.01",
        "3.02",
        "6.02",
        "10.02",
        "13.02",
        "17.02",
        "20.02"
      ],
      "subjects": [
        {
          "name": "\u0410\u043b\u0433\u0435\u0431\u0440\u0430",
          "grades": [
            "4",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "5",
            "",
            "",
            "4"
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a",
          "grades": [
            "",
            "3",
            "",
            "",
            "3",
            "",
            "",
            "",
            "",
            "4",
            "",
            ""
          ],
          "average": "3",
          "tone": "bad"
        },
        {
          "name": "\u0411\u0438\u043e\u043b\u043e\u0433\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "",
            "",
            "4",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430",
          "grades": [
            "",
            "",
            "5",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0413\u0435\u043e\u0433\u0440\u0430\u0444\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "",
          "tone": "none"
        },
        {
          "name": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f",
          "grades": [
            "4",
            "",
            "",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0425\u0438\u043c\u0438\u044f",
          "grades": [
            "",
            "",
            "4",
            "",
            "",
            "4",
            "",
            "",
            "",
            "5",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0424\u0438\u0437\u0438\u043a\u0430",
          "grades": [
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "4"
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430",
          "grades": [
            "5",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        }
      ],
      "completion_percent": 91,
      "risk_subjects": [
        {
          "key": "\u0430\u043b\u0433",
          "value": 4,
          "tone": "good"
        },
        {
          "key": "\u0430\u043d\u0433\u043b",
          "value": 3,
          "tone": "bad"
        },
        {
          "key": "\u0431\u0438\u043e",
          "value": 4,
          "tone": "good"
        },
        {
          "key": "\u0432\u0438\u0441",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0433\u0435\u043e\u0433",
          "value": 0,
          "tone": "none"
        }
      ]
    },
    {
      "id": "q4",
      "label": "4 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c",
      "columns": [
        "1.03",
        "4.03",
        "7.03",
        "10.03",
        "13.03",
        "16.03",
        "19.03",
        "22.03",
        "25.03",
        "28.03",
        "31.03",
        "3.04",
        "6.04",
        "9.04",
        "12.04",
        "15.04",
        "18.04",
        "21.04",
        "24.04",
        "27.04",
        "30.04"
      ],
      "subjects": [
        {
          "name": "\u0410\u043b\u0433\u0435\u0431\u0440\u0430",
          "grades": [
            "5",
            "",
            "4",
            "",
            "",
            "5",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "4",
            "",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0410\u043d\u0433\u043b\u0438\u0439\u0441\u043a\u0438\u0439 \u044f\u0437\u044b\u043a",
          "grades": [
            "",
            "2",
            "",
            "",
            "3",
            "",
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "3",
            "",
            "",
            "",
            "",
            "4"
          ],
          "average": "3",
          "tone": "bad"
        },
        {
          "name": "\u0411\u0438\u043e\u043b\u043e\u0433\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "",
          "tone": "none"
        },
        {
          "name": "\u0412\u0435\u0440\u043e\u044f\u0442\u043d\u043e\u0441\u0442\u044c \u0438 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430",
          "grades": [
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0413\u0435\u043e\u0433\u0440\u0430\u0444\u0438\u044f",
          "grades": [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
          ],
          "average": "",
          "tone": "none"
        },
        {
          "name": "\u0418\u0441\u0442\u043e\u0440\u0438\u044f",
          "grades": [
            "4",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0425\u0438\u043c\u0438\u044f",
          "grades": [
            "",
            "",
            "3",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "",
            "4",
            "",
            ""
          ],
          "average": "4",
          "tone": "good"
        },
        {
          "name": "\u0424\u0438\u0437\u0438\u043a\u0430",
          "grades": [
            "",
            "4",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "",
            "4",
            "",
            "",
            "",
            "",
            "",
            "5",
            ""
          ],
          "average": "5",
          "tone": "good"
        },
        {
          "name": "\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0430",
          "grades": [
            "5",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "",
            "5",
            "",
            "",
            "",
            "",
            "5"
          ],
          "average": "5",
          "tone": "good"
        }
      ],
      "completion_percent": 88,
      "risk_subjects": [
        {
          "key": "\u0430\u043b\u0433",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0430\u043d\u0433\u043b",
          "value": 2,
          "tone": "bad"
        },
        {
          "key": "\u0431\u0438\u043e",
          "value": 0,
          "tone": "none"
        },
        {
          "key": "\u0432\u0438\u0441",
          "value": 5,
          "tone": "good"
        },
        {
          "key": "\u0433\u0435\u043e\u0433",
          "value": 0,
          "tone": "none"
        }
      ]
    }
  ]
}''')


def _default_state() -> dict[str, Any]:
    return {
        "homework": [_seed_example_homework()],
        "notes": [],
        "searches": [],
        "chat_sessions": [],
    }


def _normalize_state(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        state = _default_state()
    else:
        state = {
            "homework": [item for item in payload.get("homework", []) if isinstance(item, dict)],
            "notes": [item for item in payload.get("notes", []) if isinstance(item, dict)],
            "searches": [item for item in payload.get("searches", []) if isinstance(item, dict)],
            "chat_sessions": [item for item in payload.get("chat_sessions", []) if isinstance(item, dict)],
        }

    if not any(item.get("id") == "seed-homework-overdue-2026-04-21" for item in state["homework"]):
        state["homework"].insert(0, _seed_example_homework())
    return state


def ensure_user_storage(data_root: str, storage_key: str) -> None:
    os.makedirs(_chat_dir(data_root, storage_key), exist_ok=True)
    state_path = _state_path(data_root, storage_key)
    if not os.path.exists(state_path):
        with open(state_path, "w", encoding="utf-8") as file:
            json.dump(_default_state(), file, ensure_ascii=False, indent=2)
    completed_tasks_path = _completed_tasks_path(data_root, storage_key)
    if not os.path.exists(completed_tasks_path):
        with open(completed_tasks_path, "w", encoding="utf-8") as file:
            json.dump(_default_archive(), file, ensure_ascii=False, indent=2)
    student_performance_path = _student_performance_path(data_root, storage_key)
    if not os.path.exists(student_performance_path):
        with open(student_performance_path, "w", encoding="utf-8") as file:
            json.dump(_default_performance(), file, ensure_ascii=False, indent=2)
    student_grades_path = _student_grades_path(data_root, storage_key)
    if not os.path.exists(student_grades_path):
        with open(student_grades_path, "w", encoding="utf-8") as file:
            json.dump(_default_student_grades(), file, ensure_ascii=False, indent=2)


def load_state(data_root: str, storage_key: str) -> dict[str, Any]:
    ensure_user_storage(data_root, storage_key)
    with open(_state_path(data_root, storage_key), "r", encoding="utf-8") as file:
        payload = json.load(file)
    normalized = _normalize_state(payload)
    save_state(data_root, storage_key, normalized)
    return normalized


def save_state(data_root: str, storage_key: str, state: dict[str, Any]) -> None:
    ensure_user_storage(data_root, storage_key)
    with open(_state_path(data_root, storage_key), "w", encoding="utf-8") as file:
        json.dump(_normalize_state(state), file, ensure_ascii=False, indent=2)


def _normalize_archive_entry(item: dict[str, Any], status: str) -> dict[str, Any]:
    result = item.get("result", {}) if isinstance(item.get("result"), dict) else {}
    return {
        "id": item.get("id") or secrets.token_hex(8),
        "kind": item.get("kind") or ("homework" if item.get("kind") == "homework" else "note"),
        "status": item.get("status") or status,
        "title": item.get("title") or ("Домашнее задание" if item.get("kind") == "homework" else "Личное задание"),
        "description": item.get("description") or result.get("task") or item.get("source_text") or "Без описания",
        "date": item.get("date") or result.get("date"),
        "archived_at": item.get("archived_at") or item.get("completed_at") or item.get("saved_at") or _utc_now(),
    }


def _normalize_archive_store(payload: Any) -> dict[str, list[dict[str, Any]]]:
    if isinstance(payload, list):
        store = {
            "completed": [_normalize_archive_entry(item, "completed") for item in payload if isinstance(item, dict)],
            "missed": [],
            "trash": [],
        }
    elif isinstance(payload, dict):
        store = {
            "completed": [_normalize_archive_entry(item, "completed") for item in payload.get("completed", []) if isinstance(item, dict)],
            "missed": [_normalize_archive_entry(item, "missed") for item in payload.get("missed", []) if isinstance(item, dict)],
            "trash": [_normalize_archive_entry(item, "trash") for item in payload.get("trash", []) if isinstance(item, dict)],
        }
    else:
        store = _default_archive()

    if not any(item.get("id") == "seed-missed-homework-2026-04-20" for item in store["missed"]):
        store["missed"].append(_seed_missed_homework())
    return store


def load_completed_tasks(data_root: str, storage_key: str) -> dict[str, list[dict[str, Any]]]:
    ensure_user_storage(data_root, storage_key)
    with open(_completed_tasks_path(data_root, storage_key), "r", encoding="utf-8") as file:
        payload = json.load(file)
    normalized = _normalize_archive_store(payload)
    save_completed_tasks(data_root, storage_key, normalized)
    return normalized


def save_completed_tasks(data_root: str, storage_key: str, items: dict[str, list[dict[str, Any]]]) -> None:
    ensure_user_storage(data_root, storage_key)
    with open(_completed_tasks_path(data_root, storage_key), "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def load_student_performance(data_root: str, storage_key: str) -> dict[str, list[dict[str, Any]]]:
    ensure_user_storage(data_root, storage_key)
    with open(_student_performance_path(data_root, storage_key), "r", encoding="utf-8") as file:
        return json.load(file)


def _parse_student_grades_updated_at(value: Any) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _subject_grade_values(subject: dict[str, Any]) -> list[float]:
    values: list[float] = []
    for grade in subject.get("grades", []):
        try:
            numeric = float(str(grade).strip().replace(",", "."))
        except (TypeError, ValueError):
            continue
        if numeric > 0:
            values.append(numeric)
    return values


def _subject_average(subject: dict[str, Any]) -> float | None:
    values = _subject_grade_values(subject)
    if values:
        return sum(values) / len(values)
    try:
        numeric = float(str(subject.get("average") or "").strip().replace(",", "."))
    except (TypeError, ValueError):
        return None
    return numeric if numeric > 0 else None


def _build_grades_assistant_prompt(subject_name: str) -> str:
    normalized = str(subject_name or "").strip()
    if not normalized:
        return "Что делать, если у меня есть сложности с учебой?"
    return f"Что делать, если у меня проблемы по предмету «{normalized}»?"


def _refresh_student_grades_insights(payload: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    last_updated = _parse_student_grades_updated_at(payload.get("assistant_updated_at"))
    now = datetime.now(timezone.utc)
    if last_updated and (now - last_updated).total_seconds() < 24 * 60 * 60:
        return payload, False

    subject_totals: dict[str, list[float]] = {}
    for quarter in payload.get("quarters", []):
        for subject in quarter.get("subjects", []):
            subject_name = str(subject.get("name") or "").strip()
            if not subject_name:
                continue
            values = _subject_grade_values(subject)
            if not values:
                average_value = _subject_average(subject)
                if average_value is not None:
                    values = [average_value]
            if not values:
                continue
            subject_totals.setdefault(subject_name, []).extend(values)

    weakest_subject = ""
    weakest_average: float | None = None
    for subject_name, values in subject_totals.items():
        if not values:
            continue
        average_value = sum(values) / len(values)
        if weakest_average is None or average_value < weakest_average or (
            average_value == weakest_average and subject_name < weakest_subject
        ):
            weakest_subject = subject_name
            weakest_average = average_value

    prompt = _build_grades_assistant_prompt(weakest_subject)
    changed = (
        payload.get("assistant_prompt") != prompt
        or payload.get("assistant_subject") != weakest_subject
        or payload.get("assistant_updated_at") != now.isoformat()
    )
    payload["assistant_prompt"] = prompt
    payload["assistant_subject"] = weakest_subject
    payload["assistant_updated_at"] = now.isoformat()
    return payload, changed


def _save_student_grades(data_root: str, storage_key: str, payload: dict[str, Any]) -> None:
    ensure_user_storage(data_root, storage_key)
    with open(_student_grades_path(data_root, storage_key), "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=True, indent=2)


def load_student_grades(data_root: str, storage_key: str) -> dict[str, Any]:
    ensure_user_storage(data_root, storage_key)
    with open(_student_grades_path(data_root, storage_key), "r", encoding="utf-8") as file:
        payload = json.load(file)
    refreshed, changed = _refresh_student_grades_insights(payload)
    if changed:
        _save_student_grades(data_root, storage_key, refreshed)
    return refreshed


def save_planner_result(data_root: str, storage_key: str, source_text: str, result: dict[str, Any]) -> None:
    state = load_state(data_root, storage_key)
    entry = {
        "id": secrets.token_hex(8),
        "source_text": source_text,
        "saved_at": _utc_now(),
        "result": result,
    }

    if result.get("category") == 1:
        state["notes"].insert(0, entry)
    else:
        state["searches"].insert(0, entry)

    save_state(data_root, storage_key, state)


def complete_note(data_root: str, storage_key: str, note_id: str) -> dict[str, Any] | None:
    state = load_state(data_root, storage_key)
    notes = state.get("notes", [])
    note = next((item for item in notes if item.get("id") == note_id), None)
    if note is None:
        return None

    state["notes"] = [item for item in notes if item.get("id") != note_id]
    save_state(data_root, storage_key, state)

    archive = load_completed_tasks(data_root, storage_key)
    archived_note = _normalize_archive_entry(
        {
            **note,
            "kind": "note",
            "status": "completed",
            "title": "Личное задание",
            "description": (note.get("result") or {}).get("task") or note.get("source_text"),
            "date": (note.get("result") or {}).get("date"),
            "archived_at": _utc_now(),
        },
        "completed",
    )
    archive["completed"].insert(0, archived_note)
    save_completed_tasks(data_root, storage_key, archive)
    return archived_note


def archive_overdue_notes(data_root: str, storage_key: str, today_iso: str) -> dict[str, list[dict[str, Any]]]:
    state = load_state(data_root, storage_key)
    archive = load_completed_tasks(data_root, storage_key)
    remaining_notes: list[dict[str, Any]] = []
    changed = False

    for note in state.get("notes", []):
        result = note.get("result") or {}
        note_date = str(result.get("date") or "").strip()
        if note_date and note_date < today_iso:
            if not any(item.get("id") == note.get("id") for item in archive["missed"]):
                archive["missed"].insert(
                    0,
                    _normalize_archive_entry(
                        {
                            **note,
                            "kind": "note",
                            "status": "missed",
                            "title": "Личное задание",
                            "description": result.get("task") or note.get("source_text"),
                            "date": note_date,
                            "archived_at": _utc_now(),
                        },
                        "missed",
                    ),
                )
            changed = True
            continue
        remaining_notes.append(note)

    if changed:
        state["notes"] = remaining_notes
        save_state(data_root, storage_key, state)
        save_completed_tasks(data_root, storage_key, archive)

    return archive


def move_archive_item_to_trash(data_root: str, storage_key: str, section: str, item_id: str) -> dict[str, list[dict[str, Any]]]:
    archive = load_completed_tasks(data_root, storage_key)
    if section not in {"completed", "missed", "trash"}:
        return archive

    items = archive.get(section, [])
    target = next((item for item in items if item.get("id") == item_id), None)
    if target is None:
        return archive

    archive[section] = [item for item in items if item.get("id") != item_id]
    if section != "trash":
        archive["trash"].insert(0, {**target, "status": "trash", "archived_at": _utc_now()})
    save_completed_tasks(data_root, storage_key, archive)
    return archive


def clear_archive_trash(data_root: str, storage_key: str) -> dict[str, list[dict[str, Any]]]:
    archive = load_completed_tasks(data_root, storage_key)
    archive["trash"] = []
    save_completed_tasks(data_root, storage_key, archive)
    return archive


def list_chat_sessions(data_root: str, storage_key: str) -> list[dict[str, Any]]:
    state = load_state(data_root, storage_key)
    sessions = state.get("chat_sessions", [])
    return sorted(sessions, key=lambda item: item.get("updated_at", ""), reverse=True)


def get_chat_session(data_root: str, storage_key: str, chat_id: str) -> dict[str, Any] | None:
    ensure_user_storage(data_root, storage_key)
    path = _chat_path(data_root, storage_key, chat_id)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _save_chat_session(data_root: str, storage_key: str, session: dict[str, Any]) -> None:
    ensure_user_storage(data_root, storage_key)
    path = _chat_path(data_root, storage_key, session["chat_id"])
    with open(path, "w", encoding="utf-8") as file:
        json.dump(session, file, ensure_ascii=False, indent=2)


def _upsert_chat_summary(data_root: str, storage_key: str, summary: dict[str, Any]) -> None:
    state = load_state(data_root, storage_key)
    sessions = state.get("chat_sessions", [])
    sessions = [item for item in sessions if item.get("chat_id") != summary["chat_id"]]
    sessions.insert(0, summary)
    state["chat_sessions"] = sessions
    save_state(data_root, storage_key, state)


def save_chat_exchange(
    data_root: str,
    storage_key: str,
    user_message: str,
    assistant_message: str,
    chat_id: str | None = None,
) -> dict[str, Any]:
    now = _utc_now()
    session = get_chat_session(data_root, storage_key, chat_id) if chat_id else None

    if session is None:
        session = {
            "chat_id": chat_id or secrets.token_hex(10),
            "title": user_message.strip()[:48] or "Новый чат",
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }

    session["messages"].extend(
        [
            {"role": "user", "content": user_message, "created_at": now},
            {"role": "assistant", "content": assistant_message, "created_at": _utc_now()},
        ]
    )
    session["updated_at"] = _utc_now()

    _save_chat_session(data_root, storage_key, session)
    _upsert_chat_summary(
        data_root,
        storage_key,
        {
            "chat_id": session["chat_id"],
            "title": session["title"],
            "created_at": session["created_at"],
            "updated_at": session["updated_at"],
        },
    )
    return session
