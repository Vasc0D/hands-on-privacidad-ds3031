"""Insert four invented records and save the GET /registros response."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from app import create_app


DEMO_RECORDS = [
    {"nombres": "Ana", "apellidos": "Quispe", "correo": "ana@example.test", "telefono": "+000-0000-0001"},
    {"nombres": "Luis", "apellidos": "Rojas", "correo": "luis@example.test", "telefono": "+000-0000-0002"},
    {"nombres": "Mia", "apellidos": "Salazar", "correo": "mia@example.test", "telefono": "+000-0000-0003"},
    {"nombres": "Noah", "apellidos": "Vega", "correo": "noah@example.test", "telefono": "+000-0000-0004"},
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "demo_output.json",
        help="archivo para guardar la respuesta de GET /registros",
    )
    args = parser.parse_args()

    # A temporary database demonstrates the API without leaving a database file.
    with tempfile.TemporaryDirectory(prefix="hands_on_privacidad_") as directory:
        app = create_app({"TESTING": True, "DATABASE": str(Path(directory) / "demo.sqlite3")})
        client = app.test_client()
        for record in DEMO_RECORDS:
            response = client.post("/registro", json=record)
            if response.status_code != 201:
                raise RuntimeError(f"POST /registro devolvió {response.status_code}")

        response = client.get("/registros")
        if response.status_code != 200:
            raise RuntimeError(f"GET /registros devolvió {response.status_code}")

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(response.get_json(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"Salida guardada en {args.output}")


if __name__ == "__main__":
    main()
