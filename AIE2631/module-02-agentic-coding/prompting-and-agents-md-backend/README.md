# My Little Library with Backend

This folder keeps the original browser app idea and adds a small Python backend. The server hosts the frontend and exposes an in-memory books API.

## Run

```powershell
python server.py
```

Open <http://127.0.0.1:8001>.

## API

- `GET /api/books` lists books.
- `POST /api/books` adds a book from JSON such as `{ "title": "Dune" }`.

Books remain available while the server is running and reset when it restarts.

## Test

```powershell
python -m unittest -v
```
