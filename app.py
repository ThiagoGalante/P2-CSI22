# app.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import BookRepository
from book import Book, BookBuilder
from exceptions import ValidationError, BookNotFoundError, BookAlreadyExistsError

class BookCatalogApp:
    """Main application class for the Books Catalog."""
    def __init__(self, root):
        self.repository = BookRepository()
        self.root = root
        self.root.title("Books Catalog")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self._setup_ui()

    def _setup_ui(self):
        """Sets up the user interface for the application."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(main_frame, text="Book Data", padding="10")
        form_frame.pack(fill=tk.X, expand=True, pady=5)

        labels = ["ISBN (13 dígitos):", "Title:", "Author:", "Genre:", "Publisher:", "Published_Year:"]
        self.entries = {}
        for i, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            self.entries[label_text.split(' ')[0].lower()] = entry
        
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X, expand=True)

        buttons = [
            ("Search", self._search_book), ("Add", self._add_book),
            ("Edit", self._edit_book), ("Delete", self._delete_book),
            ("Clear Form", self._clear_form)
        ]
        for i, (text, command) in enumerate(buttons):
            button = ttk.Button(button_frame, text=text, command=command)
            button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def _get_entry(self, key):
        """Returns the entry widget for a given key."""
        for k, v in self.entries.items():
            if key in k:
                return v
        return None

    def _clear_form(self):
        """Clears all form entries."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _populate_form(self, book: Book):
        """Populates the form with book data."""
        self._clear_form()
        self._get_entry('isbn').insert(0, book.isbn)
        self._get_entry('title').insert(0, book.title)
        self._get_entry('author').insert(0, book.author)
        self._get_entry('genre').insert(0, book.genre)
        self._get_entry('publisher').insert(0, book.publisher)
        self._get_entry('published_year').insert(0, book.published_year)

    def _get_builder_from_form(self):
        """Creates a BookBuilder from the form entries."""
        builder = BookBuilder()
        builder.with_isbn(self._get_entry('isbn').get())
        builder.with_title(self._get_entry('title').get())
        builder.with_author(self._get_entry('author').get())
        builder.with_genre(self._get_entry('genre').get())
        builder.with_publisher(self._get_entry('publisher').get())
        builder.with_published_year(self._get_entry('published_year').get())
        return builder
    
    def _search_book(self):
        """Searches for a book by ISBN and populates the form with its data."""
        isbn = self._get_entry('isbn').get()
        if not isbn or not isbn.isdigit() or not len(isbn) == 13:
            messagebox.showerror("Invalid Input", "Please enter a valid ISBN to search.")
            return
        
        try:
            book_obj = self.repository.search(int(isbn))
            self._populate_form(book_obj)
        except BookNotFoundError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

    def _add_book(self):
        """Adds a new book to the repository."""
        try:
            builder = self._get_builder_from_form()
            book_obj = builder.build() # Cria o objeto
            self.repository.add(book_obj) # Passa o objeto
            messagebox.showinfo("Success", "Book added successfully!")
            self._clear_form()
        except (ValidationError, BookAlreadyExistsError) as e:
            messagebox.showerror("Error Adding Book", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

    def _edit_book(self):
        """Edits an existing book in the repository."""
        try:
            builder = self._get_builder_from_form()
            book_obj = builder.build() # Cria o objeto
            self.repository.edit(book_obj) # Passa o objeto
            messagebox.showinfo("Success", "Book edited successfully!")
            self._clear_form()
        except (ValidationError, BookNotFoundError) as e:
            messagebox.showerror("Error Editing Book", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

    def _delete_book(self):
        """Deletes a book from the repository by ISBN."""
        isbn = self._get_entry('isbn').get()
        if not isbn or not isbn.isdigit() or not len(isbn) == 13:
            messagebox.showerror("Invalid Input", "Please enter a valid ISBN to delete.")
            return
        
        try:
            self.repository.delete(int(isbn))
            messagebox.showinfo("Success", "Book deleted successfully!")
            self._clear_form()
        except BookNotFoundError as e:
            messagebox.showerror("Error Deleting Book", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookCatalogApp(root)
    root.mainloop()