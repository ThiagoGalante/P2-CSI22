import sqlite3
import os
from tkinter import messagebox
from book import Book, BookBuilder
from typing import Optional

class BookRepository:
    """
    Manages the database operations for the Book catalog.
    """
    def __init__(self, db_name='repository.db'):
        self.db_name = db_name
        self._load_sql()
        self.setup_database()

    def _load_sql(self):
        """Loads SQL queries from files."""
        try:
            with open('sql/create_table.sql', 'r', encoding='utf-8') as f:
                self.create_table = f.read()
            with open('sql/add_book.sql', 'r', encoding='utf-8') as f:
                self.add_query = f.read()
            with open('sql/edit_book.sql', 'r', encoding='utf-8') as f:
                self.edit_query = f.read()
            with open('sql/search_book.sql', 'r', encoding='utf-8') as f:
                self.search_query = f.read()
            with open('sql/delete_book.sql', 'r', encoding='utf-8') as f:
                self.delete_query = f.read()
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Error when loading SQL files: {e}")
            raise

    def _get_connection(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def setup_database(self):
        """
        Creates the database and the books table if it does not exist.
        """
        if os.path.exists(self.db_name):
            return

        conn = self._get_connection()
        try:
            conn.executescript(self.create_table) #
            conn.commit()
        except FileNotFoundError:
            messagebox.showerror("Error", "Error when creating the database: SQL file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"It was not possible to create the database: {e}")
        finally:
            conn.close()

    def search(self, isbn: int) -> Optional[Book]:
        """
        Searches for a book by ISBN in the database and returns a Book object if found.
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row 
        try:
            cursor = conn.cursor()
            cursor.execute(self.search_query, (isbn,))
            row = cursor.fetchone()
            if row:
                try:
                    builder = BookBuilder()
                    book = (builder.set_isbn(str(row["isbn"]))
                                    .set_title(row["title"])
                                    .set_author(row["author"])
                                    .set_genre(row["genre"])
                                    .set_publisher(row["publisher"])
                                    .set_published_year(str(row["published_year"]))
                                    .build())
                    return book
                except (ValueError, AssertionError) as e:
                    messagebox.showerror("Error", f"Error when building Book object: {e}")  
                    return None
            else:
                messagebox.showerror("Error", f"Book with ISBN '{isbn}' not found.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Error when searching for book: {e}")
            return None
        finally:
            conn.close()

    def add(self, book: Book) -> bool:
        """Adds a new book to the database."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            book_data = (
                book.isbn, 
                book.title, 
                book.author, 
                book.genre, 
                book.publisher, 
                book.published_year
            )
            cursor.execute(self.add_query, book_data)
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"The ISBN '{book.isbn}' already exists in the database.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error when adding book: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def edit(self, book: Book) -> bool:
        """Edits an existing book in the database."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                self.edit_query,
                (book.title, book.author, book.genre, book.publisher, book.published_year, book.isbn)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"The ISBN '{book.isbn}' does not exist in the database.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Error when editing book: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def delete(self, isbn: int) -> bool:
        """Deletes a book from the database by ISBN."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(self.delete_query, (isbn,))
            conn.commit()
            if cursor.rowcount > 0:
                return True
            else:
                messagebox.showerror("Error", f"The book with ISBN '{isbn}' does not exist in the database.")
                return False
        except Exception as e:
            messagebox.showerror("Error", f"Error when deleting book: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
