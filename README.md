# Laboratorio de privacidad de datos DS3031

Backend mínimo de registro y listado con Flask y SQLite y [evaluación de impacto de protección de datos](DPIA.docx).

## Ejecución

Requiere Python 3.10 o superior.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

La API se ejecuta en `http://127.0.0.1:5000`:

- `POST /registro`: guarda nombres, apellidos, correo y teléfono. El teléfono es opcional. También acepta `/registros` como alias.
- `GET /registros`: devuelve los registros almacenados.

La base `lab.db` se crea al primer acceso y está excluida del repositorio.

## Demostración

```bash
python demo.py
```

Inserta cuatro registros ficticios en una base temporal, consulta `GET /registros` y guarda la respuesta en `demo_output.json`. La base temporal se elimina al finalizar.

Las restricciones de privacidad se documentan en la DPIA y no se implementan, según el enunciado. Utilizar exclusivamente datos ficticios en el entorno local.
