# P2 CSI 22

# Alunos

* Daniel da Silveira Sahadi
* Thiago Galante Pereira

# Book Catalog with Python and Tkinter

This is a simple desktop application for managing a personal book catalog. The application allows users to add, search, edit, and remove books from an SQLite database.

## Features

* **Add Book:** Inserts a new book into the database with field validation.
* **Search Book:** Searches for an existing book by its ISBN.
* **Edit Book:** Modifies the information of a registered book.
* **Delete Book:** Removes a book from the database.
* **Clear Form:** Clears all data entry fields.

## Project Structure

The code is organized into the following files for a clean separation of concerns:

* `app.py`: Contains the main application class (`BookCatalogApp`) and all the logic for the graphical user interface (GUI) built with `tkinter`.
* `database.py`: Handles all interactions with the SQLite database (`BookRepository`), such as connecting, creating the table, and executing CRUD (Create, Read, Update, Delete) operations.
* `book.py`: Defines the `Book` data model and the `BookBuilder` class, which is used to validate and create book objects before saving them to the database.
* `sql/`: A directory that stores all SQL queries in separate files, keeping the Python code cleaner.
    * `create_table.sql`: Script to create the `books` table.
    * `add_book.sql`: Query to insert a new book.
    * `edit_book.sql`: Query to update an existing book.
    * `delete_book.sql`: Query to delete a book.
    * `search_book.sql`: Query to search for a book by ISBN.

## How to Run on Windows

Run the following command in your terminal:

    ```sh
    python -m venv venv

    .\venv\Scripts\activate.bat

    python app.py
    ```

The application window will open. The database file `repository.db` will be created automatically in the same directory the first time you run the program.