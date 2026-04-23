import json
import os
from functools import partial
from http import cookies
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from auth import (
    authenticate_user,
    create_session,
    delete_session,
    get_user_by_session,
    init_database,
)
from planner import chat_reply, smart_processor
from user_store import (
    ensure_user_storage,
    get_chat_session,
    list_chat_sessions,
    save_chat_exchange,
    save_planner_result,
)


SESSION_COOKIE_NAME = "jarvis_session"
DB_FILENAME = "jarvis_study.db"


class AppHandler(SimpleHTTPRequestHandler):
    db_path: str
    data_root: str

    def _send_json(self, status_code: int, payload: dict, extra_headers: list[tuple[str, str]] | None = None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for header_name, header_value in extra_headers or []:
            self.send_header(header_name, header_value)
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, filename: str) -> None:
        target = os.path.join(self.directory, filename)
        try:
            with open(target, "rb") as source:
                body = source.read()
        except FileNotFoundError:
            self.send_error(404, "File not found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str, extra_headers: list[tuple[str, str]] | None = None) -> None:
        self.send_response(302)
        self.send_header("Location", location)
        for header_name, header_value in extra_headers or []:
            self.send_header(header_name, header_value)
        self.end_headers()

    def _read_json_body(self) -> dict:
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Некорректная длина запроса") from exc

        try:
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            return json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Некорректный JSON") from exc

    def _build_cookie_header(self, token: str, max_age: int) -> str:
        cookie = cookies.SimpleCookie()
        cookie[SESSION_COOKIE_NAME] = token
        cookie[SESSION_COOKIE_NAME]["path"] = "/"
        cookie[SESSION_COOKIE_NAME]["httponly"] = True
        cookie[SESSION_COOKIE_NAME]["samesite"] = "Lax"
        cookie[SESSION_COOKIE_NAME]["max-age"] = str(max_age)
        return cookie.output(header="").strip()

    def _get_session_token(self) -> str | None:
        raw_cookie = self.headers.get("Cookie")
        if not raw_cookie:
            return None

        jar = cookies.SimpleCookie()
        jar.load(raw_cookie)
        morsel = jar.get(SESSION_COOKIE_NAME)
        return morsel.value if morsel else None

    def _get_current_user(self) -> dict | None:
        return get_user_by_session(self.db_path, self._get_session_token())

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        user = self._get_current_user()

        if path == "/":
            if user:
                self._redirect("/dashboard")
                return
            self._send_html("login.html")
            return

        if path == "/dashboard":
            if not user:
                self._redirect("/")
                return
            self._send_html("dashboard.html")
            return

        if path == "/logout":
            delete_session(self.db_path, self._get_session_token())
            self._redirect("/", [("Set-Cookie", self._build_cookie_header("", 0))])
            return

        if path == "/api/me":
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            self._send_json(200, {"ok": True, "user": user})
            return

        if path == "/api/homework":
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            ensure_user_storage(self.data_root, user["storage_key"])
            from user_store import load_state
            state = load_state(self.data_root, user["storage_key"])
            self._send_json(200, {"ok": True, "homework": state.get("homework", [])})
            return

        if path == "/api/notes":
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            ensure_user_storage(self.data_root, user["storage_key"])
            state = __import__("user_store").load_state(self.data_root, user["storage_key"])
            self._send_json(200, {"ok": True, "notes": state.get("notes", [])})
            return

            self._send_json(200, {"ok": True, "items": list_chat_sessions(self.data_root, user["storage_key"])})
            return

        if path == "/api/chat/thread":
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            chat_id = parse_qs(parsed_url.query).get("chat_id", [""])[0].strip()
            if not chat_id:
                self._send_json(400, {"ok": False, "error": "Не указан chat_id"})
                return
            session = get_chat_session(self.data_root, user["storage_key"], chat_id)
            if session is None:
                self._send_json(404, {"ok": False, "error": "Чат не найден"})
                return
            self._send_json(200, {"ok": True, "session": session})
            return

        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path == "/api/login":
            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return

            username = str(payload.get("username", "")).strip()
            password = str(payload.get("password", "")).strip()

            if not username or not password:
                self._send_json(400, {"ok": False, "error": "Введите логин и пароль"})
                return

            user = authenticate_user(self.db_path, username, password)
            if user is None:
                self._send_json(401, {"ok": False, "error": "Неверный логин или пароль"})
                return

            session_token = create_session(self.db_path, user["id"])
            headers = [("Set-Cookie", self._build_cookie_header(session_token, 7 * 24 * 60 * 60))]
            self._send_json(
                200,
                {
                    "ok": True,
                    "user": {
                        "username": user["username"],
                        "role": user["role"],
                        "display_name": user["display_name"],
                    },
                    "redirect": "/dashboard",
                },
                headers,
            )
            return

        if path == "/api/homework/toggle":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return
            hw_id = str(payload.get("id", "")).strip()
            from user_store import load_state, save_state
            state = load_state(self.data_root, user["storage_key"])
            for hw in state.get("homework", []):
                if hw.get("id") == hw_id:
                    hw["done"] = not hw.get("done", False)
                    break
            save_state(self.data_root, user["storage_key"], state)
            self._send_json(200, {"ok": True})
            return

        if path == "/api/notes/delete":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Требуется вход"})
                return
            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return
            note_id = str(payload.get("id", "")).strip()
            if not note_id:
                self._send_json(400, {"ok": False, "error": "Не указан id"})
                return
            from user_store import load_state, save_state
            state = load_state(self.data_root, user["storage_key"])
            state["notes"] = [n for n in state.get("notes", []) if n.get("id") != note_id]
            save_state(self.data_root, user["storage_key"], state)
            self._send_json(200, {"ok": True})
            return

        if path == "/api/process":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Сначала войдите в аккаунт"})
                return

            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return

            text = str(payload.get("text", "")).strip()
            if not text:
                self._send_json(400, {"ok": False, "error": "Введите текст для обработки"})
                return

            try:
                result = smart_processor(text)
                save_planner_result(self.data_root, user["storage_key"], text, result)
                self._send_json(200, {"ok": True, "result": result})
            except Exception:
                self._send_json(500, {"ok": False, "error": "Не удалось обработать запрос"})
            return

        if path == "/api/chat/send":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Сначала войдите в аккаунт"})
                return

            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return

            message = str(payload.get("message", "")).strip()
            chat_id = str(payload.get("chat_id", "")).strip()
            chat_id = None if not chat_id or chat_id == "None" else chat_id
            if not message:
                self._send_json(400, {"ok": False, "error": "Введите сообщение"})
                return

            # --- Фильтрация через smart_processor ---
            # Если пользователь хочет создать заметку/напоминание — сохраняем и отвечаем подтверждением,
            # иначе — идём в обычный chat_reply.
            try:
                parsed = smart_processor(message)
            except Exception:
                parsed = {"category": 2}

            if parsed.get("category") == 1:
                # Сохраняем заметку в планировщик
                try:
                    save_planner_result(self.data_root, user["storage_key"], message, parsed)
                except Exception:
                    pass

                task = parsed.get("task") or message
                date = parsed.get("date")
                if date:
                    assistant_message = f"✅ Напоминание сохранено: «{task}» на {date}."
                else:
                    assistant_message = f"✅ Напоминание сохранено: «{task}»."

                session = save_chat_exchange(
                    self.data_root,
                    user["storage_key"],
                    user_message=message,
                    assistant_message=assistant_message,
                    chat_id=chat_id,
                )
                self._send_json(
                    200,
                    {
                        "ok": True,
                        "chat_id": session["chat_id"],
                        "messages": session["messages"],
                        "history": list_chat_sessions(self.data_root, user["storage_key"]),
                        "reminder_saved": True,
                        "reminder": {"task": task, "date": date},
                    },
                )
                return
            # --- конец фильтрации ---

            existing_session = get_chat_session(self.data_root, user["storage_key"], chat_id) if chat_id else None
            conversation = []
            if existing_session:
                conversation.extend(
                    {"role": item["role"], "content": item["content"]}
                    for item in existing_session.get("messages", [])
                )
            conversation.append({"role": "user", "content": message})

            try:
                assistant_message = chat_reply(conversation)
            except Exception:
                self._send_json(500, {"ok": False, "error": "Не удалось получить ответ от модели"})
                return

            session = save_chat_exchange(
                self.data_root,
                user["storage_key"],
                user_message=message,
                assistant_message=assistant_message,
                chat_id=chat_id,
            )
            self._send_json(
                200,
                {
                    "ok": True,
                    "chat_id": session["chat_id"],
                    "messages": session["messages"],
                    "history": list_chat_sessions(self.data_root, user["storage_key"]),
                },
            )
            return

        if path == "/api/tts":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Не авторизован"})
                return
            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return
            text = str(payload.get("text", "")).strip()
            voice = str(payload.get("voice", "male")).strip()
            if not text:
                self._send_json(400, {"ok": False, "error": "Нет текста"})
                return
            try:
                from tts_engine import synthesize_to_bytes
                wav = synthesize_to_bytes(text, gender=voice)
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Content-Length", str(len(wav)))
                self.end_headers()
                self.wfile.write(wav)
            except Exception as exc:
                self._send_json(500, {"ok": False, "error": str(exc)})
            return

        if path == "/api/settings/model":
            user = self._get_current_user()
            if not user:
                self._send_json(401, {"ok": False, "error": "Сначала войдите в аккаунт"})
                return

            try:
                payload = self._read_json_body()
            except ValueError as error:
                self._send_json(400, {"ok": False, "error": str(error)})
                return

            allowed_models = {"qwen2.5:3b", "mistral:7b-instruct-v0.3-q4_0"}
            model = str(payload.get("model", "")).strip()
            if model not in allowed_models:
                self._send_json(400, {"ok": False, "error": f"Недопустимая модель: {model}"})
                return

            import planner
            planner.MODEL = model
            self._send_json(200, {"ok": True, "model": model})
            return

        self._send_json(404, {"ok": False, "error": "Маршрут не найден"})


def main() -> None:
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    project_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(project_dir, "templates")
    base_dir = templates_dir if os.path.isdir(templates_dir) else project_dir
    db_path = os.path.join(project_dir, DB_FILENAME)
    data_root = os.path.join(project_dir, "user_data")

    init_database(db_path)
    os.makedirs(data_root, exist_ok=True)

    AppHandler.db_path = db_path
    AppHandler.data_root = data_root
    handler = partial(AppHandler, directory=base_dir)
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Server started: http://{host}:{port}")
    print(f"Serving directory: {base_dir}")
    print(f"SQLite DB: {db_path}")
    print(f"User data root: {data_root}")
    print("POST API: /api/login, /api/process, /api/chat/send")
    print("Press Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
