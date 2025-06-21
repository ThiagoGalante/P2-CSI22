import tkinter
from tkinter import messagebox
from book import BookBuilder
from database import BookRepository

class BookCatalogApp:
    """
    Application class for managing the book catalog.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Book Catalog")
        self.root.config(bg="#f0f0f0")

        self.repository = BookRepository()

        self._setup_ui()

    def _setup_ui(self):
        """Creates and organizes all the widgets for the user interface."""
        form_frame = tkinter.Frame(self.root, padx=20, pady=20)
        form_frame.pack(padx=10, pady=10, fill="x")

        form_fields = {
            "ISBN:": "entry_isbn", "Title:": "entry_title", "Author:": "entry_author",
            "Genre:": "entry_genre", "Publisher:": "entry_publisher", "Published Year:": "entry_published_year"
        }
        for i, (text, attr_name) in enumerate(form_fields.items()):
            label = tkinter.Label(form_frame, text=text)
            label.grid(row=i, column=0, sticky="w", pady=4)
            entry = tkinter.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, pady=4, padx=5, sticky="we")
            setattr(self, attr_name, entry)

        button_frame = tkinter.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill="x")

        button_search = tkinter.Button(button_frame, text="Search", command=self._search_book)
        button_search.pack(side="left", padx=5)

        self.button_add = tkinter.Button(button_frame, text="Add", command=self._add_book)
        self.button_add.pack(side="left", padx=5)
        
        self.button_edit = tkinter.Button(button_frame, text="Edit", command=self._edit_book)
        self.button_edit.pack(side="left", padx=5)

        self.button_delete = tkinter.Button(button_frame, text="Delete", command=self._delete_book)
        self.button_delete.pack(side="left", padx=5)

        button_clear = tkinter.Button(button_frame, text="Clear Form", command=self._clear_form)
        button_clear.pack(side="right", padx=5)

    def _clear_form(self):
        """Clears all input fields and resets the UI state."""
        self.entry_isbn.config(state='normal')
        self.entry_isbn.delete(0, 'end')
        self.entry_title.delete(0, 'end')
        self.entry_author.delete(0, 'end')
        self.entry_genre.delete(0, 'end')
        self.entry_publisher.delete(0, 'end')
        self.entry_published_year.delete(0, 'end')

        self.entry_isbn.focus_set()

    def _search_book(self):
        """Searches for a book by its ISBN."""
        if not self.entry_isbn.get():
            messagebox.showerror("Invalid Input", "Please enter an ISBN to search for.")
            return

        for entry in [self.entry_title, self.entry_author, self.entry_genre, self.entry_publisher, self.entry_published_year]:
            entry.delete(0, 'end')

        book = self.repository.search(self.entry_isbn.get())
        
        if book:
            self.entry_title.insert(0, book.title)
            self.entry_author.insert(0, book.author)
            self.entry_genre.insert(0, book.genre)
            self.entry_publisher.insert(0, book.publisher)
            self.entry_published_year.insert(0, str(book.published_year))

    def _add_book(self):
        """Adds a new book to the catalog."""
        try:
            builder = BookBuilder()

            book = (builder.set_isbn(self.entry_isbn.get())
                           .set_title(self.entry_title.get())
                           .set_author(self.entry_author.get())
                           .set_genre(self.entry_genre.get())
                           .set_publisher(self.entry_publisher.get())
                           .set_published_year(self.entry_published_year.get())
                           .build())

            if self.repository.add(book):
                messagebox.showinfo("Success", "New book added successfully!")
                self._clear_form()

        except (ValueError, AssertionError) as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror(f"An unexpected error occurred: {e}")

    def _edit_book(self):
        """Edits book details in the catalog."""
        try:
            builder = BookBuilder()

            book = (builder.set_isbn(self.entry_isbn.get())
                           .set_title(self.entry_title.get())
                           .set_author(self.entry_author.get())
                           .set_genre(self.entry_genre.get())
                           .set_publisher(self.entry_publisher.get())
                           .set_published_year(self.entry_published_year.get())
                           .build())

            if self.repository.edit(book):
                messagebox.showinfo("Success", "Book edited successfully!")
                self._clear_form()

        except (ValueError, AssertionError) as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror(f"An unexpected error occurred: {e}")

    def _delete_book(self):
        """Deletes book from the catalog."""


        if self.repository.delete(self.entry_isbn.get()):
            messagebox.showinfo("Success", "Book deleted successfully!")
            self._clear_form()

if __name__ == "__main__":
    root = tkinter.Tk()
    app = BookCatalogApp(root)
    root.mainloop()
