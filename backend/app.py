"""Minimal Flask backend for the privacy workshop exercise.

This intentionally has no authentication or privacy controls. Use only invented
training data; the risks and design restrictions belong in the DPIA exercise.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, current_app, g, jsonify, request


SCHEMA = """
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    correo TEXT NOT NULL,
    telefono TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    """Create the app and initialize its configured SQLite database."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=str(Path(__file__).resolve().parent / "lab.db"),
    )
    if test_config:
        app.config.update(test_config)

    @app.teardown_appcontext
    def close_db(_error: BaseException | None = None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.post("/registro")
    @app.post("/registros")
    def create_registro():
        if not request.is_json:
            return jsonify(error="El cuerpo debe ser JSON (Content-Type: application/json)."), 400

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON válido."), 400

        required = ("nombres", "apellidos", "correo")
        values: dict[str, str] = {}
        for field in required:
            value = payload.get(field)
            if not isinstance(value, str) or not value.strip():
                return jsonify(error=f"'{field}' es obligatorio y debe ser texto no vacío."), 400
            values[field] = value.strip()

        telefono = payload.get("telefono")
        if telefono is not None and not isinstance(telefono, str):
            return jsonify(error="'telefono' debe ser texto o null."), 400
        if isinstance(telefono, str):
            telefono = telefono.strip() or None

        cursor = get_db().execute(
            "INSERT INTO registros (nombres, apellidos, correo, telefono) "
            "VALUES (?, ?, ?, ?)",
            (values["nombres"], values["apellidos"], values["correo"], telefono),
        )
        get_db().commit()
        return jsonify(ok=True, id=cursor.lastrowid), 201

    @app.get("/registros")
    def list_registros():
        rows = get_db().execute(
            "SELECT id, nombres, apellidos, correo, telefono, created_at "
            "FROM registros ORDER BY id"
        ).fetchall()
        return jsonify([dict(row) for row in rows])

    return app


def get_db() -> sqlite3.Connection:
    """Return the request/app-context SQLite connection."""
    if "db" not in g:
        database = current_app.config["DATABASE"]
        if database != ":memory:":
            Path(database).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(database)
        db.row_factory = sqlite3.Row
        db.executescript(SCHEMA)
        g.db = db
    return g.db


app = create_app()


if __name__ == "__main__":
    # Bind only to the local machine for the workshop.
    app.run(host="127.0.0.1", port=5000, debug=False)
