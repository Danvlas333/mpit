import hashlib
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any


SESSION_TTL_DAYS = 7


def _connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt_bytes = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 120000)
    return f"{salt_bytes.hex()}${digest.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, digest_hex = stored_hash.split("$", 1)
    except ValueError:
        return False

    check_hash = _hash_password(password, bytes.fromhex(salt_hex))
    return secrets.compare_digest(check_hash, stored_hash)


def init_database(db_path: str) -> None:
    with _connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                display_name TEXT NOT NULL,
                storage_key TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

        columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(users)").fetchall()
        }
        if "storage_key" not in columns:
            connection.execute("ALTER TABLE users ADD COLUMN storage_key TEXT")

        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_storage_key ON users(storage_key)"
        )

        users = (
            ("student", "student123", "student", "Ученик"),
            ("teacher", "teacher123", "teacher", "Учитель"),
        )

        for username, password, role, display_name in users:
            connection.execute(
                """
                INSERT INTO users (username, password_hash, role, display_name)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(username) DO NOTHING
                """,
                (username, _hash_password(password), role, display_name),
            )

        rows = connection.execute(
            "SELECT id FROM users WHERE storage_key IS NULL OR storage_key = ''"
        ).fetchall()
        for row in rows:
            connection.execute(
                "UPDATE users SET storage_key = ? WHERE id = ?",
                (secrets.token_hex(16), row["id"]),
            )

        connection.commit()


def authenticate_user(db_path: str, username: str, password: str) -> dict[str, Any] | None:
    with _connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT id, username, password_hash, role, display_name, storage_key
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if row is None or not _verify_password(password, row["password_hash"]):
        return None

    return {
        "id": row["id"],
        "username": row["username"],
        "role": row["role"],
        "display_name": row["display_name"],
        "storage_key": row["storage_key"],
    }


def create_session(db_path: str, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = (_utc_now() + timedelta(days=SESSION_TTL_DAYS)).isoformat()

    with _connect(db_path) as connection:
        connection.execute(
            "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
            (token, user_id, expires_at),
        )
        connection.commit()

    return token


def get_user_by_session(db_path: str, token: str | None) -> dict[str, Any] | None:
    if not token:
        return None

    now_iso = _utc_now().isoformat()

    with _connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT users.id, users.username, users.role, users.display_name, users.storage_key, sessions.expires_at
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token = ?
            """,
            (token,),
        ).fetchone()

        if row is None:
            return None

        if row["expires_at"] <= now_iso:
            connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
            connection.commit()
            return None

    return {
        "id": row["id"],
        "username": row["username"],
        "role": row["role"],
        "display_name": row["display_name"],
        "storage_key": row["storage_key"],
    }


def delete_session(db_path: str, token: str | None) -> None:
    if not token:
        return

    with _connect(db_path) as connection:
        connection.execute("DELETE FROM sessions WHERE token = ?", (token,))
        connection.commit()
