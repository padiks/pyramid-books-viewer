# Mini Books Viewer - Pyramid

A **minimal Pyramid web app** to display books from a Django SQLite database.
This project is for **learning and study purposes**: no templates, no ORM, just plain SQL and HTML.

---

## Features

* Connects directly to the existing **Django SQLite database** (`db.sqlite3`)
* Fetches all books and their **categories**
* Displays data in a **simple HTML table**
* No templates, frameworks, or CSS dependencies beyond inline styling
* Lightweight, minimal Pyramid setup

---

## Installation

```bash
python -m venv venv           # create a virtual environment
source venv/bin/activate      # (Debian) activate the environment
# venv\Scripts\activate       # (Windows) activate the environment
pip install --upgrade pip     # update pip
pip install pyramid waitress  # install Pyramid and Waitress
```

> After this, your environment is ready. You can run the app with `python app.py` and open `http://127.0.0.1:6543/books` in the browser.

---

## Project Structure

```
pyramid_books/
+
+- app.py          # Main Pyramid application
+- db.sqlite3      # SQLite database (copied from Django project)
+- README.md       # This file
```

---

## `app.py` - Overview

* Uses **Pyramid** to handle HTTP requests
* Uses **SQLite3** to read books and categories
* Builds **HTML table dynamically** in Python

### Key code snippet

```python
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
    SELECT b.id, b.title, b.hepburn, b.author, b.published_date, c.name AS category_name
    FROM books b
    LEFT JOIN categories c ON b.category_id = c.id
    ORDER BY b.id
""")
books = cur.fetchall()
conn.close()

rows = ""
for i, book in enumerate(books, start=1):
    rows += f"""
    <tr>
        <td>{i}</td>
        <td>{book['title']}</td>
        <td>{book['hepburn']}</td>
        <td>{book['author']}</td>
        <td>{book['published_date']}</td>
        <td>{book['category_name'] or ''}</td>
    </tr>
    """
```

* The rest of the code **wraps the rows in a full HTML table** and returns a `Response` via Pyramid.

---

## How to Run

1. Install dependencies:

```bash
pip install pyramid waitress
```

2. Place your **Django `db.sqlite3`** file in the project folder
3. Run the app:

```bash
python app.py
```

4. Open your browser:

```
http://127.0.0.1:6543/books
```

You will see a **simple HTML table** showing all books and their categories.

---

## Full Source Code

```
from pyramid.config import Configurator
from pyramid.response import Response
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db.sqlite3"


def books_view(request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Join books with categories to get category name
    cur.execute("""
        SELECT b.id, b.title, b.hepburn, b.author, b.published_date, c.name AS category_name
        FROM books b
        LEFT JOIN categories c ON b.category_id = c.id
        ORDER BY b.id
    """)
    books = cur.fetchall()
    conn.close()

    rows = ""
    for i, book in enumerate(books, start=1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{book['title']}</td>
            <td>{book['hepburn']}</td>
            <td>{book['author']}</td>
            <td>{book['published_date']}</td>
            <td>{book['category_name'] or ''}</td>
        </tr>
        """

    html = f"""
    <html>
    <head>
        <title>Books</title>
        <style>
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 6px; }}
            th {{ background: #eee; }}
        </style>
    </head>
    <body>
        <h2>Books</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Title</th>
                    <th>Hepburn</th>
                    <th>Author</th>
                    <th>Published</th>
                    <th>Category</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else "<tr><td colspan='6'>No books found</td></tr>"}
            </tbody>
        </table>
    </body>
    </html>
    """

    return Response(html)


if __name__ == "__main__":
    with Configurator() as config:
        config.add_route("books", "/books")
        config.add_view(books_view, route_name="books")
        app = config.make_wsgi_app()

    from waitress import serve
    serve(app, host="0.0.0.0", port=6543)
```

---

## Learning Notes

* Uses **raw SQL** instead of Django ORM for clarity
* `sqlite3.Row` allows **accessing columns by name** (`book['title']`)
* Demonstrates **LEFT JOIN** to fetch related category data
* HTML is **generated dynamically in Python** (no templates)
* Excellent for studying **web app request ? DB ? response flow**

---

## Next Steps (optional)

* Add more columns (like `summary` or `url`)
* Paginate results for large tables
* Switch to **SQLAlchemy ORM** for more advanced querying
* Move HTML to a **template** (Jinja2) while keeping Pyramid
* Convert to **API endpoint** returning JSON

---

## License

This project is for **learning and educational use**.
Feel free to explore, extend, and build upon it.
