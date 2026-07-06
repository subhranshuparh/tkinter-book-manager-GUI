"""
SQLite backend for the Book Store app.

Fixes applied:
- `isbn` column changed from INTEGER to TEXT: real ISBNs can have leading
  zeros or an 'X' check digit (ISBN-10), which an INTEGER column would
  silently corrupt or reject.
- Every connection now uses a `with sqlite3.connect(...)` context manager,
  so the connection/commit is handled safely even if an exception occurs
  partway through (previously a raised exception would skip conn.close()).
- `search()` previously used OR across all fields, which meant filling in
  two fields (e.g. title AND author) returned rows matching EITHER one --
  far too broad. It now builds the WHERE clause dynamically from only the
  fields the user actually filled in, combined with AND.
- Centralized the DB filename in DB_NAME instead of repeating the literal
  string in every function.
"""

import sqlite3

DB_NAME = "books.db"


def connect():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                year INTEGER,
                isbn TEXT
            )
            """
        )
        conn.commit()


def insert(title, author, year, isbn):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO book (title, author, year, isbn) VALUES (?, ?, ?, ?)",
            (title, author, year, isbn),
        )
        conn.commit()


def view():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute("SELECT * FROM book")
        return cur.fetchall()


def search(title="", author="", year="", isbn=""):
    """Return rows matching ALL of the non-empty fields provided."""
    filters = {"title": title, "author": author, "year": year, "isbn": isbn}
    filters = {k: v for k, v in filters.items() if v not in ("", None)}

    if not filters:
        return view()

    clause = " AND ".join(f"{field}=?" for field in filters)
    values = tuple(filters.values())

    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute(f"SELECT * FROM book WHERE {clause}", values)
        return cur.fetchall()


def delete(book_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM book WHERE id=?", (book_id,))
        conn.commit()


def update(book_id, title, author, year, isbn):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?",
            (title, author, year, isbn, book_id),
        )
        conn.commit()
