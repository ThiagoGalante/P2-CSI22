import sqlite3
import os
from book import Book
from exceptions import BookAlreadyExistsError, BookNotFoundError

class BookRepository:
    def __init__(self, db_name="repository.db"):
        self.db_name = db_name
        self.sql_dir = os.path.join(os.path.dirname(__file__), 'sql')
        self._load_sql_queries()
        self.setup_database()

    def _load_sql_queries(self):
        queries = {}
        for filename in os.listdir(self.sql_dir):
            if filename.endswith(".sql"):
                query_name = filename.split('.')[0]
                with open(os.path.join(self.sql_dir, filename), 'r') as f:
                    queries[query_name + "_query"] = f.read()
        self.__dict__.update(queries)

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def setup_database(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.executescript(self.create_table_query)
            conn.commit()
        finally:
            conn.close()


    def search(self, isbn: int) -> Book:
        """Searches for a book by ISBN and returns a Book object."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            cursor.execute(self.search_book_query, (isbn,))
            row = cursor.fetchone()
            if not row:
                raise BookNotFoundError(isbn)
            row_dict = dict(row)
            del row_dict['id']
            return Book(**row_dict) # Validations not needed here, as the database schema ensures data integrity. 
                                     # So we can directly unpack the row into a Book object without BookBuilder.
        finally:
            conn.close()

    def add(self, book: Book):
        """Adds a new book to the repository from a Book object."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                self.add_book_query,
                (book.isbn, book.title, book.author, book.genre, book.publisher, book.published_year)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            raise BookAlreadyExistsError(book.isbn)
        finally:
            conn.close()

    def edit(self, book: Book):
        """Edita um livro existente a partir de um objeto Book."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                self.edit_book_query,
                (book.title, book.author, book.genre, book.publisher, book.published_year, book.isbn)
            )
            if cursor.rowcount == 0:
                raise BookNotFoundError(book.isbn)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, isbn: int):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.delete_book_query, (isbn,))
            if cursor.rowcount == 0:
                raise BookNotFoundError(isbn)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()