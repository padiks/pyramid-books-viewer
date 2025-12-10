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
